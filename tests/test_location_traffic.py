"""Location exposure is conditional; a quiet-window estimate never waives capability."""
import pytest
from tools.boat_analysis.model.runtime import load_model, numerical_value

@pytest.fixture(scope='module')
def model():
    return load_model()

def window(model, **changes):
    args=dict(sectorId='hatchery',targetClass='wingfoiler',earliestEntryUtcS=3600,
        latestExitUtcS=5400,evidenceStartUtcS=3000,evidenceEndUtcS=6000,
        encounterRateUpperPerHour=2,reviewedExposureLimit=1,
        geometryReviewRef='synthetic geometry',rateEvidenceRef='synthetic counts',
        rateMethodReviewRef='synthetic method',exposureCriterionRef='synthetic review',
        conditionMatch=True,classAllocationAccepted=True,
        responseWithoutRiderCooperationSupported=True,navigationObligationsSupported=True,
        recoverySupported=True)
    args.update(changes)
    result=model.run_analysis('BlueDogLocationTraffic::WindowAssessment',
        subject='BlueDogLocationTraffic::policy',named_arguments=args)
    assert result
    return numerical_value(result.outputs)

def test_conditional_exposure_is_not_launch_authorization(model):
    r=window(model)
    assert r['expectedEncountersUpper']==1
    assert r['rowSupported'] is True
    assert r['launchAuthorized'] is False
    busy=window(model,encounterRateUpperPerHour=10)
    assert busy['expectedEncountersUpper']==5
    assert busy['rowSupported'] is False

@pytest.mark.parametrize('changes',[
    {'sectorId':'unmapped'}, {'targetClass':'unknown'},
    {'earliestEntryUtcS':-1}, {'latestExitUtcS':3600},
    {'evidenceStartUtcS':3601}, {'evidenceEndUtcS':5399},
    {'encounterRateUpperPerHour':-1}, {'geometryReviewRef':''},
    {'rateEvidenceRef':''}, {'rateMethodReviewRef':''}, {'conditionMatch':False},
])
def test_missing_scope_or_time_support_is_not_zero_exposure(model,changes):
    r=window(model,**changes)
    assert r['exposureSupported'] is False
    assert r['expectedEncountersUpper']==-1
    assert r['rowSupported'] is False

@pytest.mark.parametrize('changes',[
    {'reviewedExposureLimit':-1}, {'exposureCriterionRef':''},
    {'classAllocationAccepted':False}, {'responseWithoutRiderCooperationSupported':False},
    {'navigationObligationsSupported':False}, {'recoverySupported':False},
])
def test_low_exposure_never_waives_acceptance(model,changes):
    assert window(model,encounterRateUpperPerHour=0,**changes)['rowSupported'] is False

def test_delay_can_invalidate_previously_supported_window(model):
    assert window(model)['rowSupported'] is True
    late=window(model,latestExitUtcS=6001,reviewedExposureLimit=100)
    assert late['intervalSupported'] is False
    assert late['rowSupported'] is False

def test_hazard_and_verification_cases_remain_explicit(model):
    for name in ['windsurfCrossing','wingfoilTurn','kiteSweep','fallenRider','groupEncounter','windowOverrun']:
        assert model.find('BlueDogLocationTraffic::'+name)
    for name in ['WindSportEncounterVerification','LocationTrafficAdmissionVerification']:
        assert model.find('GorgeChallengeVerification::'+name)
