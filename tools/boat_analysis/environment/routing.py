"""Chart-constrained reference route, independent of vessel steering strategy."""
from __future__ import annotations

import heapq
import json
import math
from pathlib import Path

import numpy as np
from shapely import contains_xy, transform, unary_union
from shapely.geometry import LineString, Point, shape, mapping

from tools.boat_analysis.environment.course import LocalFrame, marker_gate
from tools.boat_analysis.model.runtime import ROOT, analysis_values


def course_inputs():
    return analysis_values('TransGorgeCourse::GateGeometry')


def chart_domains(features, settings, frame=LocalFrame()):
    depth, shore, restriction, obstacle, _ = settings
    if min(settings) <= 0:
        raise ValueError('Positive routing allocations required')
    groups = {}
    for feature in features:
        if not feature['geometry']:
            continue
        properties = feature['properties']
        kind = properties['object_class']
        geom = transform(shape(feature['geometry']), frame.project, interleaved=False)
        if kind == 'DEPARE' and (properties.get('DRVAL1') is None or properties['DRVAL1'] < depth):
            continue
        groups.setdefault(kind, []).append(geom)
    groups = {k: unary_union(v) for k, v in groups.items()}
    empty = Point().buffer(0)
    # Exclude all charted restrictions at this fidelity, even where a particular
    # activity could be permitted. No missing chart coverage is treated as water.
    excluded = unary_union([
        groups.get('LNDARE', empty).buffer(shore),
        groups.get('RESARE', empty).buffer(restriction),
        groups.get('LOKBSN', empty).buffer(restriction),
        groups.get('OBSTRN', empty).buffer(obstacle),
        groups.get('UNSARE', empty),
    ])
    water = groups['DEPARE'].difference(excluded)
    return water, groups


def reference_route(water, start, finish, spacing):
    """A* on conservatively inset grid cells, followed by visible shortcuts.

    Every edge and shortcut is checked against the original allowed polygon.
    A failed search reports failure; it never bridges a gap in chart coverage.
    """
    start, finish = Point(start), Point(finish)
    if not water.covers(start) or not water.covers(finish):
        raise ValueError('Gate center outside routing domain')
    xmin, ymin, xmax, ymax = water.bounds
    xs = np.arange(xmin, xmax + spacing, spacing)
    ys = np.arange(ymin, ymax + spacing, spacing)
    xx, yy = np.meshgrid(xs, ys)
    allowed = contains_xy(water.buffer(-spacing * math.sqrt(2)), xx, yy)
    coordinates = np.column_stack((xx[allowed], yy[allowed]))
    indices = np.column_stack(np.nonzero(allowed))
    def attach(point):
        distances = np.sum((coordinates - (point.x, point.y)) ** 2, axis=1)
        for i in np.argsort(distances)[:128]:
            if water.covers(LineString([point, coordinates[i]])):
                return tuple(indices[i])
        raise ValueError('No chart-clear connection from gate to routing grid')
    first, last = attach(start), attach(finish)
    def xy(node):
        return (xs[node[1]], ys[node[0]])
    def heuristic(node):
        return math.dist(xy(node), xy(last))
    queue = [(heuristic(first), 0., first)]
    costs, parent = {first: 0.}, {}
    while queue:
        _, cost, node = heapq.heappop(queue)
        if cost != costs[node]:
            continue
        if node == last:
            break
        for dy, dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
            nxt = node[0] + dy, node[1] + dx
            if not (0 <= nxt[0] < len(ys) and 0 <= nxt[1] < len(xs)) or not allowed[nxt]:
                continue
            new = cost + spacing * math.hypot(dx, dy)
            if new < costs.get(nxt, math.inf):
                costs[nxt], parent[nxt] = new, node
                heapq.heappush(queue, (new + heuristic(nxt), new, nxt))
    if last not in costs:
        raise ValueError('No connected chart-clear route at this grid resolution')
    nodes = [last]
    while nodes[-1] != first:
        nodes.append(parent[nodes[-1]])
    points = [(start.x,start.y), *[xy(n) for n in reversed(nodes)], (finish.x,finish.y)]
    result, i = [points[0]], 0
    while i < len(points) - 1:
        j = len(points) - 1
        while j > i + 1 and not water.covers(LineString([points[i], points[j]])):
            j -= 1
        result.append(points[j]); i = j
    route = LineString(result)
    if not water.covers(route):
        raise ValueError('Route edge failed exact chart-domain check')
    return route


def bridge_geometry(values=None):
    values = course_inputs() if values is None else values
    features = json.loads((ROOT/'evidence/course/2026-10-11/chart-features.geojson').read_text())['features']
    bridges = [f for f in features if f['properties']['object_class']=='BRIDGE']
    chosen = next(f for f in bridges if f['properties']['LNAM']==values['bridgeSpanIdentifier'])
    project = lambda f: transform(shape(f['geometry']), LocalFrame().project, interleaved=False)
    span = project(chosen)
    excluded = unary_union([project(f).buffer(values['bridgePierAllowanceM']) for f in bridges
                            if f['properties']['LNAM'] != values['bridgeSpanIdentifier']])
    points = np.asarray(span.exterior.coords)[:-1]
    _, vectors = np.linalg.eigh(np.cov(points.T))
    normal = vectors[:,0]
    center = np.array([span.centroid.x, span.centroid.y])
    approach = values['bridgeApproachM']
    return span, excluded, center-normal*approach, center+normal*approach


def course_route(water, start, finish, spacing, values=None):
    """Cross the selected closed lift span; never borrow its clearance for another span."""
    _, _, a, b = bridge_geometry(values)
    start, finish = Point(start), Point(finish)
    axis=b-a; center=(a+b)/2
    side=lambda p: float(np.dot(np.array([p.x,p.y])-center,axis))
    if side(start)*side(finish)>=0:
        return reference_route(water,start,finish,spacing)
    if side(start)>0: a,b=b,a
    crossing=LineString([a,b])
    if not water.covers(crossing):
        raise ValueError('Selected bridge passage is not chart-clear')
    first=reference_route(water,start,a,spacing)
    last=reference_route(water,b,finish,spacing)
    return LineString([*first.coords,*crossing.coords[1:],*list(last.coords)[1:]])


def rounding_paths(water, gates, route, spacing=40):
    """Port rounding north-west-south, followed by an independently clear return."""
    north, west, south = [gates[k].interpolate(.5, normalized=True) for k in
                          ('westGate', 'turnGate', 'returnGate')]
    center = ((north.x + south.x)/2, (north.y + south.y)/2)
    radius = north.distance(south)/2
    arcs = [LineString([(center[0]+radius*math.cos(a),center[1]+radius*math.sin(a))
                       for a in np.linspace(start,end,19)])
            for start,end in ((math.pi/2,math.pi),(math.pi,3*math.pi/2))]
    if not all(water.covers(arc) for arc in arcs):
        raise ValueError('Rounding arc outside chart-clear water')
    back = course_route(water,south,gates['eastGate'].interpolate(.5,normalized=True),spacing)
    return [route,*arcs,back]


def build():
    values = course_inputs()
    features = json.loads((ROOT/'evidence/course/2026-10-11/chart-features.geojson').read_text())['features']
    water, groups = chart_domains(features, values['routing'])
    lon,lat,radius = values['temporaryWorks']
    works = Point(LocalFrame().project(lon,lat)).buffer(radius)
    groups['TEMPORARY_WORKS'] = works
    water = water.difference(works)
    span, bridge_exclusions, _, _ = bridge_geometry(values)
    groups['SELECTED_BRIDGE_SPAN'] = span
    groups['BRIDGE_EXCLUSIONS'] = bridge_exclusions
    water = water.difference(bridge_exclusions)
    gates = {k: marker_gate(values[k]) for k in ['eastGate', 'westGate', 'turnGate', 'returnGate']}
    marker = Point(LocalFrame().project(*values['westGate'][:2]))
    groups['ROUNDING_EXCLUSION'] = marker.buffer(values['westGate'][3])
    water = water.difference(groups['ROUNDING_EXCLUSION'])
    route = course_route(water, gates['eastGate'].interpolate(.5, normalized=True),
                            gates['westGate'].interpolate(.5, normalized=True), values['routing'][4], values)
    length = sum(p.length for p in rounding_paths(water,gates,route,values['routing'][4]))/2
    if abs(length - values['referenceLegLengthM']) > 0.01:
        raise ValueError(f'Sizing reference length differs from chart route: {length}; update the model allocation')
    return values, water, groups, gates, route


if __name__ == '__main__':
    values, water, groups, gates, route = build()
    destination = ROOT/'build/analysis/mission-course.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps({'inputs': values, 'frame': vars(LocalFrame()),
        'route_m': mapping(route), 'allowed_water_m': mapping(water),
        'gates_m': {k: mapping(v) for k,v in gates.items()},
        'one_way_distance_m': route.length,
        'scope': 'Chart-constrained reference path; not a commanded sailing track or launch clearance.'})+'\n', encoding='utf-8')
    print(f'One-way reference path: {route.length/1000:.3f} km; {len(route.coords)} vertices')
