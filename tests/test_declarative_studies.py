"""Declarative intent reuses native discovery, bindings and objective semantics."""
import json
from pathlib import Path

import pytest

from tools.boat_analysis.studies.config import load_study
from tools.boat_analysis.studies.runner import run_study, resolve_selector
from tools.boat_analysis.model.runtime import load_model

FIXTURE = Path(__file__).parent / "fixtures/declarative-studies.sysml"
PREFIX = "DeclarativeStudyFixtures::"


def write_config(tmp_path, groups=None, **changes):
    value = {
        "schema_version": 1,
        "name": "Synthetic native reuse",
        "groups": groups if groups is not None else [
            {"name": "exact", "select": {"id": PREFIX + "exactValues"}}
        ],
    }
    value.update(changes)
    path = tmp_path / "study.yaml"
    # JSON is a YAML subset, making these tests independent of emitter formatting.
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


@pytest.fixture(scope="module")
def native_model():
    return load_model((FIXTURE,))


def only_output(report):
    assert len(report["nativeOutputs"]) == 1
    return next(iter(report["nativeOutputs"].values()))


def test_defaults_are_explicit_and_native_values_preserve_their_types(tmp_path, native_model):
    config = load_study(write_config(tmp_path))
    assert config.groups[0].require_holds is True
    assert config.groups[0].scenarios[0].name == "default"
    report = run_study(config, model=native_model)
    outputs = only_output(report)
    assert outputs["ratio"] == pytest.approx(1 / 3)
    assert outputs["text"] == "1/3 is a label"
    assert outputs["accepted"] is False
    assert list(report["nativeOutputs"]) == ["exact/default/" + PREFIX + "exactValues"]


@pytest.mark.parametrize("changes,path_fragment", [
    ({"schema_version": 2}, "schema_version"),
    ({"schema_version": True}, "schema_version"),
    ({"schema_version": 1.0}, "schema_version"),
    ({"schema_version": "1"}, "schema_version"),
    ({"name": 12}, "name"),
    ({"groups": []}, "groups"),
    ({"unexpected": "ignored configuration would be unsafe"}, "unexpected"),
])
def test_invalid_root_configuration_fails_before_model_loading(tmp_path, monkeypatch, changes, path_fragment):
    from tools.boat_analysis.model import runtime

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid YAML must be rejected before loading the model")

    monkeypatch.setattr(runtime, "load_model", forbidden)
    path = write_config(tmp_path, **changes)
    with pytest.raises(ValueError) as caught:
        run_study(path)
    assert path_fragment in str(caught.value)
    assert str(path) in str(caught.value)


@pytest.mark.parametrize("value", [[1, 2], {"expression": "arbitrary_python()"}, None])
def test_only_explicit_scalar_assumptions_are_allowed(tmp_path, value):
    groups = [{
        "name": "bad-input",
        "select": {"id": PREFIX + "inputOnly"},
        "scenarios": [{"name": "bad", "arguments": {"x": {
            "value": value, "rationale": "Synthetic invalid-value test",
        }}}],
    }]
    path = write_config(tmp_path, groups)
    with pytest.raises(ValueError) as caught:
        load_study(path)
    text = str(caught.value)
    assert "groups" in text and "arguments" in text and "x" in text


@pytest.mark.parametrize("assumption", [
    {"value": 2},
    {"value": 2, "rationale": ""},
    {"value": 2, "rationale": "test", "expression": "x + 1"},
])
def test_external_assumptions_require_rationale_and_reject_executable_fields(tmp_path, assumption):
    path = write_config(tmp_path, [{
        "name": "assumption", "select": {"id": PREFIX + "inputOnly"},
        "scenarios": [{"name": "test", "arguments": {"x": assumption}}],
    }])
    with pytest.raises(ValueError) as caught:
        load_study(path)
    assert "arguments" in str(caught.value) and "x" in str(caught.value)


@pytest.mark.parametrize("duplicate", [
    "schema_version: 1\nschema_version: 1\nname: Duplicate\ngroups: []\n",
    "schema_version: 1\nname: Duplicate\ngroups:\n  - name: one\n    select:\n      id: A::one\n      id: A::two\n",
])
def test_duplicate_yaml_keys_are_not_silently_overwritten(tmp_path, duplicate):
    path = tmp_path / "duplicate.yaml"
    path.write_text(duplicate, encoding="utf-8")
    with pytest.raises(ValueError) as caught:
        load_study(path)
    assert "duplicate" in str(caught.value).lower()
    assert str(path) in str(caught.value)


@pytest.mark.parametrize("selector", [
    {"id": PREFIX + "exactValues", "kind": "AnalysisCaseUsage"},
    {"kind": "AnalysisCaseUsage", "owner": PREFIX + "Cases", "cardinality": "first"},
])
def test_selectors_cannot_silently_broaden_or_pick_first(tmp_path, selector):
    with pytest.raises(ValueError):
        load_study(write_config(tmp_path, [{"name": "bad", "select": selector}]))


def test_missing_and_ambiguous_matches_report_selector_path(tmp_path, native_model):
    for selector, fragment in [
        ({"id": PREFIX + "notPresent"}, "notPresent"),
        ({"kind": "AnalysisCaseUsage", "owner": PREFIX + "Cases"}, "multiple"),
    ]:
        config = load_study(write_config(tmp_path, [{"name": "selection", "select": selector}]))
        with pytest.raises(ValueError) as caught:
            resolve_selector(native_model, config.groups[0].select, path="groups[0].select")
        message = str(caught.value)
        assert "groups[0].select" in message
        if fragment == "notPresent":
            assert fragment in message


def test_discovered_cases_are_ordered_by_native_id_and_repeated_runs_are_stable(tmp_path, native_model):
    config = load_study(write_config(tmp_path, [{
        "name": "configured",
        "select": {
            "kind": "AnalysisCaseUsage", "owner": PREFIX + "Cases",
            "type": PREFIX + "Scale", "cardinality": "many",
        },
    }]))
    selected = resolve_selector(native_model, config.groups[0].select, path="groups[0].select")
    assert selected == [PREFIX + "Cases::alpha", PREFIX + "Cases::zeta"]
    first = run_study(config, model=native_model)
    second = run_study(config, model=native_model)
    assert first["nativeOutputs"] == second["nativeOutputs"]
    assert list(first["nativeOutputs"]) == ["configured/default/" + case for case in selected]
    assert [value["product"] for value in first["nativeOutputs"].values()] == [12, 24]
    assert first["provenance"]["groups"][0]["analyses"] == selected


def test_new_model_case_is_discovered_without_a_python_registry_edit(tmp_path):
    extra = tmp_path / "additional-case.sysml"
    extra.write_text("""package NewStudyCases {
        analysis added : DeclarativeStudyFixtures::Scale {
            subject :>> target = DeclarativeStudyFixtures::alternate;
            in attribute :>> gain = 3;
        }
    }""", encoding="utf-8")
    config = load_study(write_config(tmp_path, [{
        "name": "all-configured",
        "select": {"kind": "AnalysisCaseUsage", "type": PREFIX + "Scale", "cardinality": "many"},
    }]))
    before = run_study(config, models=(FIXTURE,))
    after = run_study(config, models=(FIXTURE, extra))
    assert len(after["nativeOutputs"]) == len(before["nativeOutputs"]) + 1
    assert after["nativeOutputs"]["all-configured/default/NewStudyCases::added"]["product"] == 60
    assert list(after["nativeOutputs"]) == sorted(after["nativeOutputs"])


def test_subject_binding_uses_an_identified_model_configuration_and_records_assumptions(tmp_path, native_model):
    path = write_config(tmp_path, [{
        "name": "scale", "select": {"id": PREFIX + "Scale"},
        "subject": {"id": PREFIX + "alternate"},
        "scenarios": [{"name": "gain-three", "arguments": {
            "gain": {"value": 3, "rationale": "Synthetic numerical sensitivity"},
        }}],
    }])
    report = run_study(path, model=native_model)
    assert only_output(report) == {"product": 60, "label": "Alternate configuration"}
    provenance = report["provenance"]["groups"][0]
    assert provenance["subject"] == PREFIX + "alternate"
    assert provenance["runs"][0]["arguments"]["gain"]["rationale"] == "Synthetic numerical sensitivity"


@pytest.mark.parametrize("arguments", [
    {},
    {"unknown": {"value": 1, "rationale": "Unknown input negative control"}},
    {"x": {"value": "2", "rationale": "No string coercion into a model Real"}},
    {"x": {"value": True, "rationale": "Boolean must not silently become a model Real"}},
])
def test_missing_unknown_or_wrongly_typed_inputs_cannot_pass(tmp_path, native_model, arguments):
    config = load_study(write_config(tmp_path, [{
        "name": "inputs", "select": {"id": PREFIX + "inputOnly"},
        "scenarios": [{"name": "invalid", "arguments": arguments}],
    }]))
    with pytest.raises((ValueError, RuntimeError)) as caught:
        run_study(config, model=native_model)
    assert "groups.0.scenarios.0" in str(caught.value)
    assert str(config._source_path) in str(caught.value)


def test_failed_native_objectives_are_retained_distinctly_from_execution_errors(tmp_path, native_model):
    path = write_config(tmp_path, [{
        "name": "failing", "select": {"id": PREFIX + "failedObjective"},
        "require_holds": False,
    }])
    permissive = run_study(path, model=native_model)
    assert only_output(permissive)["value"] == -1
    execution = next(iter(permissive["nativeAnalyses"].values()))
    assert execution["verdicts"]
    strict_path = write_config(tmp_path, [{
        "name": "failing", "select": {"id": PREFIX + "failedObjective"},
    }])
    with pytest.raises(RuntimeError) as caught:
        run_study(strict_path, model=native_model)
    assert hasattr(caught.value, "report")
    assert caught.value.report["nativeOutputs"] == permissive["nativeOutputs"]


@pytest.mark.parametrize("literal", [".nan", ".inf", "-.inf"])
def test_nonfinite_external_assumptions_fail_with_argument_path(tmp_path, literal):
    path = tmp_path / "nonfinite.yaml"
    path.write_text(
        "schema_version: 1\nname: Finite values only\ngroups:\n"
        "  - name: finite\n    select:\n"
        "      id: DeclarativeStudyFixtures::inputOnly\n"
        "    scenarios:\n      - name: bad\n        arguments:\n"
        f"          x: {{value: {literal}, rationale: Negative control}}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError) as caught:
        load_study(path)
    assert "arguments" in str(caught.value) and "x" in str(caught.value)


def test_scalar_bindings_cannot_masquerade_as_native_dimensional_values(tmp_path, native_model):
    path = write_config(tmp_path, [{
        "name": "dimension", "select": {"id": PREFIX + "dimensionalInput"},
        "scenarios": [{"name": "unsupported", "arguments": {
            "distance": {"value": 2, "unit": "m", "rationale": "Synthetic unit binding negative control"},
        }}],
    }])
    with pytest.raises(ValueError) as caught:
        run_study(path, model=native_model)
    assert "distance" in str(caught.value)


def test_argument_keys_cannot_collapse_into_an_overwritten_binding(tmp_path):
    path = write_config(tmp_path, [{
        "name": "keys", "select": {"id": PREFIX + "inputOnly"},
        "scenarios": [{"name": "collision", "arguments": {
            "x": {"value": 2, "rationale": "First distinct YAML key"},
            " x ": {"value": 3, "rationale": "Whitespace key must not overwrite the first"},
        }}],
    }])
    config = load_study(path)
    arguments = config.groups[0].scenarios[0].arguments
    assert set(arguments) == {"x", " x "}
    assert arguments["x"].value == 2
    assert arguments[" x "].value == 3


@pytest.mark.parametrize("source,fragment", [
    ("!!python/object/apply:builtins.str [1]\n", "constructor"),
    (
        "defaults: &defaults {schema_version: 1, name: Merged, groups: []}\n"
        "<<: *defaults\n",
        "merge",
    ),
])
def test_yaml_cannot_invoke_python_or_hide_bindings_in_merges(tmp_path, source, fragment):
    path = tmp_path / "unsupported-yaml.yaml"
    path.write_text(source, encoding="utf-8")
    with pytest.raises(ValueError) as caught:
        load_study(path)
    assert fragment in str(caught.value).lower()
    assert str(path) in str(caught.value)


def test_preloaded_configuration_cannot_execute_after_its_source_changes(tmp_path, monkeypatch):
    from tools.boat_analysis.model import runtime

    path = write_config(tmp_path)
    config = load_study(path)
    path.write_text(path.read_text().replace("Synthetic native reuse", "Changed configuration"), encoding="utf-8")

    def forbidden(*args, **kwargs):
        pytest.fail("A changed validated configuration must fail before model loading")

    monkeypatch.setattr(runtime, "load_model", forbidden)
    with pytest.raises(ValueError) as caught:
        run_study(config)
    assert "changed" in str(caught.value).lower()
    assert str(path) in str(caught.value)


def test_injected_stale_snapshot_cannot_claim_current_disk_provenance(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from tools.boat_analysis.model import runtime

    config = load_study(write_config(tmp_path))
    old = SimpleNamespace(hash="old-snapshot", documents=(str(FIXTURE),))
    current = SimpleNamespace(hash="current-disk-snapshot")
    monkeypatch.setattr(runtime, "load_model", lambda files: current)
    with pytest.raises(ValueError) as caught:
        run_study(config, model=old)
    assert "snapshot" in str(caught.value).lower()


def test_native_trade_evaluations_export_without_losing_tie_or_selection_semantics():
    from fractions import Fraction
    from opensysml.verdict import CaseEvaluation
    from tools.boat_analysis.studies.runner import _native_json

    native = CaseEvaluation(
        "SyntheticTrade::score", [12, "1/3 is a label"],
        result=Fraction(1, 3), selected=True, tied=True,
    )
    exported = _native_json(native)
    assert exported["function_id"] == "SyntheticTrade::score"
    assert exported["arguments"] == [12, "1/3 is a label"]
    assert exported["result"] == pytest.approx(1 / 3)
    assert exported["error"] == ""
    assert exported["selected"] is True
    assert exported["tied"] is True


def test_nested_unrepresentable_output_is_execution_error_with_retained_native_report(
    tmp_path, monkeypatch, native_model,
):
    from opensysml.errors import UnsupportedValueError
    from opensysml.verdict import AnalysisResult
    from tools.boat_analysis.studies.runner import StudyExecutionError

    result = AnalysisResult(
        {"nested": [{"unrepresentable": UnsupportedValueError("synthetic unsupported value")}]},
        [],
    )
    # Exercise export/error classification with a genuine native result object.
    # This replacement executes no native analysis and changes no model source.
    monkeypatch.setattr(native_model, "run_analysis", lambda *args, **kwargs: result)
    with pytest.raises(StudyExecutionError) as caught:
        run_study(write_config(tmp_path), model=native_model)
    report = caught.value.report
    output = only_output(report)["nested"][0]["unrepresentable"]
    assert output["error"] == "UnsupportedValueError"
    assert output["message"] == "synthetic unsupported value"
    assert report["provenance"]["executionErrors"]
    assert "nested" in str(caught.value)
