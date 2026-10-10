# Atomic requirement decomposition

The 29 parent requirements below retain their original IDs and now decompose into 127 acceptance leaves. Each leaf states one observable result. Named SysML comments hold the normative qualification conditions, separate from each concise statement. Native verification cases link the parent and applicable leaves to their planned acceptance procedure; see [requirement context](requirements-context.md). A single trial can provide evidence for several leaves, but each leaf receives its own verdict.

A list of test cases, dimensions, sampled fields or operating conditions does not automatically create multiple requirements. For example, P-002 has one print-job fit decision over three axes; authentication, command application and acknowledgment have separate observable outcomes and therefore separate leaves. Speed and steering after a weed snag now have separate results, both required for each repetition.

Parent acceptance requires all applicable leaf evidence, including shared leaves reached through derivation links. These links do not execute an aggregate verdict. Do not evaluate a prose-only parent with the native requirement evaluator and interpret an empty constraint result as compliance. Five existing predicates moved to specific leaves; the other three remain on P-002, R-002 and R-003. No new physical evidence is claimed.

| Retained parent | Acceptance leaves |
| --- | --- |
| E-001 EnergyAwareness | E-101 EnergyEstimateCadence; E-102 ReserveEstimateCadence; E-103 EnergyEstimateAccuracy; E-104 ConservativeEnergyEstimate |
| E-002 NavigationAndControl | E-105 GuidanceUpdateCadence; E-106 SailCommandCadence; E-107 SteeringCommandCadence; E-108 PositionAccuracy; E-109 HeadingAccuracy |
| E-003 ResetRecovery | E-110 RestartDeadline; E-111 MissionStateRestoration; E-112 GateProgressRestoration; E-113 ResetRestrictionPreservation; E-145 QualificationRestoration |
| E-004 LowEnergyRecovery | E-114 LowEnergyEntry; E-115 LowEnergyPayloadInhibition; E-116 LowEnergyNavigationContinuity; E-117 LowEnergyCollisionContinuity; E-118 LowEnergyExit; E-119 PayloadRestartPermission |
| E-005 Communications | E-120 TelemetryDeliveryCadence; E-121 OutageAutonomy; E-122 ReconnectCurrentRecord; E-123 BacklogOrdering; E-124 BacklogCurrentPriority |
| E-006 IngressResponse | E-125 IngressDetection; E-126 IngressRecoveryRequest; E-127 IngressFlotation; E-128 IngressElectronicsProtection; E-129 IngressPositionContinuity; E-144 IngressEventDeadline |
| E-007 MissionEvidence | E-130 PeriodicLogCadence; E-131 LogRetention; E-132 CriticalEventRecording; E-133 LogTimestampAccuracy; E-134 InvalidTimestampMarking; E-135 LogGapIndication; E-136 LogInterruptionDurability; E-137 ReconnectLogPreservation; E-138 QualificationPersistence; E-139 UnknownQualificationFallback |
| E-008 NavigationAvailability | E-140 NavigationValidEpochs; E-141 StaleNavigationInvalidation; E-142 NavigationDegradedTransition; E-143 StaleNavigationUseInhibition |
| P-001 Transportability | P-101 SoloTransport; P-102 LiftMass; P-103 SetupDuration; P-104 PackDuration; P-105 SoloLaunch; P-106 SoloRetrieval |
| P-003 Serviceability | P-107 ReplacementDuration; P-108 NondestructiveService; P-109 PostServiceSealing; P-110 PostServiceActuation |
| S-001 TrafficSafety | S-101 TrafficTracking; S-102 CollisionAssessmentCadence; S-103 AvoidanceCommandDeadline; S-104 TrafficAwarenessFault |
| S-002 OperatingBoundary | S-105 BoundaryEvaluationCadence; S-106 BoundaryAvoidanceDeadline; S-107 BoundaryAvoidanceRecording; S-108 BoundaryStartInhibition; S-109 BoundaryDegradedEvidence |
| S-003 SafeRecovery | S-110 AbortLatchDeadline; S-111 RecoveryTelemetryCadence; S-112 MotorIsolationDeadline; S-113 IsolationRestartInhibition; S-114 ManualControlLossShutdown; S-115 ControlLossLocationContinuity |
| S-004 NavigationConspicuity | S-116 NavigationLightPresentation; S-117 NavigationShapePresentation; S-118 NavigationSoundPresentation; S-119 SignalingModeDeadline; S-120 SignalingFaultRecording; S-121 SignalingFaultReporting |
| S-005 RegulatoryClassification | S-122 DeploymentComplianceRecord; S-123 DeploymentReleaseGate |
| C-101 TelemetryEquipment | C-201 TelemetryDisplayContent; C-202 TelemetryStaleIndication; C-203 TelemetryIdentityPreservation; C-204 TelemetryDuplicateSuppression |
| C-102 CommandIntegrity | C-205 UnauthenticatedCommandRejection; C-206 ReplayCommandRejection; C-207 ExpiredCommandRejection; C-208 AcceptedCommandDeadline; C-209 OnboardAcknowledgmentDeadline; C-210 AcknowledgmentQueueing; C-211 ExternalControlDisqualification |
| N-033 Visibility | N-101 VisibilityNavigationCapability; N-102 VisibilityTrafficCapability; N-103 RestrictedVisibilityEntry; N-104 RestrictedVisibilityEvidence; N-105 RestrictedVisibilityCollisionAssessment |
| N-035 EnvelopeTransition | N-106 SurvivalEntryDeadline; N-107 SurvivalTransitionRecording; N-108 SailingResumptionDeadline; N-109 SailingResumptionInhibition; N-110 ResumptionBlockEvidence |
| N-044 WetMechanicalIntegrity | N-111 WetMechanismTravel; N-112 WetJointIntegrity |
| N-045 WetElectricalIntegrity | N-113 WetConductorResistance; N-114 WetInsulationResistance |
| N-046 SolarHeating | N-115 HotSunElectronicsOperation; N-116 HotSunBatteryTemperature; N-117 BatteryChargeTemperatureInhibition |
| N-051 SelfRighting | N-118 RightingDeadline; N-119 CapsizeRigRetention; N-120 CapsizeBallastRetention; N-121 CapsizeElectronicsSealing |
| N-052 CapsizeControlRecovery | N-122 ControlRecoveryDeadline; N-123 CapsizeGateProgressRetention; N-124 CapsizeQualificationRetention; N-125 CapsizeRestrictionRetention |
| N-053 SubmergedWeedPassage | N-126 WeedPassageSpeed; N-127 WeedPassageSteering |
| N-054 WeedSnagShedding | N-128 WeedSnagSpeedRecovery; N-129 WeedSnagSteeringRecovery |
| N-055 WeedBlockageResponse | N-130 WeedBlockageFault; N-131 WeedBlockageContingency; N-132 WeedBlockageLocation |
| N-056 RecoveryPropulsorWeeds | N-133 PoweredWeedSpeed; N-134 PoweredWeedCurrent; N-135 PoweredWeedTemperature; N-136 LockedPropulsorShutdown |
| R-004 ChallengeMotorInhibition | R-101 MotorQualificationInvariant; R-102 FreshRecoveryCommand |

The [native register](requirements-register.md) is the authoritative published statement and derivation list. The [traceability table](traceability.md) includes intended allocations for the leaves; deployment-process requirements have no invented hardware allocation. Shared obligations such as durable qualification state, log retention and motor inhibition have one normative definition with multiple incoming derivations.

The executable acceptance definitions are listed in the [verification plan](verification-plan.md). Regression expectations in `tests/atomic_requirements.json` check that publishing retains every added ID and relationship. This fixture is not a second source for generated requirements; publishing reads SysML directly.

Traffic scenario parameters, deployment classification, mission coordinates and weed-surrogate equivalence remain unresolved acceptance inputs. Decomposition makes those gaps visible; it does not supply missing evidence. Environmental performance parents and top-level mission/challenge rules remain aggregate outcomes.
