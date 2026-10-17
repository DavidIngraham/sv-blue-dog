"""Native causal model, gate behavior and publication checks."""
import re
import pytest
from tools.boat_analysis.model.runtime import connection, load_model, model_files, ROOT, native
from tools.publishing.relationships import compact_failure_diagram

LEAVES = ('encounterDemand missedDetection lateObservation falseOrSwappedTrack '
          'wrongClassification wrongMotionPrediction wrongRuleAssessment noFeasibleCommand '
          'unsafeCourtesyChange steeringUnavailable sailControlUnavailable unobservedExecutionError '
          'sharedPowerLoss sharedComputeLoss unsafeAbortTransition inadequateRecoveryObservation '
          'noSafeRecoveryRoute recoveryTooLate').split()

@pytest.fixture(scope='module')
def cases():
    settings = {
        'clear': set(),
        'demandOnly': {'encounterDemand'},
        'primaryOnly': {'encounterDemand', 'steeringUnavailable'},
        'fallbackOnly': {'encounterDemand', 'noSafeRecoveryRoute'},
        'both': {'encounterDemand', 'steeringUnavailable', 'noSafeRecoveryRoute'},
        'commonPower': {'encounterDemand', 'sharedPowerLoss'},
        'commonCompute': {'encounterDemand', 'sharedComputeLoss'},
        'noDemand': {'sharedPowerLoss'},
    }
    parts = []
    for name, active in settings.items():
        fields = ''.join('occurrence :>> ' + leaf + ' { attribute :>> present = '
                         + str(leaf in active).lower() + '; }' for leaf in LEAVES)
        parts.append('occurrence ' + name + ' : BlueDogAvoidanceFailures::Exposure {' + fields + '}')
    source = 'package FailureProbe {' + ''.join(parts) + '}'
    return connection().parse_sources((*[(str(p), p.read_text()) for p in model_files()],
                                      ('failure-probe.sysml', source)), strict=True)

@pytest.mark.parametrize('case,primary,fallback,top', [
    ('clear', False, False, False), ('demandOnly', False, False, False),
    ('primaryOnly', True, False, False), ('fallbackOnly', False, True, False),
    ('both', True, True, True), ('commonPower', True, True, True),
    ('commonCompute', True, True, True), ('noDemand', True, True, False),
])
def test_encounter_demand_and_complete_response_paths(cases, case, primary, fallback, top):
    result = cases.run_analysis('BlueDogAvoidanceFailures::EvaluateExposure',
                               subject='FailureProbe::' + case)
    assert result.outputs == dict(primaryUnavailable=primary,
                                  recoveryUnavailable=fallback,
                                  safeSeparationUnsupported=top)

@pytest.mark.parametrize('review,count,critical', [
    ('BlueDogDFMEA::starter', 12, 10),
    ('BlueDogAvoidanceFailures::functional', 17, 17),
    ('BlueDogAvoidanceFailures::concepts', 15, 15),
])
def test_open_actions_cannot_be_mistaken_for_accepted_safeguards(review, count, critical):
    result = load_model().run_analysis('BlueDogDFMEA::DesignFailureReview', subject=review)
    assert result.outputs == dict(modeCount=count, safetyCriticalCount=critical,
                                  unresolvedCriticalCount=critical, openActionCount=count,
                                  reviewReady=False)


def test_shared_cause_is_one_native_node_with_two_response_connections():
    model = load_model((*model_files(), ROOT/'tools/publishing/reference.sysml'))
    view = model.render_view('BlueDogFailureViews::SystemTreeView')
    nodes = {node.name.rsplit('::', 1)[-1]: node.id for node in view.nodes if not node.parent}
    for common in ['sharedPowerLoss', 'sharedComputeLoss']:
        targets = {edge.to_id for edge in view.edges if edge.from_id == nodes[common]}
        assert targets == {nodes['OR_primaryUnavailable'], nodes['OR_recoveryUnavailable']}
    assert len(nodes) == 6 and len(view.edges) == 7


def test_native_tables_resolve_event_references_and_diagrams_preserve_connectors():
    paths = (*model_files(), ROOT/'tools/publishing/reference.sysml')
    table = native('-render-document', 'BlueDogAvoidanceDocuments::functional', models=paths)
    assert 'A relevant target is not observed before the response deadline.' in table
    assert 'Sensor coverage or sensitivity is inadequate' in table
    assert '|  |' not in table
    concepts = native('-render-document', 'BlueDogAvoidanceDocuments::concepts', models=paths)
    assert 'Scanner stops or reports a false azimuth' in concepts
    assert 'AC-01' in concepts and 'SC-03' in concepts and '|  |' not in concepts
    for name, count in [('SystemTree', 7), ('PrimaryTree', 4), ('ScannerTree', 5)]:
        raw = native('-render-document', 'BlueDogFailureViews::'+name,
                     '-diagram-form', 'mermaid', models=paths)
        compact = compact_failure_diagram(raw)
        old = re.findall(r'(n\d+)_anchor === (n\d+)_anchor', raw)
        new = re.findall(r'(n\d+) === (n\d+)', compact)
        assert old == new and len(new) == count
        assert 'subgraph' not in compact and '_anchor' not in compact
        assert 'description' not in compact and 'inputs' not in compact


def test_unassessed_exposure_does_not_default_to_safe():
    from opensysml.errors import AnalysisRunError
    with pytest.raises(AnalysisRunError):
        load_model().run_analysis('BlueDogAvoidanceFailures::EvaluateExposure',
                                  subject='BlueDogAvoidanceFailures::exposure')
