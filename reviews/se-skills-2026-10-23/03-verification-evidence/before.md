# Native OOSEM model audit

Coverage identifies defined objectives, not executed procedures or accepted physical evidence. Future-only is applicability, not a verification verdict. Native pass/fail/inconclusive/error semantics are unchanged.

Model hash: `447b852709781e2d9852bcc5d2723c41a6ef8055dc476b14117bb76bdc901f42`. OpenSysML: `23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2`.

245 of 245 current statements have verification objectives (243 requirements and 2 provisional study objectives); 12 have explicit future applicability.

## Verification coverage

| ID | Requirement | Applicability | Classification | Defined verification objectives |
| --- | --- | --- | --- | --- |
| C-000 | GorgeChallenge::transGorgeChallenge | current_gorge | requirement | GorgeChallengeVerification::PassageQualificationVerification |
| C-001 | GorgeChallenge::courseCompletion | current_gorge | requirement | GorgeChallengeVerification::PassageQualificationVerification |
| C-002 | GorgeChallenge::repeatedOperation | future_only | requirement | None |
| C-003 | GorgeChallenge::unassistedAttempt | current_gorge | requirement | GorgeChallengeVerification::PassageQualificationVerification |
| C-004 | GorgeChallenge::sailingPropulsion | current_gorge | requirement | GorgeChallengeVerification::PassageQualificationVerification |
| C-005 | GorgeChallenge::liveObservation | current_gorge | requirement | GorgeChallengeVerification::ObservationAndInterventionVerification |
| C-006 | GorgeChallenge::emergencyIntervention | current_gorge | requirement | GorgeChallengeVerification::ObservationAndInterventionVerification |
| C-007 | GorgeChallenge::navigationRules | current_gorge | requirement | GorgeChallengeVerification::WindSportEncounterVerification, GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification, GorgeChallengeVerification::InlandApplicabilityVerification, GorgeChallengeVerification::InlandLookoutAndAvoidanceVerification, GorgeChallengeVerification::InlandEncounterConductVerification, GorgeChallengeVerification::InlandChannelAndVisibilityVerification, GorgeChallengeVerification::InlandSignalsVerification |
| C-008 | GorgeChallenge::restrictedWaters | current_gorge | requirement | GorgeChallengeVerification::RestrictedWatersVerification |
| C-009 | GorgeChallenge::trafficCoexistence | current_gorge | requirement | GorgeChallengeVerification::WindSportEncounterVerification |
| C-010 | GorgeChallenge::overallLength | current_gorge | requirement | GorgeChallengeVerification::OverallLengthVerification |
| C-012 | GorgeChallenge::safetyCapabilityAbort | current_gorge | requirement | GorgeChallengeVerification::SafetyCapabilityAbortVerification |
| C-013 | GorgeChallenge::autonomousShoreRecovery | current_gorge | requirement | GorgeChallengeVerification::AutonomousShoreRecoveryVerification |
| C-014 | GorgeChallenge::abortAlert | current_gorge | requirement | GorgeChallengeVerification::AbortAlertVerification |
| C-015 | GorgeChallenge::noLittering | current_gorge | requirement | GorgeChallengeVerification::NoLitteringVerification |
| C-016 | GorgeChallenge::casualtyFlotation | current_gorge | requirement | GorgeChallengeVerification::CasualtyFlotationVerification |
| C-017 | GorgeChallenge::majorComponentRetention | current_gorge | requirement | GorgeChallengeVerification::MajorComponentRetentionVerification |
| C-018 | GorgeChallenge::capsizeRecovery | current_gorge | requirement | GorgeChallengeVerification::CapsizeRecoveryVerification |
| C-019 | GorgeChallenge::unattachedPassage | current_gorge | requirement | GorgeChallengeVerification::UnattachedPassageVerification |
| C-020 | GorgeChallenge::communicationOutageAutonomy | current_gorge | requirement | GorgeChallengeVerification::OutageAutonomyVerification |
| C-021 | GorgeChallenge::forecastAdmission | current_gorge | requirement | GorgeChallengeVerification::ForecastAdmissionVerification, GorgeChallengeVerification::LocationTrafficAdmissionVerification |
| C-022 | GorgeChallenge::weatherOutageContinuation | current_gorge | requirement | GorgeChallengeVerification::WeatherOutageContinuationVerification |
| C-023 | GorgeChallenge::courseRecoveryReserve | current_gorge | requirement | GorgeChallengeVerification::CourseRecoveryReserveVerification |
| C-024 | GorgeChallenge::reserveAbort | current_gorge | requirement | GorgeChallengeVerification::ReserveAbortVerification |
| C-025 | GorgeChallenge::nightOperation | current_gorge | requirement | GorgeChallengeVerification::NightOperationVerification |
| C-026 | GorgeChallenge::abortPersistence | current_gorge | requirement | GorgeChallengeVerification::AbortPersistenceVerification |
| C-027 | GorgeChallenge::recoveryConspicuity | current_gorge | requirement | GorgeChallengeVerification::RecoveryConspicuityVerification |
| C-028 | GorgeChallenge::navigationRuleApplicability | current_gorge | requirement | GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification |
| C-029 | GorgeChallenge::navigationRuleBaseline | current_gorge | requirement | GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification |
| C-030 | GorgeChallenge::navigationEntryEvidence | current_gorge | requirement | GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification |
| C-031 | GorgeChallenge::operatorSafetyIntervention | current_gorge | requirement | GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification |
| C-032 | GorgeChallenge::navigationAdjudication | current_gorge | requirement | GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification |
| H-001 | BlueDog::Goals::hawaiiVoyage | future_only | requirement | None |
| M-001 | BlueDogRequirements::roundTrip | current_gorge | requirement | BlueDogRequirementVerification::RoundTripVerification |
| M-002 | BlueDogRequirements::multiDayEndurance | current_gorge | requirement | BlueDogRequirementVerification::MultiDayEnduranceVerification |
| E-001 | BlueDogRequirements::energyAwareness | current_gorge | requirement | BlueDogRequirementVerification::EnergyAwarenessVerification |
| E-002 | BlueDogRequirements::navigationAndControl | current_gorge | requirement | BlueDogRequirementVerification::NavigationAndControlVerification |
| E-003 | BlueDogRequirements::resetRecovery | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification |
| E-004 | BlueDogRequirements::lowEnergyRecovery | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification |
| E-005 | BlueDogRequirements::communications | current_gorge | requirement | BlueDogRequirementVerification::CommunicationsVerification |
| E-006 | BlueDogRequirements::ingressResponse | current_gorge | requirement | BlueDogRequirementVerification::IngressResponseVerification |
| E-007 | BlueDogRequirements::missionEvidence | current_gorge | requirement | BlueDogRequirementVerification::MissionEvidenceVerification |
| P-001 | BlueDogRequirements::transportability | current_gorge | requirement | BlueDogRequirementVerification::TransportabilityVerification |
| P-002 | BlueDogRequirements::desktopManufacture | current_gorge | requirement | BlueDogRequirementVerification::DesktopManufactureVerification |
| P-003 | BlueDogRequirements::serviceability | current_gorge | requirement | BlueDogRequirementVerification::ServiceabilityVerification |
| S-001 | BlueDogRequirements::trafficSafety | current_gorge | requirement | BlueDogRequirementVerification::TrafficSafetyVerification |
| S-002 | BlueDogRequirements::operatingBoundary | current_gorge | requirement | BlueDogRequirementVerification::OperatingBoundaryVerification |
| S-003 | BlueDogRequirements::emergencyControl | current_gorge | requirement | BlueDogRequirementVerification::EmergencyControlVerification |
| S-004 | BlueDogRequirements::navigationConspicuity | current_gorge | requirement | BlueDogRequirementVerification::NavigationConspicuityVerification |
| S-005 | BlueDogRequirements::regulatoryClassification | current_gorge | requirement | BlueDogRequirementVerification::RegulatoryClassificationVerification |
| N-001 | BlueDogRequirements::environmentalEnvelope | current_gorge | requirement | BlueDogRequirementVerification::EnvironmentalEnvelopeVerification |
| N-002 | BlueDogRequirements::marineDurability | current_gorge | requirement | BlueDogRequirementVerification::MarineDurabilityVerification |
| N-003 | BlueDogRequirements::capsizeResilience | current_gorge | requirement | BlueDogRequirementVerification::CapsizeResilienceVerification |
| R-001 | BlueDogRequirements::recoveryPropulsion | current_gorge | requirement | BlueDogRequirementVerification::RecoveryPropulsionVerification |
| R-002 | BlueDogRequirements::recoveryEnergy | current_gorge | requirement | BlueDogRequirementVerification::RecoveryEnergyVerification |
| C-101 | BlueDogRequirements::telemetryEquipment | current_gorge | requirement | BlueDogRequirementVerification::TelemetryEquipmentVerification |
| C-102 | BlueDogRequirements::commandIntegrity | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| N-010 | BlueDogRequirements::gorgeEnvironment | current_gorge | requirement | BlueDogRequirementVerification::EnvironmentalEnvelopeVerification |
| N-020 | BlueDogRequirements::oceanEnvironment | future_only | requirement | None |
| N-011 | BlueDogRequirements::gorgeWind | current_gorge | requirement | BlueDogRequirementVerification::GorgeWindVerification |
| N-012 | BlueDogRequirements::gorgeWaves | current_gorge | requirement | BlueDogRequirementVerification::GorgeWavesVerification |
| N-013 | BlueDogRequirements::gorgeCurrent | current_gorge | requirement | BlueDogRequirementVerification::GorgeCurrentVerification |
| N-014 | BlueDogRequirements::gorgeSurvivalWind | current_gorge | requirement | BlueDogRequirementVerification::EnvironmentalEnvelopeVerification |
| N-015 | BlueDogRequirements::gorgeSurvivalWaves | current_gorge | requirement | BlueDogRequirementVerification::GorgeSurvivalWavesVerification |
| N-021 | BlueDogRequirements::oceanWind | future_only | requirement | BlueDogRequirementVerification::OceanWindVerification |
| N-022 | BlueDogRequirements::oceanWaves | future_only | requirement | BlueDogRequirementVerification::OceanWavesVerification |
| N-023 | BlueDogRequirements::oceanCurrent | future_only | requirement | BlueDogRequirementVerification::OceanCurrentVerification |
| N-024 | BlueDogRequirements::oceanSurvivalWind | future_only | requirement | None |
| N-025 | BlueDogRequirements::oceanSurvivalWaves | future_only | requirement | BlueDogRequirementVerification::OceanSurvivalWavesVerification |
| N-030 | BlueDogRequirements::airTemperature | current_gorge | requirement | BlueDogRequirementVerification::AirTemperatureVerification |
| N-031 | BlueDogRequirements::waterTemperature | current_gorge | requirement | BlueDogRequirementVerification::WaterTemperatureVerification |
| N-032 | BlueDogRequirements::humidity | current_gorge | requirement | BlueDogRequirementVerification::HumidityVerification |
| N-033 | BlueDogRequirements::visibility | current_gorge | requirement | BlueDogRequirementVerification::VisibilityVerification |
| N-034 | BlueDogRequirements::calmOperation | current_gorge | requirement | BlueDogRequirementVerification::CalmOperationVerification |
| N-035 | BlueDogRequirements::envelopeTransition | current_gorge | requirement | BlueDogRequirementVerification::EnvelopeTransitionVerification |
| N-041 | BlueDogRequirements::freshwaterExposure | current_gorge | requirement | BlueDogRequirementVerification::EnvironmentalEnvelopeVerification |
| N-042 | BlueDogRequirements::saltwaterExposure | future_only | requirement | None |
| N-043 | BlueDogRequirements::enclosureSealing | current_gorge | requirement | BlueDogRequirementVerification::EnvironmentalEnvelopeVerification |
| N-044 | BlueDogRequirements::wetMechanicalIntegrity | current_gorge | requirement | BlueDogRequirementVerification::WetMechanicalIntegrityVerification |
| N-045 | BlueDogRequirements::wetElectricalIntegrity | current_gorge | requirement | BlueDogRequirementVerification::WetElectricalIntegrityVerification |
| N-046 | BlueDogRequirements::solarHeating | current_gorge | requirement | BlueDogRequirementVerification::SolarHeatingVerification |
| N-047 | BlueDogRequirements::printedMaterialAging | current_gorge | requirement | BlueDogRequirementVerification::PrintedMaterialAgingVerification |
| N-051 | BlueDogRequirements::selfRighting | current_gorge | requirement | BlueDogRequirementVerification::SelfRightingVerification |
| N-052 | BlueDogRequirements::capsizeControlRecovery | current_gorge | requirement | BlueDogRequirementVerification::CapsizeControlRecoveryVerification |
| N-053 | BlueDogRequirements::submergedWeedPassage | current_gorge | requirement | BlueDogRequirementVerification::SubmergedWeedPassageVerification |
| N-054 | BlueDogRequirements::weedSnagShedding | current_gorge | requirement | BlueDogRequirementVerification::WeedSnagSheddingVerification |
| N-055 | BlueDogRequirements::weedBlockageResponse | current_gorge | requirement | BlueDogRequirementVerification::WeedBlockageResponseVerification |
| N-056 | BlueDogRequirements::recoveryPropulsorWeeds | current_gorge | requirement | BlueDogRequirementVerification::RecoveryPropulsorWeedsVerification |
| E-008 | BlueDogRequirements::navigationAvailability | current_gorge | requirement | BlueDogRequirementVerification::NavigationAvailabilityVerification |
| R-003 | BlueDogRequirements::launchEnergyAdmission | current_gorge | requirement | BlueDogRequirementVerification::LaunchEnergyAdmissionVerification |
| R-004 | BlueDogRequirements::challengeMotorInhibition | current_gorge | requirement | BlueDogRequirementVerification::ChallengeMotorInhibitionVerification |
| E-101 | BlueDogRequirements::energyEstimateCadence | current_gorge | requirement | BlueDogRequirementVerification::EnergyAwarenessVerification |
| E-102 | BlueDogRequirements::reserveEstimateCadence | current_gorge | requirement | BlueDogRequirementVerification::EnergyAwarenessVerification |
| E-103 | BlueDogRequirements::energyEstimateAccuracy | current_gorge | requirement | BlueDogRequirementVerification::EnergyAwarenessVerification |
| E-104 | BlueDogRequirements::conservativeEnergyEstimate | current_gorge | requirement | BlueDogRequirementVerification::EnergyAwarenessVerification |
| E-105 | BlueDogRequirements::guidanceUpdateCadence | current_gorge | requirement | BlueDogRequirementVerification::NavigationAndControlVerification |
| E-106 | BlueDogRequirements::sailCommandCadence | current_gorge | requirement | BlueDogRequirementVerification::NavigationAndControlVerification |
| E-107 | BlueDogRequirements::steeringCommandCadence | current_gorge | requirement | BlueDogRequirementVerification::NavigationAndControlVerification |
| E-108 | BlueDogRequirements::positionAccuracy | current_gorge | requirement | BlueDogRequirementVerification::NavigationAndControlVerification |
| E-109 | BlueDogRequirements::headingAccuracy | current_gorge | requirement | BlueDogRequirementVerification::NavigationAndControlVerification |
| E-110 | BlueDogRequirements::restartDeadline | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification |
| E-111 | BlueDogRequirements::missionStateRestoration | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification |
| E-112 | BlueDogRequirements::gateProgressRestoration | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification |
| E-113 | BlueDogRequirements::resetRestrictionPreservation | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification |
| E-114 | BlueDogRequirements::lowEnergyEntry | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification |
| E-115 | BlueDogRequirements::lowEnergyPayloadInhibition | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification |
| E-116 | BlueDogRequirements::lowEnergyNavigationContinuity | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification |
| E-117 | BlueDogRequirements::lowEnergyCollisionContinuity | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification |
| E-118 | BlueDogRequirements::lowEnergyExit | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification |
| E-119 | BlueDogRequirements::payloadRestartPermission | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification |
| E-120 | BlueDogRequirements::telemetryDeliveryCadence | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification, BlueDogRequirementVerification::CommunicationsVerification |
| E-121 | BlueDogRequirements::outageAutonomy | current_gorge | requirement | BlueDogRequirementVerification::CommunicationsVerification |
| E-122 | BlueDogRequirements::reconnectCurrentRecord | current_gorge | requirement | BlueDogRequirementVerification::CommunicationsVerification |
| E-123 | BlueDogRequirements::backlogOrdering | current_gorge | requirement | BlueDogRequirementVerification::CommunicationsVerification |
| E-124 | BlueDogRequirements::backlogCurrentPriority | current_gorge | requirement | BlueDogRequirementVerification::CommunicationsVerification |
| E-125 | BlueDogRequirements::ingressDetection | current_gorge | requirement | BlueDogRequirementVerification::IngressResponseVerification |
| E-126 | BlueDogRequirements::ingressRecoveryRequest | current_gorge | requirement | BlueDogRequirementVerification::IngressResponseVerification |
| E-127 | BlueDogRequirements::ingressFlotation | current_gorge | requirement | BlueDogRequirementVerification::IngressResponseVerification |
| E-128 | BlueDogRequirements::ingressElectronicsProtection | current_gorge | requirement | BlueDogRequirementVerification::IngressResponseVerification |
| E-129 | BlueDogRequirements::ingressPositionContinuity | current_gorge | requirement | BlueDogRequirementVerification::IngressResponseVerification |
| E-130 | BlueDogRequirements::periodicLogCadence | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification, BlueDogRequirementVerification::MissionEvidenceVerification, BlueDogRequirementVerification::EmergencyControlVerification, BlueDogRequirementVerification::EnvelopeTransitionVerification |
| E-131 | BlueDogRequirements::logRetention | current_gorge | requirement | BlueDogRequirementVerification::CommunicationsVerification, BlueDogRequirementVerification::MissionEvidenceVerification |
| E-132 | BlueDogRequirements::criticalEventRecording | current_gorge | requirement | BlueDogRequirementVerification::LowEnergyRecoveryVerification, BlueDogRequirementVerification::IngressResponseVerification, BlueDogRequirementVerification::MissionEvidenceVerification, BlueDogRequirementVerification::CommandIntegrityVerification, BlueDogRequirementVerification::NavigationAvailabilityVerification, BlueDogRequirementVerification::ChallengeMotorInhibitionVerification |
| E-133 | BlueDogRequirements::logTimestampAccuracy | current_gorge | requirement | BlueDogRequirementVerification::MissionEvidenceVerification |
| E-134 | BlueDogRequirements::invalidTimestampMarking | current_gorge | requirement | BlueDogRequirementVerification::MissionEvidenceVerification |
| E-135 | BlueDogRequirements::logGapIndication | current_gorge | requirement | BlueDogRequirementVerification::MissionEvidenceVerification |
| E-136 | BlueDogRequirements::logInterruptionDurability | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification, BlueDogRequirementVerification::MissionEvidenceVerification |
| E-137 | BlueDogRequirements::reconnectLogPreservation | current_gorge | requirement | BlueDogRequirementVerification::CommunicationsVerification, BlueDogRequirementVerification::MissionEvidenceVerification |
| E-138 | BlueDogRequirements::qualificationPersistence | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification, BlueDogRequirementVerification::MissionEvidenceVerification, BlueDogRequirementVerification::EmergencyControlVerification, BlueDogRequirementVerification::CommandIntegrityVerification, BlueDogRequirementVerification::ChallengeMotorInhibitionVerification |
| E-139 | BlueDogRequirements::unknownQualificationFallback | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification, BlueDogRequirementVerification::MissionEvidenceVerification |
| E-140 | BlueDogRequirements::navigationValidEpochs | current_gorge | requirement | BlueDogRequirementVerification::NavigationAvailabilityVerification |
| E-141 | BlueDogRequirements::staleNavigationInvalidation | current_gorge | requirement | BlueDogRequirementVerification::NavigationAvailabilityVerification |
| E-142 | BlueDogRequirements::navigationDegradedTransition | current_gorge | requirement | BlueDogRequirementVerification::NavigationAvailabilityVerification |
| E-143 | BlueDogRequirements::staleNavigationUseInhibition | current_gorge | requirement | BlueDogRequirementVerification::NavigationAvailabilityVerification |
| P-101 | BlueDogRequirements::soloTransport | current_gorge | requirement | BlueDogRequirementVerification::TransportabilityVerification |
| P-102 | BlueDogRequirements::liftMass | current_gorge | requirement | BlueDogRequirementVerification::TransportabilityVerification |
| P-103 | BlueDogRequirements::setupDuration | current_gorge | requirement | BlueDogRequirementVerification::TransportabilityVerification |
| P-104 | BlueDogRequirements::packDuration | current_gorge | requirement | BlueDogRequirementVerification::TransportabilityVerification |
| P-105 | BlueDogRequirements::soloLaunch | current_gorge | requirement | BlueDogRequirementVerification::TransportabilityVerification |
| P-106 | BlueDogRequirements::soloRetrieval | current_gorge | requirement | BlueDogRequirementVerification::TransportabilityVerification |
| P-107 | BlueDogRequirements::replacementDuration | current_gorge | requirement | BlueDogRequirementVerification::ServiceabilityVerification |
| P-108 | BlueDogRequirements::nondestructiveService | current_gorge | requirement | BlueDogRequirementVerification::ServiceabilityVerification |
| P-109 | BlueDogRequirements::postServiceSealing | current_gorge | requirement | BlueDogRequirementVerification::ServiceabilityVerification |
| P-110 | BlueDogRequirements::postServiceActuation | current_gorge | requirement | BlueDogRequirementVerification::ServiceabilityVerification |
| S-101 | BlueDogRequirements::trafficTracking | current_gorge | requirement | BlueDogRequirementVerification::TrafficSafetyVerification |
| S-102 | BlueDogRequirements::collisionAssessmentCadence | current_gorge | requirement | BlueDogRequirementVerification::TrafficSafetyVerification |
| S-103 | BlueDogRequirements::avoidanceCommandDeadline | current_gorge | requirement | BlueDogRequirementVerification::TrafficSafetyVerification |
| S-104 | BlueDogRequirements::trafficAwarenessFault | current_gorge | requirement | BlueDogRequirementVerification::TrafficSafetyVerification |
| S-105 | BlueDogRequirements::boundaryEvaluationCadence | current_gorge | requirement | BlueDogRequirementVerification::OperatingBoundaryVerification |
| S-106 | BlueDogRequirements::boundaryAvoidanceDeadline | current_gorge | requirement | BlueDogRequirementVerification::OperatingBoundaryVerification |
| S-107 | BlueDogRequirements::boundaryAvoidanceRecording | current_gorge | requirement | BlueDogRequirementVerification::OperatingBoundaryVerification |
| S-108 | BlueDogRequirements::boundaryStartInhibition | current_gorge | requirement | BlueDogRequirementVerification::OperatingBoundaryVerification |
| S-109 | BlueDogRequirements::boundaryDegradedEvidence | current_gorge | requirement | BlueDogRequirementVerification::OperatingBoundaryVerification |
| S-110 | BlueDogRequirements::abortLatchDeadline | current_gorge | requirement | BlueDogRequirementVerification::EmergencyControlVerification |
| S-111 | BlueDogRequirements::recoveryTelemetryCadence | current_gorge | requirement | BlueDogRequirementVerification::EmergencyControlVerification |
| S-112 | BlueDogRequirements::motorIsolationDeadline | current_gorge | requirement | BlueDogRequirementVerification::EmergencyControlVerification |
| S-113 | BlueDogRequirements::isolationRestartInhibition | current_gorge | requirement | BlueDogRequirementVerification::EmergencyControlVerification |
| S-114 | BlueDogRequirements::manualControlLossShutdown | current_gorge | requirement | BlueDogRequirementVerification::EmergencyControlVerification |
| S-115 | BlueDogRequirements::controlLossLocationContinuity | current_gorge | requirement | BlueDogRequirementVerification::EmergencyControlVerification |
| S-116 | BlueDogRequirements::navigationLightPresentation | current_gorge | requirement | BlueDogRequirementVerification::NavigationConspicuityVerification |
| S-117 | BlueDogRequirements::navigationShapePresentation | current_gorge | requirement | BlueDogRequirementVerification::NavigationConspicuityVerification |
| S-118 | BlueDogRequirements::navigationSoundPresentation | current_gorge | requirement | BlueDogRequirementVerification::NavigationConspicuityVerification |
| S-119 | BlueDogRequirements::signalingModeDeadline | current_gorge | requirement | BlueDogRequirementVerification::NavigationConspicuityVerification |
| S-120 | BlueDogRequirements::signalingFaultRecording | current_gorge | requirement | BlueDogRequirementVerification::NavigationConspicuityVerification |
| S-121 | BlueDogRequirements::signalingFaultReporting | current_gorge | requirement | BlueDogRequirementVerification::NavigationConspicuityVerification |
| S-122 | BlueDogRequirements::deploymentComplianceRecord | current_gorge | requirement | BlueDogRequirementVerification::RegulatoryClassificationVerification |
| S-123 | BlueDogRequirements::deploymentReleaseGate | current_gorge | requirement | BlueDogRequirementVerification::RegulatoryClassificationVerification |
| C-201 | BlueDogRequirements::telemetryDisplayContent | current_gorge | requirement | BlueDogRequirementVerification::TelemetryEquipmentVerification |
| C-202 | BlueDogRequirements::telemetryStaleIndication | current_gorge | requirement | BlueDogRequirementVerification::TelemetryEquipmentVerification |
| C-203 | BlueDogRequirements::telemetryIdentityPreservation | current_gorge | requirement | BlueDogRequirementVerification::TelemetryEquipmentVerification |
| C-204 | BlueDogRequirements::telemetryDuplicateSuppression | current_gorge | requirement | BlueDogRequirementVerification::TelemetryEquipmentVerification |
| C-205 | BlueDogRequirements::unauthenticatedCommandRejection | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| C-206 | BlueDogRequirements::replayCommandRejection | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| C-207 | BlueDogRequirements::expiredCommandRejection | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| C-208 | BlueDogRequirements::acceptedCommandDeadline | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| C-209 | BlueDogRequirements::onboardAcknowledgmentDeadline | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| C-210 | BlueDogRequirements::acknowledgmentQueueing | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| C-211 | BlueDogRequirements::externalControlDisqualification | current_gorge | requirement | BlueDogRequirementVerification::CommandIntegrityVerification |
| N-101 | BlueDogRequirements::visibilityNavigationCapability | current_gorge | requirement | BlueDogRequirementVerification::VisibilityVerification |
| N-102 | BlueDogRequirements::visibilityTrafficCapability | current_gorge | requirement | BlueDogRequirementVerification::VisibilityVerification |
| N-103 | BlueDogRequirements::restrictedVisibilityEntry | current_gorge | requirement | BlueDogRequirementVerification::VisibilityVerification |
| N-104 | BlueDogRequirements::restrictedVisibilityEvidence | current_gorge | requirement | BlueDogRequirementVerification::VisibilityVerification |
| N-105 | BlueDogRequirements::restrictedVisibilityCollisionAssessment | current_gorge | requirement | BlueDogRequirementVerification::VisibilityVerification |
| N-106 | BlueDogRequirements::survivalEntryDeadline | current_gorge | requirement | BlueDogRequirementVerification::EnvelopeTransitionVerification |
| N-107 | BlueDogRequirements::survivalTransitionRecording | current_gorge | requirement | BlueDogRequirementVerification::EnvelopeTransitionVerification |
| N-108 | BlueDogRequirements::sailingResumptionDeadline | current_gorge | requirement | BlueDogRequirementVerification::EnvelopeTransitionVerification |
| N-109 | BlueDogRequirements::sailingResumptionInhibition | current_gorge | requirement | BlueDogRequirementVerification::EnvelopeTransitionVerification |
| N-110 | BlueDogRequirements::resumptionBlockEvidence | current_gorge | requirement | BlueDogRequirementVerification::EnvelopeTransitionVerification |
| N-111 | BlueDogRequirements::wetMechanismTravel | current_gorge | requirement | BlueDogRequirementVerification::WetMechanicalIntegrityVerification |
| N-112 | BlueDogRequirements::wetJointIntegrity | current_gorge | requirement | BlueDogRequirementVerification::WetMechanicalIntegrityVerification |
| N-113 | BlueDogRequirements::wetConductorResistance | current_gorge | requirement | BlueDogRequirementVerification::WetElectricalIntegrityVerification |
| N-114 | BlueDogRequirements::wetInsulationResistance | current_gorge | requirement | BlueDogRequirementVerification::WetElectricalIntegrityVerification |
| N-115 | BlueDogRequirements::hotSunElectronicsOperation | current_gorge | requirement | BlueDogRequirementVerification::SolarHeatingVerification |
| N-116 | BlueDogRequirements::hotSunBatteryTemperature | current_gorge | requirement | BlueDogRequirementVerification::SolarHeatingVerification |
| N-117 | BlueDogRequirements::batteryChargeTemperatureInhibition | current_gorge | requirement | BlueDogRequirementVerification::SolarHeatingVerification |
| N-118 | BlueDogRequirements::rightingDeadline | current_gorge | requirement | BlueDogRequirementVerification::SelfRightingVerification |
| N-119 | BlueDogRequirements::capsizeRigRetention | current_gorge | requirement | BlueDogRequirementVerification::SelfRightingVerification |
| N-120 | BlueDogRequirements::capsizeBallastRetention | current_gorge | requirement | BlueDogRequirementVerification::SelfRightingVerification |
| N-121 | BlueDogRequirements::capsizeElectronicsSealing | current_gorge | requirement | BlueDogRequirementVerification::SelfRightingVerification |
| N-122 | BlueDogRequirements::controlRecoveryDeadline | current_gorge | requirement | BlueDogRequirementVerification::CapsizeControlRecoveryVerification |
| N-123 | BlueDogRequirements::capsizeGateProgressRetention | current_gorge | requirement | BlueDogRequirementVerification::CapsizeControlRecoveryVerification |
| N-124 | BlueDogRequirements::capsizeQualificationRetention | current_gorge | requirement | BlueDogRequirementVerification::CapsizeControlRecoveryVerification |
| N-125 | BlueDogRequirements::capsizeRestrictionRetention | current_gorge | requirement | BlueDogRequirementVerification::CapsizeControlRecoveryVerification |
| N-126 | BlueDogRequirements::weedPassageSpeed | current_gorge | requirement | BlueDogRequirementVerification::SubmergedWeedPassageVerification |
| N-127 | BlueDogRequirements::weedPassageSteering | current_gorge | requirement | BlueDogRequirementVerification::SubmergedWeedPassageVerification |
| N-128 | BlueDogRequirements::weedSnagSpeedRecovery | current_gorge | requirement | BlueDogRequirementVerification::WeedSnagSheddingVerification |
| N-129 | BlueDogRequirements::weedSnagSteeringRecovery | current_gorge | requirement | BlueDogRequirementVerification::WeedSnagSheddingVerification |
| N-130 | BlueDogRequirements::weedBlockageFault | current_gorge | requirement | BlueDogRequirementVerification::WeedBlockageResponseVerification |
| N-131 | BlueDogRequirements::weedBlockageContingency | current_gorge | requirement | BlueDogRequirementVerification::WeedBlockageResponseVerification |
| N-132 | BlueDogRequirements::weedBlockageLocation | current_gorge | requirement | BlueDogRequirementVerification::WeedBlockageResponseVerification |
| N-133 | BlueDogRequirements::poweredWeedSpeed | current_gorge | requirement | BlueDogRequirementVerification::RecoveryPropulsorWeedsVerification |
| N-134 | BlueDogRequirements::poweredWeedCurrent | current_gorge | requirement | BlueDogRequirementVerification::RecoveryPropulsorWeedsVerification |
| N-135 | BlueDogRequirements::poweredWeedTemperature | current_gorge | requirement | BlueDogRequirementVerification::RecoveryPropulsorWeedsVerification |
| N-136 | BlueDogRequirements::lockedPropulsorShutdown | current_gorge | requirement | BlueDogRequirementVerification::RecoveryPropulsorWeedsVerification |
| R-101 | BlueDogRequirements::motorQualificationInvariant | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification, BlueDogRequirementVerification::LowEnergyRecoveryVerification, BlueDogRequirementVerification::IngressResponseVerification, BlueDogRequirementVerification::EmergencyControlVerification, BlueDogRequirementVerification::EnvelopeTransitionVerification, BlueDogRequirementVerification::WeedBlockageResponseVerification, BlueDogRequirementVerification::RecoveryPropulsorWeedsVerification, BlueDogRequirementVerification::ChallengeMotorInhibitionVerification |
| R-102 | BlueDogRequirements::freshRecoveryCommand | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification, BlueDogRequirementVerification::ChallengeMotorInhibitionVerification |
| E-144 | BlueDogRequirements::ingressEventDeadline | current_gorge | requirement | BlueDogRequirementVerification::IngressResponseVerification |
| E-145 | BlueDogRequirements::qualificationRestoration | current_gorge | requirement | BlueDogRequirementVerification::ResetRecoveryVerification |
| E-200 | BlueDogRequirements::sustainedEnergyFeasibility | future_only | requirement | BlueDogEnergy::SustainedEnergyVerification |
| E-201 | BlueDogRequirements::sustainedReserveProtection | current_gorge | requirement | BlueDogRequirementVerification::SustainedReserveProtectionVerification |
| E-202 | BlueDogRequirements::repeatableCycleBalance | future_only | requirement | None |
| E-203 | BlueDogRequirements::peakSupplyCapability | current_gorge | requirement | BlueDogRequirementVerification::PeakSupplyCapabilityVerification |
| E-204 | BlueDogRequirements::harvestCampaignCoverage | future_only | requirement | None |
| E-205 | BlueDogRequirements::energyEvidenceReadiness | current_gorge | requirement | BlueDogRequirementVerification::EnergyEvidenceReadinessVerification |
| Q-001 | BlueDogRequirements::cruisePerformance | current_gorge | requirement | BlueDogRequirementVerification::MissionCapabilityVerification |
| Q-101 | BlueDogRequirements::legProgress | current_gorge | requirement | BlueDogRequirementVerification::MissionPerformanceAssessmentVerification |
| Q-102 | BlueDogRequirements::passageDuration | current_gorge | requirement | BlueDogReliability::PassageDurationVerification |
| Q-103 | BlueDogRequirements::cruiseEvidence | current_gorge | requirement | BlueDogRequirementVerification::MissionPerformanceAssessmentVerification |
| L-001 | BlueDogRequirements::missionReliability | current_gorge | requirement | BlueDogRequirementVerification::MissionCapabilityVerification |
| L-101 | BlueDogRequirements::missionSuccessProbability | current_gorge | study_objective | BlueDogReliability::VoyageReliabilityVerification |
| L-102 | BlueDogRequirements::failureRateBudget | current_gorge | study_objective | BlueDogReliability::VoyageReliabilityVerification |
| L-103 | BlueDogRequirements::reliabilityEvidence | current_gorge | requirement | BlueDogRequirementVerification::ReliabilityEvidenceVerification |
| L-104 | BlueDogRequirements::criticalFailureDisposition | current_gorge | requirement | BlueDogRequirementVerification::FailureDispositionVerification |
| E-009 | BlueDogRequirements::windObservation | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| E-146 | BlueDogRequirements::windSampleCadence | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| E-147 | BlueDogRequirements::windSpeedAccuracy | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| E-148 | BlueDogRequirements::windDirectionAccuracy | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| E-149 | BlueDogRequirements::windStaleInvalidation | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| E-150 | BlueDogRequirements::invalidWindUseInhibition | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| E-151 | BlueDogRequirements::windLossResponse | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| E-152 | BlueDogRequirements::windSensingEndurance | current_gorge | requirement | BlueDogRequirementVerification::WindObservationVerification |
| N-004 | BlueDogRequirements::vegetationResilience | current_gorge | requirement | BlueDogRequirementVerification::VegetationResilienceVerification |
| T-001 | BlueDogStructure::hybridConstruction | current_gorge | requirement | BlueDogRequirementVerification::ConstructionArchitectureVerification |
| T-100 | BlueDogStructure::structuralIntegrity | current_gorge | requirement | BlueDogRequirementVerification::StructuralLoadEvidence |
| T-101 | BlueDogStructure::bendingStrength | current_gorge | requirement | BlueDogRequirementVerification::StructuralLoadEvidence |
| T-102 | BlueDogStructure::appendageDeflection | current_gorge | requirement | BlueDogRequirementVerification::FunctionalDeformationEvidence |
| T-103 | BlueDogStructure::hullDeflection | current_gorge | requirement | BlueDogRequirementVerification::FunctionalDeformationEvidence |
| T-104 | BlueDogStructure::panelStrength | current_gorge | requirement | BlueDogRequirementVerification::StructuralLoadEvidence |
| T-105 | BlueDogStructure::panelDeflection | current_gorge | requirement | BlueDogRequirementVerification::FunctionalDeformationEvidence |
| T-106 | BlueDogStructure::rootProofLoad | current_gorge | requirement | BlueDogRequirementVerification::StructuralLoadEvidence |
| T-107 | BlueDogStructure::wetCouponStrength | current_gorge | requirement | BlueDogRequirementVerification::StructuralMaterialEvidence |
| T-108 | BlueDogStructure::wetCouponStiffness | current_gorge | requirement | BlueDogRequirementVerification::StructuralMaterialEvidence |
| T-109 | BlueDogStructure::bondProof | current_gorge | requirement | BlueDogRequirementVerification::StructuralLoadEvidence |
| T-110 | BlueDogStructure::loadedFreeboard | current_gorge | requirement | BlueDogRequirementVerification::FlotationEvidence |
| T-111 | BlueDogStructure::reserveBuoyancy | current_gorge | requirement | BlueDogRequirementVerification::FlotationEvidence |
| T-112 | BlueDogStructure::launchClearance | current_gorge | requirement | BlueDogRequirementVerification::LaunchSiteEvidence |
| T-113 | BlueDogStructure::printTileEnvelope | current_gorge | requirement | BlueDogRequirementVerification::StructuralPrintEnvelope |

## Native impact queries

- `GorgeChallenge::capsizeRecovery` — derivation incoming, depth 2: `GorgeChallenge::noLittering`, `GorgeChallenge::transGorgeChallenge`
- `BlueDogRequirements::recoveryEnergy` — verification incoming, depth 2: `BlueDogRequirementVerification::RecoveryEnergyVerification`
- `BlueDogRequirements::capsizeQualificationRetention` — verification incoming, depth 2: `BlueDogRequirementVerification::CapsizeControlRecoveryVerification`
- `BlueDogRequirements::capsizeQualificationRetention` — satisfaction incoming, depth 2: `BlueDogLogicalArchitecture::LogicalVessel::supervision`
- `BlueDogRequirements::emergencyControl` — satisfaction incoming, depth 2: `BlueDog::Architecture::MissionContext::boat`
- `BlueDogLogicalArchitecture::LogicalVessel::supervision` — allocation outgoing, depth 2: `BlueDogPhysicalArchitecture::IC01Candidate::primaryController`, `BlueDogPhysicalArchitecture::IC01Candidate::recoveryController`

## Checks requiring action

No missing current objective or malformed governing derivation found.

The JSON companion contains every queried derivation and dependency, its native endpoints and declared rationale. Empty rationale remains visible for engineering review; this tool does not certify semantic validity from graph shape.
