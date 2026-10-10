"""Exercise the production SysML constraints with synthetic observations.

These are evaluator/criterion regressions, not vessel qualification evidence.
"""
import pytest


@pytest.fixture
def evaluate(run_model):
    def evaluate(definition, inputs):
        bindings = '\n'.join(f'attribute :>> {key} = {value};' for key, value in inputs.items())
        source = ('package CriterionExample { private import SI::*; '
                  f'requirement sample : BlueDogRequirements::{definition} {{ {bindings} }} }}')
        code, report = run_model(source, '-requirement', 'CriterionExample::sample')
        return code, report['status']

    return evaluate


@pytest.mark.parametrize("axis", ["jobX", "jobY", "jobZ"])
@pytest.mark.parametrize("invalid", ["250.1 [mm]", "0 [mm]", "-1 [mm]"])
def test_print_job_out_of_bounds(evaluate, axis, invalid):
    baseline = dict(jobX='250 [mm]', jobY='0.25 [m]', jobZ='249 [mm]')
    assert evaluate('DesktopManufacture', baseline | {axis: invalid}) == (1, 'fails')


def test_print_job_boundaries_and_units(evaluate):
    assert evaluate('DesktopManufacture', dict(jobX='250 [mm]', jobY='0.25 [m]', jobZ='249 [mm]')) == (0, 'holds')


@pytest.mark.parametrize("value, expected", [
    ('30 [s]', (0, 'holds')), ('30.1 [s]', (1, 'fails')), ('-1 [s]', (1, 'fails')),
])
def test_reset_deadline(evaluate, value, expected):
    assert evaluate('RestartDeadline', {'measuredRestartTime': value}) == expected


@pytest.mark.parametrize("change, expected", [
    ({}, (0, 'holds')), ({'reserveEnergy': '302399 [J]'}, (1, 'fails')),
    ({'motorPower': '-100 [W]'}, (1, 'fails')),
], ids=['boundary', 'insufficient-reserve', 'negative-power'])
def test_recovery_energy_boundary(evaluate, change, expected):
    # 1.2 * (100 W * 1800 s + 10 W * 7200 s) = 302400 J.
    inputs = dict(motorPower='100 [W]', essentialPower='10 [W]', reserveEnergy='302400 [J]')
    assert evaluate('RecoveryEnergy', inputs | change) == expected


@pytest.mark.parametrize("definition, field, limit", [
    ('RightingDeadline', 'measuredRightingTime', 60),
    ('ControlRecoveryDeadline', 'measuredControlRecoveryTime', 120),
])
@pytest.mark.parametrize("case", ['boundary', 'over-limit', 'negative'])
def test_capsize_deadlines(evaluate, definition, field, limit, case):
    seconds = {'boundary': limit, 'over-limit': limit + 1, 'negative': -1}[case]
    expected = (0, 'holds') if case == 'boundary' else (1, 'fails')
    assert evaluate(definition, {field: f'{seconds} [s]'}) == expected


@pytest.mark.parametrize("count, expected", [
    (1710, (0, 'holds')), (1709, (1, 'fails')), (1800, (0, 'holds')),
    (1801, (1, 'fails')), (-1, (1, 'fails')),
])
def test_navigation_availability_counts_missing_epochs(evaluate, count, expected):
    assert evaluate('NavigationValidEpochs', {'validEpochs': str(count)}) == expected


LAUNCH_INPUTS = dict(conservativeStartEnergy='101 [J]', protectedReserve='100 [J]',
                     estimateAge='1 [s]', estimateValid='true', reserveValid='true', missionStartEnabled='true')


def test_launch_energy_valid_start(evaluate):
    assert evaluate('LaunchEnergyAdmission', LAUNCH_INPUTS) == (0, 'holds')


@pytest.mark.parametrize("change", [
    {'conservativeStartEnergy': '100 [J]'}, {'conservativeStartEnergy': '99 [J]'},
    {'estimateAge': '1.1 [s]'}, {'estimateAge': '-1 [s]'},
    {'estimateValid': 'false'}, {'reserveValid': 'false'}, {'protectedReserve': '0 [J]'},
], ids=['at-reserve', 'below-reserve', 'stale', 'negative-age', 'invalid-estimate', 'invalid-reserve', 'zero-reserve'])
@pytest.mark.parametrize("enabled", [True, False], ids=['enabled', 'inhibited'])
def test_launch_energy_gate_and_input_validity(evaluate, change, enabled):
    inputs = LAUNCH_INPUTS | change | {'missionStartEnabled': str(enabled).lower()}
    assert evaluate('LaunchEnergyAdmission', inputs) == ((1, 'fails') if enabled else (0, 'holds'))


@pytest.mark.parametrize("known", [False, True], ids=['unknown', 'known'])
@pytest.mark.parametrize("qualifying", [False, True], ids=['nonqualifying', 'qualifying'])
@pytest.mark.parametrize("motor", [False, True], ids=['motor-off', 'motor-on'])
def test_challenge_motor_invariant(evaluate, known, qualifying, motor):
    allowed = not motor or (known and not qualifying)
    inputs = dict(qualificationStateKnown=str(known).lower(),
                  qualifying=str(qualifying).lower(), motorEnabled=str(motor).lower())
    assert evaluate('MotorQualificationInvariant', inputs) == ((0, 'holds') if allowed else (1, 'fails'))


@pytest.mark.parametrize("definition", [
    'DesktopManufacture', 'RestartDeadline', 'RecoveryEnergy', 'RightingDeadline',
    'ControlRecoveryDeadline', 'NavigationValidEpochs', 'LaunchEnergyAdmission', 'MotorQualificationInvariant',
])
def test_missing_observations_cannot_pass(evaluate, definition):
    code, status = evaluate(definition, {})
    assert code == 2
    assert status != 'holds'


@pytest.mark.parametrize("definition, inputs, failing", [
    ('SustainedReserveProtection', {'samples': '(101 [J], 102 [J])', 'reserve': '100 [J]'}, {'samples': '(101 [J], 100 [J], 102 [J])'}),
    ('RepeatableCycleBalance', {'initialEnergy': '100 [J]', 'finalEnergy': '100 [J]'}, {'finalEnergy': '99 [J]'}),
    ('PeakSupplyCapability', {'demands': '(10 [W], 10 [W])', 'availablePower': '10 [W]'}, {'demands': '(10 [W], 10.1 [W])'}),
    ('HarvestCampaignCoverage', {'duration': '259200 [s]', 'dayCount': '3', 'enabledHours': '(6, 6, 6)'}, {'enabledHours': '(6, 6.1, 6)'}),
    ('EnergyEvidenceReadiness', {'accepted': 'true'}, {'accepted': 'false'}),
], ids=['reserve', 'cycle-balance', 'peak-supply', 'harvest-coverage', 'evidence'])
@pytest.mark.parametrize("case", ['boundary', 'failing', 'missing'])
def test_sustained_energy_atomic_criteria_boundaries(evaluate, definition, inputs, failing, case):
    supplied = {'boundary': inputs, 'failing': inputs | failing, 'missing': {}}[case]
    code, status = evaluate(definition, supplied)
    assert code == {'boundary': 0, 'failing': 1, 'missing': 2}[case]
    assert (status == 'holds') == (case == 'boundary')
