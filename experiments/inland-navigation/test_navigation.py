import json
from pathlib import Path
import pytest
import run as experiment

FIXTURE = json.loads((experiment.HERE/'cases.json').read_text())

@pytest.fixture(scope='module')
def model():
    return experiment.load()

@pytest.mark.parametrize('case',FIXTURE['cases'],ids=lambda c:c['name'])
def test_rule_scenario(model,case):
    experiment.execute_case(model,FIXTURE,case)

def test_missing_input_is_not_defaulted(model):
    inputs=dict(FIXTURE['base']); del inputs['inSight']
    with pytest.raises(ValueError,match='every declared input'):
        experiment.assess(model,inputs)

def test_native_interface_matches_transport_schema(model):
    assert set(experiment.input_types(model)) == set(FIXTURE['base'])

def test_reusable_rule_sources_are_loaded_once():
    from tools.boat_analysis.model.runtime import model_files
    assert set(experiment.SOURCES) <= set(model_files())
    assert not (experiment.HERE/'navigation.sysml').exists()


EXTENDED = json.loads((experiment.HERE/'extended-cases.json').read_text())['suites']
EXTENDED_CASES = [(suite, case) for suite in EXTENDED for case in suite['cases']]

@pytest.mark.parametrize('suite,case', EXTENDED_CASES, ids=[c['name'] for _,c in EXTENDED_CASES])
def test_extended_rule_scenario(model, suite, case):
    experiment.execute_case(model, suite, case)

@pytest.mark.parametrize('suite', EXTENDED, ids=[s['analysis'] for s in EXTENDED])
def test_extended_interface_and_missing_input(model, suite):
    assert set(experiment.input_types(model, suite['analysis'])) == set(suite['base'])
    inputs = dict(suite['base'])
    inputs.pop(next(iter(inputs)))
    with pytest.raises(ValueError, match='every declared input'):
        experiment.assess(model, inputs, suite['analysis'])


def composed_frames():
    frames = {s['analysis']: dict(s['base']) for s in EXTENDED if not s['analysis'].endswith('CandidateAssessment')}
    frames['InlandNavigationExperiment::Assess'] = dict(FIXTURE['base'])
    frames['InlandExtended::RestrictedVisibility'].update(inSight=True, inOrNearRestricted=False)
    frames['InlandExtended::Signals']['inSight'] = True
    frames['InlandExtended::General']['riskAssessment'] = 'yes'
    return frames


def test_composed_native_assessment_rejects_independent_channel_failure(model):
    frames = composed_frames()
    assurance = dict(additionalApplicableClausesReviewed=True)
    nominal = experiment.compose_candidate(model, frames, assurance)
    assert nominal['InlandExtended::CandidateAssessment']['candidateSupported'] is True
    frames['InlandExtended::ChannelsAndTSS'].update(channel=True, otherConfined=True,
        crossingChannel=True, crossingImpede=True)
    frames['InlandNavigationExperiment::Assess'].update(channelContext='yes', otherConfinedToChannel='yes',
        crossingChannel='yes', crossingWouldImpede='yes')
    adverse = experiment.compose_candidate(model, frames, assurance)
    assert adverse['InlandExtended::SnapshotConsistency']['consistent'] is True
    assert adverse['InlandExtended::ChannelsAndTSS']['channelSupported'] is False
    assert adverse['InlandExtended::CandidateAssessment']['candidateSupported'] is False


def test_native_required_input_is_not_defaulted(model):
    from opensysml import EnumLiteral
    inputs = dict(FIXTURE['base']); del inputs['inSight']
    kinds = experiment.input_types(model)
    args = {k: EnumLiteral(kinds[k].resolved_id+'::'+v, kinds[k].resolved_id)
            if kinds[k].resolved_kind == 'enumDef' else v for k,v in inputs.items()}
    with pytest.raises(Exception, match='unbound parameter'):
        model.run_analysis('InlandNavigationExperiment::Assess',
            subject='InlandNavigationExperiment::context', named_arguments=args)


def test_composition_cannot_override_inconsistent_visibility(model):
    frames = composed_frames()
    frames['InlandExtended::Signals']['inSight'] = False
    result = experiment.compose_candidate(model, frames, dict(additionalApplicableClausesReviewed=True))
    assert result['InlandExtended::SnapshotConsistency']['consistent'] is False
    assert result['InlandExtended::CandidateAssessment']['candidateSupported'] is False


def test_composition_rejects_risk_discarded_after_steady_bearing(model):
    frames = composed_frames()
    frames['InlandNavigationExperiment::Assess']['riskOfCollision'] = 'no'
    frames['InlandExtended::RestrictedVisibility']['risk'] = 'no'
    frames['InlandExtended::General'].update(riskAssessment='no', approaching=True, bearingSteady=True)
    result = experiment.compose_candidate(model, frames, dict(additionalApplicableClausesReviewed=True))
    assert result['InlandExtended::General']['rule7RiskPresent'] is True
    assert result['InlandExtended::CandidateAssessment']['candidateSupported'] is False


def test_assurance_cannot_override_native_failed_domain(model):
    frames = composed_frames()
    frames['InlandExtended::General']['hearingLookout'] = False
    with pytest.raises(ValueError, match='Assurance may only supply'):
        experiment.compose_candidate(model, frames,
            dict(additionalApplicableClausesReviewed=True, generalSupported=True))


def test_composition_rejects_disconnected_passage_exchange(model):
    frames = composed_frames()
    frames['InlandExtended::Signals'].update(powerPair=True, underway=True, meetingCrossing=True, withinHalfMile=True)
    result = experiment.compose_candidate(model, frames, dict(additionalApplicableClausesReviewed=True))
    assert result['InlandExtended::Signals']['maneuverSignalRequired'] is True
    assert result['InlandExtended::SnapshotConsistency']['passageAgrees'] is False
    assert result['InlandExtended::CandidateAssessment']['candidateSupported'] is False


def test_composition_requires_evidence_for_core_agreement(model):
    frames = composed_frames()
    frames['InlandNavigationExperiment::Assess']['passageAgreement'] = 'portToPort'
    result = experiment.compose_candidate(model, frames, dict(additionalApplicableClausesReviewed=True))
    assert result['InlandExtended::SnapshotConsistency']['passageAgrees'] is False


def test_motor_sailing_requires_powered_signal_mode(model):
    frames = composed_frames()
    frames['InlandNavigationExperiment::Assess']['ownKind'] = 'power'
    frames['InlandExtended::LightsAndShapes'].update(mode='sail', sailAlsoPowered=True)
    frames['InlandExtended::Signals']['mode'] = 'sail'
    result = experiment.compose_candidate(model, frames, dict(additionalApplicableClausesReviewed=True))
    assert result['InlandExtended::SnapshotConsistency']['modeAgrees'] is False
    frames['InlandExtended::Signals']['mode'] = 'power'
    result = experiment.compose_candidate(model, frames, dict(additionalApplicableClausesReviewed=True))
    assert result['InlandExtended::SnapshotConsistency']['modeAgrees'] is True
