"""Render the Gorge overview from charted water polygons and model course geometry.

Run with ``python -m tools.publishing.course_map``. Coordinates use a local
equirectangular projection at 45.7 N. Town labels locate their river reaches;
the charted water and reference paths share the same projection; the mission model owns the challenge definition and operational gate decisions.
"""
from tools.boat_analysis.environment.routing import build, rounding_paths
from tools.boat_analysis.environment.course import LocalFrame
from html import escape
import json
from math import cos, radians
from pathlib import Path
from shapely.geometry import shape
from shapely import unary_union

ROOT = Path(__file__).resolve().parents[2]


def render():
    scale = 1050 / (0.53 * cos(radians(45.7)))

    def xy(lon, lat):
        return (45 + (lon + 121.94) * scale * cos(radians(45.7)),
                365 - (lat - 45.65) * scale)

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 570" '
             'role="img" aria-labelledby="title desc">',
             '<title id="title">The Gorge challenge course</title>',
             '<desc id="desc">North-up map of the Columbia River between '
             'Stevenson and Bingen, passing Hood River. '
             'The challenge begins at Bingen, heads downstream '
             'toward Stevenson, and returns upstream. Washington lies north '
             'of the river and Oregon south.</desc>',
             '<rect width="1140" height="570" fill="#f5f8fa"/>',
             '<defs><marker id="out" markerWidth="8" markerHeight="8" '
             'refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" '
             'fill="#ab4e23"/></marker><marker id="back" markerWidth="8" '
             'markerHeight="8" refX="7" refY="4" orient="auto">'
             '<path d="M0 0L8 4L0 8Z" fill="#176a65"/></marker></defs>',
             '<g font-family="system-ui, sans-serif" fill="#183047">']

    def text(x, y, value, size=18, extra=''):
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
                     f'{extra}>{escape(value)}</text>')

    def path(points, color, width, extra=''):
        coords = ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)
        parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" '
                     f'stroke-width="{width}" stroke-linecap="round" '
                     f'stroke-linejoin="round" {extra}/>')

    text(32, 40, 'The Gorge challenge: Bingen → Stevenson → Bingen', 25)
    text(32, 72, 'Columbia River · Oregon–Washington', 18)
    text(620, 122, 'WASHINGTON', 20, 'letter-spacing="3" fill="#65796d"')
    text(620, 365, 'OREGON', 20, 'letter-spacing="3" fill="#65796d"')
    # DEPARE polygons show water extent, not an artificial stroke around a centerline.
    features = json.loads((ROOT/'evidence/course/2026-10-11/chart-features.geojson').read_text())['features']
    river = unary_union([shape(f['geometry']) for f in features
                         if f['geometry'] and f['properties']['object_class']=='DEPARE'])
    parts.append('<g clip-path="url(#mapclip)">')
    for polygon in getattr(river, 'geoms', [river]):
        rings = [polygon.exterior, *polygon.interiors]
        commands = []
        for ring in rings:
            points = [xy(lon,lat) for lon,lat in ring.coords]
            commands.append('M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in points)+' Z')
        parts.append('<path d="'+' '.join(commands)+'" fill="#b5d8e7" stroke="#508ba6" stroke-width=".7" fill-rule="evenodd"/>')
    parts.append('</g>')
    values, water, _, gates, route = build()
    frame = LocalFrame()
    outbound = [xy(*frame.unproject(x,y)) for x,y in route.coords]
    path(outbound, '#ab4e23', 4, 'marker-end="url(#out)"')
    paths = rounding_paths(water,gates,route,values['routing'][4])
    returning = [xy(*frame.unproject(x,y)) for piece in paths[1:] for x,y in piece.coords]
    path(returning, '#176a65', 2.5, 'stroke-dasharray="7 6" marker-end="url(#back)"')
    for name, lon, lat, dx, dy in [
        ('Bingen', -121.46, 45.706, -45, 50),
        ('Hood River', -121.522, 45.709, -55, 76),
        ('Cascade Locks', -121.89, 45.669, 28, 40),
        ('Stevenson', -121.884, 45.695, -80, -43),
    ]:
        x, y = xy(lon, lat)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#183047"/>')
        path([(x, y), (x+dx, y+dy-8)], '#81929c', 1)
        text(x+dx, y+dy, name, 18)
    for name,label in [('turnGate','Buoy 16'),('eastGate','Buoy 39')]:
        x,y=xy(*values[name][:2])
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#96396a"/>')
        text(x-(85 if name=='westGate' else 30),y-22,label,15)
    text(230, 397, 'Shared tracks overlap: solid outbound · dashed return', 18)
    # Geographic distance scale: 111.195 km per latitude degree.
    bar = 10 / 111.195 * scale
    path([(50, 435), (50+bar, 435)], '#183047', 3)
    for x in (50, 50+bar):
        path([(x, 430), (x, 440)], '#183047', 2)
    text(50, 459, '0', 15)
    text(50+bar-15, 459, '10 km', 15)
    text(1062, 118, 'N', 18)
    path([(1069, 175), (1069, 131)], '#183047', 2)
    path([(1060, 144), (1069, 131), (1078, 144)], '#183047', 2)
    path([(320, 435), (380, 435)], '#ab4e23', 3, 'marker-end="url(#out)"')
    text(397, 442, '1  Downstream to Stevenson', 18)
    path([(320, 474), (380, 474)], '#176a65', 3, 'stroke-dasharray="7 6" marker-end="url(#back)"')
    text(397, 481, '2  Upstream to Bingen (dashed)', 18)
    text(32, 518, 'Gate references and route: NOAA ENC · Gate offsets: BlueDog::Mission::Course model', 14)
    text(32, 545, 'Water extent: NOAA ENC depth-area polygons · Reference paths, not simulated sailing tracks', 14)
    parts += ['</g><defs><clipPath id="mapclip"><rect x="25" y="90" width="1090" '
              'height="315"/></clipPath></defs></svg>']
    target = ROOT / 'docs/figures/gorge-course-map.svg'
    target.write_text('\n'.join(parts)+'\n', encoding='utf-8')
    return target


if __name__ == '__main__':
    print(render())
