import pytest
from shapely.geometry import Polygon, Point, box

from tools.boat_analysis.environment.routing import reference_route, chart_domains


def test_route_goes_around_island_without_shortcutting():
    water = box(0,0,1000,500).difference(box(400,0,600,300))
    path = reference_route(water, (100,100), (900,100), 20)
    assert water.covers(path)
    assert path.length > 800
    assert not path.intersects(box(401,1,599,299))


def test_disconnected_water_is_not_bridged():
    water = box(0,0,400,400).union(box(600,0,1000,400))
    with pytest.raises(ValueError, match='No connected'):
        reference_route(water,(100,100),(900,100),20)


def test_gate_on_land_is_rejected():
    with pytest.raises(ValueError, match='outside routing'):
        reference_route(box(0,0,100,100),(-1,50),(50,50),10)
