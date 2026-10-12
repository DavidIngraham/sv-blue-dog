from dataclasses import asdict
import numpy as np
import pytest
from shapely.geometry import LineString, box

from tools.boat_analysis.mission.engine import simulate, Event
from tools.boat_analysis.mission.traffic import Traffic


def fixture():
    route=LineString([(0,0),(-1000,0)])
    water=box(-1500,-500,500,500)
    gates={'eastGate':LineString([(0,100),(0,-100)]),
           'westGate':LineString([(-1000,100),(-1000,-100)])}
    inputs={'gateNames':['eastGate','westGate','westGate','eastGate'], 'gateDirections':[-1,-1,1,1], 'gateApproachM':80, 'time':[10,4,30,80,2,1], 'energy':[500,500,60,5,.01,40,.85,.9],
            'dimensions':[2,.8,3], 'angles':[0,35,45,60,90,135,180],
            'speedRatios':[0,0,.28,.36,.45,.38,.3], 'weather':[270,7,.4,36,.2,.85,.8,.15,.8,.08,.03,6,18,8]}
    return inputs,route,water,gates


def test_mission_crosses_all_gates_in_order():
    r=simulate(*fixture())
    assert r.outcome=='qualified_completion'
    assert [c['direction'] for c in r.crossings]==[-1,-1,1,1]
    assert r.minimum_energy_wh>60
    assert r.physically_validated is False


def test_monitoring_outage_does_not_require_intervention():
    r=simulate(*fixture(),events=[Event(0,'communications_loss',3600)])
    assert r.outcome=='qualified_completion'
    assert any(not row[-1] for row in r.history)


@pytest.mark.parametrize('event',['operator_intervention','motor_use'])
def test_intervention_disqualifies_attempt(event):
    assert simulate(*fixture(),events=[Event(0,event)]).outcome=='disqualified'


def test_horizon_is_censoring_not_deadline_failure():
    inputs,route,water,gates=fixture();inputs['time'][1]=.01
    r=simulate(inputs,route,water,gates)
    assert r.outcome=='censored' and r.cause=='computational_horizon'


def test_no_harvesting_can_complete_finite_mission():
    inputs,route,water,gates=fixture();inputs['energy'][5]=0
    r=simulate(inputs,route,water,gates)
    assert r.outcome=='qualified_completion'
    assert r.history[-1][3]<inputs['energy'][1]


def test_reserve_depletion_stops_mission():
    inputs,route,water,gates=fixture();inputs['energy'][1]=61;inputs['energy'][5]=0
    r=simulate(inputs,route,water,gates)
    assert r.outcome=='incomplete' and r.cause=='recovery_reserve_reached'


def test_fast_crossing_traffic_cannot_tunnel_between_samples():
    actor=Traffic('ski boat',LineString([(0,-100),(0,100)]),0,20,6,2,10)
    previous=np.array([-50.,0]);endpoint=np.array([50.,0])
    assert actor.collides(previous,endpoint,0,10,[2,.8,3])
    safe,_=actor.assess(previous,np.array([endpoint]),0,10,30,[2,.8,3])
    assert not safe[0]


def test_same_crossing_at_different_times_is_not_collision():
    actor=Traffic('fishing boat',LineString([(0,-100),(0,100)]),100,2,6,2,10)
    assert not actor.collides(np.array([-50.,0]),np.array([50.,0]),0,10,[2,.8,3])


def test_full_tow_footprint_is_used():
    actor=Traffic('tow',LineString([(-1000,0),(1000,0)]),0,2,180,24,30)
    assert actor.collides(np.array([-930.,0]),np.array([-930.,0]),0,10,[2,.8,3])


@pytest.mark.parametrize('facts,expected', [
    ((True,False,False,False,False,True,True),'qualified_completion'),
    ((True,True,False,False,False,True,False),'disqualified'),
    ((True,False,True,False,False,True,False),'disqualified'),
    ((True,True,False,True,False,True,False),'safety_violation'),
    ((True,False,False,False,False,False,False),'incomplete'),
    ((False,False,False,False,False,True,True),'censored'),
])
def test_native_acceptance_precedence(facts,expected):
    from tools.boat_analysis.mission.engine import evaluate_outcome
    assert evaluate_outcome(*facts)==expected


@pytest.mark.parametrize('name,track,speed,own_start,own_end', [
    ('oncoming tow',[(-100,0),(100,0)],10,[100,0],[-100,0]),
    ('overtaking powerboat',[(-100,0),(200,0)],20,[0,0],[50,0]),
    ('reversing ski boat',[(0,-50),(0,50),(0,-50)],20,[-37.5,0],[62.5,0]),
    ('crossing sailboat',[(0,-50),(0,50)],5,[-50,0],[50,0]),
])
def test_continuous_encounter_geometry(name,track,speed,own_start,own_end):
    actor=Traffic(name,LineString(track),0,speed,8,3,10)
    assert actor.collides(np.array(own_start,dtype=float),np.array(own_end,dtype=float),0,20,[2,.8,3])


def test_stationary_non_ais_fisherman_is_obstacle_for_declared_duration():
    actor=Traffic('anchored fishing craft',LineString([(0,0),(1,0)]),0,0,6,2,10,stationary_seconds=60)
    assert actor.collides(np.array([-50.,0]),np.array([50.,0]),0,10,[2,.8,3])
    assert not actor.collides(np.array([-50.,0]),np.array([50.,0]),70,10,[2,.8,3])


def test_terminal_history_records_reserve_stop():
    inputs,route,water,gates=fixture();inputs['energy'][1]=60.01;inputs['energy'][5]=0
    r=simulate(inputs,route,water,gates)
    assert r.history[-1][0]==r.elapsed_seconds
    assert r.history[-1][3]==r.minimum_energy_wh
