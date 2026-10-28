"""Check scope, process responsibility and evidence independence through native queries."""
import pytest
from tools.boat_analysis.model.runtime import ROOT, load_model, model_files


@pytest.fixture(scope="module")
def quality_model():
    return load_model((*model_files(), ROOT / 'tools/publishing/reference.sysml',
                       ROOT / 'tests/fixtures/requirement-quality.sysml'))


def test_new_process_and_disturbance_outcomes_have_direct_objectives(quality_model):
    table = quality_model.run_document_query('RequirementQualityTests::Trace')
    rows = {r.element.id: r for r in table.rows}
    for name in ['navigationRuleApplicability', 'navigationRuleBaseline', 'navigationEntryEvidence',
                 'operatorSafetyIntervention', 'navigationAdjudication']:
        assert {v.id for v in rows['GorgeChallenge::'+name].cells[0]} == {
            'GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification'}
    for requirement, case in [('capsizeResilience', 'CapsizeResilienceVerification'),
                              ('vegetationResilience', 'VegetationResilienceVerification')]:
        assert {v.id for v in rows['BlueDogRequirements::'+requirement].cells[0]} == {
            'BlueDogRequirementVerification::'+case}
    for requirement in ['serviceability', 'wetElectricalIntegrity']:
        assert {v.id for v in rows['BlueDogRequirements::'+requirement].cells[1]} == {
            'BlueDog::Architecture::MissionContext::boat'}


def test_open_allocations_and_procedure_choices_have_reviewable_closure_records(quality_model):
    table = quality_model.run_document_query('BlueDogRequirementBasisDocuments::AllocationClosureRows')
    assert len(table.rows) == 80  # 77 requirement allocations and three procedure choices.
    for row in table.rows:
        assert all(row.cells[i] for i in range(8)), row.element.id
        assert row.cells[8] == (False,), row.element.id
    processes = quality_model.run_document_query('BlueDogRequirementBasisDocuments::ProcessRows')
    assert len(processes.rows) == 13
    assert all(all(row.cells) for row in processes.rows)
    decisions = quality_model.run_document_query('BlueDogRequirementBasisDocuments::EngineeringDecisionRows')
    assert len(decisions.rows) == 6
    assert all(row.cells[-1] == (False,) for row in decisions.rows)
