// Full requirement graph is a regression oracle, not a reader-facing view.
package BlueDogViews {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view requirements : GeneralView {
        expose GorgeChallenge::*;
        expose BlueDog::Goals::*;
        expose BlueDogRequirements::*;
        filter @SysML::RequirementUsage;
    }
    view transGorgeChallenge1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 300; y = 200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 600; y = 200; }
    }
    view transGorgeChallenge2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::emergencyIntervention;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 200; }
        metadata Layout about GorgeChallenge::liveObservation { x = 300; y = 200; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 600; y = 200; }
    }
    view courseCompletion1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::courseCompletion;
        expose BlueDogRequirements::roundTrip;
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 200; }
    }
    view liveObservation1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::liveObservation;
        expose BlueDogRequirements::communications;
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 200; }
    }
    view multiDayEndurance1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::peakSupplyCapability;
        expose BlueDogRequirements::harvestCampaignCoverage;
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::harvestCampaignCoverage { x = 600; y = 200; }
    }
    view multiDayEndurance2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::energyEvidenceReadiness;
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 0; y = 200; }
    }
    view energyAwareness1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::energyEstimateCadence;
        expose BlueDogRequirements::reserveEstimateCadence;
        expose BlueDogRequirements::energyEstimateAccuracy;
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEstimateCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::reserveEstimateCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::energyEstimateAccuracy { x = 600; y = 200; }
    }
    view energyAwareness2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::conservativeEnergyEstimate;
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::conservativeEnergyEstimate { x = 0; y = 200; }
    }
    view navigationAndControl1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::guidanceUpdateCadence;
        expose BlueDogRequirements::sailCommandCadence;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::guidanceUpdateCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::sailCommandCadence { x = 600; y = 200; }
    }
    view navigationAndControl2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::steeringCommandCadence;
        expose BlueDogRequirements::positionAccuracy;
        expose BlueDogRequirements::headingAccuracy;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::steeringCommandCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::positionAccuracy { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::headingAccuracy { x = 600; y = 200; }
    }
    view trafficSafety1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::trafficTracking;
        expose BlueDogRequirements::collisionAssessmentCadence;
        expose BlueDogRequirements::avoidanceCommandDeadline;
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::trafficTracking { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::collisionAssessmentCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::avoidanceCommandDeadline { x = 600; y = 200; }
    }
    view trafficSafety2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::trafficAwarenessFault;
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::trafficAwarenessFault { x = 0; y = 200; }
    }
    view environmentalEnvelope1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::airTemperature;
        expose BlueDogRequirements::waterTemperature;
        expose BlueDogRequirements::humidity;
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::airTemperature { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::waterTemperature { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::humidity { x = 600; y = 200; }
    }
    view environmentalEnvelope2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::calmOperation;
        expose BlueDogRequirements::envelopeTransition;
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::calmOperation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 600; y = 200; }
    }
    view safeRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::abortLatchDeadline;
        expose BlueDogRequirements::recoveryTelemetryCadence;
        expose BlueDogRequirements::motorIsolationDeadline;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::abortLatchDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::recoveryTelemetryCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::motorIsolationDeadline { x = 600; y = 200; }
    }
    view safeRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::isolationRestartInhibition;
        expose BlueDogRequirements::manualControlLossShutdown;
        expose BlueDogRequirements::controlLossLocationContinuity;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::isolationRestartInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::manualControlLossShutdown { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::controlLossLocationContinuity { x = 600; y = 200; }
    }
    view safeRecovery3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::periodicLogCadence;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 600; y = 200; }
    }
    view communications1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        expose BlueDogRequirements::outageAutonomy;
        expose BlueDogRequirements::reconnectCurrentRecord;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::outageAutonomy { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::reconnectCurrentRecord { x = 600; y = 200; }
    }
    view communications2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::backlogOrdering;
        expose BlueDogRequirements::backlogCurrentPriority;
        expose BlueDogRequirements::logRetention;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::backlogOrdering { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::backlogCurrentPriority { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logRetention { x = 600; y = 200; }
    }
    view communications3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::reconnectLogPreservation;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 0; y = 200; }
    }
    view gorgeEnvironment1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeWind;
        expose BlueDogRequirements::gorgeWaves;
        expose BlueDogRequirements::gorgeCurrent;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeCurrent { x = 600; y = 200; }
    }
    view gorgeEnvironment2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeSurvivalWind;
        expose BlueDogRequirements::gorgeSurvivalWaves;
        expose BlueDogRequirements::freshwaterExposure;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 600; y = 200; }
    }
    view gorgeEnvironment3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedSnagShedding;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 300; y = 200; }
    }
    view oceanEnvironment1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanWind;
        expose BlueDogRequirements::oceanWaves;
        expose BlueDogRequirements::oceanCurrent;
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::oceanWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::oceanCurrent { x = 600; y = 200; }
    }
    view oceanEnvironment2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanSurvivalWind;
        expose BlueDogRequirements::oceanSurvivalWaves;
        expose BlueDogRequirements::saltwaterExposure;
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 600; y = 200; }
    }
    view marineDurability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::freshwaterExposure;
        expose BlueDogRequirements::saltwaterExposure;
        expose BlueDogRequirements::enclosureSealing;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::enclosureSealing { x = 600; y = 200; }
    }
    view marineDurability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetElectricalIntegrity;
        expose BlueDogRequirements::solarHeating;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::solarHeating { x = 600; y = 200; }
    }
    view marineDurability3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::printedMaterialAging;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::printedMaterialAging { x = 0; y = 200; }
    }
    view stabilityAndFouling1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::submergedWeedPassage;
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 600; y = 200; }
    }
    view stabilityAndFouling2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::weedSnagShedding;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 600; y = 200; }
    }
    view resetRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::restartDeadline;
        expose BlueDogRequirements::missionStateRestoration;
        expose BlueDogRequirements::gateProgressRestoration;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::restartDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::missionStateRestoration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::gateProgressRestoration { x = 600; y = 200; }
    }
    view resetRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::resetRestrictionPreservation;
        expose BlueDogRequirements::qualificationRestoration;
        expose BlueDogRequirements::logInterruptionDurability;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::resetRestrictionPreservation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationRestoration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 600; y = 200; }
    }
    view resetRecovery3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::unknownQualificationFallback;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::freshRecoveryCommand;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 600; y = 200; }
    }
    view resetRecovery4 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view lowEnergyRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::lowEnergyEntry;
        expose BlueDogRequirements::lowEnergyPayloadInhibition;
        expose BlueDogRequirements::lowEnergyNavigationContinuity;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyEntry { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyPayloadInhibition { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyNavigationContinuity { x = 600; y = 200; }
    }
    view lowEnergyRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::lowEnergyCollisionContinuity;
        expose BlueDogRequirements::lowEnergyExit;
        expose BlueDogRequirements::payloadRestartPermission;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyCollisionContinuity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyExit { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::payloadRestartPermission { x = 600; y = 200; }
    }
    view lowEnergyRecovery3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 600; y = 200; }
    }
    view lowEnergyRecovery4 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view ingressResponse1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::ingressDetection;
        expose BlueDogRequirements::ingressRecoveryRequest;
        expose BlueDogRequirements::ingressFlotation;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::ingressDetection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::ingressRecoveryRequest { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::ingressFlotation { x = 600; y = 200; }
    }
    view ingressResponse2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::ingressElectronicsProtection;
        expose BlueDogRequirements::ingressPositionContinuity;
        expose BlueDogRequirements::ingressEventDeadline;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::ingressElectronicsProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::ingressPositionContinuity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::ingressEventDeadline { x = 600; y = 200; }
    }
    view ingressResponse3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
    }
    view missionEvidence1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::logRetention;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::logRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 600; y = 200; }
    }
    view missionEvidence2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::logTimestampAccuracy;
        expose BlueDogRequirements::invalidTimestampMarking;
        expose BlueDogRequirements::logGapIndication;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::logTimestampAccuracy { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::invalidTimestampMarking { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logGapIndication { x = 600; y = 200; }
    }
    view missionEvidence3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::logInterruptionDurability;
        expose BlueDogRequirements::reconnectLogPreservation;
        expose BlueDogRequirements::qualificationPersistence;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
    view missionEvidence4 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::unknownQualificationFallback;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 0; y = 200; }
    }
    view navigationAvailability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::navigationValidEpochs;
        expose BlueDogRequirements::staleNavigationInvalidation;
        expose BlueDogRequirements::navigationDegradedTransition;
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationValidEpochs { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::staleNavigationInvalidation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::navigationDegradedTransition { x = 600; y = 200; }
    }
    view navigationAvailability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::staleNavigationUseInhibition;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::staleNavigationUseInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 300; y = 200; }
    }
    view transportability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::transportability;
        expose BlueDogRequirements::soloTransport;
        expose BlueDogRequirements::liftMass;
        expose BlueDogRequirements::setupDuration;
        metadata Layout about BlueDogRequirements::transportability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::soloTransport { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::liftMass { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::setupDuration { x = 600; y = 200; }
    }
    view transportability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::transportability;
        expose BlueDogRequirements::packDuration;
        expose BlueDogRequirements::soloLaunch;
        expose BlueDogRequirements::soloRetrieval;
        metadata Layout about BlueDogRequirements::transportability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::packDuration { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::soloLaunch { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::soloRetrieval { x = 600; y = 200; }
    }
    view serviceability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::replacementDuration;
        expose BlueDogRequirements::nondestructiveService;
        expose BlueDogRequirements::postServiceSealing;
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::replacementDuration { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::nondestructiveService { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::postServiceSealing { x = 600; y = 200; }
    }
    view serviceability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::postServiceActuation;
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::postServiceActuation { x = 0; y = 200; }
    }
    view operatingBoundary1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::boundaryEvaluationCadence;
        expose BlueDogRequirements::boundaryAvoidanceDeadline;
        expose BlueDogRequirements::boundaryAvoidanceRecording;
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryEvaluationCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceDeadline { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceRecording { x = 600; y = 200; }
    }
    view operatingBoundary2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::boundaryStartInhibition;
        expose BlueDogRequirements::boundaryDegradedEvidence;
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryStartInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryDegradedEvidence { x = 300; y = 200; }
    }
    view navigationConspicuity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::navigationLightPresentation;
        expose BlueDogRequirements::navigationShapePresentation;
        expose BlueDogRequirements::navigationSoundPresentation;
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationLightPresentation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::navigationShapePresentation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::navigationSoundPresentation { x = 600; y = 200; }
    }
    view navigationConspicuity2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::signalingModeDeadline;
        expose BlueDogRequirements::signalingFaultRecording;
        expose BlueDogRequirements::signalingFaultReporting;
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::signalingModeDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::signalingFaultRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::signalingFaultReporting { x = 600; y = 200; }
    }
    view regulatoryClassification1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::regulatoryClassification;
        expose BlueDogRequirements::deploymentComplianceRecord;
        expose BlueDogRequirements::deploymentReleaseGate;
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::deploymentComplianceRecord { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::deploymentReleaseGate { x = 300; y = 200; }
    }
    view telemetryEquipment1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryDisplayContent;
        expose BlueDogRequirements::telemetryStaleIndication;
        expose BlueDogRequirements::telemetryIdentityPreservation;
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDisplayContent { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryStaleIndication { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryIdentityPreservation { x = 600; y = 200; }
    }
    view telemetryEquipment2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryDuplicateSuppression;
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDuplicateSuppression { x = 0; y = 200; }
    }
    view commandIntegrity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::unauthenticatedCommandRejection;
        expose BlueDogRequirements::replayCommandRejection;
        expose BlueDogRequirements::expiredCommandRejection;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unauthenticatedCommandRejection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::replayCommandRejection { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::expiredCommandRejection { x = 600; y = 200; }
    }
    view commandIntegrity2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::acceptedCommandDeadline;
        expose BlueDogRequirements::onboardAcknowledgmentDeadline;
        expose BlueDogRequirements::acknowledgmentQueueing;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::acceptedCommandDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::onboardAcknowledgmentDeadline { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::acknowledgmentQueueing { x = 600; y = 200; }
    }
    view commandIntegrity3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::externalControlDisqualification;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::qualificationPersistence;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::externalControlDisqualification { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
    view visibility1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::visibilityNavigationCapability;
        expose BlueDogRequirements::visibilityTrafficCapability;
        expose BlueDogRequirements::restrictedVisibilityEntry;
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::visibilityNavigationCapability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::visibilityTrafficCapability { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEntry { x = 600; y = 200; }
    }
    view visibility2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::restrictedVisibilityEvidence;
        expose BlueDogRequirements::restrictedVisibilityCollisionAssessment;
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEvidence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityCollisionAssessment { x = 300; y = 200; }
    }
    view envelopeTransition1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::survivalEntryDeadline;
        expose BlueDogRequirements::survivalTransitionRecording;
        expose BlueDogRequirements::sailingResumptionDeadline;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::survivalEntryDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::survivalTransitionRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::sailingResumptionDeadline { x = 600; y = 200; }
    }
    view envelopeTransition2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::sailingResumptionInhibition;
        expose BlueDogRequirements::resumptionBlockEvidence;
        expose BlueDogRequirements::periodicLogCadence;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sailingResumptionInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::resumptionBlockEvidence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 600; y = 200; }
    }
    view envelopeTransition3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view wetMechanicalIntegrity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetMechanismTravel;
        expose BlueDogRequirements::wetJointIntegrity;
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetMechanismTravel { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetJointIntegrity { x = 300; y = 200; }
    }
    view wetElectricalIntegrity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::wetElectricalIntegrity;
        expose BlueDogRequirements::wetConductorResistance;
        expose BlueDogRequirements::wetInsulationResistance;
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetConductorResistance { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetInsulationResistance { x = 300; y = 200; }
    }
    view solarHeating1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::solarHeating;
        expose BlueDogRequirements::hotSunElectronicsOperation;
        expose BlueDogRequirements::hotSunBatteryTemperature;
        expose BlueDogRequirements::batteryChargeTemperatureInhibition;
        metadata Layout about BlueDogRequirements::solarHeating { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::hotSunElectronicsOperation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::hotSunBatteryTemperature { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::batteryChargeTemperatureInhibition { x = 600; y = 200; }
    }
    view selfRighting1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::rightingDeadline;
        expose BlueDogRequirements::capsizeRigRetention;
        expose BlueDogRequirements::capsizeBallastRetention;
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::rightingDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeRigRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeBallastRetention { x = 600; y = 200; }
    }
    view selfRighting2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeElectronicsSealing;
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeElectronicsSealing { x = 0; y = 200; }
    }
    view capsizeControlRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::controlRecoveryDeadline;
        expose BlueDogRequirements::capsizeGateProgressRetention;
        expose BlueDogRequirements::capsizeQualificationRetention;
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::controlRecoveryDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeGateProgressRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeQualificationRetention { x = 600; y = 200; }
    }
    view capsizeControlRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::capsizeRestrictionRetention;
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeRestrictionRetention { x = 0; y = 200; }
    }
    view submergedWeedPassage1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedPassageSpeed;
        expose BlueDogRequirements::weedPassageSteering;
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedPassageSpeed { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedPassageSteering { x = 300; y = 200; }
    }
    view weedSnagShedding1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::weedSnagShedding;
        expose BlueDogRequirements::weedSnagSpeedRecovery;
        expose BlueDogRequirements::weedSnagSteeringRecovery;
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedSnagSpeedRecovery { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedSnagSteeringRecovery { x = 300; y = 200; }
    }
    view weedBlockageResponse1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedBlockageFault;
        expose BlueDogRequirements::weedBlockageContingency;
        expose BlueDogRequirements::weedBlockageLocation;
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedBlockageFault { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageContingency { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageLocation { x = 600; y = 200; }
    }
    view weedBlockageResponse2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
    view recoveryPropulsorWeeds1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::poweredWeedSpeed;
        expose BlueDogRequirements::poweredWeedCurrent;
        expose BlueDogRequirements::poweredWeedTemperature;
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::poweredWeedSpeed { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::poweredWeedCurrent { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::poweredWeedTemperature { x = 600; y = 200; }
    }
    view recoveryPropulsorWeeds2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::lockedPropulsorShutdown;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lockedPropulsorShutdown { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
    }
    view challengeMotorInhibition1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::freshRecoveryCommand;
        expose BlueDogRequirements::qualificationPersistence;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
    view challengeMotorInhibition2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 200; }
    }
    view sustainedEnergyFeasibility1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::repeatableCycleBalance;
        expose BlueDogRequirements::peakSupplyCapability;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::repeatableCycleBalance { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 600; y = 200; }
    }
    view sustainedEnergyFeasibility2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::energyEvidenceReadiness;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 0; y = 200; }
    }
    view cruisePerformance1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::legProgress;
        expose BlueDogRequirements::passageDuration;
        expose BlueDogRequirements::cruiseEvidence;
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::legProgress { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::passageDuration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::cruiseEvidence { x = 600; y = 200; }
    }
    view missionReliability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::failureRateBudget;
        expose BlueDogRequirements::reliabilityEvidence;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::failureRateBudget { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::reliabilityEvidence { x = 600; y = 200; }
    }
    view missionReliability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::criticalFailureDisposition;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalFailureDisposition { x = 0; y = 200; }
    }
}
