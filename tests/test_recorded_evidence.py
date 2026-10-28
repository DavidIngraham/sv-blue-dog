from tools.boat_analysis.evidence.records import baseline_record, verify_baseline_sources


def test_recorded_sources_match_original_revision():
    assert verify_baseline_sources() > 10


def test_archived_candidate_is_not_relabelled_as_verified():
    result = baseline_record("coupled-sizing-search.json")
    assert result["qualified"] is False
    assert 1.80 < result["design"]["length_m"] < 1.82


def test_model_projection_matches_immutable_evidence():
    from tools.boat_analysis.evidence.model import model_source
    from tools.boat_analysis.model.runtime import ROOT
    from tools.boat_analysis.evidence.projection import read_projection
    assert read_projection("coupled-2026-10-10") == model_source()


def test_native_record_review_distinguishes_nominal_and_adverse_cases():
    import json
    from tools.boat_analysis.model.runtime import native
    for name in ("nominal", "construction", "aerodynamic", "hydrodynamic", "energy", "combined"):
        report = json.loads(native("-analysis", f"BlueDog::Evidence::RecordedSizing::{name}Review", "-json"))
        assert report["status"] == "holds"
        values = {v["name"]: v["value"] for v in report["checks"][0]["values"]}
        assert values["operatingScreensPass"] == ("true" if name == "nominal" else "false")
        assert values["evidenceAccepted"] == "false"


def test_archive_preserves_dependencies_and_rejects_changed_sources(tmp_path, monkeypatch):
    import json
    import subprocess
    import pytest
    from tools.boat_analysis.evidence import records
    root = tmp_path / "repo"
    root.mkdir()
    work = root / "build/analysis"
    work.mkdir(parents=True)
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
    (root / "model.sysml").write_text("package Example;\n")
    subprocess.run(["git", "add", "model.sysml"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                    "commit", "-m", "Model"], cwd=root, check=True, capture_output=True)
    dependency = work / "input.json"
    dependency.write_text(json.dumps({"sourceHashes": {"model.sysml": records.digest(root / "model.sysml")}}))
    output = work / "result.json"
    output.write_text(json.dumps({"sourceHashes": {"build/analysis/input.json": records.digest(dependency)}}))
    monkeypatch.setattr(records, "ROOT", root)
    monkeypatch.setattr(records, "WORK", work)
    destination = records.archive_run("study", ["result.json"], "HEAD", "Synthetic archive test")
    assert records.verify_run_sources(destination) == 2
    assert (destination / "input.json").exists()
    with pytest.raises(ValueError, match="immutable"):
        records.archive_run("study", ["result.json"], "HEAD", "Overwrite prohibited")
    dependency.write_text(json.dumps({"sourceHashes": {"model.sysml": "0" * 64}}))
    output.write_text(json.dumps({"sourceHashes": {"build/analysis/input.json": records.digest(dependency)}}))
    with pytest.raises(ValueError, match="source mismatch"):
        records.archive_run("bad-study", ["result.json"], "HEAD", "Mismatched source")
    assert not (root / "evidence/runs/bad-study").exists()
