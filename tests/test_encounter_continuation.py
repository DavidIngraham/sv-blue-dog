import json
import pytest
from shapely.geometry import box, LineString
from tools.boat_analysis.mission.command import CommandClock
from tools.boat_analysis.mission.recovery import execute_drift
from tools.boat_analysis.mission.traffic import Traffic
from tools.boat_analysis.mission.engine import simulate, Event
from tests.test_mission_execution import fixture


def test_delivery_and_maneuver_cannot_restart_at_fast_assessment():
    clock=CommandClock(2,15)
    clock.heading=90
    clock.select(0,180,True)
    assert not clock.advance(1) and clock.heading==90
    assert clock.advance(2) and clock.heading==180
    assert not clock.advance(3)
    for t in range(3,17):
        assert clock.drifting(t)
        with pytest.raises(ValueError):clock.select(t,0,True)
    assert not clock.busy(17)
    assert clock.trace[0]['maneuverCompleteSeconds']==17


@pytest.mark.parametrize('dt',[1,.5])
def test_depleted_energy_does_not_stop_drift_before_shore(dt):
    r=execute_drift(box(-10,-10,10,10),(0,0),0,.001,lambda p,t:(1,0),dt=dt,horizon_seconds=30,essential_w=36)
    assert r.termination=='shore_contact'
    assert r.seconds==pytest.approx(10)
    assert r.position==pytest.approx([10,0])
    assert r.energy_wh==0 and r.energy_exhausted


def test_drift_continues_after_clearance_to_collision():
    actor=Traffic('blocker',LineString([(8,0),(9,0)]),0,0,2,2,3,stationary_seconds=100)
    r=execute_drift(box(-20,-20,20,20),(0,0),0,5,lambda p,t:(1,0),dt=.5,horizon_seconds=30,essential_w=0,traffic=[actor])
    assert r.termination=='drift_collision' and r.clearance_violated
    assert r.seconds>0 and r.energy_wh==5


def test_common_cause_continues_to_declared_horizon():
    args=fixture();args[0]['continueAfterAbort']=True;args[0]['time'][1]=20/3600
    r=simulate(*args,events=[Event(0,'steering_loss')])
    assert r.elapsed_seconds==20
    assert r.consequence_summary['termination']=='drift_censored'
    assert r.recovery_summary['outcome']=='recovery_unavailable_common_cause'
    assert r.outcome!='qualified_completion'


def records(tmp_path, replaced=0):
    power=tmp_path/'power.csv';power.write_text('seconds,voltage_v,current_a\n0,5,1\n10,5,3\n20,5,1\n')
    obs=tmp_path/'observations.csv';obs.write_text('frame_seconds,decision_seconds,target_present,detected\n0,2,1,1\n5,,1,0\n10,13,1,1\n')
    meta=tmp_path/'metadata.json';meta.write_text(json.dumps(dict(installationId='synthetic',pipelineRevision='test',conditions='fixture',clockBasis='shared',instrument='fixture',operator='test',measuredOn='2026-10-15',measurementBoundary='regulated-bus',evidenceType='synthetic-test',replacedBaseElectronicsW=replaced,replacementScope='declared fixture functions')))
    return power,obs,meta


def test_measurement_accounting_excludes_declared_shared_base(tmp_path):
    from tools.boat_analysis.mission.measurements import ingest
    r=ingest(*records(tmp_path,4.5))
    assert r['averageBusW']==10 and r['incrementalBusW']==5.5
    assert r['maximumObservedLatencyS']==3
    assert r['missFraction']==pytest.approx(1/3)
    assert not r['physicalQualification'] and not r['hardwareSelected']
    assert r['metadata']['evidenceType']=='synthetic-test'


def test_measurement_rejects_excess_replacement(tmp_path):
    from tools.boat_analysis.mission.measurements import ingest
    with pytest.raises(ValueError,match='Replacement'):ingest(*records(tmp_path,5))


@pytest.mark.parametrize('period,expected',[(1,True),(30,False)])
def test_native_timing_requirement(period,expected):
    from tools.boat_analysis.model.runtime import load_model
    verdict=load_model().verify_requirement('BlueDog::Analyses::EncounterFeasibility::TimingCriterion',named_arguments={'assessmentPeriodS':period,'commandLatencyS':2})
    assert verdict.evaluated and verdict.holds is expected


def test_completed_recovery_result_uses_standard_json():
    from dataclasses import asdict
    from tools.boat_analysis.mission.recovery import RecoveryPlanner,RecoverySite,RecoveryCapability
    args=fixture();args[0]['continueAfterAbort']=True
    planner=RecoveryPlanner(args[2],[RecoverySite('test',(80,30),'synthetic','synthetic')],RecoveryCapability(2,50,8,1.2,2))
    result=simulate(*args,events=[Event(0,'sensing_loss')],recovery_planner=planner)
    assert result.recovery_summary['outcome']=='recovery_approach_reached'
    assert json.loads(json.dumps(asdict(result)))['consequence_summary']['termination']=='recovery_approach_reached'
