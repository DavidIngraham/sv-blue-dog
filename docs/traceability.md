# Use-case and architecture traceability

Use-case objectives subset the referenced requirements. Satisfy relationships express intended design allocations, not verified compliance; criteria and evidence remain open.

## Use-case objectives

| name | documentation | Requirement |
| --- | --- | --- |
| prepare | Prepare and launch. | transportability |
| sailGorge | Complete Gorge challenge. | roundTrip |
| sailOcean | Sail to Hawaii. | hawaiiVoyage |
| monitor | Monitor live and reconnect. | telemetryEquipment |
| recover | Abort and recover. | safeRecovery |
| maintain | Manufacture and service. | serviceability |
| avoidTraffic | Detect AIS and non-AIS traffic, assess collision risk, maneuver, and monitor separation without depending on operator intervention or cooperation by the other vessel. | trafficSafety |
| presentNavigationSignals | Present mode-appropriate navigation signals to other vessels during sailing, powered recovery and stationary operation. | navigationConspicuity |

## Architecture satisfaction allocations

| name | Design element |
| --- | --- |
| roundTrip | boat |
| multiDayEndurance | boat |
| energyAwareness | powerManagement |
| navigationAndControl | boat |
| resetRecovery | boat |
| lowEnergyRecovery | boat |
| communications | boat |
| ingressResponse | boat |
| missionEvidence | boat |
| transportability | handling |
| desktopManufacture | printedHull |
| serviceability | enclosure |
| trafficSafety | boat |
| operatingBoundary | boundarySupervisor |
| safeRecovery | boat |
| navigationConspicuity | signaling |
| regulatoryClassification |  |
| environmentalEnvelope | boat |
| marineDurability | boat |
| stabilityAndFouling | boat |
| recoveryPropulsion | boat |
| recoveryEnergy | boat |
| telemetryEquipment | monitoringStation |
| commandIntegrity | commandGateway |
| gorgeEnvironment | boat |
| oceanEnvironment | boat |
| gorgeWind | boat |
| gorgeWaves | boat |
| gorgeCurrent | boat |
| gorgeSurvivalWind | boat |
| gorgeSurvivalWaves | boat |
| oceanWind | boat |
| oceanWaves | boat |
| oceanCurrent | boat |
| oceanSurvivalWind | boat |
| oceanSurvivalWaves | boat |
| airTemperature | boat |
| waterTemperature | boat |
| humidity | boat |
| visibility | boat |
| calmOperation | boat |
| envelopeTransition | boat |
| freshwaterExposure | boat |
| saltwaterExposure | boat |
| enclosureSealing | enclosure |
| wetMechanicalIntegrity | hullAndRig |
| wetElectricalIntegrity | communications |
| solarHeating | powerManagement |
| printedMaterialAging | printedHull |
| selfRighting | boat |
| capsizeControlRecovery | boat |
| submergedWeedPassage | boat |
| weedSnagShedding | boat |
| weedBlockageResponse | boat |
| recoveryPropulsorWeeds | boat |
| navigationAvailability | navigation |
| launchEnergyAdmission | powerManagement |
| challengeMotorInhibition | recoveryController |
| energyEstimateCadence | powerManagement |
| reserveEstimateCadence | powerManagement |
| energyEstimateAccuracy | powerManagement |
| conservativeEnergyEstimate | powerManagement |
| guidanceUpdateCadence | control |
| sailCommandCadence | actuation |
| steeringCommandCadence | actuation |
| positionAccuracy | positionAndAttitude |
| headingAccuracy | positionAndAttitude |
| restartDeadline | recoveryController |
| missionStateRestoration | control |
| gateProgressRestoration | control |
| resetRestrictionPreservation | control |
| lowEnergyEntry | powerManagement |
| lowEnergyPayloadInhibition | powerManagement |
| lowEnergyNavigationContinuity | control |
| lowEnergyCollisionContinuity | collisionAvoidance |
| lowEnergyExit | powerManagement |
| payloadRestartPermission | powerManagement |
| telemetryDeliveryCadence | communications |
| outageAutonomy | control |
| reconnectCurrentRecord | communications |
| backlogOrdering | communications |
| backlogCurrentPriority | communications |
| ingressDetection | ingressMonitor |
| ingressRecoveryRequest | recoveryController |
| ingressFlotation | hullAndRig |
| ingressElectronicsProtection | enclosure |
| ingressPositionContinuity | communications |
| periodicLogCadence | recording |
| logRetention | recording |
| criticalEventRecording | recording |
| logTimestampAccuracy | recording |
| invalidTimestampMarking | recording |
| logGapIndication | recording |
| logInterruptionDurability | recording |
| reconnectLogPreservation | recording |
| qualificationPersistence | recoveryController |
| unknownQualificationFallback | recoveryController |
| navigationValidEpochs | navigation |
| staleNavigationInvalidation | navigation |
| navigationDegradedTransition | control |
| staleNavigationUseInhibition | control |
| soloTransport | handling |
| liftMass | handling |
| setupDuration | handling |
| packDuration | handling |
| soloLaunch | handling |
| soloRetrieval | handling |
| replacementDuration | boat |
| nondestructiveService | boat |
| postServiceSealing | enclosure |
| postServiceActuation | actuation |
| trafficTracking | traffic |
| collisionAssessmentCadence | collisionAvoidance |
| avoidanceCommandDeadline | collisionAvoidance |
| trafficAwarenessFault | collisionAvoidance |
| boundaryEvaluationCadence | boundarySupervisor |
| boundaryAvoidanceDeadline | boundarySupervisor |
| boundaryAvoidanceRecording | recording |
| boundaryStartInhibition | boundarySupervisor |
| boundaryDegradedEvidence | boundarySupervisor |
| abortLatchDeadline | recoveryController |
| recoveryTelemetryCadence | communications |
| motorIsolationDeadline | motorSystem |
| isolationRestartInhibition | motorSystem |
| manualControlLossShutdown | recoveryController |
| controlLossLocationContinuity | communications |
| navigationLightPresentation | signaling |
| navigationShapePresentation | signaling |
| navigationSoundPresentation | signaling |
| signalingModeDeadline | signaling |
| signalingFaultRecording | recording |
| signalingFaultReporting | communications |
| deploymentComplianceRecord |  |
| deploymentReleaseGate |  |
| telemetryDisplayContent | monitoringStation |
| telemetryStaleIndication | monitoringStation |
| telemetryIdentityPreservation | monitoringStation |
| telemetryDuplicateSuppression | monitoringStation |
| unauthenticatedCommandRejection | commandGateway |
| replayCommandRejection | commandGateway |
| expiredCommandRejection | commandGateway |
| acceptedCommandDeadline | commandGateway |
| onboardAcknowledgmentDeadline | commandGateway |
| acknowledgmentQueueing | commandGateway |
| externalControlDisqualification | recoveryController |
| visibilityNavigationCapability | navigation |
| visibilityTrafficCapability | traffic |
| restrictedVisibilityEntry | control |
| restrictedVisibilityEvidence | recording |
| restrictedVisibilityCollisionAssessment | collisionAvoidance |
| survivalEntryDeadline | control |
| survivalTransitionRecording | recording |
| sailingResumptionDeadline | control |
| sailingResumptionInhibition | control |
| resumptionBlockEvidence | recording |
| wetMechanismTravel | hullAndRig |
| wetJointIntegrity | hullAndRig |
| wetConductorResistance | energy |
| wetInsulationResistance | energy |
| hotSunElectronicsOperation | boat |
| hotSunBatteryTemperature | storage |
| batteryChargeTemperatureInhibition | powerManagement |
| rightingDeadline | hullAndRig |
| capsizeRigRetention | hullAndRig |
| capsizeBallastRetention | keelAndBallast |
| capsizeElectronicsSealing | enclosure |
| controlRecoveryDeadline | control |
| capsizeGateProgressRetention | missionManager |
| capsizeQualificationRetention | recoveryController |
| capsizeRestrictionRetention | control |
| weedPassageSpeed | boat |
| weedPassageSteering | actuation |
| weedSnagSpeedRecovery | boat |
| weedSnagSteeringRecovery | actuation |
| weedBlockageFault | recording |
| weedBlockageContingency | control |
| weedBlockageLocation | communications |
| poweredWeedSpeed | motorSystem |
| poweredWeedCurrent | motorSystem |
| poweredWeedTemperature | motorSystem |
| lockedPropulsorShutdown | motorSystem |
| motorQualificationInvariant | recoveryController |
| freshRecoveryCommand | recoveryController |
| ingressEventDeadline | recording |
| qualificationRestoration | recoveryController |
| sustainedEnergyFeasibility | energy |
| sustainedReserveProtection | energy |
| repeatableCycleBalance | energy |
| peakSupplyCapability | energy |
| harvestCampaignCoverage |  |
| energyEvidenceReadiness |  |
| cruisePerformance | boat |
| legProgress | boat |
| passageDuration | boat |
| cruiseEvidence |  |
| missionReliability | boat |
| missionSuccessProbability | boat |
| failureRateBudget | boat |
| reliabilityEvidence |  |
| criticalFailureDisposition |  |
