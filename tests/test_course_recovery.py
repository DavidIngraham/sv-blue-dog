"""Recovery integration using native physics; synthetic sites are not approved refuges."""
import sys
import numpy as np
import pytest
from shapely.geometry import box
from tools.boat_analysis.mission.recovery import RecoverySite, RecoveryCapability, RecoveryPlanner, execute_recovery
from tools.boat_analysis.mission.engine import simulate, Event
from tests.test_mission_execution import fixture

pytestmark = pytest.mark.skipif(sys.platform != 'linux', reason='Native C adapters require GCC')

@pytest.fixture(scope='module')
def planner():
    return RecoveryPlanner(box(-1500,-500,500,500),
        [RecoverySite('synthetic pickup', (0., 400.), 'synthetic access case', 'synthetic approach case')],
        RecoveryCapability(2., 50., 8., 1.2, 2., 1., 60.))


def test_current_compensation_and_energy(planner):
    value = planner.segment(300., np.array([1., 0.]), np.array([-.4, 1.2]))
    # Along-water speed sqrt(2**2-1.2**2)=1.6; net ground speed=1.2.
    assert value == pytest.approx([1., 1.2, 250., 1.2*58*250/3600])
    assert planner.segment(300., np.array([1., 0.]), np.array([-2., 0.])) is None
    assert planner.segment(300., np.array([1., 0.]), np.array([0., 2.])) is None


def test_reserve_varies_with_position_and_current(planner):
    near = planner.plan((0., 300.), (0., 0.))
    far = planner.plan((0., 0.), (0., 0.))
    adverse = planner.plan((0., 0.), (0., -1.))
    assert near.reserve_wh < far.reserve_wh < adverse.reserve_wh
    assert planner.plan((0., 0.), (0., -3.)) is None


def test_capsized_performance_is_explicit(planner):
    upright = planner.plan((0., 0.), (0., 0.))
    inverted = planner.plan((0., 0.), (0., 0.), capsized=True)
    assert inverted.seconds == pytest.approx(2*upright.seconds)
    assert inverted.reserve_wh > upright.reserve_wh
    missing = RecoveryPlanner(planner.water, planner.sites, RecoveryCapability(2.,50.,8.,1.2,2.), kernel=planner.kernel)
    assert missing.plan((0., 0.), (0., 0.), capsized=True) is None


def test_recovery_stops_when_current_changes_beyond_authority(planner):
    r = execute_recovery(planner, (0.,0.), 0., 100., lambda p,t: (0.,0.) if t<20 else (0.,-3.))
    assert r.outcome == 'recovery_current_exceeds_authority'
    assert r.seconds == 20


def test_capsize_recovers_without_communications_and_disqualifies(planner):
    r = simulate(*fixture(), recovery_planner=planner,
        events=[Event(0,'communications_loss',3600), Event(0,'capsize')])
    assert r.outcome == 'disqualified'
    assert r.recovery_summary['outcome'] == 'recovery_approach_reached'
    assert r.recovery_summary['position'] == pytest.approx([0.,400.])
    assert any(e['kind']=='abort_alert_queued' for e in r.events)
    assert any(e['kind']=='motor_use' for e in r.events)
    assert all(not row[-1] for row in r.history)


def test_refuge_does_not_autonomously_resume(planner):
    r = simulate(*fixture(), recovery_planner=planner, events=[Event(0,'refuge_entry')])
    assert r.outcome == 'disqualified'
    assert r.recovery_summary['outcome']=='awaiting_operator_retrieval_or_relocation'
    assert not any(e['kind']=='motor_use' for e in r.events)


def test_no_recovery_model_cannot_claim_recovery():
    r = simulate(*fixture(), events=[Event(0,'capsize')])
    assert r.outcome == 'disqualified'
    assert r.recovery_summary['outcome']=='recovery_model_unavailable'


def test_recovery_collision_is_not_hidden_by_failed_detector(planner):
    from shapely.geometry import LineString
    from tools.boat_analysis.mission.traffic import Traffic
    actor = Traffic('unseen anchored craft', LineString([(0.,100.), (1.,100.)]), 0., 0., 10., 5., 0., stationary_seconds=3600.)
    r = execute_recovery(planner, (0.,0.), 0., 100., lambda p,t: (0.,0.), traffic=[actor])
    assert r.collision
    assert r.outcome == 'recovery_collision'


def test_dynamic_reserve_triggers_before_exhaustion(planner):
    inputs, route, water, gates = fixture()
    start = np.array([80.,0.])
    reserve = planner.plan(start, (-.4,0.)).reserve_wh
    inputs['energy'][1] = reserve + .01
    inputs['energy'][5] = 0.
    r = simulate(inputs, route, water, gates, recovery_planner=planner)
    assert r.outcome == 'disqualified'
    assert r.cause == 'course_recovery_reserve_trigger'
    assert r.recovery_summary['outcome'] == 'recovery_approach_reached'
    assert r.minimum_energy_wh >= planner.capability.arrival_allowance_wh
