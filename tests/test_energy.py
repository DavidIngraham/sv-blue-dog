"""Native energy accounting regressions; no Python implementation of the model."""
import json
import re
import pytest
from scripts.render_requirements import native_energy_case


def check_values(check):
    return {v['name']: v['value'] for v in check['values']}

@pytest.fixture
def run_case(run_model):
    def run_case(body='', base='BlueDogEnergyExamples::campaign', extra='', analysis='SustainedOperation'):
        source = ('package EnergyTest { private import SI::*; ' + extra +
                  f'part candidate :> {base} {{ {body} }} }}')
        code, report = run_model(source, '-instantiate', 'EnergyTest::candidate', '-analysis',
                                 f'BlueDogEnergy::{analysis} EnergyTest::candidate')
        assert not [d for d in report['diagnostics'] or [] if d['pass'] != 'runtime'], 'Test must reach execution, not fail parsing or resolution'
        return code, report, check_values(report['checks'][0]) if report['checks'] else {}

    return run_case


def numbers(sequence):
    return [float(n) for n in re.findall(r'(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?) \[', sequence)]

def test_rollup_and_synthetic_campaign():
    report = json.loads(native_energy_case())
    budget, case = map(check_values, report['checks'])
    assert float(budget['averageDemand'].split()[0]) == pytest.approx(6.38825, rel=0, abs=5e-08)
    assert float(budget['coincidentPeak'].split()[0]) == pytest.approx(31.433333333, rel=0, abs=5e-08)
    assert case['modeledEnergyFeasible'] == 'true'
    assert case['energyCaseSupported'] == 'false'
    assert case['evidenceReady'] == 'false'
    assert case['harvestHoursPerDay'] == '[6.0, 6.0, 6.0]'
    history = numbers(case['energyHistory'])
    assert len(history) == 7
    assert history[1] == pytest.approx(186750.0, rel=0, abs=5e-08)
    assert history[-1] == pytest.approx(720000.0, rel=0, abs=5e-08)
    assert max(history) <= 720000.0

def test_overnight_failure_despite_recovered_final_energy(run_case):
    code, _, v = run_case('attribute :>> initialEnergy = 630000 [J];')
    assert code == 1
    assert v['repeatableBalance'] == 'true'
    assert v['reserveProtected'] == 'false'
    assert v['modeledEnergyFeasible'] == 'false'

def test_no_harvest_exhausts_storage(run_case):
    body = ' '.join(f'part redefines harvest{i} {{ attribute :>> harvestEnabled = false; }}' for i in range(1, 4))
    code, _, v = run_case(body)
    assert code == 1
    assert v['reserveProtected'] == 'false'
    assert v['repeatableBalance'] == 'false'
    # Negative balance is exposed as a deficit, not clipped to a reassuring zero.
    assert numbers(v['energyHistory'])[-1] < 0

def test_charge_rate_limit_cannot_hide_behind_available_solar(run_case):
    code, _, v = run_case('part redefines battery { attribute :>> maxChargePower = 1 [W]; }')
    assert code == 1
    assert v['repeatableBalance'] == 'false'

def test_peak_supply_is_independent_of_average_energy(run_case):
    code, _, v = run_case('part redefines battery { attribute :>> maxDischargePower = 10 [W]; }')
    assert code == 1
    assert v['repeatableBalance'] == 'true'
    assert v['reserveProtected'] == 'true'
    assert v['peakSupported'] == 'false'

def test_enabled_zero_resource_still_counts_against_campaign(run_case):
    code, _, v = run_case('part redefines dark1 { attribute :>> harvestEnabled = true; }')
    assert code == 1
    assert v['campaignCovered'] == 'false'
    assert v['harvestHoursPerDay'] == '[24.0, 6.0, 6.0]'

@pytest.mark.parametrize("body", [
    'part redefines battery { attribute :>> usableFraction = 1.1; }',
    'part redefines dark1 { attribute :>> duration = -1 [s]; }',
    'attribute :>> initialEnergy = 720001 [J];',
], ids=['invalid-usable-fraction', 'negative-duration', 'above-capacity'])
def test_invalid_input_does_not_pass(run_case, body):
    code, report, _ = run_case(body)
    assert code != 0
    assert report['status'] != 'holds'


def test_missing_input_does_not_pass(run_case):
    code, report, _ = run_case(base='BlueDogEnergy::Scenario')
    assert code == 2
    assert report['status'] != 'holds'


def test_mode_change_and_component_growth_are_rolled_up(run_case):
    extra = '''part heavy :> BlueDogEnergyExamples::sailing {
        part additionalLoad :> loads {
            attribute :>> label = "Extra load";
            attribute :>> activePower = 100 [W];
            attribute :>> idlePower = 100 [W];
            attribute :>> activeFraction = 1;
            attribute :>> conversionEfficiency = 1;
            attribute :>> uncertaintyFactor = 1;
        }
    }'''
    code, _, v = run_case('part redefines dark1 { ref part :>> budget = heavy; }', extra=extra)
    assert code == 1
    assert v['reserveProtected'] == 'false'
    assert v['peakSupported'] == 'false'

def test_surviving_finite_run_does_not_establish_repeatability(run_case):
    body = ('part redefines battery { attribute :>> nominalEnergy = 9000000 [J]; } '
            'attribute :>> initialEnergy = 3600000 [J]; ' +
            ' '.join(f'part redefines harvest{i} {{ attribute :>> rawHarvestPower = 20 [W]; }}' for i in range(1, 4)))
    code, _, v = run_case(body)
    assert code == 1
    assert v['reserveProtected'] == 'true'
    assert v['repeatableBalance'] == 'false'

def test_verification_requires_evidence_and_numerical_success(run_case):
    code, _, v = run_case(analysis='SustainedEnergyVerification')
    assert code != 0
    assert v['verdict'] == 'VerdictKind::inconclusive'
    code, _, v = run_case('attribute :>> evidenceAccepted = true;', analysis='SustainedEnergyVerification')
    assert code == 0
    assert v['verdict'] == 'VerdictKind::pass'
    code, _, v = run_case('attribute :>> evidenceAccepted = true; attribute :>> initialEnergy = 630000 [J];', analysis='SustainedEnergyVerification')
    assert code != 0
    assert v['verdict'] == 'VerdictKind::fail'

def test_invalid_inputs_cannot_be_verified_even_with_evidence_flag(run_case):
    code, _, v = run_case('attribute :>> evidenceAccepted = true; part redefines battery { attribute :>> usableFraction = 1.1; }', analysis='SustainedEnergyVerification')
    assert code != 0
    assert v['verdict'] == 'VerdictKind::fail'

def test_harvest_window_overlap_is_counted_in_each_day(run_case):
    # Extend the first enabled interval across midnight. It contributes six
    # hours to day one and one hour to day two; the later harvest shifts too.
    # The profile is now 73 hours and fails complete-day coverage.
    code, _, v = run_case('part redefines harvest1 { attribute :>> duration = 25200 [s]; }')
    assert code == 1
    assert v['harvestHoursPerDay'] == '[6.0, 6.0, 6.0]'
    assert v['campaignCovered'] == 'false'
