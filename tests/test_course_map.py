"""Publication must not displace real route coordinates to separate line styles."""
import json
from math import cos, radians
from xml.etree import ElementTree
import pytest
from tools.boat_analysis.environment.course import LocalFrame
from tools.boat_analysis.environment.routing import build, rounding_paths
from tools.publishing.course_map import render
from tools.publishing.course_satellite import mercator, image_xy, ARCHIVE


def test_rendered_tracks_retain_model_coordinates():
    tree=ElementTree.parse(render())
    values,water,_,gates,route=build()
    expected=[list(route.coords),[p for line in rounding_paths(water,gates,route,values['routing'][4])[1:] for p in line.coords]]
    scale=1050/(.53*cos(radians(45.7)))
    for color,coordinates in zip(['#ab4e23','#176a65'],expected,strict=True):
        line=next(e for e in tree.iter() if e.tag.endswith('polyline') and e.get('stroke')==color)
        points=[tuple(map(float,p.split(','))) for p in line.get('points').split()]
        assert len(points)==len(coordinates)
        for (px,py),(x,y) in zip(points,coordinates,strict=True):
            lon,lat=LocalFrame().unproject(x,y)
            assert px==pytest.approx(45+(lon+121.94)*scale*cos(radians(45.7)),abs=.051)
            assert py==pytest.approx(365-(lat-45.65)*scale,abs=.051)
    assert any(e.get('fill')=='#b5d8e7' and e.tag.endswith('path') for e in tree.iter())


def test_satellite_overlay_uses_returned_extent_and_north_up():
    assert mercator(0,0)==pytest.approx((0,0),abs=1e-8)
    assert mercator(180,0)[0]==pytest.approx(20037508.342789244)
    records=json.loads((ARCHIVE/'manifest.json').read_text())['views']
    values,*_=build()
    for name,key in [('bingen','eastGate'),('stevenson','westGate')]:
        r=records[name];lon,lat=values[key][:2]
        x,y=image_xy(lon,lat,r['extent'],r['width'],r['height'])
        assert x==pytest.approx(r['width']/2,abs=.01)
        assert y==pytest.approx(r['height']/2,abs=.01)
        assert image_xy(lon,lat+.001,r['extent'],r['width'],r['height'])[1]<y
        assert image_xy(lon+.001,lat,r['extent'],r['width'],r['height'])[0]>x
