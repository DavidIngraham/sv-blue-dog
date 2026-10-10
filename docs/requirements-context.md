# Requirement context and verification specifications

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

Requirement statements are in the register and focused views. Qualification conditions below are normative definitions and test applicability; they are not optional rationale. Notes and rationale explain scope and decisions. Verification specifications describe planned evidence collection and return inconclusive until implemented with accepted evidence. No physical compliance is asserted.

## Qualification conditions (normative)

| ID | Requirement | Text |
| --- | --- | --- |
| C-003 | UnassistedAttempt | Passive live monitoring is permitted. Remote emergency abort or manual control disqualifies the attempt as unassisted.  |
| C-004 | SailingPropulsion | An auxiliary motor may remain installed. Motor use is permitted during separate development tests and vessel recovery; use during an attempt ends its qualification.  |
| C-005 | LiveObservation | Monitoring-link loss shall not interrupt autonomous mission execution. Retained telemetry shall be transmitted after contact returns.  |
| C-006 | EmergencyIntervention | Use disqualifies the attempt as unassisted.  |
| M-001 | RoundTrip | C-003 through C-006 govern attempt qualification.  |
| M-002 | MultiDayEndurance | N-010 operational functions and applicable N-001 shared conditions apply. The campaign comprises three consecutive 24-hour cycles, each with at most 6 hours of harvesting and at least 18 hours with harvesting disabled. Conservative usable energy must remain above the R-002 reserve.  |
| E-001 | EnergyAwareness | Energy estimation and conservative decision inputs; accuracy uses calibrated energy integration across operating battery temperatures.  |
| E-002 | NavigationAndControl | Qualification uses the selected mission profile. Accuracy trials contain 1800 scheduled one-second epochs in 30 minutes; invalid or missing epochs fail. Position and heading criteria use the same set of at least 1710 qualifying epochs, preventing separate selection of different good samples. Fault-injection runs are separate.  |
| E-003 | ResetRecovery | Watchdog-reset tests start above protected reserve with valid navigation observations. Normal sailing remains subject to N-035; data and qualification persistence have shared leaf criteria.  |
| E-004 | LowEnergyRecovery | Reserve means R-002. Emergency/recovery cadence takes precedence; clearing low-energy state is independent of other modes, while payload enabling respects all restrictions.  |
| E-005 | Communications | Link availability is a delivery-test precondition, not a coverage guarantee. Normal cadence is 60 seconds; low-energy alone permits 300 seconds; emergency/powered recovery takes precedence at 60 seconds. Outage tests last 24 hours.  |
| E-006 | IngressResponse | All leaves use a 30-minute freshwater injection at 10 mL/min into the normally dry hull. No pump technology is prescribed; R-004 remains applicable.  |
| E-007 | MissionEvidence | Periodic records contain position, heading, mode, gate progress, battery energy and fault state. Critical events are independent of periodic cadence. Timestamp accuracy is assessed with valid GNSS time.  |
| P-001 | Transportability | Demonstrate with one adult, no powered lift, a firm bank or ramp of slope at most 1:12, wind at most 5 m/s and waves at most 0.2 m. This is not a survival-envelope recovery claim.  |
| P-002 | DesktopManufacture | Every printed component must be producible as one or more such jobs. The envelope includes the selected build orientation, supports, brim, raft and printer-required clearance.  |
| P-003 | Serviceability | Exercise individual replacement of the battery, every electronics module, every actuator and every serviceable enclosure seal by one operator using hand tools.  |
| S-001 | TrafficSafety | Use independently recorded head-on, crossing and overtaking AIS and non-AIS targets, day and night in the selected operational profile.  |
| S-002 | OperatingBoundary | Use uploaded permitted-water and exclusion polygons, with a 60-second prediction horizon. Inject approaches to every boundary, navigation loss and no-feasible-maneuver cases. Coordinates and uncertainty/clearance margins are controlled mission inputs with no default values.  |
| S-003 | SafeRecovery | Emergency intervention ends attempt qualification. Exercise active emergency, powered recovery, local isolation and remote-control loss, including coexisting low-energy flags.  |
| S-004 | NavigationConspicuity | Use the deployment-specific compliance matrix for sailing, powered-recovery and stationary modes, including its visibility, arcs, colors and sound criteria. The matrix remains a deployment hold point under S-005.  |
| S-005 | RegulatoryClassification | Acceptance is deployment document review, not onboard behavior or an assertion of buoy status.  |
| N-001 | EnvironmentalEnvelope | Gorge qualification uses N-010; ocean qualification uses N-020. Both include applicable shared exposure requirements. Operational functions are navigation, sail/steering control, recording and available-link telemetry. Survival requires flotation, attached rig/ballast, dry electronics and retained mission state; course progress is not required.  |
| N-002 | MarineDurability | Gorge uses N-041 freshwater exposure; ocean uses N-042 saltwater exposure; dual-profile qualification requires both. Shared sealing, material-aging and thermal checks use the selected campaign.  |
| N-003 | StabilityAndFouling | Righting, control recovery, weed passage, snag shedding and blockage-response criteria apply without operator intervention during a qualifying attempt.  |
| R-001 | RecoveryPropulsion | Wind must be no greater than 5 m/s and waves no greater than 0.2 m. R-004 governs motor enable and challenge qualification; S-003 governs isolation and control loss.  |
| R-002 | RecoveryEnergy | Motor demand uses the R-001 case. Essential demand includes navigation, control, recording and telemetry at S-003 recovery cadence. Use separate, non-overlapping power values for the selected installed configuration.  |
| C-101 | TelemetryEquipment | Freshness threshold is 120 seconds for normal, emergency, powered recovery or unknown mode, and 600 seconds only for explicitly reported low energy without emergency or powered recovery. Staleness describes data age, not diagnosed link failure. Exercise a 24-hour outage and reconnection.  |
| C-102 | CommandIntegrity | Exercise complete command receipt, authentication failure, replayed sequence numbers, age greater than 30 seconds, and external control during a qualifying attempt.  |
| N-010 | GorgeEnvironment | Gorge-specific parameter limits and applicable shared exposure requirements apply together.  |
| N-020 | OceanEnvironment | Ocean-specific parameter limits and applicable shared exposure requirements apply together.  |
| N-011 | GorgeWind | Operational functions are defined by N-001. Mean wind uses a 10-minute average referenced to 10 m above water.  |
| N-012 | GorgeWaves | N-001 defines operational functions. Wave statistics use 20-minute records.  |
| N-013 | GorgeCurrent | Predicted boundary risk invokes S-002.  |
| N-014 | GorgeSurvivalWind | Use N-001 survival outcomes and the operational wind reference convention. Selected-profile wave, current, temperature and humidity limits apply concurrently.  |
| N-015 | GorgeSurvivalWaves | N-001 defines survival outcomes.  |
| N-021 | OceanWind | Operational functions are defined by N-001. Mean wind uses a 10-minute average referenced to 10 m above water.  |
| N-022 | OceanWaves | N-001 defines operational functions. Wave statistics use 20-minute records.  |
| N-023 | OceanCurrent | Predicted boundary risk invokes S-002.  |
| N-024 | OceanSurvivalWind | Use N-001 survival outcomes and the operational wind reference convention. Selected-profile wave, current, temperature and humidity limits apply concurrently.  |
| N-025 | OceanSurvivalWaves | N-001 defines survival outcomes.  |
| N-030 | AirTemperature | N-001/N-035 define operational and survival functions.  |
| N-031 | WaterTemperature | N-001/N-035 define operational and survival functions.  |
| N-033 | Visibility | Exercise daylight and darkness at meteorological visibility of at least 1 km, and detected visibility below 1 km. Traffic performance remains subject to unresolved S-001 scenarios.  |
| N-034 | CalmOperation | Calm-mode functions are navigation, recording and autonomous boundary/traffic contingency. Initial conservative usable energy must cover the reserve plus 24 hours of measured worst-case calm-mode electrical load. R-004 prohibits automatic motor activation in a qualifying attempt.  |
| N-035 | EnvelopeTransition | The trigger is a detected upper operational wind or wave limit exceedance for the selected profile; calm invokes N-034. Resumption eligibility requires 10 continuous minutes inside the selected wind/wave limits, valid navigation and no low-energy, emergency-recovery or isolation restriction.  |
| N-044 | WetMechanicalIntegrity | Evaluate after each selected profile wet-exposure campaign under N-002.  |
| N-045 | WetElectricalIntegrity | Evaluate disconnected cable assemblies after each selected profile wet-exposure campaign under N-002; disconnect electronics for insulation measurement.  |
| N-046 | SolarHeating | Expose the powered vessel to 40 degC ambient air and 1000 W/m2 incident solar irradiance for 8 hours; use the installed battery manufacturer temperature limits.  |
| N-047 | PrintedMaterialAging | Apply 300 MJ/m2 cumulative UV exposure in the 300–400 nm band, then N-041 for Gorge or N-042 for ocean. Dual-profile qualification requires both sequences.  |
| N-051 | SelfRighting | Use minimum and maximum mission loading, five releases at each angle of 90 and 180 degrees toward each side, without external action or motor thrust. Use freshwater for Gorge or 35 g/kg saltwater for ocean; dual qualification requires both media. All leaves apply to every release.  |
| N-052 | CapsizeControlRecovery | Apply to every N-051 release without operator input. Mode-appropriate control does not mean normal sailing before the N-035 resumption gate permits it.  |
| N-053 | SubmergedWeedPassage | Gorge campaign: five consecutive sailing passes without manual clearing or motor use through a 5 m by 1 m patch of 20 flexible branched stems per square metre, each 0.5-1.0 m long, extending from below the deepest appendage to within 0.1 m of the surface. Use 5 m/s mean wind and the weed-free reference heading. Record material, branch geometry, wet bending stiffness and anchoring.  |
| N-054 | WeedSnagShedding | Gorge campaign: drape one wet 1 m branched stem over one appendage leading edge at a time, five repetitions per appendage, with N-053 surrogate characteristics, 5 m/s mean wind and the unobstructed reference heading. No manual assistance or motor use. Both leaf criteria apply to every repetition; visible stem removal alone is insufficient.  |
| N-055 | WeedBlockageResponse | Gorge trigger: vegetation prevents completion of commanded rudder motion for 5 seconds, or keeps water-relative speed below 25 percent of the preceding weed-free 60-second mean for 60 seconds with mean wind at least 3 m/s. Dense mats are a blockage/avoidance case, not a pass-through claim.  |
| N-056 | RecoveryPropulsorWeeds | Use a separately designated Gorge powered-recovery test with five passes through the N-053 patch without manual propulsor clearing, on the weed-free powered reference heading. Exercise locked propulsor separately.  |
| E-008 | NavigationAvailability | Campaigns use 1800 scheduled one-second epochs in 30 minutes, with missing/invalid epochs counted as failures. Fault injection is separate.  |
| R-003 | LaunchEnergyAdmission | Missing, stale or invalid estimates or reserve configuration inhibit start.  |
| R-004 | ChallengeMotorInhibition | Exercise qualifying, nonqualifying and unknown qualification states, restart, link loss, power loss during transitions and conflicting/stale commands. Shared qualification persistence applies before enabling intervention.  |
| E-202 | RepeatableCycleBalance | The repeatability criterion assumes fixed capacity, loads and resource bounds.  |
| E-203 | PeakSupplyCapability | Load power includes conversion losses and the declared uncertainty allowance.  |
| E-204 | HarvestCampaignCoverage | Each modeled day is gap-free; the remaining time has harvesting disabled. Enabling harvesting with zero resource still counts as enabled.  |
| Q-001 | CruisePerformance | The declared route includes sailing legs, current projections, weather holds and maneuvering time. Apply Q-101 through Q-103.  |
| Q-101 | LegProgress | Evaluate sailing-only, loaded configuration under the declared wind, wave, current and fouling profile. Include tacking in water-relative velocity made good. Holds are separate exposure intervals, not discarded samples.  |
| Q-102 | PassageDuration | Passage duration includes every sailing leg, weather hold and maneuver. Qualified duration must come from the same configuration and applicable environment.  |
| Q-103 | CruiseEvidence | Evidence records route distance, wind/sea state, signed along-route current, sailing polar or measured velocity made good, fouling allowance, holds, uncertainty and configuration. No auxiliary propulsion credit for the Gorge challenge.  |
| L-001 | MissionReliability | Apply L-101 through L-104 separately to the Gorge and Hawaii profiles. Failure includes loss of required control, mission completion, safety function or required observation service. Recovery that violates the mission rules is not success.  |
| L-101 | MissionSuccessProbability | Reliability means absence of mission-critical failure over total elapsed exposure, including holds. Statistical evidence must represent the declared configuration, environment and failure definition.  |
| L-102 | FailureRateBudget | The initial constant-hazard model sums non-overlapping independent critical failure rates plus a separately assessed common-cause contribution. Component bounds require a joint-confidence argument; summing individual 95-percent bounds does not establish a system 95-percent bound. Wear, systematic software faults, variable stress and recovery need a different model when this assumption is unsupported.  |
| L-103 | ReliabilityEvidence | Document confidence method, censoring, configuration, mission profile, exposure and observed critical failures. The initial zero-failure demonstration is invalid when failures occurred or the constant-hazard assumption is unsupported.  |
| L-104 | CriticalFailureDisposition | Acceptance requires evidence for prevention, detection and response, or an explicitly reviewed residual risk. The DFMEA starter is incomplete; completing listed rows does not demonstrate hazard coverage.  |

## Rationale

| ID | Requirement | Text |
| --- | --- | --- |
| C-000 | TransGorgeChallenge | The first The Dalles–Bonneville–The Dalles circuit is the threshold; repeated circuits are the endurance objective. |
| H-001 | HawaiiVoyage | The Gorge is a proving ground for the ocean objective, not evidence of ocean readiness. |
| Q-001 | CruisePerformance | Cruise speed determines exposure to failures; water speed alone does not establish route completion. |
| Q-101 | LegProgress | 0.5 m/s is a proposed design target, not a measured capability or a guarantee throughout the survival envelope. |
| Q-102 | PassageDuration | A fast moving-leg average cannot conceal long periods waiting for usable wind. |
| Q-103 | CruiseEvidence | Synthetic inputs support sensitivity analysis only. |
| L-001 | MissionReliability | Longer passages impose tighter reliability budgets; Gorge performance does not qualify an ocean mission. |
| L-101 | MissionSuccessProbability | 0.90 at 95-percent confidence is a proposed engineering target. It is not a measured reliability estimate. |
| L-102 | FailureRateBudget | Use lambda\_max = -ln(0.90)/T. Do not sum DFMEA ordinal rankings or assume missing rates are zero. |
| L-103 | ReliabilityEvidence | A numerical estimate is not a confidence bound; shorter tests cannot establish an indefinite lifetime. |
| L-104 | CriticalFailureDisposition | Potential harm to other waterway users must not be traded against an attractive aggregate reliability score. |

## Explanatory notes

| ID | Requirement | Text |
| --- | --- | --- |
| C-002 | RepeatedOperation | This is an endurance objective, not a finite-duration pass/fail claim.  |
| C-004 | SailingPropulsion | The restriction concerns propulsion, not onboard electrical power.  |
| H-001 | HawaiiVoyage | Gorge-specific challenge rules do not automatically apply to the ocean mission.  |
| M-002 | MultiDayEndurance | Passing this bounded campaign does not establish indefinite energy balance.  |
| N-001 | EnvironmentalEnvelope | Profiles are not interchangeable. Gorge release does not require ocean qualification, and Gorge success does not establish ocean capability.  |
| N-002 | MarineDurability | A derivation does not make every mission-specific descendant applicable to every deployment.  |
| N-003 | StabilityAndFouling | Submerged-weed passage qualification does not cover dense floating mats or fishing-line entanglement.  |
| R-001 | RecoveryPropulsion | This sheltered recovery target is not a storm-recovery guarantee.  |
| R-002 | RecoveryEnergy | R-003 governs launch admission; E-004 governs in-mission reserve crossing.  |
| N-010 | GorgeEnvironment | The profile excludes dam transit, ice and surf-zone launch.  |
| N-020 | OceanEnvironment | This baseline is neither a hurricane-survival claim nor completed route/season qualification.  |
| N-011 | GorgeWind | Wind tolerance does not guarantee upstream progress.  |
| N-013 | GorgeCurrent | Current tolerance does not guarantee progress or station keeping; positive upstream speed is not required at every wind speed or heading.  |
| N-021 | OceanWind | Wind tolerance does not guarantee upstream progress.  |
| N-023 | OceanCurrent | Current tolerance does not guarantee progress or station keeping; positive upstream speed is not required at every wind speed or heading.  |
| N-034 | CalmOperation | Neither progress nor station keeping is required.  |
| N-042 | SaltwaterExposure | The exposure campaign does not establish the eventual passage duration.  |
| E-200 | SustainedEnergyFeasibility | A 72-hour energy demonstration does not prove indefinite weather availability, functional performance or ocean readiness.  |
| E-201 | SustainedReserveProtection | Unmodeled intrainterval dips are outside the analysis claim.  |
| E-202 | RepeatableCycleBalance | This conditional result is not an indefinite-endurance verdict.  |

## Open issues

| ID | Requirement | Text |
| --- | --- | --- |
| C-001 | CourseCompletion | Start/finish and turnaround gates, permitted corridor and crossing evidence remain to be agreed. |
| C-002 | RepeatedOperation | No fixed objective endurance duration has been selected. |
| C-003 | UnassistedAttempt | Restart criteria remain to be agreed. |
| C-005 | LiveObservation | Challenge-level coverage, update rate and outage-retention criteria remain to be agreed; vehicle design targets do not amend the challenge automatically. |
| C-006 | EmergencyIntervention | Challenge-level abort and recovery procedures remain to be agreed. |
| H-001 | HawaiiVoyage | Departure point, destination gate, route, duration, route/season suitability of the candidate ocean envelope, assistance/propulsion rules and acceptance evidence remain to be agreed. |
| S-001 | TrafficSafety | Detection ranges, target signatures, closest-approach margins and maneuver feasibility remain unresolved acceptance parameters; tracking and avoidance cannot receive complete passes until these are frozen. |
| N-053 | SubmergedWeedPassage | Equivalence of the vegetation surrogate to local milfoil requires physical-test validation. |
| Q-101 | LegProgress | Proposed target pending design review and mission-profile selection. |
| L-101 | MissionSuccessProbability | Proposed target pending design review and mission-profile selection. |

## Verification specifications

| shortName | name | documentation | Verifies |
| --- | --- | --- | --- |
| V-M-001 | RoundTripVerification | Apply the M-001 qualification conditions. Use the timestamped trajectory and intervention/propulsion log. Missing gate crossings or disqualifying events prevent a completion verdict. | roundTrip |
| V-M-002 | MultiDayEnduranceVerification | Apply the M-002 qualification conditions. Record initial battery state, harvester configuration, resource profile, harvested energy and loads. Limit input to installed-harvester output measured under a frozen, recorded resource profile; any test supply replay must not exceed measured power or accumulated energy. Absent profile evidence invalidates the test. | multiDayEndurance |
| V-E-001 | EnergyAwarenessVerification | Apply the E-001 qualification conditions. Assess every applicable acceptance outcome separately: E-101, E-102, E-103, E-104. | energyAwareness, energyEstimateCadence, reserveEstimateCadence, energyEstimateAccuracy, conservativeEnergyEstimate |
| V-E-002 | NavigationAndControlVerification | Apply the E-002 qualification conditions. Assess every applicable acceptance outcome separately: E-105, E-106, E-107, E-108, E-109. | navigationAndControl, guidanceUpdateCadence, sailCommandCadence, steeringCommandCadence, positionAccuracy, headingAccuracy |
| V-E-003 | ResetRecoveryVerification | Apply the E-003 qualification conditions. Assess every applicable acceptance outcome separately: E-110, E-111, E-112, E-113, E-145, E-136, E-139, E-138, R-102, R-101. | resetRecovery, restartDeadline, missionStateRestoration, gateProgressRestoration, resetRestrictionPreservation, qualificationRestoration, logInterruptionDurability, unknownQualificationFallback, qualificationPersistence, freshRecoveryCommand, motorQualificationInvariant |
| V-E-004 | LowEnergyRecoveryVerification | Apply the E-004 qualification conditions. Assess every applicable acceptance outcome separately: E-114, E-115, E-116, E-117, E-118, E-119, E-130, E-120, E-132, R-101. | lowEnergyRecovery, lowEnergyEntry, lowEnergyPayloadInhibition, lowEnergyNavigationContinuity, lowEnergyCollisionContinuity, lowEnergyExit, payloadRestartPermission, periodicLogCadence, telemetryDeliveryCadence, criticalEventRecording, motorQualificationInvariant |
| V-E-005 | CommunicationsVerification | Apply the E-005 qualification conditions. Assess every applicable acceptance outcome separately: E-120, E-121, E-122, E-123, E-124, E-131, E-137. | communications, telemetryDeliveryCadence, outageAutonomy, reconnectCurrentRecord, backlogOrdering, backlogCurrentPriority, logRetention, reconnectLogPreservation |
| V-E-006 | IngressResponseVerification | Apply the E-006 qualification conditions. Assess every applicable acceptance outcome separately: E-125, E-126, E-127, E-128, E-129, E-144, E-132, R-101. | ingressResponse, ingressDetection, ingressRecoveryRequest, ingressFlotation, ingressElectronicsProtection, ingressPositionContinuity, ingressEventDeadline, criticalEventRecording, motorQualificationInvariant |
| V-E-007 | MissionEvidenceVerification | Apply the E-007 qualification conditions. Assess every applicable acceptance outcome separately: E-130, E-131, E-132, E-133, E-134, E-135, E-136, E-137, E-138, E-139. | missionEvidence, periodicLogCadence, logRetention, criticalEventRecording, logTimestampAccuracy, invalidTimestampMarking, logGapIndication, logInterruptionDurability, reconnectLogPreservation, qualificationPersistence, unknownQualificationFallback |
| V-P-001 | TransportabilityVerification | Apply the P-001 qualification conditions. Assess every applicable acceptance outcome separately: P-101, P-102, P-103, P-104, P-105, P-106. | transportability, soloTransport, liftMass, setupDuration, packDuration, soloLaunch, soloRetrieval |
| V-P-002 | DesktopManufactureVerification | Apply the P-002 qualification conditions. Compare slicer/job-envelope measurements for every job with the 250 × 250 × 250 mm usable Cartesian travel; raw part volume is insufficient. | desktopManufacture |
| V-P-003 | ServiceabilityVerification | Apply the P-003 qualification conditions. Assess every applicable acceptance outcome separately: P-107, P-108, P-109, P-110. | serviceability, replacementDuration, nondestructiveService, postServiceSealing, postServiceActuation |
| V-S-001 | TrafficSafetyVerification | Apply the S-001 qualification conditions. Assess every applicable acceptance outcome separately: S-101, S-102, S-103, S-104. | trafficSafety, trafficTracking, collisionAssessmentCadence, avoidanceCommandDeadline, trafficAwarenessFault |
| V-S-002 | OperatingBoundaryVerification | Apply the S-002 qualification conditions. Assess every applicable acceptance outcome separately: S-105, S-106, S-107, S-108, S-109. | operatingBoundary, boundaryEvaluationCadence, boundaryAvoidanceDeadline, boundaryAvoidanceRecording, boundaryStartInhibition, boundaryDegradedEvidence |
| V-S-003 | SafeRecoveryVerification | Apply the S-003 qualification conditions. Assess every applicable acceptance outcome separately: S-110, S-111, S-112, S-113, S-114, S-115, E-138, R-101, E-130. | safeRecovery, abortLatchDeadline, recoveryTelemetryCadence, motorIsolationDeadline, isolationRestartInhibition, manualControlLossShutdown, controlLossLocationContinuity, qualificationPersistence, motorQualificationInvariant, periodicLogCadence |
| V-S-004 | NavigationConspicuityVerification | Apply the S-004 qualification conditions. Assess every applicable acceptance outcome separately: S-116, S-117, S-118, S-119, S-120, S-121. | navigationConspicuity, navigationLightPresentation, navigationShapePresentation, navigationSoundPresentation, signalingModeDeadline, signalingFaultRecording, signalingFaultReporting |
| V-S-005 | RegulatoryClassificationVerification | Apply the S-005 qualification conditions. Assess every applicable acceptance outcome separately: S-122, S-123. | regulatoryClassification, deploymentComplianceRecord, deploymentReleaseGate |
| V-N-001 | EnvironmentalEnvelopeVerification | Apply the N-001 qualification conditions. Exercise operational functions concurrently during profile qualification. | environmentalEnvelope |
| V-N-002 | MarineDurabilityVerification | Apply the N-002 qualification conditions. Perform post-exposure functional checks for the selected profile. | marineDurability |
| V-R-001 | RecoveryPropulsionVerification | Apply the R-001 qualification conditions. Measure track, current and electrical power. | recoveryPropulsion |
| V-R-002 | RecoveryEnergyVerification | Apply the R-002 qualification conditions. Measure motor and essential powers; characterize available battery energy at the lowest operating battery temperature and end-of-service capacity. | recoveryEnergy |
| V-C-101 | TelemetryEquipmentVerification | Apply the C-101 qualification conditions. Assess every applicable acceptance outcome separately: C-201, C-202, C-203, C-204. | telemetryEquipment, telemetryDisplayContent, telemetryStaleIndication, telemetryIdentityPreservation, telemetryDuplicateSuppression |
| V-C-102 | CommandIntegrityVerification | Apply the C-102 qualification conditions. Assess every applicable acceptance outcome separately: C-205, C-206, C-207, C-208, C-209, C-210, C-211, E-132, E-138. | commandIntegrity, unauthenticatedCommandRejection, replayCommandRejection, expiredCommandRejection, acceptedCommandDeadline, onboardAcknowledgmentDeadline, acknowledgmentQueueing, externalControlDisqualification, criticalEventRecording, qualificationPersistence |
| V-N-011 | GorgeWindVerification | Apply the N-011 qualification conditions. Include upwind, crosswind and downwind headings. | gorgeWind |
| V-N-012 | GorgeWavesVerification | Apply the N-012 qualification conditions. Include head, beam and following seas and physically realizable wind-wave-current combinations within the selected profile. | gorgeWaves |
| V-N-013 | GorgeCurrentVerification | Apply the N-013 qualification conditions. Include opposing current. | gorgeCurrent |
| V-N-015 | GorgeSurvivalWavesVerification | Apply the N-015 qualification conditions. Include adverse relative directions and physically realizable combinations with profile survival wind and current. | gorgeSurvivalWaves |
| V-N-021 | OceanWindVerification | Apply the N-021 qualification conditions. Include upwind, crosswind and downwind headings. | oceanWind |
| V-N-022 | OceanWavesVerification | Apply the N-022 qualification conditions. Include head, beam and following seas and physically realizable wind-wave-current combinations within the selected profile. | oceanWaves |
| V-N-023 | OceanCurrentVerification | Apply the N-023 qualification conditions. Include opposing current. | oceanCurrent |
| V-N-025 | OceanSurvivalWavesVerification | Apply the N-025 qualification conditions. Include adverse relative directions and physically realizable combinations with profile survival wind and current. | oceanSurvivalWaves |
| V-N-030 | AirTemperatureVerification | Apply the N-030 qualification conditions. Test powered cold and hot endpoints after internal temperatures stabilize to less than 1 degC change per hour; operate for 2 hours at each endpoint. | airTemperature |
| V-N-031 | WaterTemperatureVerification | Apply the N-031 qualification conditions. Operate for 2 hours at each endpoint after thermal stabilization. | waterTemperature |
| V-N-032 | HumidityVerification | Apply the N-032 qualification conditions. Apply three powered 24-hour cycles between 10 and 40 degC at at least 95 percent relative humidity. Produce visible external condensation during cooling; no liquid water may reach enclosed electronics. | humidity |
| V-N-033 | VisibilityVerification | Apply the N-033 qualification conditions. Assess every applicable acceptance outcome separately: N-101, N-102, N-103, N-104, N-105. | visibility, visibilityNavigationCapability, visibilityTrafficCapability, restrictedVisibilityEntry, restrictedVisibilityEvidence, restrictedVisibilityCollisionAssessment |
| V-N-034 | CalmOperationVerification | Apply the N-034 qualification conditions. Record initial energy, the load measurement and the full energy history. | calmOperation |
| V-N-035 | EnvelopeTransitionVerification | Apply the N-035 qualification conditions. Assess every applicable acceptance outcome separately: N-106, N-107, N-108, N-109, N-110, E-130, R-101. | envelopeTransition, survivalEntryDeadline, survivalTransitionRecording, sailingResumptionDeadline, sailingResumptionInhibition, resumptionBlockEvidence, periodicLogCadence, motorQualificationInvariant |
| V-N-044 | WetMechanicalIntegrityVerification | Apply the N-044 qualification conditions. Assess every applicable acceptance outcome separately: N-111, N-112. | wetMechanicalIntegrity, wetMechanismTravel, wetJointIntegrity |
| V-N-045 | WetElectricalIntegrityVerification | Apply the N-045 qualification conditions. Assess every applicable acceptance outcome separately: N-113, N-114. | wetElectricalIntegrity, wetConductorResistance, wetInsulationResistance |
| V-N-046 | SolarHeatingVerification | Apply the N-046 qualification conditions. Assess every applicable acceptance outcome separately: N-115, N-116, N-117. | solarHeating, hotSunElectronicsOperation, hotSunBatteryTemperature, batteryChargeTemperatureInhibition |
| V-N-047 | PrintedMaterialAgingVerification | Apply the N-047 qualification conditions. Compare the lowest failure loads of five aged and five unaged coupons with identical geometry, material, print orientation and process, using the same fixture and loading rate. | printedMaterialAging |
| V-N-051 | SelfRightingVerification | Apply the N-051 qualification conditions. Assess every applicable acceptance outcome separately: N-118, N-119, N-120, N-121. | selfRighting, rightingDeadline, capsizeRigRetention, capsizeBallastRetention, capsizeElectronicsSealing |
| V-N-052 | CapsizeControlRecoveryVerification | Apply the N-052 qualification conditions. Assess every applicable acceptance outcome separately: N-122, N-123, N-124, N-125. | capsizeControlRecovery, controlRecoveryDeadline, capsizeGateProgressRetention, capsizeQualificationRetention, capsizeRestrictionRetention |
| V-N-053 | SubmergedWeedPassageVerification | Apply the N-053 qualification conditions. Assess every applicable acceptance outcome separately: N-126, N-127. | submergedWeedPassage, weedPassageSpeed, weedPassageSteering |
| V-N-054 | WeedSnagSheddingVerification | Apply the N-054 qualification conditions. Assess every applicable acceptance outcome separately: N-128, N-129. | weedSnagShedding, weedSnagSpeedRecovery, weedSnagSteeringRecovery |
| V-N-055 | WeedBlockageResponseVerification | Apply the N-055 qualification conditions. Assess every applicable acceptance outcome separately: N-130, N-131, N-132, R-101. | weedBlockageResponse, weedBlockageFault, weedBlockageContingency, weedBlockageLocation, motorQualificationInvariant |
| V-N-056 | RecoveryPropulsorWeedsVerification | Apply the N-056 qualification conditions. Assess every applicable acceptance outcome separately: N-133, N-134, N-135, N-136, R-101. | recoveryPropulsorWeeds, poweredWeedSpeed, poweredWeedCurrent, poweredWeedTemperature, lockedPropulsorShutdown, motorQualificationInvariant |
| V-E-008 | NavigationAvailabilityVerification | Apply the E-008 qualification conditions. Assess every applicable acceptance outcome separately: E-140, E-141, E-142, E-143, E-132. | navigationAvailability, navigationValidEpochs, staleNavigationInvalidation, navigationDegradedTransition, staleNavigationUseInhibition, criticalEventRecording |
| V-R-003 | LaunchEnergyAdmissionVerification | Apply the R-003 qualification conditions. Inject below-reserve, equal-reserve, above-reserve and missing, invalid or stale inputs. | launchEnergyAdmission |
| V-R-004 | ChallengeMotorInhibitionVerification | Apply the R-004 qualification conditions. Assess every applicable acceptance outcome separately: R-101, R-102, E-138, E-132. | challengeMotorInhibition, motorQualificationInvariant, freshRecoveryCommand, qualificationPersistence, criticalEventRecording |
| V-E-201 | SustainedReserveProtectionVerification | Apply the E-201 qualification conditions. For piecewise-constant net power, check the initial state and every interval endpoint. | sustainedReserveProtection |
| V-E-205 | EnergyEvidenceReadinessVerification | Apply the E-205 qualification conditions. Use the sustained-operations evidence checklist. | energyEvidenceReadiness |
| V-L-104 | FailureDispositionVerification | Review the architecture DFMEA, coverage, accepted mitigations, residual-risk approvals and evidence before launch. The starter list is not complete hazard coverage. | criticalFailureDisposition |
|  | VoyageReliabilityVerification |  | missionSuccessProbability, failureRateBudget, reliabilityEvidence, legProgress, passageDuration, cruiseEvidence |
