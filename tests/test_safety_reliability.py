"""Hazard linkage, honest closure and reliability dependence assumptions."""
import pytest
from tools.boat_analysis.model.runtime import load_model,connection,model_files
from tools.boat_analysis.model.safety_audit import native_safety_audit
from tests.native_edits import set_values, delete_symbols

@pytest.fixture(scope='module')
def sources():return tuple((str(p),p.read_text()) for p in model_files())

@pytest.fixture(scope='module')
def report(sources):return native_safety_audit(sources)


def test_initial_hazards_have_controls_plans_and_critical_contributors(report):
    assert not report['errors'] and not report['diagnostics']
    assert report['safetyReview']==dict(hazardCount=6,unresolvedHazardCount=6,hazardRecordsClosed=False,
        fmeaReady=False,reviewReady=False,ready=False)
    assert report['fmeaReview']==dict(modeCount=15,safetyCriticalCount=13,unresolvedCriticalCount=13,
        openActionCount=15,reviewReady=False)
    assert all(not r['closed'] and len(r['missing'])==3 for r in report['openRecords'])
    assert all(all(links.values()) for links in report['support'].values())


def test_wrong_configuration_is_detected(sources):
    mutant=set_values(sources,{'BlueDog::Analyses::Safety::HazardRecord::configuration':
                               'BlueDog::Evidence::CurrentSizing::candidate'})
    assert sum('Wrong hazard configuration' in e for e in native_safety_audit(mutant)['errors'])==6


@pytest.mark.parametrize('category,prefix,count',[
    ('contributors','handlingRetrievalExposureContributor',2),
    ('controls','handlingRetrievalExposureControl',3),
    ('verificationPlans','handlingRetrievalExposureVerification',3)])
def test_missing_hazard_argument_link_is_detected(sources,category,prefix,count):
    mutant=delete_symbols(sources, *(
        'BlueDog::Analyses::Safety::'+prefix+str(index) for index in range(1,count+1)))
    assert 'S02 Missing '+category+': BlueDog::Analyses::Safety::gorge::handlingRetrievalExposure' in native_safety_audit(mutant)['errors']


@pytest.mark.parametrize('field',['implementationEvidenceAccepted','effectivenessEvidenceAccepted',
    'residualRiskAssessmentAccepted','riskDispositionAccepted','controlEvidenceRecord','acceptanceRecord','acceptanceAuthority','condition'])
def test_incomplete_synthetic_disposition_cannot_close(sources,field):
    values={k:'true' for k in ('implementationEvidenceAccepted','effectivenessEvidenceAccepted',
        'residualRiskAssessmentAccepted','riskDispositionAccepted')}
    values|={k:'"synthetic-test-only"' for k in ('controlEvidenceRecord','acceptanceRecord','acceptanceAuthority')}
    values|={k:'"synthetic-test-only"' for k in ('identifier','condition','potentialMishap','modes','ownerRole','controlIntent')}
    values[field]='false' if field.endswith('Accepted') else '""'
    body=' '.join('attribute :>> '+k+' = '+v+';' for k,v in values.items())
    extra='package SafetyTest { part example : BlueDog::Analyses::Safety::HazardRecord {'+body+'} }'
    m=connection().parse_sources((*sources,('safety-negative.sysml',extra)),strict=True)
    assert m.eval('SafetyTest::example.closed') is False


def test_complete_synthetic_disposition_exercises_native_precondition_only(sources):
    body=' '.join('attribute :>> '+k+' = true;' for k in ('implementationEvidenceAccepted','effectivenessEvidenceAccepted',
        'residualRiskAssessmentAccepted','riskDispositionAccepted'))
    body+=' '.join('attribute :>> '+k+' = "synthetic-test-only";' for k in ('controlEvidenceRecord','acceptanceRecord','acceptanceAuthority','identifier','condition','potentialMishap','modes','ownerRole','controlIntent'))
    m=connection().parse_sources((*sources,('safety-positive.sysml',
        'package SafetyTest { part example : BlueDog::Analyses::Safety::HazardRecord {'+body+'} }')),strict=True)
    assert m.eval('SafetyTest::example.closed') is True
    assert m.eval('BlueDog::Analyses::Safety::gorge.collisionExposure.closed') is False


@pytest.mark.parametrize('missing',['criticalFunctionPartitionAccepted','dependenceTreatmentAccepted','commonCauseCoverageAccepted'])
def test_unreviewed_rate_model_cannot_become_supported(sources,missing):
    fields=('profileEvidenceAccepted','rateEvidenceAccepted','constantHazardAccepted',
        'criticalFunctionPartitionAccepted','dependenceTreatmentAccepted','commonCauseCoverageAccepted')
    body=' '.join('attribute :>> '+k+' = '+str(k!=missing).lower()+';' for k in fields)
    m=connection().parse_sources((*sources,('reliability-negative.sysml',
        'package RateTest { part example :> BlueDog::Configurations::Examples::Reliability::gorgeIllustration {'+body+'} }')),strict=True)
    r=m.run_analysis('BlueDog::Analyses::Reliability::CruiseReliability',subject='RateTest::example').outputs
    assert r['modeledFeasible'] is True
    assert r['reliabilitySupported'] is False


def test_rendered_hazards_keep_evidence_and_acceptance_open(rendered_site):
    text=(rendered_site/'imports/docs/reliability.md').read_text()
    assert 'HAZ-06' in text and '| Acceptance authority |' in text
    assert 'Six initial hazardous scenarios' in text

