from dataclasses import replace
import numpy as np
import pytest
from shapely.geometry import LineString
from tools.boat_analysis.mission.navigation import NavigationAssessment, evaluate
from tools.boat_analysis.mission.navigation_study import ASSESSED_CONTEXT, ASSESSED_FACTS
from tools.boat_analysis.mission.traffic import Traffic
from tools.boat_analysis.mission.perception import Observations, SensorEnvelope
from tools.boat_analysis.mission.engine import simulate
from tests.test_mission_execution import fixture


def candidate(response, **changes):
    inputs=dict(relevant=True,supported=True,candidateClear=True,heldClear=True,
        holdsCourseSpeed=True,substantialChange=False,missingTrackedDuty=False,response=response,continuationSupported=False)
    inputs.update(changes)
    return evaluate('BlueDogNavigationController::Candidate',**inputs)['allowed']


def test_stand_on_holds_until_assessed_escalation():
    assert candidate('holdCourseSpeed')
    assert not candidate('holdCourseSpeed',holdsCourseSpeed=False,substantialChange=True)
    assert candidate('mayAct',holdsCourseSpeed=False,substantialChange=True)
    assert not candidate('shallAct',heldClear=False)
    assert candidate('shallAct',heldClear=False,holdsCourseSpeed=False,substantialChange=True)
    assert not candidate('mayAct',supported=False)
    assert not candidate('monitor',missingTrackedDuty=True,relevant=False)


def target(facts=ASSESSED_FACTS):
    return Traffic('target',LineString([(100,0),(1000,0)]),0,1,6,2,20,source_id=7,navigation_facts=facts)


def assess(nav, contacts, position=None):
    position=np.array([0.,0.]) if position is None else np.asarray(position,dtype=float)
    velocities=np.array([[2.,0.],[0.,2.],[0.,-2.]])
    return nav.assess(position=position,contacts=contacts,seconds=0,interval=30,forecast=180,
        dimensions=[1.2,.43],headings=np.array([0.,90.,270.]),endpoints=position+velocities*30,
        velocities=velocities,held_velocity=np.array([2.,0.]),heading=0.,permitted=np.ones(3,dtype=bool))


def test_unknown_observed_status_cannot_approve_candidate():
    nav=NavigationAssessment(assessed_context=ASSESSED_CONTEXT)
    assert not assess(nav,[target({})]).any()
    assert nav.summary()['unresolvedObligations']['vessel_status']>0


def test_overtaking_memory_survives_track_loss_and_releases_on_observed_clearance():
    nav=NavigationAssessment(assessed_context=ASSESSED_CONTEXT)
    assert assess(nav,[target()]).any()
    assert nav.memory[7]=='ownDuty'
    assert not assess(nav,[]).any()
    assert nav.memory[7]=='ownDuty'
    assess(nav,[target()],position=[200.,0.])
    assert nav.memory[7]=='clear'


def test_unknown_clearance_does_not_erase_overtaking_memory():
    nav=NavigationAssessment(assessed_context=ASSESSED_CONTEXT)
    assess(nav,[target()])
    assess(nav,[target({})],position=[200.,0.])
    assert nav.memory[7]=='ownDuty'


def test_navigation_metadata_is_explicit_and_delayed_with_observation():
    actor=target()
    default=Observations(SensorEnvelope(1000,1000,1000))
    assert default.observe([actor],np.zeros(2),0)[0].navigation_facts=={}
    explicit=Observations(SensorEnvelope(1000,1000,1000,latency_s=2),observe_navigation_facts=True)
    assert explicit.observe([actor],np.zeros(2),0)==[]
    assert explicit.observe([actor],np.zeros(2),1)==[]
    assert explicit.observe([actor],np.zeros(2),2)[0].navigation_facts==ASSESSED_FACTS


def test_navigation_cannot_use_truth_or_rescue_an_unseen_target():
    with pytest.raises(ValueError,match='delivered observations'):
        simulate(*fixture(),navigation=NavigationAssessment())
    actor=Traffic('unseen',LineString([(0,0),(1,0)]),0,0,4000,4000,0,stationary_seconds=14400)
    result=simulate(*fixture(),traffic=[actor],observations=Observations(SensorEnvelope(0,0,0)),navigation=NavigationAssessment(assessed_context=ASSESSED_CONTEXT))
    assert result.cause=='traffic_collision'
    assert result.navigation_summary['filteredCandidates']==0


def test_unobserved_future_turn_cannot_change_navigation_decision():
    straight=target()
    turning=replace(straight,track=LineString([(100,0),(110,0),(110,1000)]))
    masks=[]
    for actor in (straight,turning):
        observations=Observations(SensorEnvelope(1000,1000,1000),observe_navigation_facts=True)
        observations.observe([actor],np.zeros(2),0)
        contacts=observations.observe([actor],np.zeros(2),1)
        masks.append(assess(NavigationAssessment(assessed_context=ASSESSED_CONTEXT),contacts))
    assert np.array_equal(*masks)


def test_committed_turn_does_not_need_a_second_heading_change():
    assert candidate('keepClear',heldClear=False,holdsCourseSpeed=False,continuationSupported=True)
    assert not candidate('keepClear',heldClear=False,holdsCourseSpeed=False,continuationSupported=False)
    assert not candidate('keepClear',heldClear=False,holdsCourseSpeed=False,continuationSupported=True,candidateClear=False)


def test_independent_channel_duty_is_not_skipped_when_pair_is_clear():
    nav=NavigationAssessment(assessed_context=dict(ASSESSED_CONTEXT,channelContext='yes'))
    assert not assess(nav,[target()],position=[200.,0.]).any()
    assert nav.trace
    assert not assess(nav,[],position=[200.,0.]).any()


def test_replay_hashes_include_native_decisions():
    from tools.boat_analysis.evidence.records import source_hashes
    hashes=source_hashes([])
    assert 'models/libraries/navigation/inland-pair.sysml' in hashes
    assert 'models/analyses/navigation-controller.sysml' in hashes


def test_depower_is_not_a_substantial_heading_change():
    result=evaluate('BlueDogNavigationController::Geometry',rangeM=100.,closingMps=1.,protectedRadiusM=20.,
        releaseMultiplier=2.,heldConflict=True,headingKnown=False,trackAdequate=True,
        headingToleranceDeg=2.,speedToleranceMps=.05,substantialTurnDeg=15.,headingChangeDeg=0.,speedChangeMps=2.)
    assert not result['substantialChange']
    assert not result['holdsCourseSpeed']


def test_empty_scene_has_identical_candidate_grid_in_both_modes():
    inputs,route,water,gates=fixture()
    inputs['retainCurrentHeadingCandidate']=True
    baseline=simulate(inputs,route,water,gates,observations=Observations(SensorEnvelope(100,100,100)))
    rules=simulate(inputs,route,water,gates,observations=Observations(SensorEnvelope(100,100,100)),
        navigation=NavigationAssessment(assessed_context=ASSESSED_CONTEXT))
    assert baseline.history==rules.history
    assert baseline.energy_summary==rules.energy_summary


def test_new_target_during_drift_is_not_hidden_by_safe_eventual_heading():
    from tools.boat_analysis.mission.navigation import trajectory_clear
    actor=Traffic('crossing',LineString([(-10,0),(100,0)]),0,1,1,1,0,source_id=4)
    position=np.zeros(2)
    segments=[(15.,np.zeros(2)),(20.,np.array([0.,2.]))]
    assert not trajectory_clear(actor,position,0,segments,[1.2,.43])
    assert trajectory_clear(actor,position,0,[(35.,np.array([0.,2.]))],[1.2,.43])
    nav=NavigationAssessment(assessed_context=ASSESSED_CONTEXT)
    allowed=nav.assess(position=position,contacts=[actor],seconds=0,interval=35,forecast=35,
        dimensions=[1.2,.43],headings=np.array([90.]),endpoints=np.array([[0.,40.]]),
        velocities=np.array([[0.,2.]]),held_velocity=np.array([0.,2.]),heading=90.,permitted=np.array([True]),
        committed=True,trajectories=[segments],reference_trajectory=segments)
    assert not allowed[0]
    assert nav.trace


def test_approval_cannot_carry_a_skipped_pair_into_a_new_command():
    nav=NavigationAssessment(assessed_context=ASSESSED_CONTEXT)
    assess(nav,[target()])
    nav.selected(0,1)
    assert 7 in nav.approved
    nav.memory[7]='clear'
    assess(nav,[])
    nav.selected(0,0)
    assert nav.approved=={}


def test_new_candidate_segment_conflict_is_checked_even_when_holding_is_clear():
    actor=Traffic('crossing',LineString([(-10,0),(100,0)]),0,1,1,1,0,source_id=4)
    nav=NavigationAssessment(assessed_context=ASSESSED_CONTEXT)
    allowed=nav.assess(position=np.zeros(2),contacts=[actor],seconds=0,interval=35,forecast=35,
        dimensions=[1.2,.43],headings=np.array([90.]),endpoints=np.array([[0.,40.]]),
        velocities=np.array([[0.,2.]]),held_velocity=np.array([0.,2.]),heading=90.,permitted=np.array([True]),
        trajectories=[[(15.,np.zeros(2)),(20.,np.array([0.,2.]))]])
    assert not allowed[0]
