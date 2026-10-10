package BlueDogSizing {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    doc /* Quasi-steady upwind force-capacity screen, neglecting leeway in
     * apparent-wind kinematics, with prescribed whole-sail
     * coefficients and fixed candidate foil geometry. Not a VPP, foil polar,
     * transient maneuver model, structural qualification or capsize assessment.
     * Internal numeric calculations use SI; public dimensions use ISQ quantities.
     */
    part def Sail {
        attribute area : AreaValue;
        attribute liftCoefficient : Real;
        attribute dragCoefficient : Real;
        attribute effortHeight : LengthValue;
        attribute longitudinalOffset : LengthValue;
    }
    part def Foil {
        attribute area : AreaValue;
        attribute span : LengthValue;
        attribute allowableLiftCoefficient : Real;
        attribute profileDragCoefficient : Real;
        attribute spanEfficiency : Real;
        attribute inflowRatio : Real;
    }
    part def Rudder :> Foil {
        attribute longitudinalArm : LengthValue;
        attribute hingeOffset : LengthValue;
        attribute frictionTorque : MomentOfForceValue;
        attribute availableTorque : MomentOfForceValue;
    }
    part def Configuration {
        part sail : Sail;
        part keel : Foil;
        part rudder : Rudder;
        attribute label : String;
        attribute boatSpeed : SpeedValue;
        attribute trueWindSpeed : SpeedValue;
        attribute trueWindAngle : AngularMeasureValue;
        attribute hullResistance : ForceValue;
        attribute airDensity : MassDensityValue;
        attribute waterDensity : MassDensityValue;
        attribute airViscosityM2s : Real;
        attribute waterViscosityM2s : Real;
        attribute sailMeanChord : LengthValue;
        attribute lateralForceDepth : LengthValue;
        attribute designHeel : AngularMeasureValue;
        attribute baselineRightingMoment : MomentOfForceValue;
        attribute ballastMass : MassValue;
        attribute ballastDensity : MassDensityValue;
        attribute ballastLever : LengthValue;
        attribute otherMass : MassValue;
        attribute massBudget : MassValue;
        attribute yawMomentReserve : MomentOfForceValue;
        attribute loadFactor : Real;
        attribute torqueFactor : Real;
        attribute resistanceEvidenceAccepted : Boolean;
        attribute coefficientsEvidenceAccepted : Boolean;
        attribute stabilityEvidenceAccepted : Boolean;
        attribute controlEvidenceAccepted : Boolean;
    }
    calc def PositiveRatio {
        in numerator : Real;
        in denominator : Real;
        return ratio : Real;
        if denominator > 0 ? numerator / denominator else 0
    }
    analysis def CoupledSizing {
        subject c : Configuration;
        // Echo the evaluated configuration into each standalone analysis result.
        out attribute caseLabel : String = c.label;
        out attribute boatSpeed : SpeedValue = c.boatSpeed;
        out attribute trueWindSpeed : SpeedValue = c.trueWindSpeed;
        out attribute trueWindAngle : AngularMeasureValue = c.trueWindAngle;
        out attribute hullResistance : ForceValue = c.hullResistance;
        out attribute candidateSailArea : AreaValue = c.sail.area;
        out attribute candidateKeelArea : AreaValue = c.keel.area;
        out attribute candidateRudderArea : AreaValue = c.rudder.area;
        out attribute effortHeight : LengthValue = c.sail.effortHeight;
        out attribute lateralForceDepth : LengthValue = c.lateralForceDepth;
        out attribute candidateBallastMass : MassValue = c.ballastMass;
        out attribute otherMass : MassValue = c.otherMass;
        out attribute massBudget : MassValue = c.massBudget;
        out attribute keelSpan : LengthValue = c.keel.span;
        out attribute rudderSpan : LengthValue = c.rudder.span;
        out attribute availableTorque : MomentOfForceValue = c.rudder.availableTorque;
        objective characterization {
            doc /* Compute a valid sizing screen, including unsuccessful candidates.
             * A holds result is computation validity, not design acceptance.
             */
            require constraint { inputsValid }
        }
        out attribute inputsValid : Boolean = c.boatSpeed > 0 [m/s] and c.trueWindSpeed > 0 [m/s] and
            c.trueWindAngle > 0 [rad] and c.trueWindAngle < TrigFunctions::pi / 2 * (1 [rad]) and
            c.hullResistance > 0 [N] and c.airDensity > 0 [kg/m^3] and c.waterDensity > 0 [kg/m^3] and
            c.airViscosityM2s > 0 and c.waterViscosityM2s > 0 and c.sailMeanChord > 0 [m] and
            c.sail.area > 0 [m^2] and c.sail.liftCoefficient > 0 and c.sail.dragCoefficient >= 0 and
            c.sail.effortHeight >= 0 [m] and c.lateralForceDepth >= 0 [m] and
            c.sail.effortHeight + c.lateralForceDepth > 0 [m] and
            c.keel.area > 0 [m^2] and c.keel.span > 0 [m] and c.keel.allowableLiftCoefficient > 0 and
            c.keel.profileDragCoefficient >= 0 and c.keel.spanEfficiency > 0 and c.keel.spanEfficiency <= 1 and
            c.keel.inflowRatio > 0 and c.keel.inflowRatio <= 1 and
            c.rudder.area > 0 [m^2] and c.rudder.span > 0 [m] and c.rudder.allowableLiftCoefficient > 0 and
            c.rudder.profileDragCoefficient >= 0 and c.rudder.spanEfficiency > 0 and c.rudder.spanEfficiency <= 1 and
            c.rudder.inflowRatio > 0 and c.rudder.inflowRatio <= 1 and c.rudder.longitudinalArm < 0 [m] and
            c.rudder.hingeOffset >= 0 [m] and c.rudder.frictionTorque >= 0 [N*m] and c.rudder.availableTorque > 0 [N*m] and
            c.designHeel > 0 [rad] and c.designHeel < TrigFunctions::pi / 2 * (1 [rad]) and
            c.baselineRightingMoment >= 0 [N*m] and c.ballastMass >= 0 [kg] and c.ballastDensity > c.waterDensity and
            c.ballastLever > 0 [m] and c.otherMass > 0 [kg] and c.massBudget > 0 [kg] and
            c.yawMomentReserve >= 0 [N*m] and c.loadFactor >= 1 and c.torqueFactor >= 1;
        assert constraint validInputs { inputsValid }
        attribute v : Real = c.boatSpeed / (1 [m/s]);
        attribute wind : Real = c.trueWindSpeed / (1 [m/s]);
        attribute twa : Real = c.trueWindAngle / (1 [rad]);
        attribute apparentForward : Real = wind * TrigFunctions::cos(twa) + v;
        attribute apparentLateral : Real = wind * TrigFunctions::sin(twa);
        attribute va : Real = RealFunctions::sqrt(apparentForward * apparentForward + apparentLateral * apparentLateral);
        attribute qa : Real = 0.5 * (c.airDensity / (1 [kg/m^3])) * va * va;
        attribute vk : Real = v * c.keel.inflowRatio;
        attribute vr : Real = v * c.rudder.inflowRatio;
        attribute qk : Real = 0.5 * (c.waterDensity / (1 [kg/m^3])) * vk * vk;
        attribute qr : Real = 0.5 * (c.waterDensity / (1 [kg/m^3])) * vr * vr;
        attribute drivePerArea : Real = qa * PositiveRatio(c.sail.liftCoefficient * apparentLateral - c.sail.dragCoefficient * apparentForward, va);
        attribute sidePerArea : Real = qa * PositiveRatio(c.sail.liftCoefficient * apparentForward + c.sail.dragCoefficient * apparentLateral, va);
        attribute a : Real = c.sail.area / (1 [m^2]);
        attribute ak : Real = c.keel.area / (1 [m^2]);
        attribute ar : Real = c.rudder.area / (1 [m^2]);
        attribute bk : Real = c.keel.span / (1 [m]);
        attribute br : Real = c.rudder.span / (1 [m]);
        // +x forward from keel center. Rudder arm is negative (aft).
        // Yr = Ys*xS/xR and Yk = Ys-Yr; negative trim load is retained.
        attribute rudderFraction : Real = -PositiveRatio(c.sail.longitudinalOffset / (1 [m]), -c.rudder.longitudinalArm / (1 [m]));
        attribute side : Real = sidePerArea * a;
        attribute yr : Real = side * rudderFraction;
        attribute yk : Real = side - yr;
        attribute reserveForce : Real = PositiveRatio(c.yawMomentReserve / (1 [N*m]), -c.rudder.longitudinalArm / (1 [m]));
        attribute rudderLoad : Real = RealFunctions::abs(yr) + reserveForce;
        attribute keelLoad : Real = RealFunctions::abs(yk) + reserveForce;
        attribute kInduced : Real = PositiveRatio(sidePerArea * sidePerArea * (1-rudderFraction) * (1-rudderFraction), qk * TrigFunctions::pi * c.keel.spanEfficiency * bk * bk);
        attribute rInduced : Real = PositiveRatio(sidePerArea * sidePerArea * rudderFraction * rudderFraction, qr * TrigFunctions::pi * c.rudder.spanEfficiency * br * br);
        attribute inducedFactor : Real = kInduced + rInduced;
        attribute fixedDrag : Real = c.hullResistance / (1 [N]) + qk * ak * c.keel.profileDragCoefficient + qr * ar * c.rudder.profileDragCoefficient;
        attribute discriminant : Real = drivePerArea * drivePerArea - 4 * inducedFactor * fixedDrag;
        out attribute driveSolutionExists : Boolean = inputsValid and drivePerArea > 0 and discriminant >= 0 and inducedFactor > 0;
        attribute root : Real = if discriminant >= 0 ? RealFunctions::sqrt(discriminant) else 0;
        out attribute minimumSailArea : AreaValue = (if driveSolutionExists ? PositiveRatio(2 * fixedDrag, drivePerArea + root) else 0) * (1 [m^2]);
        out attribute maximumDriveSailArea : AreaValue = (if driveSolutionExists ? PositiveRatio(drivePerArea + root, 2 * inducedFactor) else 0) * (1 [m^2]);
        out attribute apparentWindSpeed : SpeedValue = va * (1 [m/s]);
        out attribute sailDrive : ForceValue = drivePerArea * a * (1 [N]);
        out attribute sailSideForce : ForceValue = side * (1 [N]);
        out attribute keelTrimForce : ForceValue = yk * (1 [N]);
        out attribute rudderTrimForce : ForceValue = yr * (1 [N]);
        out attribute totalResistance : ForceValue = (fixedDrag + inducedFactor * a * a) * (1 [N]);
        out attribute driveMargin : ForceValue = sailDrive - totalResistance;
        out attribute minimumKeelArea : AreaValue = PositiveRatio(c.loadFactor * keelLoad, qk * c.keel.allowableLiftCoefficient) * (1 [m^2]);
        out attribute minimumRudderArea : AreaValue = PositiveRatio(c.loadFactor * rudderLoad, qr * c.rudder.allowableLiftCoefficient) * (1 [m^2]);
        out attribute keelAspectRatio : Real = PositiveRatio(bk * bk, ak);
        out attribute rudderAspectRatio : Real = PositiveRatio(br * br, ar);
        out attribute keelMeanChord : LengthValue = PositiveRatio(ak, bk) * (1 [m]);
        out attribute rudderMeanChord : LengthValue = PositiveRatio(ar, br) * (1 [m]);
        out attribute keelReynolds : Real = PositiveRatio(vk * (keelMeanChord / (1 [m])), c.waterViscosityM2s);
        out attribute rudderReynolds : Real = PositiveRatio(vr * (rudderMeanChord / (1 [m])), c.waterViscosityM2s);
        out attribute sailReynolds : Real = PositiveRatio(va * (c.sailMeanChord / (1 [m])), c.airViscosityM2s);
        attribute lever : Real = (c.sail.effortHeight + c.lateralForceDepth) / (1 [m]);
        // Incremental submerged ballast approximation at a fixed heel and lever.
        attribute ballastMomentPerKg : Real = 9.80665 * (1 - PositiveRatio(c.waterDensity / (1 [kg/m^3]), c.ballastDensity / (1 [kg/m^3]))) * (c.ballastLever / (1 [m])) * TrigFunctions::sin(c.designHeel / (1 [rad]));
        out attribute heelingMoment : MomentOfForceValue = side * lever * (1 [N*m]);
        out attribute availableRightingMoment : MomentOfForceValue = c.baselineRightingMoment + (c.ballastMass / (1 [kg])) * ballastMomentPerKg * (1 [N*m]);
        out attribute maximumHeelSailArea : AreaValue = PositiveRatio(availableRightingMoment / (1 [N*m]), c.loadFactor * sidePerArea * lever) * (1 [m^2]);
        attribute ballastMomentNeeded : Real = c.loadFactor * (heelingMoment / (1 [N*m])) - c.baselineRightingMoment / (1 [N*m]);
        out attribute minimumBallastMass : MassValue = (if ballastMomentNeeded > 0 ? PositiveRatio(ballastMomentNeeded, ballastMomentPerKg) else 0) * (1 [kg]);
        out attribute requiredRudderTorque : MomentOfForceValue = c.torqueFactor * (c.loadFactor * rudderLoad * (c.rudder.hingeOffset / (1 [m])) * (1 [N*m]) + c.rudder.frictionTorque);
        out attribute driveMet : Boolean = driveSolutionExists and driveMargin >= 0 [N];
        out attribute heelMet : Boolean = inputsValid and availableRightingMoment >= c.loadFactor * heelingMoment;
        out attribute keelMet : Boolean = inputsValid and c.keel.area >= minimumKeelArea;
        out attribute rudderMet : Boolean = inputsValid and c.rudder.area >= minimumRudderArea;
        out attribute rudderEnvelopeTorque : MomentOfForceValue = c.torqueFactor * (c.loadFactor * qr * ar * c.rudder.allowableLiftCoefficient * (c.rudder.hingeOffset / (1 [m])) * (1 [N*m]) + c.rudder.frictionTorque);
        out attribute keelRootSideMoment : MomentOfForceValue = c.loadFactor * keelLoad * bk / 2 * (1 [N*m]);
        out attribute rudderRootSideMoment : MomentOfForceValue = c.loadFactor * rudderLoad * br / 2 * (1 [N*m]);
        out attribute torqueMet : Boolean = inputsValid and c.rudder.availableTorque >= requiredRudderTorque and c.rudder.availableTorque >= rudderEnvelopeTorque;
        out attribute massMet : Boolean = inputsValid and c.otherMass + c.ballastMass <= c.massBudget;
        out attribute sailIntervalExists : Boolean = driveSolutionExists and minimumSailArea <= maximumHeelSailArea;
        out attribute modeledFit : Boolean = inputsValid and driveMet and heelMet and keelMet and rudderMet and torqueMet and massMet;
        out attribute evidenceReady : Boolean = c.resistanceEvidenceAccepted and c.coefficientsEvidenceAccepted and c.stabilityEvidenceAccepted and c.controlEvidenceAccepted;
        return supportedSizing : Boolean = modeledFit and evidenceReady;
    }
    dependency performanceBasis from CoupledSizing to BlueDogSailing::PolarDemandAndHullScreen;
    dependency sailingEvidence from CoupledSizing to BlueDogRequirements::cruiseEvidence;
    dependency stabilityScope from CoupledSizing to BlueDogRequirements::selfRighting;
    dependency weedScope from CoupledSizing to BlueDogRequirements::submergedWeedPassage;
    dependency sailAllocation from Sail to BlueDog::Architecture::HullAndRig;
    dependency keelAllocation from Configuration::keel to BlueDog::Architecture::KeelAndBallast;
    dependency steeringAllocation from Rudder to BlueDog::Architecture::SailAndSteeringActuation;
}
package BlueDogSizingExamples {
    private import SI::*;
    part def Reference :> BlueDogSizing::Configuration {
        doc /* Synthetic clean upwind demand point. None of these dimensions,
         * resistance values, coefficients or margins is a selected design.
         * Hull resistance excludes explicitly modeled appendage drag.
         */
        attribute :>> label default = "Reference";
        attribute :>> boatSpeed default = BlueDogSailingExamples::upstreamHeadwind.requiredCleanPolar;
        attribute :>> trueWindSpeed default = BlueDogSailingExamples::upstreamHeadwind.trueWindSpeed;
        attribute :>> trueWindAngle default = BlueDogSailingExamples::upstreamHeadwind.trueWindAngle;
        attribute :>> hullResistance default = 4 [N];
        attribute :>> airDensity default = 1.225 [kg/m^3];
        attribute :>> waterDensity default = 1000 [kg/m^3];
        attribute :>> airViscosityM2s default = 0.000015;
        attribute :>> waterViscosityM2s default = 0.000001;
        attribute :>> sailMeanChord default = 0.3 [m];
        attribute :>> lateralForceDepth default = 0.2 [m];
        attribute :>> designHeel default = TrigFunctions::rad(20) * (1 [rad]);
        attribute :>> baselineRightingMoment default = 3 [N*m];
        attribute :>> ballastMass default = 6 [kg];
        attribute :>> ballastDensity default = 7800 [kg/m^3];
        attribute :>> ballastLever default = 0.6 [m];
        attribute :>> otherMass default = 4 [kg];
        attribute :>> massBudget default = 12 [kg];
        attribute :>> yawMomentReserve default = 0.5 [N*m];
        attribute :>> loadFactor default = 1.5;
        attribute :>> torqueFactor default = 1.5;
        attribute :>> resistanceEvidenceAccepted default = false;
        attribute :>> coefficientsEvidenceAccepted default = false;
        attribute :>> stabilityEvidenceAccepted default = false;
        attribute :>> controlEvidenceAccepted default = false;
        part :>> sail {
            attribute :>> area default = 0.55 [m^2];
            attribute :>> liftCoefficient default = 1;
            attribute :>> dragCoefficient default = 0.12;
            attribute :>> effortHeight default = 0.6 [m];
            attribute :>> longitudinalOffset default = -0.05 [m];
        }
        part :>> keel {
            attribute :>> area default = 0.012 [m^2];
            attribute :>> span default = 0.25 [m];
            attribute :>> allowableLiftCoefficient default = 0.6;
            attribute :>> profileDragCoefficient default = 0.01;
            attribute :>> spanEfficiency default = 0.7;
            attribute :>> inflowRatio default = 1;
        }
        part :>> rudder {
            attribute :>> area default = 0.005 [m^2];
            attribute :>> span default = 0.14 [m];
            attribute :>> allowableLiftCoefficient default = 0.6;
            attribute :>> profileDragCoefficient default = 0.01;
            attribute :>> spanEfficiency default = 0.7;
            attribute :>> inflowRatio default = 0.8;
            attribute :>> longitudinalArm default = -0.5 [m];
            attribute :>> hingeOffset default = 0.01 [m];
            attribute :>> frictionTorque default = 0.02 [N*m];
            attribute :>> availableTorque default = 0.5 [N*m];
        }
    }
    part reference : Reference;
    part lowRig : Reference {
        attribute :>> label = "Lower effort / more ballast";
        attribute :>> ballastMass = 8 [kg];
        part :>> sail { attribute :>> effortHeight = 0.3 [m]; }
    }
    part slowControl : Reference {
        doc /* Frozen-load steering sensitivity at 0.5 m/s, not a steady sailing equilibrium. Hull drag is retained solely for comparison; drive results are not a resistance prediction. */
        attribute :>> label = "Slow control probe";
        attribute :>> boatSpeed = 0.5 [m/s];
    }
    part gust : Reference {
        doc /* Full-area 15 m/s steady-wind load probe, not a transient gust response or environmental-envelope qualification. */
        attribute :>> label = "Full-sail high wind";
        attribute :>> trueWindSpeed = 15 [m/s];
    }
    part highResistance : Reference {
        attribute :>> label = "Higher hull resistance";
        attribute :>> hullResistance = 12 [N];
    }
    analysis referenceSizing : BlueDogSizing::CoupledSizing { subject :>> c = reference; }
    analysis lowRigSizing : BlueDogSizing::CoupledSizing { subject :>> c = lowRig; }
    analysis slowSizing : BlueDogSizing::CoupledSizing { subject :>> c = slowControl; }
    analysis gustSizing : BlueDogSizing::CoupledSizing { subject :>> c = gust; }
    analysis resistanceSizing : BlueDogSizing::CoupledSizing { subject :>> c = highResistance; }
}
