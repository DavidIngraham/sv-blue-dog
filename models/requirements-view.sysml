// Complete graph is retained only as a regression oracle; do not publish it.
package BlueDogViews {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view requirements : GeneralView {
        expose GorgeChallenge::*;
        expose BlueDog::Goals::*;
        expose BlueDogRequirements::*;
        filter @SysML::RequirementUsage;
    }
    // Explicit native placement bounds membership. Mermaid preserves membership,
    // but lays out the retained nodes itself. Do not use render-unplaced strip.
    view transGorgeChallenge1 : GeneralView {
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::unassistedAttempt;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 300; y = 200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 600; y = 200; }
    }
    view transGorgeChallenge2 : GeneralView {
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::emergencyIntervention;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 200; }
        metadata Layout about GorgeChallenge::liveObservation { x = 300; y = 200; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 600; y = 200; }
    }
    view courseCompletion1 : GeneralView {
        expose GorgeChallenge::courseCompletion;
        expose BlueDogRequirements::roundTrip;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 200; }
    }
    view repeatedOperation1 : GeneralView {
        expose GorgeChallenge::repeatedOperation;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::serviceability { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 600; y = 200; }
    }
    view unassistedAttempt1 : GeneralView {
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 600; y = 200; }
    }
    view sailingPropulsion1 : GeneralView {
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::challengeMotorInhibition;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 300; y = 200; }
    }
    view liveObservation1 : GeneralView {
        expose GorgeChallenge::liveObservation;
        expose BlueDogRequirements::communications;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 200; }
    }
    view emergencyIntervention1 : GeneralView {
        expose GorgeChallenge::emergencyIntervention;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::commandIntegrity;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 600; y = 200; }
    }
    view hawaiiVoyage1 : GeneralView {
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::communications;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::communications { x = 600; y = 200; }
    }
    view hawaiiVoyage2 : GeneralView {
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::environmentalEnvelope;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 600; y = 200; }
    }
    view hawaiiVoyage3 : GeneralView {
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::regulatoryClassification;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 600; y = 200; }
    }
    view hawaiiVoyage4 : GeneralView {
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 300; y = 200; }
    }
    view roundTrip1 : GeneralView {
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::communications;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::communications { x = 600; y = 200; }
    }
    view roundTrip2 : GeneralView {
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::transportability;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::transportability { x = 600; y = 200; }
    }
    view roundTrip3 : GeneralView {
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::desktopManufacture;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::regulatoryClassification;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::desktopManufacture { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 600; y = 200; }
    }
    view roundTrip4 : GeneralView {
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::gorgeEnvironment;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 300; y = 200; }
    }
    view multiDayEndurance1 : GeneralView {
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::sustainedReserveProtection;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 600; y = 200; }
    }
    view multiDayEndurance2 : GeneralView {
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::peakSupplyCapability;
        expose BlueDogRequirements::harvestCampaignCoverage;
        expose BlueDogRequirements::energyEvidenceReadiness;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::harvestCampaignCoverage { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 600; y = 200; }
    }
    view energyAwareness1 : GeneralView {
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::energyEstimateCadence;
        expose BlueDogRequirements::reserveEstimateCadence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::energyEstimateCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::reserveEstimateCadence { x = 600; y = 200; }
    }
    view energyAwareness2 : GeneralView {
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::energyEstimateAccuracy;
        expose BlueDogRequirements::conservativeEnergyEstimate;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEstimateAccuracy { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::conservativeEnergyEstimate { x = 300; y = 200; }
    }
    view navigationAndControl1 : GeneralView {
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::guidanceUpdateCadence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::guidanceUpdateCadence { x = 600; y = 200; }
    }
    view navigationAndControl2 : GeneralView {
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::sailCommandCadence;
        expose BlueDogRequirements::steeringCommandCadence;
        expose BlueDogRequirements::positionAccuracy;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sailCommandCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::steeringCommandCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::positionAccuracy { x = 600; y = 200; }
    }
    view navigationAndControl3 : GeneralView {
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::headingAccuracy;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::headingAccuracy { x = 0; y = 200; }
    }
    view trafficSafety1 : GeneralView {
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::trafficTracking;
        expose BlueDogRequirements::collisionAssessmentCadence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::trafficTracking { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::collisionAssessmentCadence { x = 600; y = 200; }
    }
    view trafficSafety2 : GeneralView {
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::avoidanceCommandDeadline;
        expose BlueDogRequirements::trafficAwarenessFault;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::avoidanceCommandDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::trafficAwarenessFault { x = 300; y = 200; }
    }
    view environmentalEnvelope1 : GeneralView {
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::airTemperature;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::airTemperature { x = 600; y = 200; }
    }
    view environmentalEnvelope2 : GeneralView {
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::waterTemperature;
        expose BlueDogRequirements::humidity;
        expose BlueDogRequirements::visibility;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::waterTemperature { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::humidity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::visibility { x = 600; y = 200; }
    }
    view environmentalEnvelope3 : GeneralView {
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::calmOperation;
        expose BlueDogRequirements::envelopeTransition;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::calmOperation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 300; y = 200; }
    }
    view safeRecovery1 : GeneralView {
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::abortLatchDeadline;
        expose BlueDogRequirements::recoveryTelemetryCadence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::abortLatchDeadline { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::recoveryTelemetryCadence { x = 600; y = 200; }
    }
    view safeRecovery2 : GeneralView {
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::motorIsolationDeadline;
        expose BlueDogRequirements::isolationRestartInhibition;
        expose BlueDogRequirements::manualControlLossShutdown;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorIsolationDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::isolationRestartInhibition { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::manualControlLossShutdown { x = 600; y = 200; }
    }
    view safeRecovery3 : GeneralView {
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::controlLossLocationContinuity;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::motorQualificationInvariant;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::controlLossLocationContinuity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 600; y = 200; }
    }
    view safeRecovery4 : GeneralView {
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::periodicLogCadence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 200; }
    }
    view recoveryPropulsion1 : GeneralView {
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 300; y = 200; }
    }
    view communications1 : GeneralView {
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 600; y = 200; }
    }
    view communications2 : GeneralView {
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::outageAutonomy;
        expose BlueDogRequirements::reconnectCurrentRecord;
        expose BlueDogRequirements::backlogOrdering;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::outageAutonomy { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::reconnectCurrentRecord { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::backlogOrdering { x = 600; y = 200; }
    }
    view communications3 : GeneralView {
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::backlogCurrentPriority;
        expose BlueDogRequirements::logRetention;
        expose BlueDogRequirements::reconnectLogPreservation;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::backlogCurrentPriority { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::logRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 600; y = 200; }
    }
    view gorgeEnvironment1 : GeneralView {
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeWind;
        expose BlueDogRequirements::gorgeWaves;
        expose BlueDogRequirements::gorgeCurrent;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeCurrent { x = 600; y = 200; }
    }
    view gorgeEnvironment2 : GeneralView {
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeSurvivalWind;
        expose BlueDogRequirements::gorgeSurvivalWaves;
        expose BlueDogRequirements::freshwaterExposure;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 600; y = 200; }
    }
    view gorgeEnvironment3 : GeneralView {
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedSnagShedding;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 300; y = 200; }
    }
    view oceanEnvironment1 : GeneralView {
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanWind;
        expose BlueDogRequirements::oceanWaves;
        expose BlueDogRequirements::oceanCurrent;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::oceanWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::oceanCurrent { x = 600; y = 200; }
    }
    view oceanEnvironment2 : GeneralView {
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanSurvivalWind;
        expose BlueDogRequirements::oceanSurvivalWaves;
        expose BlueDogRequirements::saltwaterExposure;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 600; y = 200; }
    }
    view marineDurability1 : GeneralView {
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::freshwaterExposure;
        expose BlueDogRequirements::saltwaterExposure;
        expose BlueDogRequirements::enclosureSealing;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::enclosureSealing { x = 600; y = 200; }
    }
    view marineDurability2 : GeneralView {
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetElectricalIntegrity;
        expose BlueDogRequirements::solarHeating;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::solarHeating { x = 600; y = 200; }
    }
    view marineDurability3 : GeneralView {
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::printedMaterialAging;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::printedMaterialAging { x = 0; y = 200; }
    }
    view stabilityAndFouling1 : GeneralView {
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::submergedWeedPassage;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 600; y = 200; }
    }
    view stabilityAndFouling2 : GeneralView {
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::weedSnagShedding;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 600; y = 200; }
    }
    view recoveryEnergy1 : GeneralView {
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::launchEnergyAdmission;
        expose BlueDogRequirements::sustainedReserveProtection;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::launchEnergyAdmission { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 300; y = 200; }
    }
    view resetRecovery1 : GeneralView {
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::restartDeadline;
        expose BlueDogRequirements::missionStateRestoration;
        expose BlueDogRequirements::gateProgressRestoration;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::restartDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::missionStateRestoration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::gateProgressRestoration { x = 600; y = 200; }
    }
    view resetRecovery2 : GeneralView {
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::resetRestrictionPreservation;
        expose BlueDogRequirements::qualificationRestoration;
        expose BlueDogRequirements::logInterruptionDurability;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::resetRestrictionPreservation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationRestoration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 600; y = 200; }
    }
    view resetRecovery3 : GeneralView {
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::unknownQualificationFallback;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::freshRecoveryCommand;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 600; y = 200; }
    }
    view resetRecovery4 : GeneralView {
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::motorQualificationInvariant;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view lowEnergyRecovery1 : GeneralView {
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::lowEnergyEntry;
        expose BlueDogRequirements::lowEnergyPayloadInhibition;
        expose BlueDogRequirements::lowEnergyNavigationContinuity;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyEntry { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyPayloadInhibition { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyNavigationContinuity { x = 600; y = 200; }
    }
    view lowEnergyRecovery2 : GeneralView {
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::lowEnergyCollisionContinuity;
        expose BlueDogRequirements::lowEnergyExit;
        expose BlueDogRequirements::payloadRestartPermission;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyCollisionContinuity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyExit { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::payloadRestartPermission { x = 600; y = 200; }
    }
    view lowEnergyRecovery3 : GeneralView {
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        expose BlueDogRequirements::criticalEventRecording;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 600; y = 200; }
    }
    view lowEnergyRecovery4 : GeneralView {
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::motorQualificationInvariant;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view ingressResponse1 : GeneralView {
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::ingressDetection;
        expose BlueDogRequirements::ingressRecoveryRequest;
        expose BlueDogRequirements::ingressFlotation;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::ingressDetection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::ingressRecoveryRequest { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::ingressFlotation { x = 600; y = 200; }
    }
    view ingressResponse2 : GeneralView {
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::ingressElectronicsProtection;
        expose BlueDogRequirements::ingressPositionContinuity;
        expose BlueDogRequirements::ingressEventDeadline;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::ingressElectronicsProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::ingressPositionContinuity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::ingressEventDeadline { x = 600; y = 200; }
    }
    view ingressResponse3 : GeneralView {
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::motorQualificationInvariant;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
    }
    view missionEvidence1 : GeneralView {
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::logRetention;
        expose BlueDogRequirements::criticalEventRecording;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::logRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 600; y = 200; }
    }
    view missionEvidence2 : GeneralView {
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::logTimestampAccuracy;
        expose BlueDogRequirements::invalidTimestampMarking;
        expose BlueDogRequirements::logGapIndication;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::logTimestampAccuracy { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::invalidTimestampMarking { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logGapIndication { x = 600; y = 200; }
    }
    view missionEvidence3 : GeneralView {
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::logInterruptionDurability;
        expose BlueDogRequirements::reconnectLogPreservation;
        expose BlueDogRequirements::qualificationPersistence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
    view missionEvidence4 : GeneralView {
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::unknownQualificationFallback;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 0; y = 200; }
    }
    view navigationAvailability1 : GeneralView {
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::navigationValidEpochs;
        expose BlueDogRequirements::staleNavigationInvalidation;
        expose BlueDogRequirements::navigationDegradedTransition;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationValidEpochs { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::staleNavigationInvalidation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::navigationDegradedTransition { x = 600; y = 200; }
    }
    view navigationAvailability2 : GeneralView {
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::staleNavigationUseInhibition;
        expose BlueDogRequirements::criticalEventRecording;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::staleNavigationUseInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 300; y = 200; }
    }
    view transportability1 : GeneralView {
        expose BlueDogRequirements::transportability;
        expose BlueDogRequirements::soloTransport;
        expose BlueDogRequirements::liftMass;
        expose BlueDogRequirements::setupDuration;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::transportability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::soloTransport { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::liftMass { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::setupDuration { x = 600; y = 200; }
    }
    view transportability2 : GeneralView {
        expose BlueDogRequirements::transportability;
        expose BlueDogRequirements::packDuration;
        expose BlueDogRequirements::soloLaunch;
        expose BlueDogRequirements::soloRetrieval;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::transportability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::packDuration { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::soloLaunch { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::soloRetrieval { x = 600; y = 200; }
    }
    view serviceability1 : GeneralView {
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::replacementDuration;
        expose BlueDogRequirements::nondestructiveService;
        expose BlueDogRequirements::postServiceSealing;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::replacementDuration { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::nondestructiveService { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::postServiceSealing { x = 600; y = 200; }
    }
    view serviceability2 : GeneralView {
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::postServiceActuation;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::postServiceActuation { x = 0; y = 200; }
    }
    view operatingBoundary1 : GeneralView {
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::boundaryEvaluationCadence;
        expose BlueDogRequirements::boundaryAvoidanceDeadline;
        expose BlueDogRequirements::boundaryAvoidanceRecording;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryEvaluationCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceDeadline { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceRecording { x = 600; y = 200; }
    }
    view operatingBoundary2 : GeneralView {
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::boundaryStartInhibition;
        expose BlueDogRequirements::boundaryDegradedEvidence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryStartInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryDegradedEvidence { x = 300; y = 200; }
    }
    view navigationConspicuity1 : GeneralView {
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::navigationLightPresentation;
        expose BlueDogRequirements::navigationShapePresentation;
        expose BlueDogRequirements::navigationSoundPresentation;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationLightPresentation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::navigationShapePresentation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::navigationSoundPresentation { x = 600; y = 200; }
    }
    view navigationConspicuity2 : GeneralView {
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::signalingModeDeadline;
        expose BlueDogRequirements::signalingFaultRecording;
        expose BlueDogRequirements::signalingFaultReporting;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::signalingModeDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::signalingFaultRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::signalingFaultReporting { x = 600; y = 200; }
    }
    view regulatoryClassification1 : GeneralView {
        expose BlueDogRequirements::regulatoryClassification;
        expose BlueDogRequirements::deploymentComplianceRecord;
        expose BlueDogRequirements::deploymentReleaseGate;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::deploymentComplianceRecord { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::deploymentReleaseGate { x = 300; y = 200; }
    }
    view telemetryEquipment1 : GeneralView {
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryDisplayContent;
        expose BlueDogRequirements::telemetryStaleIndication;
        expose BlueDogRequirements::telemetryIdentityPreservation;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDisplayContent { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryStaleIndication { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryIdentityPreservation { x = 600; y = 200; }
    }
    view telemetryEquipment2 : GeneralView {
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryDuplicateSuppression;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDuplicateSuppression { x = 0; y = 200; }
    }
    view commandIntegrity1 : GeneralView {
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::unauthenticatedCommandRejection;
        expose BlueDogRequirements::replayCommandRejection;
        expose BlueDogRequirements::expiredCommandRejection;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unauthenticatedCommandRejection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::replayCommandRejection { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::expiredCommandRejection { x = 600; y = 200; }
    }
    view commandIntegrity2 : GeneralView {
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::acceptedCommandDeadline;
        expose BlueDogRequirements::onboardAcknowledgmentDeadline;
        expose BlueDogRequirements::acknowledgmentQueueing;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::acceptedCommandDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::onboardAcknowledgmentDeadline { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::acknowledgmentQueueing { x = 600; y = 200; }
    }
    view commandIntegrity3 : GeneralView {
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::externalControlDisqualification;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::qualificationPersistence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::externalControlDisqualification { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
    view visibility1 : GeneralView {
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::visibilityNavigationCapability;
        expose BlueDogRequirements::visibilityTrafficCapability;
        expose BlueDogRequirements::restrictedVisibilityEntry;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::visibilityNavigationCapability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::visibilityTrafficCapability { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEntry { x = 600; y = 200; }
    }
    view visibility2 : GeneralView {
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::restrictedVisibilityEvidence;
        expose BlueDogRequirements::restrictedVisibilityCollisionAssessment;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEvidence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityCollisionAssessment { x = 300; y = 200; }
    }
    view envelopeTransition1 : GeneralView {
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::survivalEntryDeadline;
        expose BlueDogRequirements::survivalTransitionRecording;
        expose BlueDogRequirements::sailingResumptionDeadline;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::survivalEntryDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::survivalTransitionRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::sailingResumptionDeadline { x = 600; y = 200; }
    }
    view envelopeTransition2 : GeneralView {
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::sailingResumptionInhibition;
        expose BlueDogRequirements::resumptionBlockEvidence;
        expose BlueDogRequirements::periodicLogCadence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sailingResumptionInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::resumptionBlockEvidence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 600; y = 200; }
    }
    view envelopeTransition3 : GeneralView {
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::motorQualificationInvariant;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view wetMechanicalIntegrity1 : GeneralView {
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetMechanismTravel;
        expose BlueDogRequirements::wetJointIntegrity;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetMechanismTravel { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetJointIntegrity { x = 300; y = 200; }
    }
    view wetElectricalIntegrity1 : GeneralView {
        expose BlueDogRequirements::wetElectricalIntegrity;
        expose BlueDogRequirements::wetConductorResistance;
        expose BlueDogRequirements::wetInsulationResistance;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetConductorResistance { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetInsulationResistance { x = 300; y = 200; }
    }
    view solarHeating1 : GeneralView {
        expose BlueDogRequirements::solarHeating;
        expose BlueDogRequirements::hotSunElectronicsOperation;
        expose BlueDogRequirements::hotSunBatteryTemperature;
        expose BlueDogRequirements::batteryChargeTemperatureInhibition;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::solarHeating { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::hotSunElectronicsOperation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::hotSunBatteryTemperature { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::batteryChargeTemperatureInhibition { x = 600; y = 200; }
    }
    view selfRighting1 : GeneralView {
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::rightingDeadline;
        expose BlueDogRequirements::capsizeRigRetention;
        expose BlueDogRequirements::capsizeBallastRetention;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::rightingDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeRigRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeBallastRetention { x = 600; y = 200; }
    }
    view selfRighting2 : GeneralView {
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeElectronicsSealing;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeElectronicsSealing { x = 0; y = 200; }
    }
    view capsizeControlRecovery1 : GeneralView {
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::controlRecoveryDeadline;
        expose BlueDogRequirements::capsizeGateProgressRetention;
        expose BlueDogRequirements::capsizeQualificationRetention;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::controlRecoveryDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeGateProgressRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeQualificationRetention { x = 600; y = 200; }
    }
    view capsizeControlRecovery2 : GeneralView {
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::capsizeRestrictionRetention;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeRestrictionRetention { x = 0; y = 200; }
    }
    view submergedWeedPassage1 : GeneralView {
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedPassageSpeed;
        expose BlueDogRequirements::weedPassageSteering;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedPassageSpeed { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedPassageSteering { x = 300; y = 200; }
    }
    view weedSnagShedding1 : GeneralView {
        expose BlueDogRequirements::weedSnagShedding;
        expose BlueDogRequirements::weedSnagSpeedRecovery;
        expose BlueDogRequirements::weedSnagSteeringRecovery;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedSnagSpeedRecovery { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedSnagSteeringRecovery { x = 300; y = 200; }
    }
    view weedBlockageResponse1 : GeneralView {
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedBlockageFault;
        expose BlueDogRequirements::weedBlockageContingency;
        expose BlueDogRequirements::weedBlockageLocation;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedBlockageFault { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageContingency { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageLocation { x = 600; y = 200; }
    }
    view weedBlockageResponse2 : GeneralView {
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::motorQualificationInvariant;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view recoveryPropulsorWeeds1 : GeneralView {
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::poweredWeedSpeed;
        expose BlueDogRequirements::poweredWeedCurrent;
        expose BlueDogRequirements::poweredWeedTemperature;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::poweredWeedSpeed { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::poweredWeedCurrent { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::poweredWeedTemperature { x = 600; y = 200; }
    }
    view recoveryPropulsorWeeds2 : GeneralView {
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::lockedPropulsorShutdown;
        expose BlueDogRequirements::motorQualificationInvariant;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lockedPropulsorShutdown { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
    }
    view challengeMotorInhibition1 : GeneralView {
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::freshRecoveryCommand;
        expose BlueDogRequirements::qualificationPersistence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
    view challengeMotorInhibition2 : GeneralView {
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::criticalEventRecording;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 200; }
    }
    view sustainedEnergyFeasibility1 : GeneralView {
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::repeatableCycleBalance;
        expose BlueDogRequirements::peakSupplyCapability;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::repeatableCycleBalance { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 600; y = 200; }
    }
    view sustainedEnergyFeasibility2 : GeneralView {
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::energyEvidenceReadiness;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 0; y = 200; }
    }
    view roundTrip5 : GeneralView {
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::missionReliability;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 300; y = 200; }
    }
    view hawaiiVoyage5 : GeneralView {
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::missionReliability;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 300; y = 200; }
    }
    view repeatedOperation2 : GeneralView {
        expose GorgeChallenge::repeatedOperation;
        expose BlueDogRequirements::missionReliability;
        filter @SysML::RequirementUsage;
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 200; }
    }
    view cruisePerformance1 : GeneralView {
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::legProgress;
        expose BlueDogRequirements::passageDuration;
        expose BlueDogRequirements::cruiseEvidence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::legProgress { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::passageDuration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::cruiseEvidence { x = 600; y = 200; }
    }
    view missionReliability1 : GeneralView {
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::failureRateBudget;
        expose BlueDogRequirements::reliabilityEvidence;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::failureRateBudget { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::reliabilityEvidence { x = 600; y = 200; }
    }
    view missionReliability2 : GeneralView {
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::criticalFailureDisposition;
        filter @SysML::RequirementUsage;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalFailureDisposition { x = 0; y = 200; }
    }
}
