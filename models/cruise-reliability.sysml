package BlueDogReliability {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    doc /* Conditional constant-hazard exposure model, not a sailing simulator.
     * Water VMG already includes heading/tacking; current is signed along route.
     * Rates must be mission-critical, non-overlapping and confidence-qualified.
     * No repair, independence of random modes and constant hazard are assumptions.
     * Common-cause exposure is explicit. DFMEA rankings are not failure rates.
     */
    part def SailingLeg {
        attribute distance : LengthValue;
        attribute waterVMG : SpeedValue;
        attribute currentVMG : SpeedValue;
        attribute retainedPerformance : Real;
        attribute groundVMG : SpeedValue = waterVMG * retainedPerformance + currentVMG;
        attribute valid : Boolean = distance > 0 [m] and waterVMG > 0 [m/s] and
            retainedPerformance > 0 and retainedPerformance <= 1 and groundVMG > 0 [m/s];
        attribute travelTime : TimeValue = if valid ? distance / groundVMG else 0 [s];
    }
    part def VoyageProfile {
        ref part vessel : BlueDog::Architecture::Boat;
        part legs : SailingLeg [1..*] ordered;
        attribute holdTime : TimeValue;
        attribute qualifiedDuration : TimeValue;
        attribute criticalRatesPerHour : Real [1..*] ordered nonunique;
        attribute commonCauseRatePerHour : Real;
        attribute zeroFailureTestHours : Real;
        attribute observedCriticalFailures : Integer;
        attribute profileEvidenceAccepted : Boolean;
        attribute rateEvidenceAccepted : Boolean;
        attribute constantHazardAccepted : Boolean;
        attribute totalRatePerHour : Real = NumericalFunctions::sum(criticalRatesPerHour) + commonCauseRatePerHour;
        attribute voyageDuration : TimeValue = NumericalFunctions::sum(legs.travelTime) + holdTime;
        attribute valid : Boolean = SequenceFunctions::size(legs) > 0 and
            legs->ControlFunctions::forAll { in leg : SailingLeg; leg.valid } and
            holdTime >= 0 [s] and qualifiedDuration > 0 [s] and
            SequenceFunctions::size(criticalRatesPerHour) > 0 and
            criticalRatesPerHour->ControlFunctions::forAll { in rate : Real; rate >= 0 } and
            commonCauseRatePerHour >= 0 and zeroFailureTestHours > 0 and observedCriticalFailures >= 0;
    }
    analysis def CruiseReliability {
        subject profile : VoyageProfile;
        out attribute inputsValid : Boolean = profile.valid;
        assert constraint validInputs { inputsValid }
        out attribute groundSpeeds : SpeedValue [*] ordered nonunique = profile.legs.groundVMG;
        out attribute voyageHours : Real = profile.voyageDuration / (3600 [s]);
        out attribute minimumProgressMet : Boolean = BlueDogRequirements::LegProgressCriterion(groundSpeeds);
        out attribute durationMet : Boolean = BlueDogRequirements::PassageDurationCriterion(profile.voyageDuration, profile.qualifiedDuration);
        out attribute allowableRatePerHour : Real = if inputsValid ? -OpenSysMLMathFunctions::ln(0.90) / voyageHours else 0;
        out attribute modeledReliability : Real = if inputsValid ? OpenSysMLMathFunctions::exp(-profile.totalRatePerHour * voyageHours) else 0;
        out attribute rateBudgetMet : Boolean = inputsValid and BlueDogRequirements::FailureRateCriterion(profile.totalRatePerHour, voyageHours);
        out attribute requiredZeroFailureHours : Real = if inputsValid ? -OpenSysMLMathFunctions::ln(0.05) / allowableRatePerHour else 0;
        out attribute demonstrationApplicable : Boolean = inputsValid and profile.observedCriticalFailures == 0;
        out attribute zeroFailureUpperRate : Real = if demonstrationApplicable ? -OpenSysMLMathFunctions::ln(0.05) / profile.zeroFailureTestHours else 0;
        out attribute demonstratedReliabilityLowerBound : Real = if demonstrationApplicable ? OpenSysMLMathFunctions::exp(-zeroFailureUpperRate * voyageHours) else 0;
        out attribute demonstrationMet : Boolean = demonstrationApplicable and BlueDogRequirements::MissionReliabilityCriterion(demonstratedReliabilityLowerBound, 0.95);
        out attribute evidenceReady : Boolean = profile.profileEvidenceAccepted and profile.rateEvidenceAccepted and profile.constantHazardAccepted;
        return modeledFeasible : Boolean = inputsValid and minimumProgressMet and durationMet and rateBudgetMet;
        out attribute reliabilitySupported : Boolean = modeledFeasible and demonstrationMet and evidenceReady;
        objective feasibility { require constraint { modeledFeasible } }
    }
    verification def VoyageReliabilityVerification {
        subject profile : VoyageProfile;
        analysis calculation : CruiseReliability { subject = profile; }
        objective reliabilityAcceptance {
            verify BlueDogRequirements::missionSuccessProbability;
            verify BlueDogRequirements::failureRateBudget;
            verify BlueDogRequirements::reliabilityEvidence;
            verify BlueDogRequirements::legProgress;
            verify BlueDogRequirements::passageDuration;
            verify BlueDogRequirements::cruiseEvidence;
            require constraint { calculation.reliabilitySupported }
        }
        return verdict : VerificationCases::VerdictKind =
            if not calculation.evidenceReady ? VerificationCases::VerdictKind::inconclusive
            else VerificationCases::PassIf(calculation.reliabilitySupported);
    }
    dependency progressCriterion from CruiseReliability to BlueDogRequirements::legProgress;
    dependency durationCriterion from CruiseReliability to BlueDogRequirements::passageDuration;
    dependency reliabilityCriterion from CruiseReliability to BlueDogRequirements::missionSuccessProbability;
    dependency budgetCriterion from CruiseReliability to BlueDogRequirements::failureRateBudget;
    dependency evidenceCriterion from CruiseReliability to BlueDogRequirements::reliabilityEvidence;
    dependency cruiseEvidenceCriterion from CruiseReliability to BlueDogRequirements::cruiseEvidence;
    dependency durationEnergyCoupling from CruiseReliability to BlueDogEnergy::SustainedOperation;
    dependency currentContext from CruiseReliability to BlueDogRequirements::gorgeCurrent;
    dependency weedContext from CruiseReliability to BlueDogRequirements::submergedWeedPassage;
}
package BlueDogReliabilityExamples {
    private import SI::*;
    part gorgeIllustration : BlueDogReliability::VoyageProfile {
        doc /* Synthetic 100 km each-way profile; not surveyed challenge gates or a predicted polar.
         * 2.5 m/s water VMG with 20 percent loss, +/-1.5 m/s current, six hours of holds.
         * Failure-rate and test-hour inputs are illustrative, not collected evidence. */
        ref part :>> vessel = BlueDog::Architecture::missionContext.boat;
        part upstream : BlueDogReliability::SailingLeg subsets legs {
            attribute :>> distance default = 100000 [m];
            attribute :>> waterVMG default = 2.5 [m/s];
            attribute :>> currentVMG default = -1.5 [m/s];
            attribute :>> retainedPerformance default = 0.8;
        }
        part downstream : BlueDogReliability::SailingLeg subsets legs {
            attribute :>> distance default = 100000 [m];
            attribute :>> waterVMG default = 2.5 [m/s];
            attribute :>> currentVMG default = 1.5 [m/s];
            attribute :>> retainedPerformance default = 0.8;
        }
        attribute :>> holdTime default = 21600 [s];
        attribute :>> qualifiedDuration default = 259200 [s];
        attribute :>> criticalRatesPerHour default = (0.0002, 0.0003);
        attribute :>> commonCauseRatePerHour default = 0.0001;
        attribute :>> zeroFailureTestHours default = 2000;
        attribute :>> observedCriticalFailures default = 0;
        attribute :>> profileEvidenceAccepted default = false;
        attribute :>> rateEvidenceAccepted default = false;
        attribute :>> constantHazardAccepted default = false;
    }
    analysis gorgeAssessment : BlueDogReliability::CruiseReliability { subject :>> profile = gorgeIllustration; }
}
