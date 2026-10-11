package BlueDogMissionScope {
    private import ScalarValues::*;
    enum def MissionKind { gorge; futureOcean; futureEndurance; }
    metadata def Applicability {
        attribute mission : MissionKind;
    }
    metadata applicability : Applicability about GorgeChallenge::RepeatedOperation {
        mission = MissionKind::futureEndurance;
    }
    part current {
        attribute designObjective : String = "Maximize probability of completing one unassisted sail-only Gorge round trip within a selected weather window";
        attribute requiresOceanQualification : Boolean = false;
        attribute requiresIndefiniteOperation : Boolean = false;
        attribute requiresRepeatableEnergyBalance : Boolean = false;
        attribute enduranceCampaignHours : Real = 72;
        metadata rationale : ModelingMetadata::Rationale { text = "Owner decision: focus on the finite Gorge challenge. Retain the existing bounded 72-hour endurance campaign and reserve protection; no Hawaii route, saltwater profile or indefinite operation constraint is inherited. Passage time, speed-dependent failure exposure and weather-window completion should be compared together. Safety dispositions remain independent launch gates."; }
        metadata issue : ModelingMetadata::Issue { text = "The archived sizing search still enforces nonnegative daily energy balance. It is a conservative research screen, not the finite mission acceptance criterion. A future mission-success search needs finite energy histories, speed/load-dependent failure evidence and a valid planing model before relaxing that screen or comparing hull regimes."; }
    }
    part future {
        attribute designObjective : String = "Define a separate Hawaii mission and persistent-operation capability";
        attribute acceptanceAllocated : Boolean = false;
        metadata rationale : ModelingMetadata::Rationale { text = "Hawaii remains a future mission with independently allocated route, weather, endurance, communications, maintenance and recovery constraints. Existing ocean limits and repeating-energy cases are candidate future studies; they do not constrain Gorge acceptance."; }
    }
    dependency currentMission from current to GorgeChallenge::transGorgeChallenge;
    dependency futureMission from future to BlueDog::Goals::hawaiiVoyage;
}
