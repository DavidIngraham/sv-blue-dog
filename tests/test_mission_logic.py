"""Native behavior and simulator integration, including a model-policy perturbation."""
import json
import pytest
from tools.boat_analysis.mission.logic import MissionLogic
from tools.boat_analysis.mission.engine import simulate, Event
from tools.boat_analysis.model.runtime import ROOT, load_model, model_files
from tests.test_mission_execution import fixture


def test_abort_latch_survives_restored_inputs_and_run_reset():
    logic = MissionLogic()
    assert logic.cycle(0)['sailingPermitted']
    aborted = logic.cycle(1, abort_requested=True, communications_available=False)
    assert aborted['mode'] == 'abort_recovery'
    assert aborted['alert'] == 'queue'
    restored = logic.cycle(2)
    assert restored['abortLatchedNext'] and not restored['sailingPermitted']
    assert restored['alert'] == 'none'
    assert MissionLogic().cycle(0)['sailingPermitted']


def test_supervisor_precedence_and_traffic_mode():
    logic = MissionLogic()
    assert logic.cycle(0, traffic_conflict=True)['mode'] == 'traffic_avoidance'
    assert logic.cycle(1, traffic_conflict=True, wind_valid=False)['mode'] == 'degraded_drift'
    assert logic.cycle(2, wind_valid=False, abort_requested=True)['mode'] == 'abort_recovery'


def test_unknown_event_fails_explicitly():
    with pytest.raises(ValueError, match='Unknown mission event'):
        simulate(*fixture(), events=[Event(0, 'misspelled_event')])


def test_wind_loss_and_expiry_drive_executed_motion():
    result = simulate(*fixture(), events=[Event(0, 'wind_sensor_loss', 25)], save_every=1)
    assert result.outcome == 'qualified_completion'
    assert any(row[4] == 'degraded_drift' for row in result.history if row[0] <= 25)
    cycles = [row for row in result.logic_trace if row['action'].endswith('SupervisoryCycle')]
    assert cycles[0]['outputs']['sailingPermitted'] is False
    assert any(row['seconds'] == 25 and row['outputs']['sailingPermitted'] for row in cycles)
    json.dumps(result.logic_trace, allow_nan=False)


def test_model_policy_change_changes_simulator_behavior(tmp_path, monkeypatch):
    # Change only native policy, not Python dispatch or a mocked action result.
    from tools.boat_analysis.mission import logic
    path = ROOT/'models/vehicle/mission-logic.sysml'
    altered = tmp_path/'mission-logic.sysml'
    altered.write_text(path.read_text().replace('? "retain_forecast"', '? "abort"'))
    model = load_model(tuple(p for p in model_files() if p != path)+(altered,))
    monkeypatch.setattr(logic, 'load_model', lambda: model)
    result = simulate(*fixture(), events=[Event(0, 'weather_service_loss')])
    assert result.outcome == 'disqualified'
    assert result.cause == 'weather_service_loss'
    assert result.logic_trace[0]['outputs']['directive'] == 'abort'
    assert any(row['outputs'].get('abortLatchedNext') for row in result.logic_trace)


@pytest.mark.parametrize('capsized,upright,safe,expected', [
    (False, False, True, 'await_righting'),
    (True, True, True, 'resume'),
    (True, True, False, 'abort'),
    (False, False, False, 'abort'),
    (False, True, True, 'invalid_observation'),
])
def test_native_capsize_observation_policy(capsized, upright, safe, expected):
    logic = MissionLogic()
    assert logic.event('capsize', 0)['directive'] == 'assess_capsize'
    assert logic.capsize(0, capsized, upright, safe) == expected
    logic.cycle(1, abort_requested=True)
    assert logic.capsize(2, True, True, True) == 'abort'


def test_unassisted_righting_preserves_attempt_but_never_sails_inverted():
    result = simulate(*fixture(), events=[
        Event(0, 'capsize', required_safety_confirmed=True),
        Event(25, 'unassisted_righting', required_safety_confirmed=True)], save_every=1)
    assert result.outcome == 'qualified_completion'
    inverted = [row for row in result.history if row[0] < 25]
    assert inverted and all(row[4] == 'capsized_drift' for row in inverted)
    # Fixture current is 0.4 m/s westward; sailing velocity is absent.
    assert next(row for row in result.history if row[0] == 25)[1] == pytest.approx(70.)
    assert all(crossing['seconds'] > 25 for crossing in result.crossings)
    assert not any(event['kind'] in {'motor_use', 'safety_abort'} for event in result.events)
    assert result.recovery_summary['outcome'] == 'unassisted_righting_observed'
    assert result.physically_validated is False


@pytest.mark.parametrize('kind', ['motor_use', 'operator_intervention', 'safety_capability_loss', 'power_loss'])
def test_righting_cannot_erase_disqualifying_event(kind):
    result = simulate(*fixture(), events=[
        Event(0, 'capsize', required_safety_confirmed=True), Event(10, kind),
        Event(25, 'unassisted_righting', required_safety_confirmed=True)])
    assert result.outcome == 'disqualified'


def test_unobserved_righting_never_resumes_or_counts_drift_gate_crossings():
    inputs, route, water, gates = fixture()
    inputs['time'][1] = .1
    result = simulate(inputs, route, water, gates,
        events=[Event(0, 'capsize', required_safety_confirmed=True)], save_every=1)
    assert result.outcome == 'censored'
    assert not result.crossings
    assert result.recovery_summary['outcome'] == 'awaiting_unassisted_righting'
    assert all(row[4] == 'capsized_drift' for row in result.history[:-1])


def test_righting_without_safety_confirmation_aborts():
    result = simulate(*fixture(), events=[
        Event(0, 'capsize', required_safety_confirmed=True), Event(25, 'unassisted_righting')])
    assert result.outcome == 'disqualified'


def test_righting_without_capsize_is_invalid():
    with pytest.raises(ValueError, match='preceding capsize'):
        simulate(*fixture(), events=[Event(0, 'unassisted_righting', required_safety_confirmed=True)])
