package BlueDogSemanticViews {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view MissionSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirementVerification::RoundTripVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 200; }
        metadata Layout about BlueDogRequirementVerification::RoundTripVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
    view EnergySemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::SustainedReserveProtectionCriterion;
        expose BlueDogEnergy::SustainedEnergyVerification;
        expose BlueDog::Architecture::missionContext::boat::energy;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::SustainedReserveProtectionCriterion { x = 0; y = 200; }
        metadata Layout about BlueDogEnergy::SustainedEnergyVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat::energy { x = 0; y = 400; }
    }
    view CruiseSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::legProgress;
        expose BlueDogRequirements::LegProgressCriterion;
        expose BlueDogReliability::VoyageReliabilityVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::legProgress { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::LegProgressCriterion { x = 0; y = 200; }
        metadata Layout about BlueDogReliability::VoyageReliabilityVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
    view ReliabilitySemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::MissionReliabilityCriterion;
        expose BlueDogReliability::VoyageReliabilityVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::MissionReliabilityCriterion { x = 0; y = 200; }
        metadata Layout about BlueDogReliability::VoyageReliabilityVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
    view ManufacturingSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::desktopManufacture;
        expose BlueDog::Architecture::missionContext::boat::hullAndRig::printedHull;
        expose BlueDogRequirementVerification::DesktopManufactureVerification;
        metadata Layout about BlueDogRequirements::desktopManufacture { x = 0; y = 0; }
        metadata Layout about BlueDog::Architecture::missionContext::boat::hullAndRig::printedHull { x = 360; y = 0; }
        metadata Layout about BlueDogRequirementVerification::DesktopManufactureVerification { x = 0; y = 200; }
    }
    view WeedSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedPassageSpeed;
        expose BlueDogRequirements::weedPassageSteering;
        expose BlueDog::Architecture::missionContext::boat;
        expose BlueDogRequirementVerification::SubmergedWeedPassageVerification;
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedPassageSpeed { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::weedPassageSteering { x = 0; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 360; y = 200; }
        metadata Layout about BlueDogRequirementVerification::SubmergedWeedPassageVerification { x = 0; y = 400; }
    }
    view SailingIntegration : GeneralView {
        filter @SysML::PartDefinition;
        expose BlueDogSailing::PolarLeg;
        expose BlueDogReliability::SailingLeg;
        expose BlueDogSailing::PolarVoyageProfile;
        expose BlueDogReliability::VoyageProfile;
        metadata Layout about BlueDogSailing::PolarLeg { x = 0; y = 200; }
        metadata Layout about BlueDogReliability::SailingLeg { x = 0; y = 0; }
        metadata Layout about BlueDogSailing::PolarVoyageProfile { x = 350; y = 200; }
        metadata Layout about BlueDogReliability::VoyageProfile { x = 350; y = 0; }
    }
    view SizingIntegration : GeneralView {
        filter @SysML::PartDefinition;
        expose BlueDogSizing::Configuration;
        expose BlueDogSizing::Sail;
        expose BlueDogSizing::Foil;
        expose BlueDogSizing::Rudder;
        metadata Layout about BlueDogSizing::Configuration { x = 300; y = 0; }
        metadata Layout about BlueDogSizing::Sail { x = 0; y = 220; }
        metadata Layout about BlueDogSizing::Foil { x = 300; y = 220; }
        metadata Layout about BlueDogSizing::Rudder { x = 600; y = 220; }
    }
}
