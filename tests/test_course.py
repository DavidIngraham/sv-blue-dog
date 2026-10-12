"""Gate crossings and actual chart coverage, independent of route controller."""
import json
from pathlib import Path

import pytest
from shapely.geometry import LineString, shape
from shapely import transform, unary_union

from tools.boat_analysis.environment.course import LocalFrame, marker_gate, crossing_direction
from tools.boat_analysis.model.runtime import native_value


def test_finite_directed_gate_crossing():
    gate = LineString([(0, 0), (0, 100)])
    assert crossing_direction(gate, (-10, 50), (10, 50)) == -1
    assert crossing_direction(gate, (10, 50), (-10, 50)) == 1
    assert crossing_direction(gate, (-10, 150), (10, 150)) == 0
    assert crossing_direction(gate, (-10, 50), (0, 50)) == 0
    assert crossing_direction(gate, (0, 20), (0, 60)) == 0


def test_frame_round_trip_and_offset():
    frame = LocalFrame()
    xy = frame.project(-121.9105283, 45.655125)
    assert frame.unproject(*xy) == pytest.approx((-121.9105283, 45.655125))
    assert marker_gate((-121.91, 45.65, 135, 80, 220)).length == pytest.approx(140)
    with pytest.raises(ValueError):
        marker_gate((-121.91, 45.65, 135, 220, 80))


def test_model_gate_segments_clear_charted_land_and_restrictions(run_model):
    code, report = run_model('package GateProbe {}', '-analysis', 'TransGorgeCourse::GateGeometry')
    assert code == 0
    values = {r['name']: native_value(r['value']) for r in report['checks'][0]['values']}
    root = Path(__file__).resolve().parents[1]
    features = json.loads((root / 'evidence/course/2026-10-11/chart-features.geojson').read_text())['features']
    frame = LocalFrame()
    def collect(kind):
        return unary_union([transform(shape(f['geometry']), frame.project, interleaved=False) for f in features
                            if f['properties']['object_class'] == kind and f['geometry']])
    land, restricted, depth, fairway = [collect(k) for k in ['LNDARE', 'RESARE', 'DEPARE', 'FAIRWY']]
    for key in ['westGate', 'eastGate']:
        gate = marker_gate(values[key], frame)
        assert not gate.intersects(land)
        assert not gate.intersects(restricted)
        assert depth.covers(gate)
        # Crossing is a traffic decision, not an empty-water assumption.
        assert gate.intersects(fairway)


def test_long_passage_has_no_gorge_deadline(run_model):
    states = ','.join(str(v) for _ in range(4) for v in [2,45,0,0,0,0,2,-45,0,0,0,0])
    source = f'''package DurationProbe {{ private import ScalarValues::*;
        analysis Probe {{
            out attribute noDeadline : Real [6] ordered nonunique = MarineCourse::Route(
                (2,2,2,2,2,2,2,2), ({states}), (1,0.2,0.3,1000000,0,0.5,0));
            out attribute legacyDeadline : Real [6] ordered nonunique = MarineCourse::Route(
                (2,2,2,2,2,2,2,2), ({states}), (1,0.2,0.3,1000000,72,0.5,0));
            out attribute activeDeadline : Real = BlueDogCoupledOperation::Inputs.routeParameters#(5);
        }}
    }}'''
    code, report = run_model(source, '-analysis', 'DurationProbe::Probe')
    assert code == 0
    values = {r['name']: native_value(r['value']) for r in report['checks'][0]['values']}
    assert values['noDeadline'][5] > 72
    assert values['noDeadline'][2] == 1
    assert values['legacyDeadline'][2] < 0
    assert values['activeDeadline'] == 0


def test_sizing_and_replay_share_chart_reference_distance(run_model):
    source = """package SizingCourseProbe { analysis Inputs {
        out attribute sizing : ScalarValues::Real = BlueDogCoupledOperation::Inputs.routeParameters#(4);
        out attribute primary : ScalarValues::Real = BlueDogCoupledUncertainty::Inputs.nominalRoute#(4);
        out attribute adverse : ScalarValues::Real = BlueDogCoupledUncertainty::Inputs.adverseRoute#(4);
        out attribute chart : ScalarValues::Real = TransGorgeCourse::policy.referenceLegLengthM;
    } }"""
    code, report = run_model(source, '-analysis', 'SizingCourseProbe::Inputs')
    assert code == 0
    values = {r['name']: native_value(r['value']) for r in report['checks'][0]['values']}
    assert values['sizing'] == values['primary'] == values['adverse'] == values['chart']
    assert 68000 < values['chart'] < 69000
