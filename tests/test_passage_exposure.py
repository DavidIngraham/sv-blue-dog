"""Native mission-scoping and conditional reliability sensitivity."""
import math
import pytest
from tools.boat_analysis.model.runtime import native_value


def test_equal_survival_contours_and_faster_example(run_model):
    code, report = run_model('package ExposureProbe {}', '-analysis', 'BlueDogPassageExposure::Contours')
    assert code == 0
    v = {row['name']: native_value(row['value']) for row in report['checks'][0]['values']}
    for target in [80, 90, 95, 99]:
        for hours, rate in zip(v['hours'], v[f'rate{target}']):
            assert math.exp(-hours * rate) == pytest.approx(target / 100)
    assert v['fasterWins'] is True
    assert v['slowerSurvival'] == pytest.approx(math.exp(-.06))
    assert v['fasterSurvival'] == pytest.approx(math.exp(-.045))


def test_gorge_does_not_inherit_future_mission_constraints(run_model):
    source = '''package ScopeProbe { private import ScalarValues::*;
        analysis Scope {
            out attribute ocean : Boolean = BlueDogMissionScope::current.requiresOceanQualification;
            out attribute indefinite : Boolean = BlueDogMissionScope::current.requiresIndefiniteOperation;
            out attribute cyclicEnergy : Boolean = BlueDogMissionScope::current.requiresRepeatableEnergyBalance;
            out attribute deadline : Boolean = BlueDogMissionScope::current.hasCompletionDeadline;
        }
    }'''
    code, report = run_model(source, '-analysis', 'ScopeProbe::Scope')
    assert code == 0
    v = {row['name']: native_value(row['value']) for row in report['checks'][0]['values']}
    assert v == dict(ocean=False, indefinite=False, cyclicEnergy=False, deadline=False)
