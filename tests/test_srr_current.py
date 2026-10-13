"""Acceptance checks for the proposed SRR candidate, not physical qualification."""
import pytest
from tools.boat_analysis.evidence.records import ROOT, run_record, verify_run_sources


def test_current_candidate_has_positive_energy_and_passes_refined_screens():
    directory=ROOT/'evidence/runs/2026-10-13-srr-readiness'
    record=run_record(directory,'srr-readiness.json')
    replay=record['refinedReplay']
    concept=replay['concept']
    assert verify_run_sources(directory)>10
    assert concept['departureWh']>concept['requiredWh']
    assert concept['voyageEnergyMargin']==pytest.approx((concept['departureWh']-concept['requiredWh'])/100)
    assert replay['numericallyBalanced']
    assert replay['profileSampledStaticScreensPass']
    assert replay['qualified'] is False
    assert record['srrApproved'] is False
    assert record['physicalQualification'] is False
    assert all(record['course'][name] for name in ('gateClear','pathsClear','bothLegsUseSelectedSpan','avoidUnassessedSpans'))
