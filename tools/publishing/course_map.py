"""Render the Gorge overview from the archived OpenStreetMap river centerline.

Run with ``python -m tools.publishing.course_map``. Coordinates use a local
equirectangular projection at 45.7 N. Town labels locate their river reaches;
the mission model owns the challenge definition and operational gate decisions.
"""
from tools.boat_analysis.environment.routing import build
from tools.boat_analysis.environment.course import LocalFrame
from html import escape
import json
from math import cos, radians
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).with_name('data') / 'gorge-river.json'


def render():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    scale = 1050 / (0.94 * cos(radians(45.7)))

    def xy(lon, lat):
        return (45 + (lon + 122.01) * scale * cos(radians(45.7)),
                365 - (lat - 45.59) * scale)

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 570" '
             'role="img" aria-labelledby="title desc">',
             '<title id="title">The Gorge challenge course</title>',
             '<desc id="desc">North-up map of the Columbia River between '
             'Bonneville and The Dalles, passing Cascade Locks, Hood River and '
             'Mosier. The challenge begins at The Dalles, heads downstream '
             'toward Bonneville, and returns upstream. Washington lies north '
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

    text(32, 40, 'The Gorge challenge: The Dalles → Bonneville → The Dalles', 25)
    text(32, 72, 'Columbia River · Oregon–Washington', 18)
    text(620, 122, 'WASHINGTON', 20, 'letter-spacing="3" fill="#65796d"')
    text(620, 365, 'OREGON', 20, 'letter-spacing="3" fill="#65796d"')
    for way in data['elements']:
        coords = [xy(p['lon'], p['lat']) for p in way['geometry']]
        # The source query includes entire ways; clip the drawing to the map.
        parts.append('<g clip-path="url(#mapclip)">')
        path(coords, '#b5d8e7', 13)
        path(coords, '#508ba6', 1.5)
        parts.append('</g>')
    # Model-defined gates and chart-contained reference route; OSM supplies context.
    _, _, _, gates, route = build()
    frame = LocalFrame()
    outbound = [xy(*frame.unproject(x,y)) for x,y in route.coords]
    path([(x, y-8) for x, y in outbound], '#ab4e23', 3, 'marker-end="url(#out)"')
    path([(x, y+8) for x, y in reversed(outbound)], '#176a65', 3, 'marker-end="url(#back)"')
    for name, lon, lat, dx, dy in [
        ('The Dalles', -121.185, 45.608, -105, 45),
        ('Mosier', -121.399, 45.684, -10, 55),
        ('Hood River', -121.522, 45.709, -55, 76),
        ('Cascade Locks', -121.89, 45.669, 28, 40),
        ('Bonneville', -121.94, 45.645, -55, 72),
        ('Stevenson', -121.884, 45.695, -80, -43),
    ]:
        x, y = xy(lon, lat)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#183047"/>')
        path([(x, y), (x+dx, y+dy-8)], '#81929c', 1)
        text(x+dx, y+dy, name, 18)
    for name,label in [('westGate','Light 7'),('eastGate','Buoy 69')]:
        point=gates[name].interpolate(.5,normalized=True)
        x,y=xy(*frame.unproject(point.x,point.y))
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#96396a"/>')
        text(x-30,y-22,label,15)
    text(230, 397, 'Chart-based reference course between proposed gates', 18)
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
    text(397, 442, '1  Downstream to Bonneville', 18)
    path([(320, 474), (380, 474)], '#176a65', 3, 'marker-end="url(#back)"')
    text(397, 481, '2  Upstream to The Dalles', 18)
    text(32, 518, 'Gate references and route: NOAA ENC · Gate offsets: TransGorgeCourse model', 14)
    text(32, 545, 'River geometry © OpenStreetMap contributors · ODbL · openstreetmap.org/copyright', 14)
    parts += ['</g><defs><clipPath id="mapclip"><rect x="25" y="90" width="1090" '
              'height="315"/></clipPath></defs></svg>']
    target = ROOT / 'docs/figures/gorge-course-map.svg'
    target.write_text('\n'.join(parts)+'\n', encoding='utf-8')
    return target


if __name__ == '__main__':
    print(render())
