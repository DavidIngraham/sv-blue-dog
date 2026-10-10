"""Coupled force balance, signed yaw trim, stability and invalid-input checks."""
import math
from fractions import Fraction

import pytest


@pytest.fixture
def sizing(run_model):
    def run(body=""):
        code, report = run_model(
            "package SizingTest { private import SI::*; part candidate : BlueDogSizingExamples::Reference { " + body + " } }",
            "-instantiate", "SizingTest::candidate", "-analysis", "BlueDogSizing::CoupledSizing SizingTest::candidate")
        assert not [d for d in report["diagnostics"] or [] if d["pass"] != "runtime"]
        values = {v["name"]: v["value"] for c in report["checks"] or [] for v in c["values"]}
        return code, values
    return run


def n(v, key):
    return float(Fraction(v[key].split()[0]))


def test_reference_balances_and_independent_loads(sizing):
    code, v = sizing()
    assert code == 0
    speed = 2 / (0.8 * 0.95 * math.cos(math.pi / 4))
    wx, wy = 5 * math.cos(math.pi / 4) + speed, 5 * math.sin(math.pi / 4)
    va = math.hypot(wx, wy)
    q = 0.5 * 1.225 * va**2
    side = q * 0.55 * (wx + 0.12 * wy) / va
    assert n(v, "apparentWindSpeed") == pytest.approx(va)
    assert n(v, "sailSideForce") == pytest.approx(side)
    assert n(v, "keelTrimForce") + n(v, "rudderTrimForce") == pytest.approx(side)
    assert side * -0.05 - n(v, "rudderTrimForce") * -0.5 == pytest.approx(0, abs=1e-12)
    assert n(v, "minimumKeelArea") == pytest.approx(1.5 * (0.9 * side + 1) / (0.5 * 1000 * speed**2 * 0.6))
    assert n(v, "minimumRudderArea") == pytest.approx(1.5 * (0.1 * side + 1) / (0.5 * 1000 * (0.8 * speed)**2 * 0.6))
    rm = 3 + 6 * (1 - 1000 / 7800) * 9.80665 * 0.6 * math.sin(math.radians(20))
    assert n(v, "availableRightingMoment") == pytest.approx(rm)
    assert n(v, "maximumHeelSailArea") == pytest.approx(rm / (1.5 * (side / 0.55) * 0.8))
    assert n(v, "minimumSailArea") > n(v, "maximumHeelSailArea")
    assert v["driveMet"] == "true"
    assert v["heelMet"] == v["modeledFit"] == v["supportedSizing"] == "false"


@pytest.mark.parametrize("factor,expected", [(0.999, "false"), (1.001, "true")])
def test_inverse_drive_root_boundary(sizing, factor, expected):
    _, base = sizing()
    _, v = sizing(f"part :>> sail {{ attribute :>> area = {n(base, 'minimumSailArea') * factor} [m^2]; }}")
    assert v["driveMet"] == expected


def test_forward_sail_center_reverses_rudder_trim(sizing):
    _, base = sizing()
    _, v = sizing("part :>> sail { attribute :>> longitudinalOffset = 0.05 [m]; }")
    assert n(v, "rudderTrimForce") == pytest.approx(-n(base, "rudderTrimForce"))
    assert n(v, "keelTrimForce") > n(v, "sailSideForce")
    assert n(v, "minimumRudderArea") == pytest.approx(n(base, "minimumRudderArea"))


def test_rudder_at_zero_trim_still_needs_yaw_reserve(sizing):
    _, v = sizing("part :>> sail { attribute :>> longitudinalOffset = 0 [m]; }")
    assert n(v, "rudderTrimForce") == 0
    assert n(v, "minimumRudderArea") > 0


def test_slow_flow_and_wake_increase_required_area(sizing):
    _, base = sizing()
    _, slow = sizing("attribute :>> boatSpeed = 0.5 [m/s];")
    _, wake = sizing("part :>> rudder { attribute :>> inflowRatio = 0.4; }")
    assert n(wake, "minimumRudderArea") == pytest.approx(4 * n(base, "minimumRudderArea"))
    assert slow["keelMet"] == slow["rudderMet"] == "false"
    assert slow["driveSolutionExists"] == "false"
    assert n(slow, "minimumSailArea") == 0  # Explicit invalid-result sentinel.
    assert slow["modeledFit"] == "false"


def test_lower_rig_candidate_is_not_evidence(sizing):
    _, v = sizing("attribute :>> ballastMass = 8 [kg]; part :>> sail { attribute :>> effortHeight = 0.3 [m]; }")
    assert v["modeledFit"] == "true"
    assert v["supportedSizing"] == "false"


def test_required_ballast_is_boundary_and_respects_mass(sizing):
    _, base = sizing()
    mass = n(base, "minimumBallastMass")
    _, v = sizing(f"attribute :>> ballastMass = {mass * 1.001} [kg];")
    assert v["heelMet"] == "true"
    assert v["massMet"] == v["modeledFit"] == "false"


def test_torque_covers_coefficient_envelope_not_just_trim(sizing):
    _, base = sizing()
    assert n(base, "rudderEnvelopeTorque") > n(base, "requiredRudderTorque")
    torque = (n(base, "rudderEnvelopeTorque") + n(base, "requiredRudderTorque")) / 2
    _, v = sizing(f"part :>> rudder {{ attribute :>> availableTorque = {torque} [N*m]; }}")
    assert v["torqueMet"] == "false"


def test_no_forward_drive_and_excess_resistance_cannot_pass(sizing):
    for change in ["part :>> sail { attribute :>> dragCoefficient = 2; }", "attribute :>> hullResistance = 1000 [N];"]:
        _, v = sizing(change)
        assert v["driveSolutionExists"] == v["driveMet"] == v["modeledFit"] == "false"


@pytest.mark.parametrize("body", [
    "attribute :>> boatSpeed = 0 [m/s];",
    "attribute :>> trueWindAngle = 2 [rad];",
    "attribute :>> airDensity = 0 [kg/m^3];",
    "attribute :>> ballastDensity = 1000 [kg/m^3];",
    "attribute :>> designHeel = 0 [rad];",
    "attribute :>> loadFactor = 0.5;",
    "part :>> keel { attribute :>> span = 0 [m]; }",
    "part :>> keel { attribute :>> allowableLiftCoefficient = 0; }",
    "part :>> rudder { attribute :>> inflowRatio = 0; }",
    "part :>> rudder { attribute :>> longitudinalArm = 0 [m]; }",
    "part :>> rudder { attribute :>> hingeOffset = -0.01 [m]; }",
])
def test_invalid_inputs_fail_closed(sizing, body):
    code, v = sizing(body)
    assert code != 0
    assert v.get("modeledFit") != "true"
    assert v.get("supportedSizing") != "true"
