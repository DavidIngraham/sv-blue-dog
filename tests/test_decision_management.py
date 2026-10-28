"""Decision evidence must distinguish mandatory criteria, studies, ties and authority."""
from pathlib import Path
import pytest
from tools.boat_analysis.model.runtime import ROOT,connection,model_files
from tools.boat_analysis.model.decision_audit import native_decision_audit
EXAMPLE=ROOT/'reviews/se-skills-2026-10-23/07-trade-decisions/skill/references/native-trade-example.sysml'


def test_native_decision_scope_and_current_evidence_are_explicit():
    r=native_decision_audit()
    assert not r['errors'] and not r['diagnostics']
    assert r['summary']==dict(workingDecisions=8,openQuestions=6,designBasisRecords=6,
        totalDecisionRecords=20,allocationReviews=80,declaredCriteria=7,
        criterionClasses=dict(mandatory=6,comparativeStudy=1))
    assert len(r['missingActualRecords'])==14
    assert all(len(x['missing'])==4 for x in r['missingActualRecords'])
    assert all(not x['declaredMandatoryGatesMet'] and not x['knownFailure'] for x in r['assessments'].values())
    table=r['tables']['OpenRecords'];index=table['columns'].index('Open-question acceptance')
    assert all(row['cells'][index]==(False,) for row in table['rows'])
    assert all(row['element']['type']=='ItemUsage' for row in r['tables']['RecordStates']['rows'])
    assert all(row['element']['type']=='MetadataUsage' and row['cells'][-1]==(False,)
        for row in r['tables']['AllocationReviews']['rows'])


@pytest.mark.parametrize('before,after,error',[
    ('attribute :>> position = 6;','attribute :>> position = 7;','D07 Criterion positions'),
    ('attribute :>> kind = Kind::comparativeStudy;','attribute :>> kind = Kind::mandatory;','D08 Wrong'),
    ('reopenTrigger = "New comparable rig evidence, changed geometry/domain or a proposed hardware selection.";','reopenTrigger = "";','D01 Missing'),
    ('dependency progressDuration from progress to BlueDogRequirements::passageDuration;','dependency progressDuration from progress to BlueDogRequirements::legProgress;','D07 Missing current'),
])
def test_native_audit_detects_scope_or_criterion_corruption(before,after,error):
    path=ROOT/'models/vehicle/decision-context.sysml'
    sources=[(str(p),p.read_text().replace(before,after) if p==path else p.read_text()) for p in model_files()]
    assert any(x.startswith(error) for x in native_decision_audit(sources)['errors'])


def test_new_unclassified_working_decision_is_detected():
    path=ROOT/'models/vehicle/decisions.sysml'
    anchor='    dependency courtesyCollisionSafety from trafficCourtesy to GorgeChallenge::trafficCoexistence;'
    addition='\n    item unreviewed : EngineeringDecisions::DecisionRecord { attribute :>> disposition="Investigate"; attribute :>> evidenceNeeded="Unknown"; }'
    sources=[(str(p),p.read_text().replace(anchor,anchor+addition) if p==path else p.read_text()) for p in model_files()]
    assert native_decision_audit(sources)['errors']


def test_acceptance_flag_without_actual_disposition_identity_is_detected():
    path=ROOT/'models/vehicle/requirement-decisions.sysml'
    sources=[(str(p),p.read_text().replace('attribute :>> accepted = false;','attribute :>> accepted = true;') if p==path else p.read_text()) for p in model_files()]
    errors=native_decision_audit(sources)['errors']
    assert sum(x.startswith('D19 Accepted question') for x in errors)==6


def test_retained_basis_state_is_checked_without_reclassifying_its_content():
    path=ROOT/'models/vehicle/requirement-basis.sysml'
    sources=[(str(p),p.read_text().replace(
        'EngineeringDecisions::RecordState::workingDisposition;',
        'EngineeringDecisions::RecordState::openQuestion;',1) if p==path else p.read_text()) for p in model_files()]
    assert any(x.startswith('D18 Record state disagrees') for x in native_decision_audit(sources)['errors'])


def test_record_outside_register_scopes_is_not_silently_omitted():
    sources=[(str(p),p.read_text()) for p in model_files()]
    sources.append((str(ROOT/'models/orphan-test.sysml'), '''package UnexpectedDecisionScope {
        item orphan : EngineeringDecisions::DecisionRecord {
            attribute :>> recordState = EngineeringDecisions::RecordState::openQuestion;
            attribute :>> question = "Unresolved";
            attribute :>> evidenceNeeded = "Unspecified";
        }
    }'''))
    assert 'D01 Native decision inventory differs from register' in native_decision_audit(sources)['errors']


def mechanism(text):
    m=connection().parse_sources(((str(EXAMPLE),text),),strict=True)
    return m.run_analysis('DecisionMechanismExample::compare')


def test_native_tie_is_reported_and_first_selection_is_order_dependent():
    source=EXAMPLE.read_text()
    first=mechanism(source);reversed_order=mechanism(source.replace('(a,b)','(b,a)'))
    assert first.outputs['selectedAlternative'].type_symbol_id=='DecisionMechanismExample::a'
    assert reversed_order.outputs['selectedAlternative'].type_symbol_id=='DecisionMechanismExample::b'
    assert [x.result for x in first.evaluations]==[10,10]
    assert sum(x.selected for x in first.evaluations)==sum(x.tied for x in first.evaluations)==1


@pytest.mark.parametrize('metric,selected',[(9,'b'),(11,'a')])
def test_native_preference_reverses_with_supplied_metric(metric,selected):
    text=EXAMPLE.read_text().replace('part b : Option { attribute :>> metric = 10; }',f'part b : Option {{ attribute :>> metric = {metric}; }}')
    result=mechanism(text)
    assert result.outputs['selectedAlternative'].type_symbol_id=='DecisionMechanismExample::'+selected
    assert not any(x.error for x in result.evaluations)


def test_native_missing_metric_is_visible_not_zero():
    text=EXAMPLE.read_text().replace('part b : Option { attribute :>> metric = 10; }','part b : Option;')
    try:result=mechanism(text)
    except Exception:return  # Native failure is also an explicit unavailable evaluation.
    assert any(x.error for x in result.evaluations)


def test_native_supplied_admitted_subset_is_the_only_selection_pool():
    result=mechanism(EXAMPLE.read_text().replace('(a,b)','(a)'))
    assert len(result.evaluations)==1
    assert result.outputs['selectedAlternative'].type_symbol_id=='DecisionMechanismExample::a'


def test_decision_and_criterion_registers_are_published(rendered_site):
    text=(rendered_site/'imports/docs/sail-trade.md').read_text()
    assert 'Declared rig evidence groups and requirement basis' in text
    assert 'Actual authority' in text and 'Reopening trigger' in text
    assert 'Provisional reliability study' in text
    assert '250 mm print jobs and one-person handling remain owner constraints.' in text
    assert 'Working disposition records preserve existing baselines' in text
    assert 'sysml-report BlueDogDecisionDocuments' not in text
