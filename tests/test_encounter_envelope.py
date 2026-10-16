"""Historical response budgets preserve timing epochs and unknown authority.

Current class-specific acceptance is tested in test_class_specific_detection.py.
"""
import json

import pytest

from tools.boat_analysis.model.runtime import load_model, native, native_value, numerical_value


@pytest.fixture(scope="module")
def envelope_model():
    return load_model()


def evaluate(model, **changes):
    inputs = dict(
        ownEastMps=3, ownNorthMps=0, targetEastMps=-15, targetNorthMps=0,
        acquisitionS=5, deliveryS=1, occupiedS=0, occupiedAtDelivery=True,
        assessmentPhaseS=1, commandS=2, avoidanceS=15, contingencyS=15,
        separationM=30, positionAllowanceM=10,
        motionBoundAvailable=True, observationBoundAvailable=True,
        appliesTrafficRequirement=True,
    )
    inputs.update(changes)
    result = model.run_analysis("BlueDogEncounterEnvelope::Envelope",
                                subject="BlueDogEncounterEnvelope::study", named_arguments=inputs)
    assert result, result
    return numerical_value(result.outputs)


def test_original_criteria_and_archived_budget_are_unchanged(envelope_model):
    old = numerical_value(envelope_model.run_analysis("BlueDogEncounterReview::Acquisition").outputs)
    assert old["requiredRangesM"] == pytest.approx([307, 201, 724, 296, 326, 220])
    summary = numerical_value(envelope_model.run_analysis("BlueDogEncounterEnvelope::Summary").outputs)
    assert summary["targetSpeedMps"] == [3.5, 1.5, 15, 4, 4, 2, 0, 0]
    assert summary["retainedRequirementM"] == 750
    assert summary["qualificationClaim"] is False
    # One second of extra delivery, not a second copy of the assessment budget.
    assert evaluate(envelope_model, deliveryS=0)["requiredRangeM"] == 724
    assert evaluate(envelope_model)["requiredRangeM"] == 742


def test_occupied_interval_epoch_and_overlap(envelope_model):
    fresh = evaluate(envelope_model)
    shorter_than_acquisition = evaluate(envelope_model, occupiedS=4, occupiedAtDelivery=False)
    at_entry = evaluate(envelope_model, occupiedS=17, occupiedAtDelivery=False)
    at_delivery = evaluate(envelope_model, occupiedS=17)
    assert fresh["responseSeconds"] == shorter_than_acquisition["responseSeconds"] == 39
    assert at_entry["responseSeconds"] == 50  # acquisition/delivery overlap the old maneuver
    assert at_delivery["responseSeconds"] == 56
    assert at_entry["requiredRangeM"] == 940
    assert at_delivery["requiredRangeM"] == 1048
    assert fresh["fitsRetainedDistance"] is True
    assert at_entry["fitsRetainedDistance"] is at_delivery["fitsRetainedDistance"] is False


def test_assessment_phase_is_charged_once_after_release(envelope_model):
    earliest = evaluate(envelope_model, occupiedS=17, assessmentPhaseS=0)
    latest = evaluate(envelope_model, occupiedS=17, assessmentPhaseS=1)
    assert latest["responseSeconds"] - earliest["responseSeconds"] == 1
    assert latest["requiredRangeM"] - earliest["requiredRangeM"] == 18


def test_relative_motion_geometries_and_common_current(envelope_model):
    # A 3-4-5 crossing gives a hand-checkable independent kinematic case.
    crossing = evaluate(envelope_model, targetEastMps=0, targetNorthMps=4)
    head_on = evaluate(envelope_model, targetEastMps=-4)
    overtaking = evaluate(envelope_model, targetEastMps=4)
    reverse_overtake = evaluate(envelope_model, ownEastMps=4, targetEastMps=3)
    shared_current = evaluate(envelope_model, ownEastMps=4, ownNorthMps=-0.5,
                              targetEastMps=1, targetNorthMps=3.5)
    assert crossing["relativeSpeedMps"] == shared_current["relativeSpeedMps"] == 5
    assert crossing["requiredRangeM"] == shared_current["requiredRangeM"]
    assert head_on["relativeSpeedMps"] == 7
    assert overtaking["relativeSpeedMps"] == reverse_overtake["relativeSpeedMps"] == 1


def test_slow_or_stationary_target_preserves_historical_comparison(envelope_model):
    stationary = evaluate(envelope_model, targetEastMps=0, separationM=20)
    weed_boundary = evaluate(envelope_model, targetEastMps=0, separationM=0,
                             appliesTrafficRequirement=False)
    no_relative_motion = evaluate(envelope_model, ownEastMps=0, targetEastMps=0)
    assert stationary["requiredRangeM"] == 147
    assert weed_boundary["requiredRangeM"] == 127
    assert no_relative_motion["requiredRangeM"] == 40  # still preserve clearance/uncertainty
    assert stationary["combinedEnvelopeM"] == 750
    assert stationary["trafficComparisonApplicable"] is True
    assert weed_boundary["combinedEnvelopeM"] == 127
    assert weed_boundary["trafficComparisonApplicable"] is False
    assert weed_boundary["fitsRetainedDistance"] is False
    assert "not applicable" in weed_boundary["status"]
    assert no_relative_motion["combinedEnvelopeM"] == 750


def test_achieved_turn_time_replaces_fifteen_second_hypothesis(envelope_model):
    baseline = evaluate(envelope_model, occupiedS=17)
    slower = evaluate(envelope_model, occupiedS=30, avoidanceS=60)
    assert slower["responseSeconds"] == 114
    assert slower["requiredRangeM"] == 2092
    assert slower["requiredRangeM"] > baseline["requiredRangeM"]
    assert slower["combinedEnvelopeM"] == slower["requiredRangeM"]


@pytest.mark.parametrize("changes", [
    {"motionBoundAvailable": False}, {"observationBoundAvailable": False},
    {"occupiedS": -1}, {"deliveryS": -1}, {"avoidanceS": -1}, {"separationM": -1},
])
def test_unknown_or_invalid_bound_cannot_produce_a_finite_pass(envelope_model, changes):
    result = evaluate(envelope_model, **changes)
    assert result["supported"] is False
    assert result["responseSeconds"] == result["requiredRangeM"] == result["combinedEnvelopeM"] == -1
    assert result["fitsRetainedDistance"] is False
    assert result["physicalQualification"] is False
    assert result["status"].startswith("Unsupported:")


def test_interleaved_inputs_do_not_leak_between_native_evaluations(envelope_model):
    first = evaluate(envelope_model)
    evaluate(envelope_model, occupiedS=45, avoidanceS=60)
    evaluate(envelope_model, motionBoundAvailable=False)
    assert evaluate(envelope_model) == first


def test_missing_inputs_cannot_reuse_previous_response_bound(envelope_model):
    from opensysml.errors import ExecutionError
    evaluate(envelope_model)
    with pytest.raises(ExecutionError, match="unbound parameter"):
        envelope_model.run_analysis("BlueDogEncounterEnvelope::Envelope",
                                    subject="BlueDogEncounterEnvelope::study", named_arguments={})


def test_summary_native_cli_client_parity(envelope_model):
    client = numerical_value(envelope_model.run_analysis("BlueDogEncounterEnvelope::Summary").outputs)
    report = json.loads(native("-analysis", "BlueDogEncounterEnvelope::Summary", "-json"))
    cli = {row["name"]: native_value(row["value"]) for row in report["checks"][0]["values"]}
    assert cli == client
