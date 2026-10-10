"""Exercise native cruise/reliability calculations and DFMEA traceability."""
import json
import pytest
from scripts.render_requirements import native


@pytest.fixture
def cruise(run_model):
    def run(body='', analysis='CruiseReliability'):
        source = ('package ReliabilityTest { private import SI::*; '
                  'part candidate :> BlueDogReliabilityExamples::gorgeIllustration {' + body + '} }')
        code, report = run_model(source, '-instantiate', 'ReliabilityTest::candidate', '-analysis',
                                 f'BlueDogReliability::{analysis} ReliabilityTest::candidate')
        assert not [d for d in report['diagnostics'] or [] if d['pass'] != 'runtime']
        values = {v['name']: v['value'] for v in report['checks'][0]['values']} if report['checks'] else {}
        return code, values
    return run


def test_synthetic_exposure_and_evidence_gate(cruise):
    code, v = cruise()
    assert code == 0
    assert float(v['voyageHours']) == pytest.approx(69.4920634920635)
    assert float(v['requiredZeroFailureHours']) == pytest.approx(1975.878877008646)
    assert v['groundSpeeds'].count('SI') == 2
    assert v['modeledFeasible'] == 'true'
    assert v['demonstrationMet'] == 'true'
    assert v['reliabilitySupported'] == 'false'
    code, v = cruise(analysis='VoyageReliabilityVerification')
    assert code != 0
    assert v['verdict'] == 'VerdictKind::inconclusive'


def test_holds_increase_exposure_and_tighten_budget(cruise):
    _, base = cruise()
    _, v = cruise('attribute :>> holdTime = 43200 [s];')
    assert float(v['voyageHours']) == pytest.approx(float(base['voyageHours']) + 6)
    assert float(v['allowableRatePerHour']) < float(base['allowableRatePerHour'])
    assert float(v['requiredZeroFailureHours']) > float(base['requiredZeroFailureHours'])
    assert v['durationMet'] == 'false'


@pytest.mark.parametrize('body', [
    'part redefines upstream { attribute :>> currentVMG = -2 [m/s]; }',
    'part redefines upstream { attribute :>> currentVMG = -3 [m/s]; }',
    'part redefines upstream { attribute :>> retainedPerformance = 0; }',
    'attribute :>> holdTime = -1 [s];',
    'attribute :>> criticalRatesPerHour = (-0.001, 0.0003);',
    'attribute :>> commonCauseRatePerHour = -0.1;',
    'attribute :>> zeroFailureTestHours = 0;',
])
def test_invalid_profile_cannot_pass(cruise, body):
    code, v = cruise(body)
    assert code != 0
    assert v.get('modeledFeasible') != 'true'
    assert v.get('reliabilitySupported') != 'true'


def test_positive_but_inadequate_progress_fails(cruise):
    code, v = cruise('part redefines upstream { attribute :>> waterVMG = 2.4 [m/s]; }')
    assert code != 0
    assert v['inputsValid'] == 'true'
    assert v['minimumProgressMet'] == 'false'
    assert float(v['voyageHours']) > 69.5


def test_common_cause_rate_is_included(cruise):
    code, v = cruise('attribute :>> commonCauseRatePerHour = 0.01;')
    assert code != 0
    assert v['rateBudgetMet'] == 'false'
    assert float(v['modeledReliability']) < 0.90


def test_failures_invalidate_zero_failure_demonstration(cruise):
    _, v = cruise('attribute :>> observedCriticalFailures = 1;')
    assert v['demonstrationApplicable'] == 'false'
    assert v['demonstrationMet'] == 'false'
    assert v['reliabilitySupported'] == 'false'


def test_accepted_but_short_test_is_a_verification_failure(cruise):
    body = '''attribute :>> profileEvidenceAccepted = true;
              attribute :>> rateEvidenceAccepted = true;
              attribute :>> constantHazardAccepted = true;
              attribute :>> zeroFailureTestHours = 100;'''
    code, v = cruise(body, 'VoyageReliabilityVerification')
    assert code != 0
    assert v['verdict'] == 'VerdictKind::fail'


def test_accepted_synthetic_fixture_exercises_pass_path(cruise):
    # This tests verdict logic, not acceptance of the real project's synthetic evidence.
    body = '''attribute :>> profileEvidenceAccepted = true;
              attribute :>> rateEvidenceAccepted = true;
              attribute :>> constantHazardAccepted = true;'''
    code, v = cruise(body, 'VoyageReliabilityVerification')
    assert code == 0
    assert v['verdict'] == 'VerdictKind::pass'


def test_dfmea_starter_stays_open_and_has_real_links():
    report = json.loads(native('-instantiate', 'BlueDogDFMEA::starter', '-analysis',
                              'BlueDogDFMEA::DesignFailureReview BlueDogDFMEA::starter', '-json'))
    assert not report['diagnostics']
    v = {v['name']: v['value'] for v in report['checks'][0]['values']}
    assert v['modeCount'] == '12'
    assert v['unresolvedCriticalCount'] == '10'
    assert v['openActionCount'] == '12'
    assert v['reviewReady'] == 'false'
    table = native('-render-document', 'BlueDogReliabilityDocuments::DFMEA')
    for trace in ['| steeringJam | actuation |', '| steeringJam | weedSnagSteeringRecovery |',
                  '| powerCommonCause | powerManagement |', '| powerCommonCause | failureRateBudget |',
                  '| motorUncommanded | challengeMotorInhibition |']:
        assert trace in table
