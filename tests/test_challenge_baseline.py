"""Executable challenge limits; synthetic observations, not vessel qualification."""
import pytest

@pytest.mark.parametrize("length,code,status", [
    ("1.2 [m]", 0, "holds"), ("1200 [mm]", 0, "holds"),
    ("1200.1 [mm]", 1, "fails"), ("0 [m]", 1, "fails"),
    ("-1 [m]", 1, "fails"),
])
def test_overall_length(run_model, length, code, status):
    source = ("package MeasuredBoat { private import SI::*; "
              "requirement envelope : BlueDog::Mission::Challenge::OverallLength { "
              f"attribute :>> measuredOverallLength = {length};" + " } }")
    actual, report = run_model(source, "-requirement", "MeasuredBoat::envelope")
    assert (actual, report["status"]) == (code, status)


def test_missing_length_does_not_pass(run_model):
    code, report = run_model(
        "package MeasuredBoat { requirement envelope : BlueDog::Mission::Challenge::OverallLength; }",
        "-requirement", "MeasuredBoat::envelope")
    assert code != 0
    assert report["status"] != "holds"
