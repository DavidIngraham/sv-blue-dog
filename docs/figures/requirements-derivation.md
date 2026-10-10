# Requirement derivation

```mermaid
---
config:
  fontFamily: "Helvetica, Arial, sans-serif"
  theme: base
  themeCSS: ".edgeLabel rect { opacity: 1 !important; } .cluster-label .nodeLabel { text-align: center; }"
  themeVariables:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "14px"
    primaryColor: "#FFFFFF"
    secondaryColor: "#FFFFFF"
    tertiaryColor: "#FFFFFF"
    background: "#FFFFFF"
    primaryBorderColor: "#181818"
    primaryTextColor: "#000000"
    lineColor: "#181818"
    textColor: "#000000"
    noteBkgColor: "#FEFFDD"
    noteBorderColor: "#181818"
    noteTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#181818"
    edgeLabelBackground: "#FFFFFF"
---
%% BlueDogViews::requirements — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 2 exposed standard library element(s) not drawn; a requirement rendering draws the model's own elements
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::transGorgeChallenge : TransGorgeChallenge**`")
  n1("`*«requirement»*
**GorgeChallenge::courseCompletion : CourseCompletion**`")
  n2("`*«requirement»*
**GorgeChallenge::repeatedOperation : RepeatedOperation**`")
  n3("`*«requirement»*
**GorgeChallenge::unassistedAttempt : UnassistedAttempt**`")
  n4("`*«requirement»*
**GorgeChallenge::sailingPropulsion : SailingPropulsion**`")
  n5("`*«requirement»*
**GorgeChallenge::liveObservation : LiveObservation**`")
  n6("`*«requirement»*
**GorgeChallenge::emergencyIntervention : EmergencyIntervention**`")
  n7("`*«requirement»*
**BlueDog::Goals::hawaiiVoyage : HawaiiVoyage**`")
  n8("`*«requirement»*
**BlueDogRequirements::roundTrip : RoundTrip**`")
  n9("`*«requirement»*
**BlueDogRequirements::multiDayEndurance : MultiDayEndurance**`")
  n10("`*«requirement»*
**BlueDogRequirements::energyAwareness : EnergyAwareness**`")
  n11("`*«requirement»*
**BlueDogRequirements::navigationAndControl : NavigationAndControl**`")
  n12("`*«requirement»*
**BlueDogRequirements::resetRecovery : ResetRecovery**`")
  n13("`*«requirement»*
**BlueDogRequirements::lowEnergyRecovery : LowEnergyRecovery**`")
  n14("`*«requirement»*
**BlueDogRequirements::communications : Communications**`")
  n15("`*«requirement»*
**BlueDogRequirements::ingressResponse : IngressResponse**`")
  n16("`*«requirement»*
**BlueDogRequirements::missionEvidence : MissionEvidence**`")
  n17("`*«requirement»*
**BlueDogRequirements::transportability : Transportability**`")
  n18("`*«requirement»*
**BlueDogRequirements::desktopManufacture : DesktopManufacture**`")
  n19("`*«requirement»*
**BlueDogRequirements::serviceability : Serviceability**`")
  n20("`*«requirement»*
**BlueDogRequirements::trafficSafety : TrafficSafety**`")
  n21("`*«requirement»*
**BlueDogRequirements::operatingBoundary : OperatingBoundary**`")
  n22("`*«requirement»*
**BlueDogRequirements::safeRecovery : SafeRecovery**`")
  n23("`*«requirement»*
**BlueDogRequirements::navigationConspicuity : NavigationConspicuity**`")
  n24("`*«requirement»*
**BlueDogRequirements::regulatoryClassification : RegulatoryClassification**`")
  n25("`*«requirement»*
**BlueDogRequirements::environmentalEnvelope : EnvironmentalEnvelope**`")
  n26("`*«requirement»*
**BlueDogRequirements::marineDurability : MarineDurability**`")
  n27("`*«requirement»*
**BlueDogRequirements::stabilityAndFouling : StabilityAndFouling**`")
  n28("`*«requirement»*
**BlueDogRequirements::recoveryPropulsion : RecoveryPropulsion**`")
  n29("`*«requirement»*
**BlueDogRequirements::recoveryEnergy : RecoveryEnergy**`")
  n30("`*«requirement»*
**BlueDogRequirements::telemetryEquipment : TelemetryEquipment**`")
  n31("`*«requirement»*
**BlueDogRequirements::commandIntegrity : CommandIntegrity**`")
  n32("`*«requirement»*
**BlueDogRequirements::gorgeEnvironment : GorgeEnvironment**`")
  n33("`*«requirement»*
**BlueDogRequirements::oceanEnvironment : OceanEnvironment**`")
  n34("`*«requirement»*
**BlueDogRequirements::gorgeWind : GorgeWind**`")
  n35("`*«requirement»*
**BlueDogRequirements::gorgeWaves : GorgeWaves**`")
  n36("`*«requirement»*
**BlueDogRequirements::gorgeCurrent : GorgeCurrent**`")
  n37("`*«requirement»*
**BlueDogRequirements::gorgeSurvivalWind : GorgeSurvivalWind**`")
  n38("`*«requirement»*
**BlueDogRequirements::gorgeSurvivalWaves : GorgeSurvivalWaves**`")
  n39("`*«requirement»*
**BlueDogRequirements::oceanWind : OceanWind**`")
  n40("`*«requirement»*
**BlueDogRequirements::oceanWaves : OceanWaves**`")
  n41("`*«requirement»*
**BlueDogRequirements::oceanCurrent : OceanCurrent**`")
  n42("`*«requirement»*
**BlueDogRequirements::oceanSurvivalWind : OceanSurvivalWind**`")
  n43("`*«requirement»*
**BlueDogRequirements::oceanSurvivalWaves : OceanSurvivalWaves**`")
  n44("`*«requirement»*
**BlueDogRequirements::airTemperature : AirTemperature**`")
  n45("`*«requirement»*
**BlueDogRequirements::waterTemperature : WaterTemperature**`")
  n46("`*«requirement»*
**BlueDogRequirements::humidity : Humidity**`")
  n47("`*«requirement»*
**BlueDogRequirements::visibility : Visibility**`")
  n48("`*«requirement»*
**BlueDogRequirements::calmOperation : CalmOperation**`")
  n49("`*«requirement»*
**BlueDogRequirements::envelopeTransition : EnvelopeTransition**`")
  n50("`*«requirement»*
**BlueDogRequirements::freshwaterExposure : FreshwaterExposure**`")
  n51("`*«requirement»*
**BlueDogRequirements::saltwaterExposure : SaltwaterExposure**`")
  n52("`*«requirement»*
**BlueDogRequirements::enclosureSealing : EnclosureSealing**`")
  n53("`*«requirement»*
**BlueDogRequirements::wetMechanicalIntegrity : WetMechanicalIntegrity**`")
  n54("`*«requirement»*
**BlueDogRequirements::wetElectricalIntegrity : WetElectricalIntegrity**`")
  n55("`*«requirement»*
**BlueDogRequirements::solarHeating : SolarHeating**`")
  n56("`*«requirement»*
**BlueDogRequirements::printedMaterialAging : PrintedMaterialAging**`")
  n57("`*«requirement»*
**BlueDogRequirements::selfRighting : SelfRighting**`")
  n58("`*«requirement»*
**BlueDogRequirements::capsizeControlRecovery : CapsizeControlRecovery**`")
  n59("`*«requirement»*
**BlueDogRequirements::submergedWeedPassage : SubmergedWeedPassage**`")
  n60("`*«requirement»*
**BlueDogRequirements::weedSnagShedding : WeedSnagShedding**`")
  n61("`*«requirement»*
**BlueDogRequirements::weedBlockageResponse : WeedBlockageResponse**`")
  n62("`*«requirement»*
**BlueDogRequirements::recoveryPropulsorWeeds : RecoveryPropulsorWeeds**`")
  n63("`*«requirement»*
**BlueDogRequirements::navigationAvailability : NavigationAvailability**`")
  n64("`*«requirement»*
**BlueDogRequirements::launchEnergyAdmission : LaunchEnergyAdmission**`")
  n65("`*«requirement»*
**BlueDogRequirements::challengeMotorInhibition : ChallengeMotorInhibition**`")
  n66("`*«requirement»*
**BlueDogRequirements::energyEstimateCadence : EnergyEstimateCadence**`")
  n67("`*«requirement»*
**BlueDogRequirements::reserveEstimateCadence : ReserveEstimateCadence**`")
  n68("`*«requirement»*
**BlueDogRequirements::energyEstimateAccuracy : EnergyEstimateAccuracy**`")
  n69("`*«requirement»*
**BlueDogRequirements::conservativeEnergyEstimate : ConservativeEnergyEstimate**`")
  n70("`*«requirement»*
**BlueDogRequirements::guidanceUpdateCadence : GuidanceUpdateCadence**`")
  n71("`*«requirement»*
**BlueDogRequirements::sailCommandCadence : SailCommandCadence**`")
  n72("`*«requirement»*
**BlueDogRequirements::steeringCommandCadence : SteeringCommandCadence**`")
  n73("`*«requirement»*
**BlueDogRequirements::positionAccuracy : PositionAccuracy**`")
  n74("`*«requirement»*
**BlueDogRequirements::headingAccuracy : HeadingAccuracy**`")
  n75("`*«requirement»*
**BlueDogRequirements::restartDeadline : RestartDeadline**`")
  n76("`*«requirement»*
**BlueDogRequirements::missionStateRestoration : MissionStateRestoration**`")
  n77("`*«requirement»*
**BlueDogRequirements::gateProgressRestoration : GateProgressRestoration**`")
  n78("`*«requirement»*
**BlueDogRequirements::resetRestrictionPreservation : ResetRestrictionPreservation**`")
  n79("`*«requirement»*
**BlueDogRequirements::lowEnergyEntry : LowEnergyEntry**`")
  n80("`*«requirement»*
**BlueDogRequirements::lowEnergyPayloadInhibition : LowEnergyPayloadInhibition**`")
  n81("`*«requirement»*
**BlueDogRequirements::lowEnergyNavigationContinuity : LowEnergyNavigationContinuity**`")
  n82("`*«requirement»*
**BlueDogRequirements::lowEnergyCollisionContinuity : LowEnergyCollisionContinuity**`")
  n83("`*«requirement»*
**BlueDogRequirements::lowEnergyExit : LowEnergyExit**`")
  n84("`*«requirement»*
**BlueDogRequirements::payloadRestartPermission : PayloadRestartPermission**`")
  n85("`*«requirement»*
**BlueDogRequirements::telemetryDeliveryCadence : TelemetryDeliveryCadence**`")
  n86("`*«requirement»*
**BlueDogRequirements::outageAutonomy : OutageAutonomy**`")
  n87("`*«requirement»*
**BlueDogRequirements::reconnectCurrentRecord : ReconnectCurrentRecord**`")
  n88("`*«requirement»*
**BlueDogRequirements::backlogOrdering : BacklogOrdering**`")
  n89("`*«requirement»*
**BlueDogRequirements::backlogCurrentPriority : BacklogCurrentPriority**`")
  n90("`*«requirement»*
**BlueDogRequirements::ingressDetection : IngressDetection**`")
  n91("`*«requirement»*
**BlueDogRequirements::ingressRecoveryRequest : IngressRecoveryRequest**`")
  n92("`*«requirement»*
**BlueDogRequirements::ingressFlotation : IngressFlotation**`")
  n93("`*«requirement»*
**BlueDogRequirements::ingressElectronicsProtection : IngressElectronicsProtection**`")
  n94("`*«requirement»*
**BlueDogRequirements::ingressPositionContinuity : IngressPositionContinuity**`")
  n95("`*«requirement»*
**BlueDogRequirements::periodicLogCadence : PeriodicLogCadence**`")
  n96("`*«requirement»*
**BlueDogRequirements::logRetention : LogRetention**`")
  n97("`*«requirement»*
**BlueDogRequirements::criticalEventRecording : CriticalEventRecording**`")
  n98("`*«requirement»*
**BlueDogRequirements::logTimestampAccuracy : LogTimestampAccuracy**`")
  n99("`*«requirement»*
**BlueDogRequirements::invalidTimestampMarking : InvalidTimestampMarking**`")
  n100("`*«requirement»*
**BlueDogRequirements::logGapIndication : LogGapIndication**`")
  n101("`*«requirement»*
**BlueDogRequirements::logInterruptionDurability : LogInterruptionDurability**`")
  n102("`*«requirement»*
**BlueDogRequirements::reconnectLogPreservation : ReconnectLogPreservation**`")
  n103("`*«requirement»*
**BlueDogRequirements::qualificationPersistence : QualificationPersistence**`")
  n104("`*«requirement»*
**BlueDogRequirements::unknownQualificationFallback : UnknownQualificationFallback**`")
  n105("`*«requirement»*
**BlueDogRequirements::navigationValidEpochs : NavigationValidEpochs**`")
  n106("`*«requirement»*
**BlueDogRequirements::staleNavigationInvalidation : StaleNavigationInvalidation**`")
  n107("`*«requirement»*
**BlueDogRequirements::navigationDegradedTransition : NavigationDegradedTransition**`")
  n108("`*«requirement»*
**BlueDogRequirements::staleNavigationUseInhibition : StaleNavigationUseInhibition**`")
  n109("`*«requirement»*
**BlueDogRequirements::soloTransport : SoloTransport**`")
  n110("`*«requirement»*
**BlueDogRequirements::liftMass : LiftMass**`")
  n111("`*«requirement»*
**BlueDogRequirements::setupDuration : SetupDuration**`")
  n112("`*«requirement»*
**BlueDogRequirements::packDuration : PackDuration**`")
  n113("`*«requirement»*
**BlueDogRequirements::soloLaunch : SoloLaunch**`")
  n114("`*«requirement»*
**BlueDogRequirements::soloRetrieval : SoloRetrieval**`")
  n115("`*«requirement»*
**BlueDogRequirements::replacementDuration : ReplacementDuration**`")
  n116("`*«requirement»*
**BlueDogRequirements::nondestructiveService : NondestructiveService**`")
  n117("`*«requirement»*
**BlueDogRequirements::postServiceSealing : PostServiceSealing**`")
  n118("`*«requirement»*
**BlueDogRequirements::postServiceActuation : PostServiceActuation**`")
  n119("`*«requirement»*
**BlueDogRequirements::trafficTracking : TrafficTracking**`")
  n120("`*«requirement»*
**BlueDogRequirements::collisionAssessmentCadence : CollisionAssessmentCadence**`")
  n121("`*«requirement»*
**BlueDogRequirements::avoidanceCommandDeadline : AvoidanceCommandDeadline**`")
  n122("`*«requirement»*
**BlueDogRequirements::trafficAwarenessFault : TrafficAwarenessFault**`")
  n123("`*«requirement»*
**BlueDogRequirements::boundaryEvaluationCadence : BoundaryEvaluationCadence**`")
  n124("`*«requirement»*
**BlueDogRequirements::boundaryAvoidanceDeadline : BoundaryAvoidanceDeadline**`")
  n125("`*«requirement»*
**BlueDogRequirements::boundaryAvoidanceRecording : BoundaryAvoidanceRecording**`")
  n126("`*«requirement»*
**BlueDogRequirements::boundaryStartInhibition : BoundaryStartInhibition**`")
  n127("`*«requirement»*
**BlueDogRequirements::boundaryDegradedEvidence : BoundaryDegradedEvidence**`")
  n128("`*«requirement»*
**BlueDogRequirements::abortLatchDeadline : AbortLatchDeadline**`")
  n129("`*«requirement»*
**BlueDogRequirements::recoveryTelemetryCadence : RecoveryTelemetryCadence**`")
  n130("`*«requirement»*
**BlueDogRequirements::motorIsolationDeadline : MotorIsolationDeadline**`")
  n131("`*«requirement»*
**BlueDogRequirements::isolationRestartInhibition : IsolationRestartInhibition**`")
  n132("`*«requirement»*
**BlueDogRequirements::manualControlLossShutdown : ManualControlLossShutdown**`")
  n133("`*«requirement»*
**BlueDogRequirements::controlLossLocationContinuity : ControlLossLocationContinuity**`")
  n134("`*«requirement»*
**BlueDogRequirements::navigationLightPresentation : NavigationLightPresentation**`")
  n135("`*«requirement»*
**BlueDogRequirements::navigationShapePresentation : NavigationShapePresentation**`")
  n136("`*«requirement»*
**BlueDogRequirements::navigationSoundPresentation : NavigationSoundPresentation**`")
  n137("`*«requirement»*
**BlueDogRequirements::signalingModeDeadline : SignalingModeDeadline**`")
  n138("`*«requirement»*
**BlueDogRequirements::signalingFaultRecording : SignalingFaultRecording**`")
  n139("`*«requirement»*
**BlueDogRequirements::signalingFaultReporting : SignalingFaultReporting**`")
  n140("`*«requirement»*
**BlueDogRequirements::deploymentComplianceRecord : DeploymentComplianceRecord**`")
  n141("`*«requirement»*
**BlueDogRequirements::deploymentReleaseGate : DeploymentReleaseGate**`")
  n142("`*«requirement»*
**BlueDogRequirements::telemetryDisplayContent : TelemetryDisplayContent**`")
  n143("`*«requirement»*
**BlueDogRequirements::telemetryStaleIndication : TelemetryStaleIndication**`")
  n144("`*«requirement»*
**BlueDogRequirements::telemetryIdentityPreservation : TelemetryIdentityPreservation**`")
  n145("`*«requirement»*
**BlueDogRequirements::telemetryDuplicateSuppression : TelemetryDuplicateSuppression**`")
  n146("`*«requirement»*
**BlueDogRequirements::unauthenticatedCommandRejection : UnauthenticatedCommandRejection**`")
  n147("`*«requirement»*
**BlueDogRequirements::replayCommandRejection : ReplayCommandRejection**`")
  n148("`*«requirement»*
**BlueDogRequirements::expiredCommandRejection : ExpiredCommandRejection**`")
  n149("`*«requirement»*
**BlueDogRequirements::acceptedCommandDeadline : AcceptedCommandDeadline**`")
  n150("`*«requirement»*
**BlueDogRequirements::onboardAcknowledgmentDeadline : OnboardAcknowledgmentDeadline**`")
  n151("`*«requirement»*
**BlueDogRequirements::acknowledgmentQueueing : AcknowledgmentQueueing**`")
  n152("`*«requirement»*
**BlueDogRequirements::externalControlDisqualification : ExternalControlDisqualification**`")
  n153("`*«requirement»*
**BlueDogRequirements::visibilityNavigationCapability : VisibilityNavigationCapability**`")
  n154("`*«requirement»*
**BlueDogRequirements::visibilityTrafficCapability : VisibilityTrafficCapability**`")
  n155("`*«requirement»*
**BlueDogRequirements::restrictedVisibilityEntry : RestrictedVisibilityEntry**`")
  n156("`*«requirement»*
**BlueDogRequirements::restrictedVisibilityEvidence : RestrictedVisibilityEvidence**`")
  n157("`*«requirement»*
**BlueDogRequirements::restrictedVisibilityCollisionAssessment : RestrictedVisibilityCollisionAssessment**`")
  n158("`*«requirement»*
**BlueDogRequirements::survivalEntryDeadline : SurvivalEntryDeadline**`")
  n159("`*«requirement»*
**BlueDogRequirements::survivalTransitionRecording : SurvivalTransitionRecording**`")
  n160("`*«requirement»*
**BlueDogRequirements::sailingResumptionDeadline : SailingResumptionDeadline**`")
  n161("`*«requirement»*
**BlueDogRequirements::sailingResumptionInhibition : SailingResumptionInhibition**`")
  n162("`*«requirement»*
**BlueDogRequirements::resumptionBlockEvidence : ResumptionBlockEvidence**`")
  n163("`*«requirement»*
**BlueDogRequirements::wetMechanismTravel : WetMechanismTravel**`")
  n164("`*«requirement»*
**BlueDogRequirements::wetJointIntegrity : WetJointIntegrity**`")
  n165("`*«requirement»*
**BlueDogRequirements::wetConductorResistance : WetConductorResistance**`")
  n166("`*«requirement»*
**BlueDogRequirements::wetInsulationResistance : WetInsulationResistance**`")
  n167("`*«requirement»*
**BlueDogRequirements::hotSunElectronicsOperation : HotSunElectronicsOperation**`")
  n168("`*«requirement»*
**BlueDogRequirements::hotSunBatteryTemperature : HotSunBatteryTemperature**`")
  n169("`*«requirement»*
**BlueDogRequirements::batteryChargeTemperatureInhibition : BatteryChargeTemperatureInhibition**`")
  n170("`*«requirement»*
**BlueDogRequirements::rightingDeadline : RightingDeadline**`")
  n171("`*«requirement»*
**BlueDogRequirements::capsizeRigRetention : CapsizeRigRetention**`")
  n172("`*«requirement»*
**BlueDogRequirements::capsizeBallastRetention : CapsizeBallastRetention**`")
  n173("`*«requirement»*
**BlueDogRequirements::capsizeElectronicsSealing : CapsizeElectronicsSealing**`")
  n174("`*«requirement»*
**BlueDogRequirements::controlRecoveryDeadline : ControlRecoveryDeadline**`")
  n175("`*«requirement»*
**BlueDogRequirements::capsizeGateProgressRetention : CapsizeGateProgressRetention**`")
  n176("`*«requirement»*
**BlueDogRequirements::capsizeQualificationRetention : CapsizeQualificationRetention**`")
  n177("`*«requirement»*
**BlueDogRequirements::capsizeRestrictionRetention : CapsizeRestrictionRetention**`")
  n178("`*«requirement»*
**BlueDogRequirements::weedPassageSpeed : WeedPassageSpeed**`")
  n179("`*«requirement»*
**BlueDogRequirements::weedPassageSteering : WeedPassageSteering**`")
  n180("`*«requirement»*
**BlueDogRequirements::weedSnagSpeedRecovery : WeedSnagSpeedRecovery**`")
  n181("`*«requirement»*
**BlueDogRequirements::weedSnagSteeringRecovery : WeedSnagSteeringRecovery**`")
  n182("`*«requirement»*
**BlueDogRequirements::weedBlockageFault : WeedBlockageFault**`")
  n183("`*«requirement»*
**BlueDogRequirements::weedBlockageContingency : WeedBlockageContingency**`")
  n184("`*«requirement»*
**BlueDogRequirements::weedBlockageLocation : WeedBlockageLocation**`")
  n185("`*«requirement»*
**BlueDogRequirements::poweredWeedSpeed : PoweredWeedSpeed**`")
  n186("`*«requirement»*
**BlueDogRequirements::poweredWeedCurrent : PoweredWeedCurrent**`")
  n187("`*«requirement»*
**BlueDogRequirements::poweredWeedTemperature : PoweredWeedTemperature**`")
  n188("`*«requirement»*
**BlueDogRequirements::lockedPropulsorShutdown : LockedPropulsorShutdown**`")
  n189("`*«requirement»*
**BlueDogRequirements::motorQualificationInvariant : MotorQualificationInvariant**`")
  n190("`*«requirement»*
**BlueDogRequirements::freshRecoveryCommand : FreshRecoveryCommand**`")
  n191("`*«requirement»*
**BlueDogRequirements::ingressEventDeadline : IngressEventDeadline**`")
  n192("`*«requirement»*
**BlueDogRequirements::qualificationRestoration : QualificationRestoration**`")
  n193("`*«requirement»*
**BlueDogRequirements::sustainedEnergyFeasibility : SustainedEnergyFeasibility**`")
  n194("`*«requirement»*
**BlueDogRequirements::sustainedReserveProtection : SustainedReserveProtection**`")
  n195("`*«requirement»*
**BlueDogRequirements::repeatableCycleBalance : RepeatableCycleBalance**`")
  n196("`*«requirement»*
**BlueDogRequirements::peakSupplyCapability : PeakSupplyCapability**`")
  n197("`*«requirement»*
**BlueDogRequirements::harvestCampaignCoverage : HarvestCampaignCoverage**`")
  n198("`*«requirement»*
**BlueDogRequirements::energyEvidenceReadiness : EnergyEvidenceReadiness**`")
  n199["`*«verification def»*
**BlueDogEnergy::SustainedEnergyVerification**`"]
  n200("`*«part»*
**handling : HandlingInterfaces**`")
  n201("`*«part»*
**printedHull : PrintedHull**`")
  n202("`*«part»*
**enclosure : SealedEnclosure**`")
  n203("`*«part»*
**BlueDog::Architecture::missionContext::boat : Boat**`")
  n204("`*«part»*
**boundarySupervisor : BoundarySupervisor**`")
  n205("`*«part»*
**signaling : NavigationSignaling**`")
  n206("`*«part»*
**BlueDog::Architecture::ShoreSupport::monitoringStation : MonitoringStation**`")
  n207("`*«part»*
**commandGateway : CommandGateway**`")
  n208("`*«part»*
**powerManagement : PowerManagement**`")
  n209("`*«part»*
**hullAndRig : HullAndRig**`")
  n210("`*«part»*
**communications : Communications**`")
  n211("`*«part»*
**navigation : NavigationAndSensing**`")
  n212("`*«part»*
**BlueDog::Architecture::HealthAndRecovery::recoveryController : RecoveryController**`")
  n213("`*«part»*
**control : GuidanceAndControl**`")
  n214("`*«part»*
**actuation : SailAndSteeringActuation**`")
  n215("`*«part»*
**positionAndAttitude : PositionAndAttitude**`")
  n216("`*«part»*
**collisionAvoidance : CollisionAvoidance**`")
  n217("`*«part»*
**BlueDog::Architecture::HealthAndRecovery::ingressMonitor : IngressMonitor**`")
  n218("`*«part»*
**recording : DataRecording**`")
  n219("`*«part»*
**traffic : TrafficSensing**`")
  n220("`*«part»*
**BlueDog::Architecture::HealthAndRecovery::motorSystem : RecoveryPropulsion**`")
  n221("`*«part»*
**energy : EnergySubsystem**`")
  n222("`*«part»*
**storage : EnergyStorage**`")
  n223("`*«part»*
**keelAndBallast : KeelAndBallast**`")
  n224("`*«part»*
**missionManager : MissionManager**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
  n4 -.->|"derive"| n0
  n5 -.->|"derive"| n0
  n6 -.->|"derive"| n0
  n199 -.->|"verify"| n193
  n8 -.->|"derive"| n1
  n9 -.->|"derive"| n2
  n11 -.->|"derive"| n3
  n8 -.->|"derive"| n4
  n14 -.->|"derive"| n5
  n14 -.->|"derive"| n6
  n9 -.->|"derive"| n7
  n11 -.->|"derive"| n7
  n14 -.->|"derive"| n7
  n12 -.->|"derive"| n7
  n16 -.->|"derive"| n7
  n11 -.->|"derive"| n8
  n12 -.->|"derive"| n8
  n14 -.->|"derive"| n8
  n15 -.->|"derive"| n8
  n16 -.->|"derive"| n8
  n10 -.->|"derive"| n9
  n13 -.->|"derive"| n9
  n13 -.->|"derive"| n10
  n17 -.->|"derive"| n8
  n18 -.->|"derive"| n8
  n19 -.->|"derive"| n2
  n20 -.->|"derive"| n11
  n21 -.->|"derive"| n8
  n22 -.->|"derive"| n6
  n23 -.->|"derive"| n20
  n24 -.->|"derive"| n8
  n25 -.->|"derive"| n8
  n26 -.->|"derive"| n25
  n27 -.->|"derive"| n25
  n28 -.->|"derive"| n22
  n29 -.->|"derive"| n28
  n30 -.->|"derive"| n14
  n31 -.->|"derive"| n14
  n25 -.->|"derive"| n7
  n32 -.->|"derive"| n8
  n33 -.->|"derive"| n7
  n34 -.->|"derive"| n32
  n35 -.->|"derive"| n32
  n36 -.->|"derive"| n32
  n37 -.->|"derive"| n32
  n38 -.->|"derive"| n32
  n39 -.->|"derive"| n33
  n40 -.->|"derive"| n33
  n41 -.->|"derive"| n33
  n42 -.->|"derive"| n33
  n43 -.->|"derive"| n33
  n44 -.->|"derive"| n25
  n45 -.->|"derive"| n25
  n46 -.->|"derive"| n25
  n47 -.->|"derive"| n25
  n48 -.->|"derive"| n25
  n49 -.->|"derive"| n25
  n50 -.->|"derive"| n26
  n51 -.->|"derive"| n26
  n52 -.->|"derive"| n26
  n53 -.->|"derive"| n26
  n54 -.->|"derive"| n26
  n55 -.->|"derive"| n26
  n56 -.->|"derive"| n26
  n57 -.->|"derive"| n27
  n58 -.->|"derive"| n27
  n59 -.->|"derive"| n27
  n60 -.->|"derive"| n27
  n61 -.->|"derive"| n27
  n62 -.->|"derive"| n27
  n62 -.->|"derive"| n28
  n63 -.->|"derive"| n11
  n64 -.->|"derive"| n29
  n65 -.->|"derive"| n4
  n65 -.->|"derive"| n3
  n31 -.->|"derive"| n3
  n31 -.->|"derive"| n6
  n21 -.->|"derive"| n7
  n24 -.->|"derive"| n7
  n19 -.->|"derive"| n7
  n50 -.->|"derive"| n32
  n51 -.->|"derive"| n33
  n59 -.->|"derive"| n32
  n60 -.->|"derive"| n32
  n66 -.->|"derive"| n10
  n67 -.->|"derive"| n10
  n68 -.->|"derive"| n10
  n69 -.->|"derive"| n10
  n70 -.->|"derive"| n11
  n71 -.->|"derive"| n11
  n72 -.->|"derive"| n11
  n73 -.->|"derive"| n11
  n74 -.->|"derive"| n11
  n75 -.->|"derive"| n12
  n76 -.->|"derive"| n12
  n77 -.->|"derive"| n12
  n78 -.->|"derive"| n12
  n79 -.->|"derive"| n13
  n80 -.->|"derive"| n13
  n81 -.->|"derive"| n13
  n82 -.->|"derive"| n13
  n83 -.->|"derive"| n13
  n84 -.->|"derive"| n13
  n85 -.->|"derive"| n14
  n86 -.->|"derive"| n14
  n87 -.->|"derive"| n14
  n88 -.->|"derive"| n14
  n89 -.->|"derive"| n14
  n90 -.->|"derive"| n15
  n91 -.->|"derive"| n15
  n92 -.->|"derive"| n15
  n93 -.->|"derive"| n15
  n94 -.->|"derive"| n15
  n95 -.->|"derive"| n16
  n96 -.->|"derive"| n16
  n97 -.->|"derive"| n16
  n98 -.->|"derive"| n16
  n99 -.->|"derive"| n16
  n100 -.->|"derive"| n16
  n101 -.->|"derive"| n16
  n102 -.->|"derive"| n16
  n103 -.->|"derive"| n16
  n104 -.->|"derive"| n16
  n105 -.->|"derive"| n63
  n106 -.->|"derive"| n63
  n107 -.->|"derive"| n63
  n108 -.->|"derive"| n63
  n109 -.->|"derive"| n17
  n110 -.->|"derive"| n17
  n111 -.->|"derive"| n17
  n112 -.->|"derive"| n17
  n113 -.->|"derive"| n17
  n114 -.->|"derive"| n17
  n115 -.->|"derive"| n19
  n116 -.->|"derive"| n19
  n117 -.->|"derive"| n19
  n118 -.->|"derive"| n19
  n119 -.->|"derive"| n20
  n120 -.->|"derive"| n20
  n121 -.->|"derive"| n20
  n122 -.->|"derive"| n20
  n123 -.->|"derive"| n21
  n124 -.->|"derive"| n21
  n125 -.->|"derive"| n21
  n126 -.->|"derive"| n21
  n127 -.->|"derive"| n21
  n128 -.->|"derive"| n22
  n129 -.->|"derive"| n22
  n130 -.->|"derive"| n22
  n131 -.->|"derive"| n22
  n132 -.->|"derive"| n22
  n133 -.->|"derive"| n22
  n134 -.->|"derive"| n23
  n135 -.->|"derive"| n23
  n136 -.->|"derive"| n23
  n137 -.->|"derive"| n23
  n138 -.->|"derive"| n23
  n139 -.->|"derive"| n23
  n140 -.->|"derive"| n24
  n141 -.->|"derive"| n24
  n142 -.->|"derive"| n30
  n143 -.->|"derive"| n30
  n144 -.->|"derive"| n30
  n145 -.->|"derive"| n30
  n146 -.->|"derive"| n31
  n147 -.->|"derive"| n31
  n148 -.->|"derive"| n31
  n149 -.->|"derive"| n31
  n150 -.->|"derive"| n31
  n151 -.->|"derive"| n31
  n152 -.->|"derive"| n31
  n153 -.->|"derive"| n47
  n154 -.->|"derive"| n47
  n155 -.->|"derive"| n47
  n156 -.->|"derive"| n47
  n157 -.->|"derive"| n47
  n158 -.->|"derive"| n49
  n159 -.->|"derive"| n49
  n160 -.->|"derive"| n49
  n161 -.->|"derive"| n49
  n162 -.->|"derive"| n49
  n163 -.->|"derive"| n53
  n164 -.->|"derive"| n53
  n165 -.->|"derive"| n54
  n166 -.->|"derive"| n54
  n167 -.->|"derive"| n55
  n168 -.->|"derive"| n55
  n169 -.->|"derive"| n55
  n170 -.->|"derive"| n57
  n171 -.->|"derive"| n57
  n172 -.->|"derive"| n57
  n173 -.->|"derive"| n57
  n174 -.->|"derive"| n58
  n175 -.->|"derive"| n58
  n176 -.->|"derive"| n58
  n177 -.->|"derive"| n58
  n178 -.->|"derive"| n59
  n179 -.->|"derive"| n59
  n180 -.->|"derive"| n60
  n181 -.->|"derive"| n60
  n182 -.->|"derive"| n61
  n183 -.->|"derive"| n61
  n184 -.->|"derive"| n61
  n185 -.->|"derive"| n62
  n186 -.->|"derive"| n62
  n187 -.->|"derive"| n62
  n188 -.->|"derive"| n62
  n189 -.->|"derive"| n65
  n190 -.->|"derive"| n65
  n191 -.->|"derive"| n15
  n192 -.->|"derive"| n12
  n101 -.->|"derive"| n12
  n104 -.->|"derive"| n12
  n103 -.->|"derive"| n12
  n190 -.->|"derive"| n12
  n189 -.->|"derive"| n12
  n97 -.->|"derive"| n31
  n103 -.->|"derive"| n31
  n103 -.->|"derive"| n22
  n189 -.->|"derive"| n22
  n95 -.->|"derive"| n22
  n103 -.->|"derive"| n65
  n97 -.->|"derive"| n65
  n95 -.->|"derive"| n13
  n85 -.->|"derive"| n13
  n97 -.->|"derive"| n13
  n189 -.->|"derive"| n13
  n97 -.->|"derive"| n15
  n189 -.->|"derive"| n15
  n96 -.->|"derive"| n14
  n102 -.->|"derive"| n14
  n97 -.->|"derive"| n63
  n95 -.->|"derive"| n49
  n189 -.->|"derive"| n49
  n189 -.->|"derive"| n61
  n189 -.->|"derive"| n62
  n193 -.->|"derive"| n2
  n193 -.->|"derive"| n7
  n194 -.->|"derive"| n193
  n195 -.->|"derive"| n193
  n196 -.->|"derive"| n193
  n198 -.->|"derive"| n193
  n194 -.->|"derive"| n9
  n196 -.->|"derive"| n9
  n197 -.->|"derive"| n9
  n198 -.->|"derive"| n9
  n194 -.->|"derive"| n29
  n200 -.->|"satisfy"| n17
  n201 -.->|"satisfy"| n18
  n202 -.->|"satisfy"| n19
  n203 -.->|"satisfy"| n20
  n204 -.->|"satisfy"| n21
  n203 -.->|"satisfy"| n22
  n205 -.->|"satisfy"| n23
  n203 -.->|"satisfy"| n25
  n203 -.->|"satisfy"| n26
  n203 -.->|"satisfy"| n27
  n203 -.->|"satisfy"| n28
  n203 -.->|"satisfy"| n29
  n206 -.->|"satisfy"| n30
  n207 -.->|"satisfy"| n31
  n203 -.->|"satisfy"| n8
  n203 -.->|"satisfy"| n9
  n208 -.->|"satisfy"| n10
  n203 -.->|"satisfy"| n11
  n203 -.->|"satisfy"| n12
  n203 -.->|"satisfy"| n13
  n203 -.->|"satisfy"| n14
  n203 -.->|"satisfy"| n15
  n203 -.->|"satisfy"| n16
  n203 -.->|"satisfy"| n32
  n203 -.->|"satisfy"| n33
  n203 -.->|"satisfy"| n34
  n203 -.->|"satisfy"| n35
  n203 -.->|"satisfy"| n36
  n203 -.->|"satisfy"| n37
  n203 -.->|"satisfy"| n38
  n203 -.->|"satisfy"| n39
  n203 -.->|"satisfy"| n40
  n203 -.->|"satisfy"| n41
  n203 -.->|"satisfy"| n42
  n203 -.->|"satisfy"| n43
  n203 -.->|"satisfy"| n44
  n203 -.->|"satisfy"| n45
  n203 -.->|"satisfy"| n46
  n203 -.->|"satisfy"| n47
  n203 -.->|"satisfy"| n48
  n203 -.->|"satisfy"| n49
  n203 -.->|"satisfy"| n50
  n203 -.->|"satisfy"| n51
  n202 -.->|"satisfy"| n52
  n209 -.->|"satisfy"| n53
  n210 -.->|"satisfy"| n54
  n208 -.->|"satisfy"| n55
  n201 -.->|"satisfy"| n56
  n203 -.->|"satisfy"| n57
  n203 -.->|"satisfy"| n58
  n203 -.->|"satisfy"| n59
  n203 -.->|"satisfy"| n60
  n203 -.->|"satisfy"| n61
  n203 -.->|"satisfy"| n62
  n211 -.->|"satisfy"| n63
  n208 -.->|"satisfy"| n64
  n212 -.->|"satisfy"| n65
  n208 -.->|"satisfy"| n66
  n208 -.->|"satisfy"| n67
  n208 -.->|"satisfy"| n68
  n208 -.->|"satisfy"| n69
  n213 -.->|"satisfy"| n70
  n214 -.->|"satisfy"| n71
  n214 -.->|"satisfy"| n72
  n215 -.->|"satisfy"| n73
  n215 -.->|"satisfy"| n74
  n212 -.->|"satisfy"| n75
  n213 -.->|"satisfy"| n76
  n213 -.->|"satisfy"| n77
  n213 -.->|"satisfy"| n78
  n208 -.->|"satisfy"| n79
  n208 -.->|"satisfy"| n80
  n213 -.->|"satisfy"| n81
  n216 -.->|"satisfy"| n82
  n208 -.->|"satisfy"| n83
  n208 -.->|"satisfy"| n84
  n210 -.->|"satisfy"| n85
  n213 -.->|"satisfy"| n86
  n210 -.->|"satisfy"| n87
  n210 -.->|"satisfy"| n88
  n210 -.->|"satisfy"| n89
  n217 -.->|"satisfy"| n90
  n212 -.->|"satisfy"| n91
  n209 -.->|"satisfy"| n92
  n202 -.->|"satisfy"| n93
  n210 -.->|"satisfy"| n94
  n218 -.->|"satisfy"| n95
  n218 -.->|"satisfy"| n96
  n218 -.->|"satisfy"| n97
  n218 -.->|"satisfy"| n98
  n218 -.->|"satisfy"| n99
  n218 -.->|"satisfy"| n100
  n218 -.->|"satisfy"| n101
  n218 -.->|"satisfy"| n102
  n212 -.->|"satisfy"| n103
  n212 -.->|"satisfy"| n104
  n211 -.->|"satisfy"| n105
  n211 -.->|"satisfy"| n106
  n213 -.->|"satisfy"| n107
  n213 -.->|"satisfy"| n108
  n200 -.->|"satisfy"| n109
  n200 -.->|"satisfy"| n110
  n200 -.->|"satisfy"| n111
  n200 -.->|"satisfy"| n112
  n200 -.->|"satisfy"| n113
  n200 -.->|"satisfy"| n114
  n203 -.->|"satisfy"| n115
  n203 -.->|"satisfy"| n116
  n202 -.->|"satisfy"| n117
  n214 -.->|"satisfy"| n118
  n219 -.->|"satisfy"| n119
  n216 -.->|"satisfy"| n120
  n216 -.->|"satisfy"| n121
  n216 -.->|"satisfy"| n122
  n204 -.->|"satisfy"| n123
  n204 -.->|"satisfy"| n124
  n218 -.->|"satisfy"| n125
  n204 -.->|"satisfy"| n126
  n204 -.->|"satisfy"| n127
  n212 -.->|"satisfy"| n128
  n210 -.->|"satisfy"| n129
  n220 -.->|"satisfy"| n130
  n220 -.->|"satisfy"| n131
  n212 -.->|"satisfy"| n132
  n210 -.->|"satisfy"| n133
  n205 -.->|"satisfy"| n134
  n205 -.->|"satisfy"| n135
  n205 -.->|"satisfy"| n136
  n205 -.->|"satisfy"| n137
  n218 -.->|"satisfy"| n138
  n210 -.->|"satisfy"| n139
  n206 -.->|"satisfy"| n142
  n206 -.->|"satisfy"| n143
  n206 -.->|"satisfy"| n144
  n206 -.->|"satisfy"| n145
  n207 -.->|"satisfy"| n146
  n207 -.->|"satisfy"| n147
  n207 -.->|"satisfy"| n148
  n207 -.->|"satisfy"| n149
  n207 -.->|"satisfy"| n150
  n207 -.->|"satisfy"| n151
  n212 -.->|"satisfy"| n152
  n211 -.->|"satisfy"| n153
  n219 -.->|"satisfy"| n154
  n213 -.->|"satisfy"| n155
  n218 -.->|"satisfy"| n156
  n216 -.->|"satisfy"| n157
  n213 -.->|"satisfy"| n158
  n218 -.->|"satisfy"| n159
  n213 -.->|"satisfy"| n160
  n213 -.->|"satisfy"| n161
  n218 -.->|"satisfy"| n162
  n209 -.->|"satisfy"| n163
  n209 -.->|"satisfy"| n164
  n221 -.->|"satisfy"| n165
  n221 -.->|"satisfy"| n166
  n203 -.->|"satisfy"| n167
  n222 -.->|"satisfy"| n168
  n208 -.->|"satisfy"| n169
  n209 -.->|"satisfy"| n170
  n209 -.->|"satisfy"| n171
  n223 -.->|"satisfy"| n172
  n202 -.->|"satisfy"| n173
  n213 -.->|"satisfy"| n174
  n224 -.->|"satisfy"| n175
  n212 -.->|"satisfy"| n176
  n213 -.->|"satisfy"| n177
  n203 -.->|"satisfy"| n178
  n214 -.->|"satisfy"| n179
  n203 -.->|"satisfy"| n180
  n214 -.->|"satisfy"| n181
  n218 -.->|"satisfy"| n182
  n213 -.->|"satisfy"| n183
  n210 -.->|"satisfy"| n184
  n220 -.->|"satisfy"| n185
  n220 -.->|"satisfy"| n186
  n220 -.->|"satisfy"| n187
  n220 -.->|"satisfy"| n188
  n212 -.->|"satisfy"| n189
  n212 -.->|"satisfy"| n190
  n218 -.->|"satisfy"| n191
  n212 -.->|"satisfy"| n192
  n221 -.->|"satisfy"| n193
  n221 -.->|"satisfy"| n194
  n221 -.->|"satisfy"| n195
  n221 -.->|"satisfy"| n196
```
