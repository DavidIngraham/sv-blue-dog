"""Current class allocations need reviewed motion, consequence and reliability evidence."""
import pytest
from tools.boat_analysis.model.runtime import load_model, numerical_value

@pytest.fixture(scope='module')
def model():
    return load_model()

def assess(model, **changes):
    inputs=dict(classId='occupiedKayak',classificationReliable=True,conservativeEnvelopeReviewed=False,
        classificationReviewRef='synthetic classification review',relativeSpeedBoundMps=2,responseBoundS=10,
        positionAllowanceM=10,motionBoundAvailable=True,observationBoundAvailable=True,
        consequenceClearanceM=5,consequenceMarginM=5,consequenceReviewRef='synthetic consequence review',
        exposureReviewRef='synthetic exposure review',allocationReviewRef='synthetic allocation review',
        requiredTimelyTrackProbability=.99,requiredConfidenceLevel=.95,reliabilityReviewRef='synthetic reliability review',
        demonstratedRangeM=100,timelyTrackProbabilityLowerBound=.995,evidenceConfidenceLevel=.95,
        independentEncounterCount=1000,observationEvidenceRef='synthetic observation evidence',
        maneuverEvidenceRef='synthetic maneuver evidence',consequenceEvidenceRef='synthetic consequence evidence',
        riskAcceptanceRef='synthetic risk decision',collisionAndNonImpedimentSupported=True,
        requiredResponseProbability=.98,responseProbabilityLowerBound=.99,responseEvidenceConfidenceLevel=.95,
        responseEvidenceRef='synthetic whole response evidence',responseReliabilityReviewRef='synthetic response review',
        evidenceMethodReviewRef='synthetic method applicability review')
    inputs.update(changes)
    r=model.run_analysis('BlueDogClassDetection::Assessment',subject='BlueDogClassDetection::policy',named_arguments=inputs)
    assert r
    return numerical_value(r.outputs)

def test_current_class_summary_keeps_historical_numbers_separate(model):
    r=numerical_value(model.run_analysis('BlueDogClassDetection::Summary').outputs)
    assert r['classIds'][-4:]==['occupiedKayak','occupiedSUP','personInWater','unoccupiedDriftingCraft']
    assert r['illustrativeResponseDistanceM']==pytest.approx([313.5,205.5,742,303,333,225,225,225,225])
    assert r['currentAllocationsAccepted'] is False
    assert r['physicalQualification'] is False
    old=numerical_value(model.run_analysis('BlueDogEncounterReview::Acquisition').outputs)
    assert old['requiredRangesM']==pytest.approx([307,201,724,296,326,220])

def test_supplied_consistent_reviews_have_no_hidden_750_floor(model):
    r=assess(model)
    assert r['allocationAccepted'] is True
    assert r['acceptedDetectionDistanceM']==40
    assert r['physicalQualification'] is False

def test_consequence_cannot_discount_kinematic_distance(model):
    r=assess(model,consequenceClearanceM=0,consequenceMarginM=0)
    assert r['kinematicMinimumM']==30
    assert r['acceptedDetectionDistanceM']==30
    assert assess(model,consequenceMarginM=-1)['allocationAccepted'] is False

@pytest.mark.parametrize('changes',[
    {'classId':'unknown'}, {'classificationReliable':False},
    {'classId':'unclassified'}, {'classificationReviewRef':''},
    {'consequenceReviewRef':''}, {'exposureReviewRef':''}, {'riskAcceptanceRef':''},
    {'requiredTimelyTrackProbability':0}, {'requiredResponseProbability':0},
    {'timelyTrackProbabilityLowerBound':.98}, {'responseProbabilityLowerBound':.97},
    {'evidenceConfidenceLevel':.9}, {'responseEvidenceConfidenceLevel':.9},
    {'evidenceMethodReviewRef':''}, {'maneuverEvidenceRef':''},
    {'responseEvidenceRef':''}, {'independentEncounterCount':0},
    {'motionBoundAvailable':False}, {'observationBoundAvailable':False},
    {'collisionAndNonImpedimentSupported':False}, {'demonstratedRangeM':39},
])
def test_missing_or_inadequate_evidence_cannot_accept(model,changes):
    r=assess(model,**changes)
    assert r['allocationAccepted'] is False
    assert r['acceptedDetectionDistanceM']==-1

def test_unclassified_requires_declared_conservative_plausible_class_review(model):
    r=assess(model,classId='unclassified',classificationReliable=False,conservativeEnvelopeReviewed=True)
    assert r['allocationAccepted'] is True
    assert assess(model,classificationReliable=False,conservativeEnvelopeReviewed=True)['allocationAccepted'] is False

def test_sensor_timing_alone_cannot_establish_response_reliability(model):
    r=assess(model,responseProbabilityLowerBound=.1)
    assert r['timingFeasible'] is True
    assert r['reliabilitySatisfied'] is True
    assert r['allocationAccepted'] is False


@pytest.mark.parametrize('changes', [
    {'requiredResponseProbability': 0},
    {'requiredResponseProbability': 1.01},
    {'responseReliabilityReviewRef': ''},
])
def test_unreviewed_response_criterion_cannot_publish_reviewed_distance(model, changes):
    r = assess(model, **changes)
    assert r['allocationReviewed'] is False
    assert r['reviewedDesignDistanceM'] == -1
    assert r['status'] == 'Unsupported: current class allocation not reviewed'
    assert r['allocationAccepted'] is False


def test_reviewed_criteria_can_precede_response_evidence(model):
    r = assess(model, responseEvidenceRef='')
    assert r['allocationReviewed'] is True
    assert r['reviewedDesignDistanceM'] == 40
    assert r['allocationAccepted'] is False
    assert r['status'] == 'Reviewed design distance only; safety acceptance unsupported'


@pytest.mark.parametrize('kind',['windsurfer','wingfoiler','kiter'])
def test_wind_sports_require_the_same_supported_allocation_inputs(model,kind):
    assert assess(model,classId=kind)['allocationAccepted'] is True
    assert assess(model,classId=kind,classificationReliable=False)['allocationAccepted'] is False
    assert assess(model,classId=kind,responseProbabilityLowerBound=0)['allocationAccepted'] is False
