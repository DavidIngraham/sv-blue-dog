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
    assert (ROOT / "models/evidence/coupled-2026-10-10.sysml").read_text(encoding="utf-8") == model_source()


def test_native_record_review_distinguishes_nominal_and_adverse_cases():
    import json
    from tools.boat_analysis.model.runtime import native
    for name in ("nominal", "construction", "aerodynamic", "hydrodynamic", "energy", "combined"):
        report = json.loads(native("-analysis", f"BlueDogRecordedSizing::{name}Review", "-json"))
        assert report["status"] == "holds"
        values = {v["name"]: v["value"] for v in report["checks"][0]["values"]}
        assert values["operatingScreensPass"] == ("true" if name == "nominal" else "false")
        assert values["evidenceAccepted"] == "false"
