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
