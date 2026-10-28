"""Native V&V planning, evidence applicability and meaningful negative controls."""
import pytest
from opensysml.errors import ExecutionError
from tools.boat_analysis.model.runtime import ROOT,load_model,model_files,connection
from tools.boat_analysis.model.verification_audit import native_verification_audit
from tests.native_edits import set_values, delete_symbols, replace_unique


@pytest.fixture(scope='module')
def sources():return tuple((str(p),p.read_text()) for p in model_files())


@pytest.fixture(scope='module')
def report(sources):return native_verification_audit(sources)


def test_all_project_definitions_have_methods_and_objectives_without_execution(report):
    assert not report['errors'] and not report['diagnostics']
    assert report['summary']==dict(verificationDefinitions=100,withPlannedMethods=100,
        declaredPlanResults=97,integrationPlans=2)
    assert report['executedByAudit'] is False and report['evidenceAcceptanceAssessed'] is False
    assert all(set(row['missing'])=={'Actual article','Released procedure','Instruments'}
        for row in report['openEvidence'])



def test_nested_unplanned_verification_is_not_lost_beneath_namespace_containers(sources):
    extra='package AdditionalVerification { package Nested { verification def Unplanned { subject target; } } }'
    report=native_verification_audit((*sources,(str(ROOT/'reviews/nested-verification.sysml'),extra)))
    identity='AdditionalVerification::Nested::Unplanned'
    assert 'V04 Missing planned method: '+identity in report['errors']
    assert report['summary']['verificationDefinitions']==101


def test_method_choices_distinguish_inspection_analysis_and_user_demonstration(report):
    rows={r['element']['id']:r['cells'] for r in report['tables']['Plans']['rows']}
    methods=lambda name:{x['id'].rsplit('::',1)[-1] for x in rows[name][1]}
    assert methods('BlueDog::Verification::Requirements::ConstructionArchitectureVerification')=={'inspect'}
    assert methods('BlueDog::Verification::Requirements::SustainedReserveProtectionVerification')=={'analyze'}
    assert methods('BlueDog::Verification::Planning::HumanRecoveryUseValidation')=={'test','demo'}
    assert methods('BlueDog::Analyses::Energy::SustainedEnergyVerification')=={'analyze'}


def test_numerical_eligibility_never_changes_planned_verdicts(report):
    m=load_model()
    assert m.calc('BlueDog::Verification::Planning::EvidenceEligibleForAcceptance',[True]*11).value is True
    for row in report['tables']['PlannedVerdicts']['rows']:
        assert [r['id'] for r in row['cells'][1]]==['VerificationCases::VerdictKind::inconclusive']
    assert m.eval('BlueDog::Evidence::CurrentSizing::nominal.evidenceAccepted') is False


FIELDS=('executed','subjectIdentified','configurationApplicable','conditionsApplicable','procedureControlled',
    'provenanceIntact','measurementBasisAdequate','uncertaintyAdequate','criterionEvaluated','criterionHolds','anomaliesAccounted')


@pytest.mark.parametrize('case,changes',[
    ('planned-only',{'executed':False}),
    ('unidentified-article',{'subjectIdentified':False}),
    ('historical-other-configuration',{'configurationApplicable':False}),
    ('outside-admitted-conditions',{'conditionsApplicable':False}),
    ('uncontrolled-procedure',{'procedureControlled':False}),
    ('tampered-artifact',{'provenanceIntact':False}),
    ('inadequate-reference-or-instrumentation',{'measurementBasisAdequate':False}),
    ('unsupported-uncertainty',{'uncertaintyAdequate':False}),
    ('criterion-never-evaluated',{'criterionEvaluated':False}),
    ('valid-failed-test',{'criterionHolds':False}),
    ('unaccounted-anomaly',{'anomaliesAccounted':False}),
])
def test_incomplete_or_failed_evidence_cannot_support_affirmative_acceptance(case,changes):
    # Synthetic review assertions; this does not manufacture an actual evidence assessment.
    inputs={name:True for name in FIELDS}|changes
    assert load_model().calc('BlueDog::Verification::Planning::EvidenceEligibleForAcceptance',
        [inputs[name] for name in FIELDS]).value is False


def test_missing_evidence_review_input_is_not_success():
    with pytest.raises(ExecutionError):
        load_model().calc('BlueDog::Verification::Planning::EvidenceEligibleForAcceptance',[True]*10)


def test_missing_method_annotation_is_detected(sources):
    mutant=delete_symbols(sources,'BlueDog::Verification::Requirements::ResetRecoveryVerification::plannedTest')
    assert 'V04 Missing planned method: BlueDog::Verification::Requirements::ResetRecoveryVerification' in native_verification_audit(mutant)['errors']


def test_archived_design_cannot_substitute_for_planned_ic01_test_article(sources):
    mutant=set_values(sources,{'BlueDog::Verification::Planning::interfaceBench::plannedDesign':
                               'BlueDog::Evidence::CurrentSizing::candidate'})
    assert 'V02 Wrong planned design: BlueDog::Verification::Planning::interfaceBench' in native_verification_audit(mutant)['errors']


def test_removing_uncertainty_precondition_changes_native_eligibility(sources):
    old='and measurementBasisAdequate and uncertaintyAdequate and criterionEvaluated'
    assert sum(t.count(old) for _,t in sources)==1
    m=connection().parse_sources(replace_unique(sources,old,
        'and measurementBasisAdequate and criterionEvaluated'),strict=True)
    inputs={name:True for name in FIELDS}|dict(uncertaintyAdequate=False)
    assert m.calc('BlueDog::Verification::Planning::EvidenceEligibleForAcceptance',
        [inputs[name] for name in FIELDS]).value is True


def test_rendered_verification_tables_preserve_plan_and_execution_distinction(rendered_site):
    text=(rendered_site/'imports/docs/validation-plan.md').read_text()
    assert '| Planned methods |' in text
    assert '| Actual article |' in text
    assert 'executes no verification and accepts no evidence' in text
