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


def test_current_rounding_and_return_remain_chart_clear():
    from tools.boat_analysis.environment.routing import build, rounding_paths
    values,water,groups,gates,route=build()
    paths=rounding_paths(water,gates,route,values['routing'][4])
    assert all(water.covers(gate) for gate in gates.values())
    assert all(water.covers(path) for path in paths)
    assert sum(path.length for path in paths)==pytest.approx(2*values['referenceLegLengthM'],abs=.01)
    assert not paths[1].intersects(groups['ROUNDING_EXCLUSION'])
    assert not paths[2].intersects(groups['ROUNDING_EXCLUSION'])
