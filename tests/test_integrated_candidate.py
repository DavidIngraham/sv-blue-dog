from copy import deepcopy
from dataclasses import asdict
import json
import numpy as np
import pytest
from shapely.geometry import LineString
from tools.boat_analysis.mission.engine import simulate,Event
from tools.boat_analysis.mission.perception import Observations,SensorEnvelope
from tools.boat_analysis.mission.recovery import RecoveryPlanner,RecoverySite,RecoveryCapability
from tools.boat_analysis.mission.traffic import Traffic
from tools.boat_analysis.model.runtime import load_model
from tests.test_mission_execution import fixture


def candidate():
    args=fixture();args[0].update(continueAfterAbort=True,independentRecovery=True,recoveryBatteryWh=20.,recoveryStandbyW=.1,controlPeriodSeconds=1,commandLatencySeconds=2,planningHorizonSeconds=180,minimumSailingSpeedMps=.05,depowerPenaltyM=180,captureGateCenters=True,progressGuidance=True,crossTrackWeight=.5,maneuverPenaltyM=10)
    args[0]['time'][0]=1;args[0]['time'][4]=15
    planner=RecoveryPlanner(args[2],[RecoverySite('test',(80,30),'synthetic','synthetic')],RecoveryCapability(2,50,8,1.2,2,.5,40))
    return args,planner


def test_backup_activation_has_no_retrospective_tracks():
    provider=Observations(SensorEnvelope(100,100,100,latency_s=1))
    provider.activate(30)
    assert provider.observe([],np.array([0,0]),30)==[]
    assert provider.next_boundary(30)==31
    assert provider.summary()['samples']==1
    with pytest.raises(ValueError):provider.activate(31)


def test_handoff_allowance_affects_observations_without_changing_truth():
    actor=Traffic('stationary',LineString([(20,0),(21,0)]),0,0,2,1,3,stationary_seconds=100)
    provider=Observations(SensorEnvelope(100,100,100),clearance_allowance_m=10)
    contact=provider.observe([actor],np.zeros(2),0)[0]
    assert contact.clearance_m==13
    assert actor.clearance_m==3
    assert provider.summary()['clearanceAllowanceM']==10
    with pytest.raises(ValueError):Observations(SensorEnvelope(100,100,100),clearance_allowance_m=-1)


@pytest.mark.parametrize('kind',['power_loss','steering_loss','capsize'])
def test_independent_recovery_uses_its_own_bank(kind):
    args,planner=candidate()
    r=simulate(*args,events=[Event(0,kind)],recovery_planner=planner,recovery_observations=Observations(SensorEnvelope(100,100,100,latency_s=1)))
    assert r.recovery_summary['outcome']=='recovery_approach_reached'
    assert r.energy_summary['mainStoredWh']==args[0]['energy'][1]
    assert 0<r.energy_summary['recoveryStoredWh']<20
    assert r.outcome!='qualified_completion'
    json.dumps(asdict(r))


def test_shared_fault_does_not_receive_independent_authority():
    args,planner=candidate();args[0]['independentRecovery']=False;args[0]['time'][1]=10/3600
    r=simulate(*args,events=[Event(0,'power_loss')],recovery_planner=planner)
    assert r.recovery_summary['outcome']=='recovery_unavailable_common_cause'


def test_empty_recovery_bank_cannot_mask_primary_power_failure():
    args,planner=candidate();args[0]['recoveryBatteryWh']=0;args[0]['time'][1]=10/3600
    r=simulate(*args,events=[Event(0,'power_loss')],recovery_planner=planner)
    assert r.recovery_summary['outcome']!='recovery_approach_reached'
    assert r.energy_summary['recoveryStoredWh']==0


def test_sailing_accounts_for_recovery_standby_separately():
    args,planner=candidate();args[0]['time'][1]=10/3600;args[0]['energy'][5]=0
    r=simulate(*args,recovery_planner=planner)
    assert r.energy_summary['recoveryStoredWh']==pytest.approx(20-.1*10/3600)
    assert r.energy_summary['mainStoredWh']<args[0]['energy'][1]


def test_backup_observations_stop_an_obstructed_recovery():
    from tools.boat_analysis.mission.recovery import execute_recovery
    args,planner=candidate()
    actor=Traffic('blocked approach',LineString([(40,15),(41,15)]),0,0,10,10,20,stationary_seconds=1000)
    r=execute_recovery(planner,[0,0],0,20,lambda p,t:np.zeros(2),dt=1,horizon_seconds=100,
                       traffic=[actor],observations=Observations(SensorEnvelope(100,100,100,latency_s=1)))
    assert r.outcome=='recovery_observed_obstruction'
    assert not r.collision


def test_backup_observations_select_an_unobstructed_alternative_approach():
    from tools.boat_analysis.mission.recovery import execute_recovery
    args,_=candidate()
    planner=RecoveryPlanner(args[2],[RecoverySite('short blocked',(80,0),'synthetic','synthetic'),RecoverySite('alternative',(0,120),'synthetic','synthetic')],RecoveryCapability(2,50,8,1.2,2))
    actor=Traffic('blocked approach',LineString([(40,0),(41,0)]),0,0,10,10,20,stationary_seconds=1000)
    r=execute_recovery(planner,[0,0],0,20,lambda p,t:np.zeros(2),dt=1,horizon_seconds=100,
                       traffic=[actor],observations=Observations(SensorEnvelope(100,100,100,latency_s=1,miss_probability=0,error_m=0)))
    assert r.outcome=='recovery_approach_reached'
    assert r.destination=='alternative'
    assert not r.collision and not r.clearance_violated


def test_native_closure_rejects_each_unclosed_loop():
    keys=['sizingPass','nominalPass','encountersPass','recoveryPass','energyPass','timingPass','assumptionsRecorded']
    m=load_model();facts=dict.fromkeys(keys,True)
    assert m.verify_requirement('BlueDogIntegratedCandidate::VirtualClosure',named_arguments=facts).holds
    for key in keys:
        assert not m.verify_requirement('BlueDogIntegratedCandidate::VirtualClosure',named_arguments={**facts,key:False}).holds


def test_prediction_horizon_and_gate_capture_at_fast_update():
    args,_=candidate();args[0]['time'][1]=4
    r=simulate(*args)
    assert r.outcome=='qualified_completion'
    assert [x['direction'] for x in r.crossings]==[-1,-1,1,1]
    assert all(abs(x['maneuverCompleteSeconds']-x['appliedSeconds']-15)<1e-8 for x in r.timing_trace if x['turn'])


@pytest.mark.parametrize('outcome',['censored','incomplete','safety_violation'])
def test_integrated_acceptance_cannot_count_an_unresolved_run_as_safe(outcome):
    from tools.boat_analysis.mission.integrated_acceptance import safe
    assert not safe(dict(outcome=outcome,consequence_summary={},outside_performance_coverage_seconds=0))


def test_integrated_acceptance_rejects_unsupported_performance_and_truth_violations():
    from tools.boat_analysis.mission.integrated_acceptance import safe
    assert not safe(dict(outcome='qualified_completion',consequence_summary={},outside_performance_coverage_seconds=1))
    assert not safe(dict(outcome='disqualified',consequence_summary={'truthClearanceViolated':True},outside_performance_coverage_seconds=0))
    assert not safe(dict(outcome='disqualified',consequence_summary={'termination':'drift_censored'},outside_performance_coverage_seconds=0))


def test_parallel_operating_worker_binds_the_complete_candidate(monkeypatch):
    from tools.boat_analysis.optimization import replay
    seen=[]
    class Model:
        def __init__(self):seen.append(self)
    monkeypatch.setattr(replay,'CoupledModel',Model)
    monkeypatch.setattr(replay,'operating_case',lambda m,*args:(m.parameters.tolist(),args))
    first=replay._operating_worker(([1,2],[3],5,True,-1,[4],20))
    second=replay._operating_worker(([9,8],[7],8,False,1,[6],30))
    assert first==([1,2],([3],5,True,-1,[4],20))
    assert second==([9,8],([7],8,False,1,[6],30))
    assert seen[0] is not seen[1]
