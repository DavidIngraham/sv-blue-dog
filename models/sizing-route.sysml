package BlueDogSizingRoute {
    private import ScalarValues::*;
    calc def MeanProgress {
        in water : Real [*] ordered nonunique;
        in current : Real [*] ordered nonunique;
        in weights : Real [*] ordered nonunique;
        in retention : Real;
        return mean : Real;
        NumericalFunctions::sum((1..SequenceFunctions::size(water))->ControlFunctions::collect { in i : Integer;
            weights#(i) * (retention * water#(i) + current#(i)) })
    }
    part def Profile {
        doc /* Illustrative aligned westerly route: downstream/outbound is windward,
         * upstream/return is downwind. Time fractions (3,5,15 m/s clean,5 m/s fouled)
         * are synthetic, not weather probabilities or an approved mission window.
         * Negative local progress contributes to the mean; it is never discarded.
         * Gate/boundary safety and station keeping during holds are separate. */
        attribute waterVMG : Real [8] ordered nonunique;
        attribute weights : Real [4] ordered nonunique = (0.15, 0.55, 0.10, 0.20);
        attribute downstreamCurrent : Real [4] ordered nonunique = (1.5, 1.5, 1.5, 1.5);
        attribute upstreamCurrent : Real [4] ordered nonunique = (-1.5, -1.5, -1.5, -1.5);
        attribute legDistance : Real = 100000;
        attribute holdHours : Real = 6;
        attribute holdDriftLossM : Real = 0;
        attribute availableHours : Real = 72;
        attribute environmentEvidenceAccepted : Boolean = false;
        attribute holdStrategyAccepted : Boolean = false;
    }
    analysis def Assessment {
        subject profile : Profile;
        out attribute inputsValid : Boolean = SequenceFunctions::size(profile.waterVMG) == 8 and
            NumericalFunctions::sum(profile.weights) == 1 and
            profile.weights->ControlFunctions::forAll { in weight : Real; weight >= 0 } and
            profile.legDistance > 0 and profile.holdHours >= 0 and profile.holdDriftLossM >= 0;
        assert constraint validInputs { inputsValid }
        attribute retention : Real = BlueDogDesignSearch::settings.planning_retention * BlueDogDesignSearch::settings.maneuver_retention;
        out attribute downstreamMean : Real = MeanProgress((profile.waterVMG#(1), profile.waterVMG#(3), profile.waterVMG#(5), profile.waterVMG#(7)), profile.downstreamCurrent, profile.weights, retention);
        out attribute upstreamMean : Real = MeanProgress((profile.waterVMG#(2), profile.waterVMG#(4), profile.waterVMG#(6), profile.waterVMG#(8)), profile.upstreamCurrent, profile.weights, retention);
        out attribute progressMet : Boolean = downstreamMean >= 0.5 and upstreamMean >= 0.5;
        out attribute passagePossible : Boolean = downstreamMean > 0 and upstreamMean > 0;
        out attribute elapsedHours : Real [0..1] = if passagePossible ? profile.legDistance / downstreamMean / 3600 +
            (profile.legDistance + profile.holdDriftLossM) / upstreamMean / 3600 + profile.holdHours else null;
        out attribute durationMet : Boolean = if passagePossible ? elapsedHours <= profile.availableHours else false;
        out attribute evidenceReady : Boolean = profile.environmentEvidenceAccepted and profile.holdStrategyAccepted;
        return missionSupported : Boolean = inputsValid and progressMet and durationMet and evidenceReady;
        objective calculation { require constraint { inputsValid } }
    }
    dependency progressBasis from Assessment to BlueDogRequirements::legProgress;
    dependency timeBasis from Assessment to BlueDogRequirements::passageDuration;
    dependency weatherBasis from Assessment to BlueDogRequirements::cruiseEvidence;
}
