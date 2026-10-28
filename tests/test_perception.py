from dataclasses import replace
import numpy as np
import pytest
from shapely.geometry import LineString
from tools.boat_analysis.mission.perception import Observations, SensorEnvelope
from tools.boat_analysis.mission.traffic import Traffic
from tools.boat_analysis.mission.engine import simulate, Event
from tools.boat_analysis.model.runtime import load_model, analysis_values
from tests.test_mission_execution import fixture


def actor(**kw):
    return Traffic('target',LineString([(0,0),(100,0)]),0,1,2,1,0,**kw)


def test_latency_expiry_and_dropout():
    provider=Observations(SensorEnvelope(100,100,100,period_s=1,latency_s=2,expiry_s=4),dropouts=[(1,10)])
    truth=[actor()]
    assert provider.observe(truth,np.array([0.,0.]),0)==[]
    assert provider.observe(truth,np.array([0.,0.]),1)==[]
    assert len(provider.observe(truth,np.array([0.,0.]),2))==1
    assert len(provider.observe(truth,np.array([0.,0.]),3))==1
    assert provider.observe(truth,np.array([0.,0.]),4)==[]


def test_no_future_track_or_future_appearance_leaks():
    provider=Observations(SensorEnvelope(1000,1000,1000))
    turning=Traffic('turner',LineString([(0,0),(10,0),(10,100)]),0,1,2,1,0)
    assert provider.observe([replace(turning,start_seconds=10)],np.zeros(2),0)==[]
    provider.observe([turning],np.zeros(2),1)
    seen=provider.observe([turning],np.zeros(2),2)[0]
    assert seen.position(50)[1]==0  # The future northward turn is not disclosed.


def test_range_cooperation_and_weeds_are_separate():
    e=SensorEnvelope(10,5,0,cooperative_range_m=1000)
    assert Observations(e).observe([actor()],np.array([500.,0.]),0)==[]
    assert len(Observations(e).observe([actor(ais_equipped=True)],np.array([500.,0.]),0))==1
    assert Observations(e).observe([actor(target_kind='weed')],np.zeros(2),0)==[]


def test_total_misses_cannot_be_rescued_by_truth_guard():
    obstacle=Traffic('unseen obstruction',LineString([(0,0),(1,0)]),0,0,4000,4000,0,stationary_seconds=14400)
    provider=Observations(SensorEnvelope(10000,10000,10000,miss_probability=1))
    result=simulate(*fixture(),traffic=[obstacle],observations=provider)
    assert result.outcome=='safety_violation'
    assert result.cause=='traffic_collision'
    assert result.elapsed_seconds>0
    assert not result.observation_summary['trace']
    # The explicit legacy oracle baseline refuses to move instead.
    assert simulate(*fixture(),traffic=[obstacle]).cause=='no_safe_control_in_controller_search'


def test_seeded_observations_are_repeatable():
    e=SensorEnvelope(100,100,100,miss_probability=.3,error_m=5)
    results=[]
    for _ in range(2):
        p=Observations(e,17)
        positions=[]
        for t in range(10):
            positions.append([tuple(a.position(t)) for a in p.observe([actor()],np.zeros(2),t)])
        results.append((positions,p.trace))
    assert results[0]==results[1]


def test_native_distance_and_energy_sensitivities():
    m=load_model()
    def distance(maneuver,processing=1):
        return float(m.calc('BlueDog::Analyses::EncounterFeasibility::RequiredRange',arguments=[18,5,processing,2,maneuver,15,30,10]).value)
    assert distance(15)==pytest.approx(724)
    assert distance(30)==pytest.approx(994)
    assert distance(15,5)==pytest.approx(796)
    assert float(m.calc('BlueDog::Analyses::EncounterFeasibility::EnergyScreen',arguments=[0]).value)==pytest.approx(analysis_values('BlueDog::Analyses::CandidateEnergy::Reconciliation')['headroomWh'])
    assert float(m.calc('BlueDog::Analyses::EncounterFeasibility::EnergyScreen',arguments=[1]).value)<0


@pytest.mark.parametrize('kind',['steering_loss','power_loss'])
def test_common_cause_loss_does_not_invent_backup(kind):
    result=simulate(*fixture(),events=[Event(0,kind)])
    assert result.outcome=='disqualified'
    assert result.recovery_summary['outcome']=='recovery_unavailable_common_cause'
    assert not any(e['kind']=='motor_use' for e in result.events)


@pytest.mark.parametrize('field,value',[('latency_s',-1),('miss_probability',1.1),('period_s',0),('error_m',float('nan'))])
def test_invalid_envelope_rejected(field,value):
    with pytest.raises(ValueError):
        replace(SensorEnvelope(100,100,100),**{field:value})


def test_night_reduces_noncooperative_range_and_position_error_is_bounded():
    e=SensorEnvelope(100,100,100,error_m=5,night_factor=.1)
    truth=[actor()]
    assert Observations(e,night=True).observe(truth,np.array([50.,0.]),0)==[]
    contact=Observations(e).observe(truth,np.array([50.,0.]),0)[0]
    assert np.linalg.norm(contact.position(0)-truth[0].position(0))==pytest.approx(5)
    assert contact.beam_m==11


def test_unseen_weed_contact_is_independently_scored():
    weed=Traffic('weed',LineString([(0,0),(1,0)]),0,0,4000,4000,0,stationary_seconds=14400,target_kind='weed')
    r=simulate(*fixture(),traffic=[weed],observations=Observations(SensorEnvelope(0,0,0)))
    assert r.outcome=='safety_violation' and r.cause=='weed_contact'


def test_reports_publish_model_ranges_and_provisional_stack_energy(rendered_site):
    text=(rendered_site/'imports/docs/encounter-feasibility.md').read_text()
    assert 'Closing distance and maneuver allowance' in text
    assert '724' in text and '994' in text
    assert 'AIS + forward sonar + vision' in text
    assert 'sysml-report' not in text and 'STUDY_RESULTS' not in text
