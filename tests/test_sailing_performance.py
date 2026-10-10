"""Native inverse-polar, hull-screening and cruise-coupling regressions."""
import math

import pytest


@pytest.fixture
def sailing(run_model):
    def run(body='', base='BlueDogSailingExamples::UpstreamHeadwind', analysis='PolarDemandAndHullScreen'):
        source = ('package SailingTest { private import SI::*; '
                  f'part candidate : {base} {{ {body} }} }}')
        code, report = run_model(source, '-instantiate', 'SailingTest::candidate',
                                 '-analysis', f'BlueDogSailing::{analysis} SailingTest::candidate')
        assert not [d for d in report['diagnostics'] or [] if d['pass'] != 'runtime']
        values = {v['name']: v['value'] for c in report['checks'] or [] for v in c['values']}
        return code, values
    return run


def number(values, name):
    value = values[name].split()[0]
    if '/' in value:
        a, b = value.split('/')
        return float(a) / float(b)
    return float(value)


def test_upstream_polar_demand_and_hull_screen(sailing):
    code, v = sailing()
    assert code == 0
    assert number(v, 'requiredCleanPolarSpeed') == pytest.approx(3.721614637823934)
    assert number(v, 'requiredOperatingSpeed') == pytest.approx(2.977291710259147)
    assert number(v, 'requiredCleanKnots') == pytest.approx(7.23424011672039)
    assert number(v, 'waveReference') == pytest.approx(math.sqrt(9.80665 / (2 * math.pi)))
    assert number(v, 'requiredCleanFroude') == pytest.approx(1.1884230414520724)
    assert number(v, 'equivalentWaveLength') == pytest.approx(8.874052530298792)
    assert v['modeledFeasible'] == 'true'
    assert v['exceedsWaveReference'] == 'true'  # This is not treated as a hard speed ceiling.
    assert v['performanceSupported'] == 'false'


@pytest.mark.parametrize('speed,code', [('3.71', 1), ('3.73', 0)])
def test_speed_either_side_of_the_inverse_boundary(sailing, speed, code):
    result, v = sailing(f'attribute :>> cleanPolarSpeed = {speed} [m/s];')
    assert result == code
    assert v['minimumProgressMet'] == ('true' if code == 0 else 'false')
    assert v['inputsValid'] == 'true'


def test_tacking_gybing_and_current_are_not_conflated(sailing):
    _, beat = sailing()
    _, run = sailing(base='BlueDogSailingExamples::UpstreamTailwind')
    _, downstream = sailing(base='BlueDogSailingExamples::DownstreamHeadwind')
    assert number(run, 'requiredCleanPolarSpeed') == pytest.approx(3.4352823403481025)
    assert number(downstream, 'requiredGroundVMG') == pytest.approx(100000 / 36000)
    assert number(downstream, 'requiredCleanPolarSpeed') == pytest.approx(2.3776982408319576)
    assert number(beat, 'requiredCleanPolarSpeed') > number(run, 'requiredCleanPolarSpeed')


def test_shorter_time_budget_and_leeway_raise_upwind_demand(sailing):
    _, base = sailing()
    _, faster = sailing('attribute :>> allocatedTime = 43200 [s];')
    _, leeway = sailing('attribute :>> leeway = TrigFunctions::rad(5) * (1 [rad]);')
    assert number(faster, 'requiredGroundVMG') == pytest.approx(100000 / 43200)
    assert number(faster, 'requiredCleanPolarSpeed') > number(base, 'requiredCleanPolarSpeed')
    assert number(leeway, 'requiredCleanPolarSpeed') > number(base, 'requiredCleanPolarSpeed')


def test_current_reduces_or_increases_demand_without_being_derated(sailing):
    _, v = sailing('attribute :>> currentVMG = 0 [m/s];')
    assert number(v, 'requiredCleanPolarSpeed') == pytest.approx(0.5 / (0.8 * 0.95 * math.cos(math.pi / 4)))
    _, v = sailing('attribute :>> currentVMG = 1 [m/s];')
    assert number(v, 'requiredCleanPolarSpeed') == 0  # No negative required sail speed.
    assert number(v, 'candidateGroundVMG') == pytest.approx(4 * 0.8 * 0.95 * math.cos(math.pi / 4) + 1)


def test_hull_length_changes_reference_not_predicted_speed(sailing):
    _, base = sailing()
    _, longer = sailing('attribute :>> waterlineLength = 2 [m];')
    assert number(longer, 'waveReference') == pytest.approx(number(base, 'waveReference') * math.sqrt(2))
    assert number(longer, 'requiredCleanFroude') == pytest.approx(number(base, 'requiredCleanFroude') / math.sqrt(2))
    assert longer['requiredCleanPolarSpeed'] == base['requiredCleanPolarSpeed']
    assert longer['candidateGroundVMG'] == base['candidateGroundVMG']


def test_wind_strength_changes_required_ratio_not_a_predicted_polar(sailing):
    _, base = sailing()
    _, light = sailing('attribute :>> trueWindSpeed = 3 [m/s];')
    assert base['requiredCleanPolarSpeed'] == light['requiredCleanPolarSpeed']
    assert number(light, 'requiredSpeedWindRatio') == pytest.approx(number(base, 'requiredSpeedWindRatio') * 5 / 3)


@pytest.mark.parametrize('body', [
    'attribute :>> waterlineLength = 0 [m];',
    'attribute :>> retainedPerformance = 0;',
    'attribute :>> retainedPerformance = 1.01;',
    'attribute :>> maneuverRetention = 0;',
    'attribute :>> maneuverRetention = 1.01;',
    'attribute :>> allocatedTime = 0 [s];',
    'attribute :>> minimumGroundVMG = 0.49 [m/s];',
    'attribute :>> cleanPolarSpeed = 0 [m/s];',
    'attribute :>> distance = -1 [m];',
    'attribute :>> trueWindSpeed = 0 [m/s];',
    'attribute :>> leeway = -0.1 [rad];',
    'attribute :>> trueWindAngle = TrigFunctions::rad(90) * (1 [rad]);',
    'attribute :>> trueWindAngle = TrigFunctions::rad(120) * (1 [rad]);',
    'attribute :>> trueWindAngle = TrigFunctions::rad(181) * (1 [rad]);',
])
def test_invalid_inputs_or_nonforward_heading_cannot_pass(sailing, body):
    code, v = sailing(body)
    assert code != 0
    assert v.get('performanceSupported') != 'true'
    assert v.get('modeledFeasible') != 'true'


@pytest.mark.parametrize('field', ['polarEvidenceAccepted', 'hullEvidenceAccepted'])
def test_one_evidence_flag_does_not_support_the_claim(sailing, field):
    _, v = sailing(f'attribute :>> {field} = true;')
    assert v['performanceSupported'] == 'false'


def test_coupled_polar_legs_change_cruise_exposure(run_model):
    results = []
    for scenario, expected in [('gorgeWesterly', 61.54045659717509), ('gorgeEasterly', 57.31706223726946)]:
        code, report = run_model('package SailingTest {}', '-instantiate', f'BlueDogSailingExamples::{scenario}',
                                '-analysis', f'BlueDogSailing::PolarVoyageAssessment BlueDogSailingExamples::{scenario}')
        assert code == 0
        v = {x['name']: x['value'] for x in report['checks'][0]['values']}
        assert number(v, 'voyageHours') == pytest.approx(expected)
        assert number(v, 'allocatedHours') == 72
        assert v['voyageSupported'] == 'false'
        results.append(number(v, 'allowableRatePerHour'))
    assert results[1] > results[0]


def test_time_allocations_cannot_overbook_the_mission(run_model):
    source = '''package SailingTest { private import SI::*;
        part candidate :> BlueDogSailingExamples::gorgeWesterly {
            attribute :>> holdTime = 25200 [s];
        }
    }'''
    code, report = run_model(source, '-instantiate', 'SailingTest::candidate',
                             '-analysis', 'BlueDogSailing::PolarVoyageAssessment SailingTest::candidate')
    assert code != 0
    v = {x['name']: x['value'] for x in report['checks'][0]['values']}
    assert v['allocationValid'] == 'false'
    assert number(v, 'voyageHours') < 72  # Actual sample speed cannot waive an overbooked allocation.


def test_offshore_probe_is_duration_driven_and_unaccepted(run_model):
    code, report = run_model('package SailingTest {}', '-instantiate', 'BlueDogSailingExamples::oceanIllustration',
                             '-analysis', 'BlueDogSailing::PolarDemandAndHullScreen BlueDogSailingExamples::oceanIllustration')
    assert code == 0
    v = {x['name']: x['value'] for x in report['checks'][0]['values']}
    assert number(v, 'requiredGroundVMG') == pytest.approx(4000000 / 2419200)
    assert v['performanceSupported'] == 'false'
