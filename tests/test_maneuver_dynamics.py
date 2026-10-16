"""Physical consequences of the opt-in hypothesis, not measured boat claims."""
import math
import numpy as np
import pytest
from shapely.geometry import LineString
from tools.boat_analysis.mission.maneuver import ManeuverDynamics, maneuver_kind, angle_error
from tools.boat_analysis.mission.command import CommandClock
from tools.boat_analysis.mission.traffic import Traffic
from tools.boat_analysis.mission.engine import simulate
from tests.test_mission_execution import fixture


def test_command_delivery_does_not_teleport_heading_or_finish_a_slow_turn():
    m=ManeuverDynamics(0,initial_speed=1)
    clock=CommandClock(2,15,dynamics=m)
    clock.select(0,90,True)
    assert not clock.advance(1) and clock.heading==0
    assert clock.advance(2) and clock.heading==0
    first=m.step(clock.target_heading,1,1)
    assert 0<first['headingDeg']<=6
    for seconds in range(3,18):
        with pytest.raises(ValueError):clock.select(seconds,180,True)
        m.step(clock.target_heading,1,1)
    # Reduced water speed means full heading change takes longer than 15 seconds.
    assert clock.busy(18)
    assert 'maneuverCompleteSeconds' not in clock.trace[0]
    assert clock.trace[0]['earliestManeuverCompleteSeconds']==17


@pytest.mark.parametrize('kind,retention',[('turn',.8),('tack',.35),('gybe',.65),('recovery',.7)])
def test_each_maneuver_loses_speed_with_bounded_deceleration(kind,retention):
    m=ManeuverDynamics(0,initial_speed=1)
    r=m.step(170,1,.25,kind)
    assert 1-.15*.25<=r['speedMps']<1
    for _ in range(20):r=m.step(170,1,.25,kind)
    assert r['speedMps']==pytest.approx(retention,abs=.05)
    assert abs(r['deltaHeadingDeg'])<=6*.25


def test_rudder_authority_uses_water_speed_not_current_and_zero_rudder_cannot_turn():
    m=ManeuverDynamics(0,initial_speed=.1)
    current=np.array([1.,0.]);position=np.zeros(2)
    for _ in range(10):
        r=m.step(90,.1,1)
        position+=np.asarray(r['velocity'])+current
    assert m.heading==0 and position[1]==0 and position[0]>10
    stopped=ManeuverDynamics(45,initial_speed=0)
    r=stopped.step(180,0,1)
    assert r['velocity']==pytest.approx([0,0])
    assert np.asarray(r['velocity'])+current==pytest.approx(current)
    rudder_failed=ManeuverDynamics(0,initial_speed=1)
    assert rudder_failed.step(90,1,1,rudder_fraction=0)['headingDeg']==0


def trajectory(dt):
    m=ManeuverDynamics(0,initial_speed=1);point=np.zeros(2);finished=None
    for i in range(round(30/dt)):
        r=m.step(90,1,dt)
        point+=np.asarray(r['velocity'])*dt
        if not r['turning'] and finished is None:finished=(i+1)*dt
    return point,m.heading,finished


def test_turn_trajectory_converges_under_time_refinement():
    coarse=trajectory(.5);fine=trajectory(.25)
    assert coarse[1]==pytest.approx(90) and fine[1]==pytest.approx(90)
    assert abs(coarse[2]-fine[2])<=.5
    assert np.linalg.norm(coarse[0]-fine[0])<.3


def test_hazard_appearing_during_turn_is_scored_without_preempting_it():
    m=ManeuverDynamics(0,initial_speed=1);clock=CommandClock(0,15,dynamics=m)
    clock.select(0,90,True);clock.advance(0)
    point=np.zeros(2)
    for _ in range(4):point+=np.asarray(m.step(90,1,1)['velocity'])
    # Hazard first appears at t=4 on the achieved trajectory, not a planned endpoint.
    target=Traffic('late target',LineString([point,point+np.array([1.,0.])]),4,0,2,2,0,stationary_seconds=30)
    with pytest.raises(ValueError):clock.select(4,180,True)
    endpoint=point+np.asarray(m.step(90,1,1)['velocity'])
    assert target.collides(point,endpoint,4,1,[1.2,.42,1.])
    assert clock.target_heading==90 and len(clock.trace)==1


def test_shortest_turn_classification_includes_both_tacks_and_gybes():
    assert maneuver_kind(45,315,0)=='tack'
    assert maneuver_kind(315,45,0)=='tack'
    assert maneuver_kind(135,225,0)=='gybe'
    assert maneuver_kind(45,90,0)=='turn'
    assert angle_error(350,10)==-20


def test_engine_option_records_actual_bounded_steps_and_keeps_legacy_explicit():
    args=fixture();args[0]['time'][0]=.5;args[0]['time'][1]=8/3600
    args[0]['commandLatencySeconds']=2
    args[0]['maneuverDynamics']={'initialHeadingDeg':90,'initialSpeedMps':1}
    r=simulate(*args)
    record=r.timing_trace[-1]
    assert record['maneuverModel']=='bounded-rate-hypothesis' and not record['physicalValidation']
    assert record['steps']
    assert all(abs(row['outputs']['deltaHeadingDeg'])<=6*row['inputs']['intervalS']+1e-9 for row in record['steps'])
    del args[0]['maneuverDynamics']
    legacy=simulate(*args)
    assert all('maneuverModel' not in row for row in legacy.timing_trace)


def test_unknown_or_nonphysical_coefficient_is_rejected():
    with pytest.raises(ValueError):ManeuverDynamics(0,{'tackSpeedRetention':1.1})
    with pytest.raises(ValueError):ManeuverDynamics(0,{'authoritySpeedMps':.1})
    with pytest.raises(ValueError):ManeuverDynamics(0,{'unknown':1})


def test_engine_calm_current_does_not_create_rudder_authority():
    args=fixture();args[0]['time'][0]=.5;args[0]['time'][1]=8/3600
    args[0]['weather'][1]=0;args[0]['weather'][2]=.4
    args[0]['maneuverDynamics']={'initialHeadingDeg':90,'initialSpeedMps':0}
    result=simulate(*args)
    rows=result.timing_trace[-1]['steps']
    assert all(row['outputs']['turnRateDegS']==0 and row['outputs']['speedMps']==0 for row in rows)
    assert result.history[-1][1:3]==pytest.approx([80-.4*8,0])
    assert result.distance_m==pytest.approx(.4*8)


def test_engine_uses_candidate_provider_at_the_achieved_heading(monkeypatch):
    actual_angles=[]
    class Candidate:
        def __init__(self, configuration):pass
        def speeds(self, wind, angles):
            if np.ndim(angles)==0:actual_angles.append(float(angles))
            return np.zeros_like(np.asarray(angles,dtype=float))+.7
        def covered(self, wind):return True
    monkeypatch.setattr('tools.boat_analysis.mission.candidate.Performance',Candidate)
    args=fixture();args[0]['time'][0]=.5;args[0]['time'][1]=2/3600
    args[0]['performance']={'scope':'identified synthetic performance provider'}
    args[0]['maneuverDynamics']={'initialHeadingDeg':90,'initialSpeedMps':1}
    result=simulate(*args)
    steps=result.timing_trace[-1]['steps']
    assert steps and actual_angles
    assert actual_angles[0]==pytest.approx(-90)
    assert all(row['inputs']['targetSpeedMps']==pytest.approx(.7) for row in steps)
    assert 'identified synthetic performance provider' in result.model_scope


def test_capsize_does_not_relabel_interrupted_turn_as_completed():
    from tools.boat_analysis.mission.engine import Event
    args=fixture();args[0]['time'][0]=.5;args[0]['time'][1]=8/3600
    args[0]['maneuverDynamics']={'initialHeadingDeg':90,'initialSpeedMps':1}
    result=simulate(*args,events=[Event(1,'capsize',required_safety_confirmed=True),
                                 Event(3,'unassisted_righting',required_safety_confirmed=True)])
    command=result.timing_trace[0]
    assert command['status']=='interrupted' and command['interruptedSeconds']==1
    assert command['reason']=='capsize'
    assert 'actualManeuverCompleteSeconds' not in command
    assert any(row[4]=='capsized_drift' for row in result.history)


def test_cancelled_pending_command_is_never_applied_or_completed():
    m=ManeuverDynamics(0,initial_speed=1);clock=CommandClock(2,15,dynamics=m)
    clock.select(0,90,True)
    clock.cancel(1,'capsize')
    assert not clock.advance(3) and not clock.busy(3)
    row=clock.trace[0]
    assert row['status']=='cancelled' and row['cancelledSeconds']==1
    assert row['scheduledAppliedSeconds']==2
    assert 'appliedSeconds' not in row and 'actualManeuverCompleteSeconds' not in row
    assert m.heading==0
