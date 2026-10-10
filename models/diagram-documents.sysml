package BlueDogDiagramDocuments {
    private import DocumentQueries::*;
    calc def Statements1 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::transGorgeChallenge", "GorgeChallenge::courseCompletion", "GorgeChallenge::repeatedOperation", "GorgeChallenge::unassistedAttempt", "GorgeChallenge::sailingPropulsion", "GorgeChallenge::liveObservation", "GorgeChallenge::emergencyIntervention")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements2 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::courseCompletion", "BlueDogRequirements::roundTrip")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements3 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::repeatedOperation", "BlueDogRequirements::multiDayEndurance", "BlueDogRequirements::serviceability", "BlueDogRequirements::sustainedEnergyFeasibility", "BlueDogRequirements::missionReliability")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements4 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::unassistedAttempt", "BlueDogRequirements::navigationAndControl", "BlueDogRequirements::challengeMotorInhibition", "BlueDogRequirements::commandIntegrity")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements5 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::sailingPropulsion", "BlueDogRequirements::roundTrip", "BlueDogRequirements::challengeMotorInhibition")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements6 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::liveObservation", "BlueDogRequirements::communications")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements7 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::emergencyIntervention", "BlueDogRequirements::communications", "BlueDogRequirements::safeRecovery", "BlueDogRequirements::commandIntegrity")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements8 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDog::Goals::hawaiiVoyage", "BlueDogRequirements::multiDayEndurance", "BlueDogRequirements::navigationAndControl", "BlueDogRequirements::communications", "BlueDogRequirements::resetRecovery", "BlueDogRequirements::missionEvidence", "BlueDogRequirements::environmentalEnvelope", "BlueDogRequirements::oceanEnvironment", "BlueDogRequirements::operatingBoundary", "BlueDogRequirements::regulatoryClassification", "BlueDogRequirements::serviceability", "BlueDogRequirements::sustainedEnergyFeasibility", "BlueDogRequirements::cruisePerformance", "BlueDogRequirements::missionReliability")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements9 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::roundTrip", "BlueDogRequirements::navigationAndControl", "BlueDogRequirements::resetRecovery", "BlueDogRequirements::communications", "BlueDogRequirements::ingressResponse", "BlueDogRequirements::missionEvidence", "BlueDogRequirements::transportability", "BlueDogRequirements::desktopManufacture", "BlueDogRequirements::operatingBoundary", "BlueDogRequirements::regulatoryClassification", "BlueDogRequirements::environmentalEnvelope", "BlueDogRequirements::gorgeEnvironment", "BlueDogRequirements::cruisePerformance", "BlueDogRequirements::missionReliability")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements10 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::multiDayEndurance", "BlueDogRequirements::energyAwareness", "BlueDogRequirements::lowEnergyRecovery", "BlueDogRequirements::sustainedReserveProtection", "BlueDogRequirements::peakSupplyCapability", "BlueDogRequirements::harvestCampaignCoverage", "BlueDogRequirements::energyEvidenceReadiness")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements11 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::energyAwareness", "BlueDogRequirements::lowEnergyRecovery", "BlueDogRequirements::energyEstimateCadence", "BlueDogRequirements::reserveEstimateCadence", "BlueDogRequirements::energyEstimateAccuracy", "BlueDogRequirements::conservativeEnergyEstimate")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements12 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::navigationAndControl", "BlueDogRequirements::trafficSafety", "BlueDogRequirements::navigationAvailability", "BlueDogRequirements::guidanceUpdateCadence", "BlueDogRequirements::sailCommandCadence", "BlueDogRequirements::steeringCommandCadence", "BlueDogRequirements::positionAccuracy", "BlueDogRequirements::headingAccuracy")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements13 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::trafficSafety", "BlueDogRequirements::navigationConspicuity", "BlueDogRequirements::trafficTracking", "BlueDogRequirements::collisionAssessmentCadence", "BlueDogRequirements::avoidanceCommandDeadline", "BlueDogRequirements::trafficAwarenessFault")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements14 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::environmentalEnvelope", "BlueDogRequirements::marineDurability", "BlueDogRequirements::stabilityAndFouling", "BlueDogRequirements::airTemperature", "BlueDogRequirements::waterTemperature", "BlueDogRequirements::humidity", "BlueDogRequirements::visibility", "BlueDogRequirements::calmOperation", "BlueDogRequirements::envelopeTransition")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements15 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::safeRecovery", "BlueDogRequirements::recoveryPropulsion", "BlueDogRequirements::abortLatchDeadline", "BlueDogRequirements::recoveryTelemetryCadence", "BlueDogRequirements::motorIsolationDeadline", "BlueDogRequirements::isolationRestartInhibition", "BlueDogRequirements::manualControlLossShutdown", "BlueDogRequirements::controlLossLocationContinuity", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::motorQualificationInvariant", "BlueDogRequirements::periodicLogCadence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements16 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::recoveryPropulsion", "BlueDogRequirements::recoveryEnergy", "BlueDogRequirements::recoveryPropulsorWeeds")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements17 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::communications", "BlueDogRequirements::telemetryEquipment", "BlueDogRequirements::commandIntegrity", "BlueDogRequirements::telemetryDeliveryCadence", "BlueDogRequirements::outageAutonomy", "BlueDogRequirements::reconnectCurrentRecord", "BlueDogRequirements::backlogOrdering", "BlueDogRequirements::backlogCurrentPriority", "BlueDogRequirements::logRetention", "BlueDogRequirements::reconnectLogPreservation")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements18 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::gorgeEnvironment", "BlueDogRequirements::gorgeWind", "BlueDogRequirements::gorgeWaves", "BlueDogRequirements::gorgeCurrent", "BlueDogRequirements::gorgeSurvivalWind", "BlueDogRequirements::gorgeSurvivalWaves", "BlueDogRequirements::freshwaterExposure", "BlueDogRequirements::submergedWeedPassage", "BlueDogRequirements::weedSnagShedding")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements19 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::oceanEnvironment", "BlueDogRequirements::oceanWind", "BlueDogRequirements::oceanWaves", "BlueDogRequirements::oceanCurrent", "BlueDogRequirements::oceanSurvivalWind", "BlueDogRequirements::oceanSurvivalWaves", "BlueDogRequirements::saltwaterExposure")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements20 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::marineDurability", "BlueDogRequirements::freshwaterExposure", "BlueDogRequirements::saltwaterExposure", "BlueDogRequirements::enclosureSealing", "BlueDogRequirements::wetMechanicalIntegrity", "BlueDogRequirements::wetElectricalIntegrity", "BlueDogRequirements::solarHeating", "BlueDogRequirements::printedMaterialAging")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements21 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::stabilityAndFouling", "BlueDogRequirements::selfRighting", "BlueDogRequirements::capsizeControlRecovery", "BlueDogRequirements::submergedWeedPassage", "BlueDogRequirements::weedSnagShedding", "BlueDogRequirements::weedBlockageResponse", "BlueDogRequirements::recoveryPropulsorWeeds")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements22 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::recoveryEnergy", "BlueDogRequirements::launchEnergyAdmission", "BlueDogRequirements::sustainedReserveProtection")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements23 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::resetRecovery", "BlueDogRequirements::restartDeadline", "BlueDogRequirements::missionStateRestoration", "BlueDogRequirements::gateProgressRestoration", "BlueDogRequirements::resetRestrictionPreservation", "BlueDogRequirements::qualificationRestoration", "BlueDogRequirements::logInterruptionDurability", "BlueDogRequirements::unknownQualificationFallback", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::freshRecoveryCommand", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements24 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::lowEnergyRecovery", "BlueDogRequirements::lowEnergyEntry", "BlueDogRequirements::lowEnergyPayloadInhibition", "BlueDogRequirements::lowEnergyNavigationContinuity", "BlueDogRequirements::lowEnergyCollisionContinuity", "BlueDogRequirements::lowEnergyExit", "BlueDogRequirements::payloadRestartPermission", "BlueDogRequirements::periodicLogCadence", "BlueDogRequirements::telemetryDeliveryCadence", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements25 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::ingressResponse", "BlueDogRequirements::ingressDetection", "BlueDogRequirements::ingressRecoveryRequest", "BlueDogRequirements::ingressFlotation", "BlueDogRequirements::ingressElectronicsProtection", "BlueDogRequirements::ingressPositionContinuity", "BlueDogRequirements::ingressEventDeadline", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements26 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::missionEvidence", "BlueDogRequirements::periodicLogCadence", "BlueDogRequirements::logRetention", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::logTimestampAccuracy", "BlueDogRequirements::invalidTimestampMarking", "BlueDogRequirements::logGapIndication", "BlueDogRequirements::logInterruptionDurability", "BlueDogRequirements::reconnectLogPreservation", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::unknownQualificationFallback")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements27 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::navigationAvailability", "BlueDogRequirements::navigationValidEpochs", "BlueDogRequirements::staleNavigationInvalidation", "BlueDogRequirements::navigationDegradedTransition", "BlueDogRequirements::staleNavigationUseInhibition", "BlueDogRequirements::criticalEventRecording")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements28 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::transportability", "BlueDogRequirements::soloTransport", "BlueDogRequirements::liftMass", "BlueDogRequirements::setupDuration", "BlueDogRequirements::packDuration", "BlueDogRequirements::soloLaunch", "BlueDogRequirements::soloRetrieval")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements29 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::serviceability", "BlueDogRequirements::replacementDuration", "BlueDogRequirements::nondestructiveService", "BlueDogRequirements::postServiceSealing", "BlueDogRequirements::postServiceActuation")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements30 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::operatingBoundary", "BlueDogRequirements::boundaryEvaluationCadence", "BlueDogRequirements::boundaryAvoidanceDeadline", "BlueDogRequirements::boundaryAvoidanceRecording", "BlueDogRequirements::boundaryStartInhibition", "BlueDogRequirements::boundaryDegradedEvidence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements31 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::navigationConspicuity", "BlueDogRequirements::navigationLightPresentation", "BlueDogRequirements::navigationShapePresentation", "BlueDogRequirements::navigationSoundPresentation", "BlueDogRequirements::signalingModeDeadline", "BlueDogRequirements::signalingFaultRecording", "BlueDogRequirements::signalingFaultReporting")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements32 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::regulatoryClassification", "BlueDogRequirements::deploymentComplianceRecord", "BlueDogRequirements::deploymentReleaseGate")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements33 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::telemetryEquipment", "BlueDogRequirements::telemetryDisplayContent", "BlueDogRequirements::telemetryStaleIndication", "BlueDogRequirements::telemetryIdentityPreservation", "BlueDogRequirements::telemetryDuplicateSuppression")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements34 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::commandIntegrity", "BlueDogRequirements::unauthenticatedCommandRejection", "BlueDogRequirements::replayCommandRejection", "BlueDogRequirements::expiredCommandRejection", "BlueDogRequirements::acceptedCommandDeadline", "BlueDogRequirements::onboardAcknowledgmentDeadline", "BlueDogRequirements::acknowledgmentQueueing", "BlueDogRequirements::externalControlDisqualification", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::qualificationPersistence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements35 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::visibility", "BlueDogRequirements::visibilityNavigationCapability", "BlueDogRequirements::visibilityTrafficCapability", "BlueDogRequirements::restrictedVisibilityEntry", "BlueDogRequirements::restrictedVisibilityEvidence", "BlueDogRequirements::restrictedVisibilityCollisionAssessment")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements36 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::envelopeTransition", "BlueDogRequirements::survivalEntryDeadline", "BlueDogRequirements::survivalTransitionRecording", "BlueDogRequirements::sailingResumptionDeadline", "BlueDogRequirements::sailingResumptionInhibition", "BlueDogRequirements::resumptionBlockEvidence", "BlueDogRequirements::periodicLogCadence", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements37 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::wetMechanicalIntegrity", "BlueDogRequirements::wetMechanismTravel", "BlueDogRequirements::wetJointIntegrity")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements38 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::wetElectricalIntegrity", "BlueDogRequirements::wetConductorResistance", "BlueDogRequirements::wetInsulationResistance")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements39 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::solarHeating", "BlueDogRequirements::hotSunElectronicsOperation", "BlueDogRequirements::hotSunBatteryTemperature", "BlueDogRequirements::batteryChargeTemperatureInhibition")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements40 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::selfRighting", "BlueDogRequirements::rightingDeadline", "BlueDogRequirements::capsizeRigRetention", "BlueDogRequirements::capsizeBallastRetention", "BlueDogRequirements::capsizeElectronicsSealing")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements41 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::capsizeControlRecovery", "BlueDogRequirements::controlRecoveryDeadline", "BlueDogRequirements::capsizeGateProgressRetention", "BlueDogRequirements::capsizeQualificationRetention", "BlueDogRequirements::capsizeRestrictionRetention")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements42 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::submergedWeedPassage", "BlueDogRequirements::weedPassageSpeed", "BlueDogRequirements::weedPassageSteering")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements43 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::weedSnagShedding", "BlueDogRequirements::weedSnagSpeedRecovery", "BlueDogRequirements::weedSnagSteeringRecovery")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements44 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::weedBlockageResponse", "BlueDogRequirements::weedBlockageFault", "BlueDogRequirements::weedBlockageContingency", "BlueDogRequirements::weedBlockageLocation", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements45 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::recoveryPropulsorWeeds", "BlueDogRequirements::poweredWeedSpeed", "BlueDogRequirements::poweredWeedCurrent", "BlueDogRequirements::poweredWeedTemperature", "BlueDogRequirements::lockedPropulsorShutdown", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements46 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::challengeMotorInhibition", "BlueDogRequirements::motorQualificationInvariant", "BlueDogRequirements::freshRecoveryCommand", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::criticalEventRecording")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def Statements47 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::sustainedEnergyFeasibility", "BlueDogRequirements::sustainedReserveProtection", "BlueDogRequirements::repeatableCycleBalance", "BlueDogRequirements::peakSupplyCapability", "BlueDogRequirements::energyEvidenceReadiness")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }

    part def ArchitectureDiagram :> Document {
        attribute redefines title = "Boat definition and composition";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::architecture;
        }
    }
    part def ContextDiagram :> Document {
        attribute redefines title = "Mission context";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::context;
        }
    }
    part def DetailDiagram :> Document {
        attribute redefines title = "Detailed composition";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::detail;
        }
    }
    part def UseCasesDiagram :> Document {
        attribute redefines title = "Use cases and requirements";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogUseCaseViews::operations;
        }
    }
    part def TransGorgeChallengeRequirements :> Document {
        attribute redefines title = "C-000 trans gorge challenge";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements1;
        }
        part group1 : Section {
            attribute redefines title = "C-000 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::transGorgeChallenge1;
            }
        }
        part group2 : Section {
            attribute redefines title = "C-000 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::transGorgeChallenge2;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-001 course completion"; attribute redefines target = "requirements-c-001.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-002 repeated operation"; attribute redefines target = "requirements-c-002.md"; }
        }
        part next2 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-003 unassisted attempt"; attribute redefines target = "requirements-c-003.md"; }
        }
        part next3 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-004 sailing propulsion"; attribute redefines target = "requirements-c-004.md"; }
        }
        part next4 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-005 live observation"; attribute redefines target = "requirements-c-005.md"; }
        }
        part next5 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-006 emergency intervention"; attribute redefines target = "requirements-c-006.md"; }
        }
    }
    part def CourseCompletionRequirements :> Document {
        attribute redefines title = "C-001 course completion";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements2;
        }
        part group1 : Section {
            attribute redefines title = "C-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::courseCompletion1;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: M-001 round trip"; attribute redefines target = "requirements-m-001.md"; }
        }
    }
    part def RepeatedOperationRequirements :> Document {
        attribute redefines title = "C-002 repeated operation";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements3;
        }
        part group1 : Section {
            attribute redefines title = "C-002 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::repeatedOperation1;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: M-002 multi day endurance"; attribute redefines target = "requirements-m-002.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: P-003 serviceability"; attribute redefines target = "requirements-p-003.md"; }
        }
        part next2 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-200 sustained energy feasibility"; attribute redefines target = "requirements-e-200.md"; }
        }
            part group2 : Section { attribute redefines title = "C-002 derivation 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::repeatedOperation2; } }
        part continueMissionReliability : Paragraph { part link : Link { attribute redefines text = "Continue: L-001 missionReliability"; attribute redefines target = "requirements-l-001.md"; } }
}
    part def UnassistedAttemptRequirements :> Document {
        attribute redefines title = "C-003 unassisted attempt";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements4;
        }
        part group1 : Section {
            attribute redefines title = "C-003 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::unassistedAttempt1;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-002 navigation and control"; attribute redefines target = "requirements-e-002.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: R-004 challenge motor inhibition"; attribute redefines target = "requirements-r-004.md"; }
        }
        part next2 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-102 command integrity"; attribute redefines target = "requirements-c-102.md"; }
        }
    }
    part def SailingPropulsionRequirements :> Document {
        attribute redefines title = "C-004 sailing propulsion";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements5;
        }
        part group1 : Section {
            attribute redefines title = "C-004 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::sailingPropulsion1;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: M-001 round trip"; attribute redefines target = "requirements-m-001.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: R-004 challenge motor inhibition"; attribute redefines target = "requirements-r-004.md"; }
        }
    }
    part def LiveObservationRequirements :> Document {
        attribute redefines title = "C-005 live observation";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements6;
        }
        part group1 : Section {
            attribute redefines title = "C-005 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::liveObservation1;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-005 communications"; attribute redefines target = "requirements-e-005.md"; }
        }
    }
    part def EmergencyInterventionRequirements :> Document {
        attribute redefines title = "C-006 emergency intervention";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements7;
        }
        part group1 : Section {
            attribute redefines title = "C-006 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::emergencyIntervention1;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-005 communications"; attribute redefines target = "requirements-e-005.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: S-003 safe recovery"; attribute redefines target = "requirements-s-003.md"; }
        }
        part next2 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-102 command integrity"; attribute redefines target = "requirements-c-102.md"; }
        }
    }
    part def HawaiiVoyageRequirements :> Document {
        attribute redefines title = "H-001 hawaii voyage";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements8;
        }
        part group1 : Section {
            attribute redefines title = "H-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::hawaiiVoyage1;
            }
        }
        part group2 : Section {
            attribute redefines title = "H-001 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::hawaiiVoyage2;
            }
        }
        part group3 : Section {
            attribute redefines title = "H-001 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::hawaiiVoyage3;
            }
        }
        part group4 : Section {
            attribute redefines title = "H-001 derivation 4";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::hawaiiVoyage4;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: M-002 multi day endurance"; attribute redefines target = "requirements-m-002.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-002 navigation and control"; attribute redefines target = "requirements-e-002.md"; }
        }
        part next2 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-005 communications"; attribute redefines target = "requirements-e-005.md"; }
        }
        part next3 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-003 reset recovery"; attribute redefines target = "requirements-e-003.md"; }
        }
        part next4 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-007 mission evidence"; attribute redefines target = "requirements-e-007.md"; }
        }
        part next5 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-001 environmental envelope"; attribute redefines target = "requirements-n-001.md"; }
        }
        part next6 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-020 ocean environment"; attribute redefines target = "requirements-n-020.md"; }
        }
        part next7 : Paragraph {
            part next : Link { attribute redefines text = "Continue: S-002 operating boundary"; attribute redefines target = "requirements-s-002.md"; }
        }
        part next8 : Paragraph {
            part next : Link { attribute redefines text = "Continue: S-005 regulatory classification"; attribute redefines target = "requirements-s-005.md"; }
        }
        part next9 : Paragraph {
            part next : Link { attribute redefines text = "Continue: P-003 serviceability"; attribute redefines target = "requirements-p-003.md"; }
        }
        part next10 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-200 sustained energy feasibility"; attribute redefines target = "requirements-e-200.md"; }
        }
            part group5 : Section { attribute redefines title = "H-001 derivation 5"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::hawaiiVoyage5; } }
        part continueCruisePerformance : Paragraph { part link : Link { attribute redefines text = "Continue: Q-001 cruisePerformance"; attribute redefines target = "requirements-q-001.md"; } }
        part continueMissionReliability : Paragraph { part link : Link { attribute redefines text = "Continue: L-001 missionReliability"; attribute redefines target = "requirements-l-001.md"; } }
}
    part def RoundTripRequirements :> Document {
        attribute redefines title = "M-001 round trip";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements9;
        }
        part group1 : Section {
            attribute redefines title = "M-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::roundTrip1;
            }
        }
        part group2 : Section {
            attribute redefines title = "M-001 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::roundTrip2;
            }
        }
        part group3 : Section {
            attribute redefines title = "M-001 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::roundTrip3;
            }
        }
        part group4 : Section {
            attribute redefines title = "M-001 derivation 4";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::roundTrip4;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-002 navigation and control"; attribute redefines target = "requirements-e-002.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-003 reset recovery"; attribute redefines target = "requirements-e-003.md"; }
        }
        part next2 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-005 communications"; attribute redefines target = "requirements-e-005.md"; }
        }
        part next3 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-006 ingress response"; attribute redefines target = "requirements-e-006.md"; }
        }
        part next4 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-007 mission evidence"; attribute redefines target = "requirements-e-007.md"; }
        }
        part next5 : Paragraph {
            part next : Link { attribute redefines text = "Continue: P-001 transportability"; attribute redefines target = "requirements-p-001.md"; }
        }
        part next7 : Paragraph {
            part next : Link { attribute redefines text = "Continue: S-002 operating boundary"; attribute redefines target = "requirements-s-002.md"; }
        }
        part next8 : Paragraph {
            part next : Link { attribute redefines text = "Continue: S-005 regulatory classification"; attribute redefines target = "requirements-s-005.md"; }
        }
        part next9 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-001 environmental envelope"; attribute redefines target = "requirements-n-001.md"; }
        }
        part next10 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-010 gorge environment"; attribute redefines target = "requirements-n-010.md"; }
        }
            part group5 : Section { attribute redefines title = "M-001 derivation 5"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::roundTrip5; } }
        part continueCruisePerformance : Paragraph { part link : Link { attribute redefines text = "Continue: Q-001 cruisePerformance"; attribute redefines target = "requirements-q-001.md"; } }
        part continueMissionReliability : Paragraph { part link : Link { attribute redefines text = "Continue: L-001 missionReliability"; attribute redefines target = "requirements-l-001.md"; } }
}
    part def MultiDayEnduranceRequirements :> Document {
        attribute redefines title = "M-002 multi day endurance";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements10;
        }
        part group1 : Section {
            attribute redefines title = "M-002 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::multiDayEndurance1;
            }
        }
        part group2 : Section {
            attribute redefines title = "M-002 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::multiDayEndurance2;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-001 energy awareness"; attribute redefines target = "requirements-e-001.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-004 low energy recovery"; attribute redefines target = "requirements-e-004.md"; }
        }
    }
    part def EnergyAwarenessRequirements :> Document {
        attribute redefines title = "E-001 energy awareness";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements11;
        }
        part group1 : Section {
            attribute redefines title = "E-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::energyAwareness1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-001 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::energyAwareness2;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-004 low energy recovery"; attribute redefines target = "requirements-e-004.md"; }
        }
    }
    part def NavigationAndControlRequirements :> Document {
        attribute redefines title = "E-002 navigation and control";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements12;
        }
        part group1 : Section {
            attribute redefines title = "E-002 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::navigationAndControl1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-002 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::navigationAndControl2;
            }
        }
        part group3 : Section {
            attribute redefines title = "E-002 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::navigationAndControl3;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: S-001 traffic safety"; attribute redefines target = "requirements-s-001.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: E-008 navigation availability"; attribute redefines target = "requirements-e-008.md"; }
        }
    }
    part def TrafficSafetyRequirements :> Document {
        attribute redefines title = "S-001 traffic safety";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements13;
        }
        part group1 : Section {
            attribute redefines title = "S-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::trafficSafety1;
            }
        }
        part group2 : Section {
            attribute redefines title = "S-001 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::trafficSafety2;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: S-004 navigation conspicuity"; attribute redefines target = "requirements-s-004.md"; }
        }
    }
    part def EnvironmentalEnvelopeRequirements :> Document {
        attribute redefines title = "N-001 environmental envelope";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements14;
        }
        part group1 : Section {
            attribute redefines title = "N-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::environmentalEnvelope1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-001 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::environmentalEnvelope2;
            }
        }
        part group3 : Section {
            attribute redefines title = "N-001 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::environmentalEnvelope3;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-002 marine durability"; attribute redefines target = "requirements-n-002.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-003 stability and fouling"; attribute redefines target = "requirements-n-003.md"; }
        }
        part next5 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-033 visibility"; attribute redefines target = "requirements-n-033.md"; }
        }
        part next7 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-035 envelope transition"; attribute redefines target = "requirements-n-035.md"; }
        }
    }
    part def SafeRecoveryRequirements :> Document {
        attribute redefines title = "S-003 safe recovery";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements15;
        }
        part group1 : Section {
            attribute redefines title = "S-003 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::safeRecovery1;
            }
        }
        part group2 : Section {
            attribute redefines title = "S-003 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::safeRecovery2;
            }
        }
        part group3 : Section {
            attribute redefines title = "S-003 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::safeRecovery3;
            }
        }
        part group4 : Section {
            attribute redefines title = "S-003 derivation 4";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::safeRecovery4;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: R-001 recovery propulsion"; attribute redefines target = "requirements-r-001.md"; }
        }
    }
    part def RecoveryPropulsionRequirements :> Document {
        attribute redefines title = "R-001 recovery propulsion";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements16;
        }
        part group1 : Section {
            attribute redefines title = "R-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::recoveryPropulsion1;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: R-002 recovery energy"; attribute redefines target = "requirements-r-002.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-056 recovery propulsor weeds"; attribute redefines target = "requirements-n-056.md"; }
        }
    }
    part def CommunicationsRequirements :> Document {
        attribute redefines title = "E-005 communications";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements17;
        }
        part group1 : Section {
            attribute redefines title = "E-005 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::communications1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-005 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::communications2;
            }
        }
        part group3 : Section {
            attribute redefines title = "E-005 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::communications3;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-101 telemetry equipment"; attribute redefines target = "requirements-c-101.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: C-102 command integrity"; attribute redefines target = "requirements-c-102.md"; }
        }
    }
    part def GorgeEnvironmentRequirements :> Document {
        attribute redefines title = "N-010 gorge environment";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements18;
        }
        part group1 : Section {
            attribute redefines title = "N-010 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::gorgeEnvironment1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-010 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::gorgeEnvironment2;
            }
        }
        part group3 : Section {
            attribute redefines title = "N-010 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::gorgeEnvironment3;
            }
        }
        part next6 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-053 submerged weed passage"; attribute redefines target = "requirements-n-053.md"; }
        }
        part next7 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-054 weed snag shedding"; attribute redefines target = "requirements-n-054.md"; }
        }
    }
    part def OceanEnvironmentRequirements :> Document {
        attribute redefines title = "N-020 ocean environment";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements19;
        }
        part group1 : Section {
            attribute redefines title = "N-020 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::oceanEnvironment1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-020 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::oceanEnvironment2;
            }
        }
    }
    part def MarineDurabilityRequirements :> Document {
        attribute redefines title = "N-002 marine durability";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements20;
        }
        part group1 : Section {
            attribute redefines title = "N-002 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::marineDurability1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-002 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::marineDurability2;
            }
        }
        part group3 : Section {
            attribute redefines title = "N-002 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::marineDurability3;
            }
        }
        part next3 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-044 wet mechanical integrity"; attribute redefines target = "requirements-n-044.md"; }
        }
        part next4 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-045 wet electrical integrity"; attribute redefines target = "requirements-n-045.md"; }
        }
        part next5 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-046 solar heating"; attribute redefines target = "requirements-n-046.md"; }
        }
    }
    part def StabilityAndFoulingRequirements :> Document {
        attribute redefines title = "N-003 stability and fouling";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements21;
        }
        part group1 : Section {
            attribute redefines title = "N-003 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::stabilityAndFouling1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-003 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::stabilityAndFouling2;
            }
        }
        part next0 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-051 self righting"; attribute redefines target = "requirements-n-051.md"; }
        }
        part next1 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-052 capsize control recovery"; attribute redefines target = "requirements-n-052.md"; }
        }
        part next2 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-053 submerged weed passage"; attribute redefines target = "requirements-n-053.md"; }
        }
        part next3 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-054 weed snag shedding"; attribute redefines target = "requirements-n-054.md"; }
        }
        part next4 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-055 weed blockage response"; attribute redefines target = "requirements-n-055.md"; }
        }
        part next5 : Paragraph {
            part next : Link { attribute redefines text = "Continue: N-056 recovery propulsor weeds"; attribute redefines target = "requirements-n-056.md"; }
        }
    }
    part def RecoveryEnergyRequirements :> Document {
        attribute redefines title = "R-002 recovery energy";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements22;
        }
        part group1 : Section {
            attribute redefines title = "R-002 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::recoveryEnergy1;
            }
        }
    }
    part def ResetRecoveryRequirements :> Document {
        attribute redefines title = "E-003 reset recovery";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements23;
        }
        part group1 : Section {
            attribute redefines title = "E-003 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::resetRecovery1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-003 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::resetRecovery2;
            }
        }
        part group3 : Section {
            attribute redefines title = "E-003 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::resetRecovery3;
            }
        }
        part group4 : Section {
            attribute redefines title = "E-003 derivation 4";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::resetRecovery4;
            }
        }
    }
    part def LowEnergyRecoveryRequirements :> Document {
        attribute redefines title = "E-004 low energy recovery";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements24;
        }
        part group1 : Section {
            attribute redefines title = "E-004 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::lowEnergyRecovery1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-004 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::lowEnergyRecovery2;
            }
        }
        part group3 : Section {
            attribute redefines title = "E-004 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::lowEnergyRecovery3;
            }
        }
        part group4 : Section {
            attribute redefines title = "E-004 derivation 4";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::lowEnergyRecovery4;
            }
        }
    }
    part def IngressResponseRequirements :> Document {
        attribute redefines title = "E-006 ingress response";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements25;
        }
        part group1 : Section {
            attribute redefines title = "E-006 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::ingressResponse1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-006 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::ingressResponse2;
            }
        }
        part group3 : Section {
            attribute redefines title = "E-006 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::ingressResponse3;
            }
        }
    }
    part def MissionEvidenceRequirements :> Document {
        attribute redefines title = "E-007 mission evidence";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements26;
        }
        part group1 : Section {
            attribute redefines title = "E-007 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::missionEvidence1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-007 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::missionEvidence2;
            }
        }
        part group3 : Section {
            attribute redefines title = "E-007 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::missionEvidence3;
            }
        }
        part group4 : Section {
            attribute redefines title = "E-007 derivation 4";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::missionEvidence4;
            }
        }
    }
    part def NavigationAvailabilityRequirements :> Document {
        attribute redefines title = "E-008 navigation availability";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements27;
        }
        part group1 : Section {
            attribute redefines title = "E-008 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::navigationAvailability1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-008 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::navigationAvailability2;
            }
        }
    }
    part def TransportabilityRequirements :> Document {
        attribute redefines title = "P-001 transportability";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements28;
        }
        part group1 : Section {
            attribute redefines title = "P-001 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::transportability1;
            }
        }
        part group2 : Section {
            attribute redefines title = "P-001 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::transportability2;
            }
        }
    }
    part def ServiceabilityRequirements :> Document {
        attribute redefines title = "P-003 serviceability";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements29;
        }
        part group1 : Section {
            attribute redefines title = "P-003 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::serviceability1;
            }
        }
        part group2 : Section {
            attribute redefines title = "P-003 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::serviceability2;
            }
        }
    }
    part def OperatingBoundaryRequirements :> Document {
        attribute redefines title = "S-002 operating boundary";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements30;
        }
        part group1 : Section {
            attribute redefines title = "S-002 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::operatingBoundary1;
            }
        }
        part group2 : Section {
            attribute redefines title = "S-002 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::operatingBoundary2;
            }
        }
    }
    part def NavigationConspicuityRequirements :> Document {
        attribute redefines title = "S-004 navigation conspicuity";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements31;
        }
        part group1 : Section {
            attribute redefines title = "S-004 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::navigationConspicuity1;
            }
        }
        part group2 : Section {
            attribute redefines title = "S-004 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::navigationConspicuity2;
            }
        }
    }
    part def RegulatoryClassificationRequirements :> Document {
        attribute redefines title = "S-005 regulatory classification";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements32;
        }
        part group1 : Section {
            attribute redefines title = "S-005 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::regulatoryClassification1;
            }
        }
    }
    part def TelemetryEquipmentRequirements :> Document {
        attribute redefines title = "C-101 telemetry equipment";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements33;
        }
        part group1 : Section {
            attribute redefines title = "C-101 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::telemetryEquipment1;
            }
        }
        part group2 : Section {
            attribute redefines title = "C-101 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::telemetryEquipment2;
            }
        }
    }
    part def CommandIntegrityRequirements :> Document {
        attribute redefines title = "C-102 command integrity";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements34;
        }
        part group1 : Section {
            attribute redefines title = "C-102 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::commandIntegrity1;
            }
        }
        part group2 : Section {
            attribute redefines title = "C-102 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::commandIntegrity2;
            }
        }
        part group3 : Section {
            attribute redefines title = "C-102 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::commandIntegrity3;
            }
        }
    }
    part def VisibilityRequirements :> Document {
        attribute redefines title = "N-033 visibility";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements35;
        }
        part group1 : Section {
            attribute redefines title = "N-033 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::visibility1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-033 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::visibility2;
            }
        }
    }
    part def EnvelopeTransitionRequirements :> Document {
        attribute redefines title = "N-035 envelope transition";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements36;
        }
        part group1 : Section {
            attribute redefines title = "N-035 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::envelopeTransition1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-035 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::envelopeTransition2;
            }
        }
        part group3 : Section {
            attribute redefines title = "N-035 derivation 3";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::envelopeTransition3;
            }
        }
    }
    part def WetMechanicalIntegrityRequirements :> Document {
        attribute redefines title = "N-044 wet mechanical integrity";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements37;
        }
        part group1 : Section {
            attribute redefines title = "N-044 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::wetMechanicalIntegrity1;
            }
        }
    }
    part def WetElectricalIntegrityRequirements :> Document {
        attribute redefines title = "N-045 wet electrical integrity";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements38;
        }
        part group1 : Section {
            attribute redefines title = "N-045 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::wetElectricalIntegrity1;
            }
        }
    }
    part def SolarHeatingRequirements :> Document {
        attribute redefines title = "N-046 solar heating";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements39;
        }
        part group1 : Section {
            attribute redefines title = "N-046 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::solarHeating1;
            }
        }
    }
    part def SelfRightingRequirements :> Document {
        attribute redefines title = "N-051 self righting";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements40;
        }
        part group1 : Section {
            attribute redefines title = "N-051 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::selfRighting1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-051 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::selfRighting2;
            }
        }
    }
    part def CapsizeControlRecoveryRequirements :> Document {
        attribute redefines title = "N-052 capsize control recovery";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements41;
        }
        part group1 : Section {
            attribute redefines title = "N-052 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::capsizeControlRecovery1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-052 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::capsizeControlRecovery2;
            }
        }
    }
    part def SubmergedWeedPassageRequirements :> Document {
        attribute redefines title = "N-053 submerged weed passage";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements42;
        }
        part group1 : Section {
            attribute redefines title = "N-053 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::submergedWeedPassage1;
            }
        }
    }
    part def WeedSnagSheddingRequirements :> Document {
        attribute redefines title = "N-054 weed snag shedding";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements43;
        }
        part group1 : Section {
            attribute redefines title = "N-054 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::weedSnagShedding1;
            }
        }
    }
    part def WeedBlockageResponseRequirements :> Document {
        attribute redefines title = "N-055 weed blockage response";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements44;
        }
        part group1 : Section {
            attribute redefines title = "N-055 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::weedBlockageResponse1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-055 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::weedBlockageResponse2;
            }
        }
    }
    part def RecoveryPropulsorWeedsRequirements :> Document {
        attribute redefines title = "N-056 recovery propulsor weeds";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements45;
        }
        part group1 : Section {
            attribute redefines title = "N-056 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::recoveryPropulsorWeeds1;
            }
        }
        part group2 : Section {
            attribute redefines title = "N-056 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::recoveryPropulsorWeeds2;
            }
        }
    }
    part def ChallengeMotorInhibitionRequirements :> Document {
        attribute redefines title = "R-004 challenge motor inhibition";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements46;
        }
        part group1 : Section {
            attribute redefines title = "R-004 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::challengeMotorInhibition1;
            }
        }
        part group2 : Section {
            attribute redefines title = "R-004 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::challengeMotorInhibition2;
            }
        }
    }
    part def SustainedEnergyFeasibilityRequirements :> Document {
        attribute redefines title = "E-200 sustained energy feasibility";
        part navigation : Paragraph {
            part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; }
        }
        part contextLink : Paragraph {
            part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; }
        }
        part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements47;
        }
        part group1 : Section {
            attribute redefines title = "E-200 derivation 1";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::sustainedEnergyFeasibility1;
            }
        }
        part group2 : Section {
            attribute redefines title = "E-200 derivation 2";
            part diagram : Diagram {
                attribute redefines direction = "BT";
                ref redefines source = BlueDogViews::sustainedEnergyFeasibility2;
            }
        }
    }
    calc def CruisePerformanceStatements :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::cruisePerformance", "BlueDogRequirements::legProgress", "BlueDogRequirements::passageDuration", "BlueDogRequirements::cruiseEvidence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def CruisePerformanceRequirements :> Document {
        attribute redefines title = "Q-001 CruisePerformance";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part contextLink : Paragraph { part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : CruisePerformanceStatements; }
            part group1 : Section { attribute redefines title = "Q-001 derivation 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::cruisePerformance1; } }
}
    calc def MissionReliabilityStatements :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::missionReliability", "BlueDogRequirements::missionSuccessProbability", "BlueDogRequirements::failureRateBudget", "BlueDogRequirements::reliabilityEvidence", "BlueDogRequirements::criticalFailureDisposition")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("name", "documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def MissionReliabilityRequirements :> Document {
        attribute redefines title = "L-001 MissionReliability";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part contextLink : Paragraph { part context : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : MissionReliabilityStatements; }
            part group1 : Section { attribute redefines title = "L-001 derivation 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionReliability1; } }
        part group2 : Section { attribute redefines title = "L-001 derivation 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionReliability2; } }
}
}
