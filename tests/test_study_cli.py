"""CLI validation and retained native failure reports without a model launch."""
import json
import sys

import pytest

from tools.boat_analysis.cli import main
from tools.boat_analysis.studies.runner import StudyObjectivesError


def test_schema_command_uses_the_pydantic_schema_without_native_execution(tmp_path, monkeypatch):
    from tools.boat_analysis.model import runtime
    monkeypatch.setattr(runtime, 'load_model', lambda *args, **kwargs: pytest.fail('Schema export must not execute a model'))
    output = tmp_path/'schema.json'
    monkeypatch.setattr(sys, 'argv', ['blue-dog', 'study', '--schema', '--output', str(output)])
    main()
    schema = json.loads(output.read_text())
    assert schema['properties']['schema_version']['const'] == 1
    assert schema['additionalProperties'] is False


def test_cli_invalid_config_includes_path_and_has_no_native_side_effects(tmp_path, monkeypatch, capsys):
    from tools.boat_analysis.model import runtime
    monkeypatch.setattr(runtime, 'load_model', lambda *args, **kwargs: pytest.fail('Invalid config must not execute a model'))
    config = tmp_path/'invalid.yaml'
    config.write_text('schema_version: 2\nname: bad\ngroups: []\n')
    monkeypatch.setattr(sys, 'argv', ['blue-dog', 'study', str(config)])
    with pytest.raises(SystemExit) as caught:
        main()
    assert caught.value.code == 2
    error = capsys.readouterr().err
    assert str(config) in error and 'schema_version' in error


def test_cli_writes_retained_report_and_exits_nonzero_for_failed_objectives(tmp_path, monkeypatch, capsys):
    from tools.boat_analysis.studies import runner
    report = {'nativeOutputs': {'adverse/default/Model::case': {'reserveFits': False}},
              'provenance': {'requiredObjectivesNotHeld': ['Model::case']}}
    def fail(*args, **kwargs):
        raise StudyObjectivesError('native objective failed', report)
    monkeypatch.setattr(runner, 'run_study', fail)
    config = tmp_path/'adverse.yaml'
    config.write_text('explicit configuration')
    output = tmp_path/'report.json'
    monkeypatch.setattr(sys, 'argv', ['blue-dog', 'study', str(config), '--output', str(output)])
    with pytest.raises(SystemExit) as caught:
        main()
    assert caught.value.code == 1
    assert json.loads(output.read_text()) == report
    assert 'native objective failed' in capsys.readouterr().err


def test_cli_does_not_overwrite_the_study_file(tmp_path, monkeypatch):
    from tools.boat_analysis.studies import runner
    monkeypatch.setattr(runner, 'run_study', lambda *args, **kwargs: {})
    config = tmp_path/'study.yaml'
    original = 'preserve configuration bytes'
    config.write_text(original)
    monkeypatch.setattr(sys, 'argv', ['blue-dog', 'study', str(config), '--output', str(config)])
    with pytest.raises(SystemExit) as caught:
        main()
    assert caught.value.code == 2
    assert config.read_text() == original
