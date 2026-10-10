# Requirement derivation register

[Qualification conditions, rationale, open issues and verification specifications](<requirements-context.md>)

Generated natively by OpenSysML from the project models. Status describes work on the model element, not verification. Derivations record design reasoning, not proof of satisfaction.

## Requirements

| ID | Requirement | Status | Statement |
| --- | --- | --- | --- |
| C-000 | TransGorgeChallenge | open | The vessel shall complete the Trans-Gorge challenge under C-001 through C-006. |
| C-001 | CourseCompletion | open | The vessel shall complete a journey from The Dalles to Bonneville and back to The Dalles. |
| C-002 | RepeatedOperation | open | After its first circuit, the vessel should repeat The Dalles–Bonneville–The Dalles autonomously for as long as practical. |
| C-003 | UnassistedAttempt | open | A qualifying attempt shall complete the round trip without operator intervention. |
| C-004 | SailingPropulsion | open | A qualifying attempt shall use sailing propulsion without auxiliary motor propulsion. |
| C-005 | LiveObservation | open | The vessel shall provide live monitoring with autonomous operation and retained telemetry across communication outages. |
| C-006 | EmergencyIntervention | open | The vessel shall permit remote emergency abort or manual control when a command link is available. |
| H-001 | HawaiiVoyage | open | The vessel shall complete an autonomous sailing voyage to Hawaii. |
| M-001 | RoundTrip | open | The vessel shall cross the configured The Dalles departure, Bonneville turnaround and The Dalles return gates in order during one qualifying attempt. |
| M-002 | MultiDayEndurance | open | The vessel shall operate for 72 continuous hours without servicing or external charging under the specified Gorge energy campaign. |
| E-001 | EnergyAwareness | open | The vessel shall maintain conservative estimates of usable energy and protected recovery reserve. |
| E-002 | NavigationAndControl | open | The vessel shall provide autonomous navigation and sail/steering control within the selected operational profile. |
| E-003 | ResetRecovery | open | The vessel shall restore mode-appropriate autonomous operation after a watchdog reset. |
| E-004 | LowEnergyRecovery | open | The vessel shall protect essential functions when conservative usable energy reaches the recovery reserve. |
| E-005 | Communications | open | The vessel shall support live telemetry through link outages and reconnection. |
| E-006 | IngressResponse | open | The vessel shall retain recoverability during the specified hull-ingress qualification. |
| E-007 | MissionEvidence | open | The vessel shall retain time-correlated mission evidence through communication and power interruptions. |
| P-001 | Transportability | open | The vessel shall support transport, assembly, launch and retrieval by one adult under the specified handling conditions. |
| P-002 | DesktopManufacture | open | Every print job shall fit within positive X, Y and Z extents no greater than 250 mm each. |
| P-003 | Serviceability | open | The vessel shall support replacement of serviceable equipment without structural damage. |
| S-001 | TrafficSafety | open | The vessel shall assess and respond to collision risks within the deployment-specific traffic envelope. |
| S-002 | OperatingBoundary | open | The vessel shall enforce the configured operating boundaries. |
| S-003 | SafeRecovery | open | The vessel shall support controlled emergency intervention and powered recovery. |
| S-004 | NavigationConspicuity | open | The vessel shall present the navigation signals required for its operating mode. |
| S-005 | RegulatoryClassification | open | Deployment shall require documented compliance with applicable navigation, radio and authorization obligations. |
| N-001 | EnvironmentalEnvelope | open | The vessel shall retain the functions required by its selected environmental profile and operating mode. |
| N-002 | MarineDurability | open | The vessel shall retain required function and structural integrity through its selected wet-exposure campaign. |
| N-003 | StabilityAndFouling | open | The vessel shall autonomously tolerate capsize and submerged aquatic vegetation, including milfoil-like stems. |
| R-001 | RecoveryPropulsion | open | At maximum mission load, powered recovery shall sustain at least 0.5 m/s over ground for 30 minutes against a 1.5 m/s current. |
| R-002 | RecoveryEnergy | open | The protected reserve shall equal or exceed 1.2 × (30 minutes of worst-case recovery motor demand + 2 hours of essential recovery demand). |
| C-101 | TelemetryEquipment | open | The shore endpoint shall present current vessel telemetry with explicit data age and identity. |
| C-102 | CommandIntegrity | open | The vessel shall accept external commands only under the specified authentication, freshness and qualification rules. |
| N-010 | GorgeEnvironment | open | The vessel shall operate in the freshwater Columbia River reach between The Dalles and Bonneville, including opposing wind/current, short chop, traffic and submerged vegetation. |
| N-020 | OceanEnvironment | open | The vessel shall operate on a northeast Pacific passage toward Hawaii amid saltwater, ocean swell, wind seas and prolonged unattended exposure. |
| N-011 | GorgeWind | open | The vessel shall retain operational functions in 3–15 m/s mean true wind with 3-second gusts up to 20 m/s. |
| N-012 | GorgeWaves | open | The vessel shall retain operational functions in significant wave heights up to 1 m, peak periods 2–5 s and individual waves up to 2 m. |
| N-013 | GorgeCurrent | open | The vessel shall retain navigation and control in currents from 0 to 1.5 m/s from any direction relative to wind and waves. |
| N-014 | GorgeSurvivalWind | open | The vessel shall retain survival functions for 24 continuous hours in mean wind up to 25 m/s and 3-second gusts up to 35 m/s. |
| N-015 | GorgeSurvivalWaves | open | The vessel shall retain survival functions for 24 continuous hours in significant wave heights up to 2 m, peak periods 3–7 s and individual waves up to 4 m. |
| N-021 | OceanWind | open | The vessel shall retain operational functions in 3–15 m/s mean true wind with 3-second gusts up to 20 m/s. |
| N-022 | OceanWaves | open | The vessel shall retain operational functions in significant wave heights up to 3 m, peak periods 5–20 s and individual waves up to 6 m. |
| N-023 | OceanCurrent | open | The vessel shall retain navigation and control in currents from 0 to 1.0 m/s from any direction relative to wind and waves. |
| N-024 | OceanSurvivalWind | open | The vessel shall retain survival functions for 24 continuous hours in mean wind up to 25 m/s and 3-second gusts up to 35 m/s. |
| N-025 | OceanSurvivalWaves | open | The vessel shall retain survival functions for 24 continuous hours in significant wave heights up to 6 m, peak periods 6–20 s and individual waves up to 12 m. |
| N-030 | AirTemperature | open | The vessel shall retain mode-appropriate functions at ambient air temperatures from 0 to 40 degC. |
| N-031 | WaterTemperature | open | Immersed hull, appendages and equipment shall retain mode-appropriate functions in water from 2 to 30 degC. |
| N-032 | Humidity | open | Installed equipment shall retain operational functions at 0–100 percent relative humidity, including condensation. |
| N-033 | Visibility | open | The vessel shall provide mode-appropriate navigation and traffic response across the specified visibility conditions. |
| N-034 | CalmOperation | open | With harvesting disabled and mean wind below 3 m/s, the vessel shall retain calm-mode functions above the R-002 reserve for 24 continuous hours. |
| N-035 | EnvelopeTransition | open | The vessel shall select survival or sailing operation according to the defined environmental transition conditions. |
| N-041 | FreshwaterExposure | open | For Gorge qualification, following 72 hours continuous freshwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its Gorge functional checks without repair or servicing. |
| N-042 | SaltwaterExposure | open | For ocean qualification, following 30 days continuous 35 g/kg saltwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its ocean functional checks without repair or servicing. |
| N-043 | EnclosureSealing | open | Before and after each wet-exposure campaign, installed electronics enclosures, connectors and penetrations shall show no detectable liquid ingress on dry internal water-sensitive indicators after 30 minutes immersion with their highest point 1 m below the water surface. |
| N-044 | WetMechanicalIntegrity | open | External mechanisms and structural joints shall retain integrity after the selected wet-exposure campaign. |
| N-045 | WetElectricalIntegrity | open | Cable assemblies shall retain electrical integrity after the selected wet-exposure campaign. |
| N-046 | SolarHeating | open | The vessel shall retain safe powered operation during the specified solar-heating exposure. |
| N-047 | PrintedMaterialAging | open | Printed structural material shall retain at least 80 percent of unaged failure load after the specified UV and wet-exposure sequence. |
| N-051 | SelfRighting | open | The vessel shall recover from the specified capsize releases without external assistance or motor thrust. |
| N-052 | CapsizeControlRecovery | open | The vessel shall restore mode-appropriate control after each specified capsize release. |
| N-053 | SubmergedWeedPassage | open | The vessel shall tolerate submerged milfoil-like vegetation during the specified unassisted Gorge sailing passes. |
| N-054 | WeedSnagShedding | open | The vessel shall recover sailing performance after the specified appendage weed snags without assistance or motor use. |
| N-055 | WeedBlockageResponse | open | The vessel shall enter autonomous fouling contingency when the defined weed-blockage trigger occurs. |
| N-056 | RecoveryPropulsorWeeds | open | The recovery propulsion system shall tolerate the specified weed encounters within its rated electrical and thermal limits. |
| E-008 | NavigationAvailability | open | The vessel shall maintain valid navigation inputs and reject stale observations. |
| R-003 | LaunchEnergyAdmission | open | Mission start shall remain inhibited unless a valid usable-energy estimate no older than 1 second strictly exceeds a valid R-002 protected reserve. |
| R-004 | ChallengeMotorInhibition | open | The vessel shall prevent motor propulsion from qualifying as unassisted sailing. |
| E-101 | EnergyEstimateCadence | open | The vessel shall refresh usable battery-energy estimates at least once per second. |
| E-102 | ReserveEstimateCadence | open | The vessel shall refresh protected recovery-reserve estimates at least once per second. |
| E-103 | EnergyEstimateAccuracy | open | Usable-energy estimation error shall not exceed 10 percent of measured usable full-charge energy relative to calibrated charge/discharge integration across operating battery temperatures. |
| E-104 | ConservativeEnergyEstimate | open | The usable-energy input to admission and low-energy decisions shall equal estimated usable energy minus the EnergyEstimateAccuracy error allowance. |
| E-105 | GuidanceUpdateCadence | open | During operational qualification, mission guidance shall update at least once per second. |
| E-106 | SailCommandCadence | open | During operational qualification, commanded sail position shall update at least once per second. |
| E-107 | SteeringCommandCadence | open | During operational qualification, commanded steering position shall update at least once per second. |
| E-108 | PositionAccuracy | open | At every epoch in the common E-002 acceptance set, valid position error shall be at most 10 m against an independent reference. |
| E-109 | HeadingAccuracy | open | At every epoch in the common E-002 acceptance set, valid heading error shall be at most 10 degrees against an independent reference. |
| E-110 | RestartDeadline | open | After a watchdog reset under E-003 preconditions, the vessel shall restore mode-appropriate autonomous control within 30 seconds. |
| E-111 | MissionStateRestoration | open | Within 30 seconds after a watchdog reset under E-003 preconditions, restored mission mode shall equal the last persisted mode. |
| E-112 | GateProgressRestoration | open | Within 30 seconds after a watchdog reset under E-003 preconditions, restored gate progress shall equal the last persisted gate progress. |
| E-113 | ResetRestrictionPreservation | open | After watchdog reset, each active survival, low-energy, recovery and isolation restriction shall remain effective until its own release condition is met. |
| E-114 | LowEnergyEntry | open | When conservative usable energy reaches or falls below protected reserve, the vessel shall set the low-energy flag within 5 seconds. |
| E-115 | LowEnergyPayloadInhibition | open | While the low-energy flag is set, the optional observation payload shall be disabled. |
| E-116 | LowEnergyNavigationContinuity | open | While the low-energy flag is set, autonomous navigation shall remain active. |
| E-117 | LowEnergyCollisionContinuity | open | While the low-energy flag is set, collision-response behavior shall remain active. |
| E-118 | LowEnergyExit | open | After conservative usable energy exceeds 1.2 times protected reserve for 10 continuous minutes, the vessel shall clear the low-energy flag independently of survival/recovery flags. |
| E-119 | PayloadRestartPermission | open | Payload operation shall remain inhibited whenever a low-energy, survival or recovery restriction is active. |
| E-120 | TelemetryDeliveryCadence | open | With a functioning link, current telemetry delivery intervals shall not exceed 60 seconds, except that low-energy operation without emergency/powered recovery permits 300 seconds. |
| E-121 | OutageAutonomy | open | Through a 24-hour telemetry-link outage, autonomous mission control shall continue without operator intervention. |
| E-122 | ReconnectCurrentRecord | open | After link restoration, a current telemetry record shall arrive within the active TelemetryDeliveryCadence interval. |
| E-123 | BacklogOrdering | open | After reconnection, retained backlog records shall be transmitted in ascending acquisition sequence order. |
| E-124 | BacklogCurrentPriority | open | During backlog transfer, current telemetry shall continue to meet TelemetryDeliveryCadence. |
| E-125 | IngressDetection | open | In the E-006 injection test, ingress detection shall occur within 60 seconds of injection starting. |
| E-126 | IngressRecoveryRequest | open | In the E-006 test, ingress detection shall set the recovery-request state. |
| E-127 | IngressFlotation | open | In the E-006 test, the vessel shall remain afloat for the full 30 minutes. |
| E-128 | IngressElectronicsProtection | open | After the E-006 test, enclosed-electronics water-sensitive indicators shall show no liquid ingress. |
| E-129 | IngressPositionContinuity | open | Throughout the E-006 test with a functioning link, position reporting shall meet the active TelemetryDeliveryCadence. |
| E-130 | PeriodicLogCadence | open | Periodic mission records shall be acquired at least once per second normally and once per minute in low-energy or survival operation. |
| E-131 | LogRetention | open | Acquired mission records shall remain retrievable onboard for at least 30 days. |
| E-132 | CriticalEventRecording | open | Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence. |
| E-133 | LogTimestampAccuracy | open | With valid GNSS time, mission-record timestamps shall differ from reference UTC by at most 1 second. |
| E-134 | InvalidTimestampMarking | open | Each record acquired without valid time shall carry an invalid-time indication. |
| E-135 | LogGapIndication | open | Each detected missing sequence of scheduled records shall have a gap indication in retrieved data. |
| E-136 | LogInterruptionDurability | open | After watchdog reset or abrupt power removal, every record older than 5 seconds before interruption shall remain readable. |
| E-137 | ReconnectLogPreservation | open | Communication reconnection shall not delete retained mission records. |
| E-138 | QualificationPersistence | open | Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable. |
| E-139 | UnknownQualificationFallback | open | On restart with absent or inconsistent persisted qualification state, the vessel shall adopt nonqualifying status. |
| E-140 | NavigationValidEpochs | open | In each E-008 campaign, at least 1710 of 1800 scheduled epochs shall contain valid position and heading observations. |
| E-141 | StaleNavigationInvalidation | open | Navigation observations older than 5 seconds shall be marked invalid. |
| E-142 | NavigationDegradedTransition | open | When position or heading becomes invalid due to age, the vessel shall enter navigation-degraded state within 1 second. |
| E-143 | StaleNavigationUseInhibition | open | The controller shall not use observations marked invalid as current navigation inputs. |
| P-101 | SoloTransport | open | One adult shall move all mission equipment 100 m without assistance. |
| P-102 | LiftMass | open | Each separately lifted assembly shall have a mass no greater than 15 kg. |
| P-103 | SetupDuration | open | One adult shall assemble the vessel from its transport configuration within 30 minutes. |
| P-104 | PackDuration | open | One adult shall pack the vessel into its transport configuration within 30 minutes. |
| P-105 | SoloLaunch | open | One adult shall launch the assembled vessel without assistance. |
| P-106 | SoloRetrieval | open | One adult shall retrieve the vessel from the water without assistance. |
| P-107 | ReplacementDuration | open | Each P-003 replacement shall take no more than 30 minutes. |
| P-108 | NondestructiveService | open | Each P-003 replacement shall leave bonded structural joints and adjacent parts intact. |
| P-109 | PostServiceSealing | open | After each P-003 replacement, the assembly shall meet the N-043 immersion criterion. |
| P-110 | PostServiceActuation | open | After each P-003 replacement, affected actuators shall complete their full commanded travel. |
| S-101 | TrafficTracking | open | The vessel shall maintain a track for every encounter target within the frozen S-001 detection envelope. |
| S-102 | CollisionAssessmentCadence | open | The vessel shall update collision-risk estimates at least once per second. |
| S-103 | AvoidanceCommandDeadline | open | The vessel shall issue the prescribed avoiding-action command within 2 seconds of each S-001 collision-risk trigger. |
| S-104 | TrafficAwarenessFault | open | After traffic assessment has been invalid for more than 5 seconds, the vessel shall log a traffic-awareness fault within 1 second. |
| S-105 | BoundaryEvaluationCadence | open | The vessel shall evaluate its current position and predicted trajectory against the S-002 polygons at least once per second. |
| S-106 | BoundaryAvoidanceDeadline | open | The vessel shall issue an avoidance command within 2 seconds of predicting a boundary crossing. |
| S-107 | BoundaryAvoidanceRecording | open | Every boundary-avoidance command shall have a corresponding event record. |
| S-108 | BoundaryStartInhibition | open | Missing or geometrically invalid boundaries shall inhibit mission start. |
| S-109 | BoundaryDegradedEvidence | open | Navigation loss or absence of a feasible maneuver shall produce an explicit degraded-route verdict instead of a safe-route verdict. |
| S-110 | AbortLatchDeadline | open | After accepting emergency abort, the vessel shall latch the attempt as disqualified within 1 second. |
| S-111 | RecoveryTelemetryCadence | open | During active emergency or powered recovery with a functioning link, the vessel shall deliver position telemetry at least once per 60 seconds, including low-energy operation. |
| S-112 | MotorIsolationDeadline | open | A physically accessible local isolation control shall remove motor power within 1 second of activation. |
| S-113 | IsolationRestartInhibition | open | Motor restart shall remain inhibited after local isolation until deliberate local reset. |
| S-114 | ManualControlLossShutdown | open | After remote control has been lost for 5 seconds during manual powered recovery, the vessel shall command zero thrust within a further 1 second. |
| S-115 | ControlLossLocationContinuity | open | Location reporting shall continue at the active telemetry cadence after remote-control loss whenever a telemetry link is available. |
| S-116 | NavigationLightPresentation | open | The vessel shall present the lights prescribed for its current mode by the S-004 compliance matrix without a person aboard. |
| S-117 | NavigationShapePresentation | open | The vessel shall present the shapes prescribed for its current mode by the S-004 compliance matrix without a person aboard. |
| S-118 | NavigationSoundPresentation | open | The vessel shall present the sound signals prescribed for its current mode by the S-004 compliance matrix without a person aboard. |
| S-119 | SignalingModeDeadline | open | A commanded mode change shall select the corresponding signaling configuration within 1 second. |
| S-120 | SignalingFaultRecording | open | Each detectable signaling failure shall be logged within 5 seconds of detection. |
| S-121 | SignalingFaultReporting | open | With a functioning link, each detected signaling failure shall be reported to shore within 5 seconds. |
| S-122 | DeploymentComplianceRecord | open | Each deployment shall have a dated compliance record identifying the craft, dimensions, waters, operating modes, applicable navigation and radio obligations, and permission evidence. |
| S-123 | DeploymentReleaseGate | open | Deployment release shall be withheld while any mandatory authorization is absent, expired or unresolved. |
| C-201 | TelemetryDisplayContent | open | The shore endpoint shall display UTC sample time, position, mode, conservative usable energy, reserve, faults and age from each current telemetry record. |
| C-202 | TelemetryStaleIndication | open | The shore endpoint shall indicate stale data when record age exceeds its C-101 mode threshold until receipt of a record within its applicable threshold. |
| C-203 | TelemetryIdentityPreservation | open | The shore endpoint shall preserve received record identity and sequence numbers across the C-101 outage/reconnection test. |
| C-204 | TelemetryDuplicateSuppression | open | The shore endpoint shall not present a duplicate telemetry record as a new observation. |
| C-205 | UnauthenticatedCommandRejection | open | Commands failing authentication shall cause zero accepted actuator or mission-state changes. |
| C-206 | ReplayCommandRejection | open | Commands with previously used sequence numbers shall cause zero accepted actuator or mission-state changes. |
| C-207 | ExpiredCommandRejection | open | Commands older than 30 seconds shall cause zero accepted actuator or mission-state changes. |
| C-208 | AcceptedCommandDeadline | open | An accepted abort or mode-change command shall be applied within 1 second of complete receipt. |
| C-209 | OnboardAcknowledgmentDeadline | open | An accepted abort or mode-change command shall be acknowledged onboard within 1 second of complete receipt. |
| C-210 | AcknowledgmentQueueing | open | An accepted command acknowledgment shall enter the transmit queue in the same command-processing cycle when a link is available. |
| C-211 | ExternalControlDisqualification | open | Acceptance of external mission or steering control during a qualifying attempt shall permanently disqualify that attempt. |
| N-101 | VisibilityNavigationCapability | open | Navigation shall meet E-002 and E-008 acceptance criteria at visibility of at least 1 km in daylight and darkness. |
| N-102 | VisibilityTrafficCapability | open | Traffic assessment shall meet the frozen S-001 criteria at visibility of at least 1 km in daylight and darkness. |
| N-103 | RestrictedVisibilityEntry | open | On detecting visibility below 1 km, the vessel shall enter restricted-visibility state within 60 seconds. |
| N-104 | RestrictedVisibilityEvidence | open | Restricted-visibility operation shall be recorded as outside the normal operational envelope. |
| N-105 | RestrictedVisibilityCollisionAssessment | open | Collision assessment shall remain active during restricted-visibility operation. |
| N-106 | SurvivalEntryDeadline | open | The vessel shall enter survival mode within 60 seconds of the N-035 upper-limit trigger. |
| N-107 | SurvivalTransitionRecording | open | Every survival-mode entry shall have a corresponding event record. |
| N-108 | SailingResumptionDeadline | open | Full autonomous sailing shall resume within 5 minutes of N-035 resumption eligibility becoming continuously true. |
| N-109 | SailingResumptionInhibition | open | Full autonomous sailing shall remain inhibited while N-035 resumption eligibility is false. |
| N-110 | ResumptionBlockEvidence | open | Every blocked sailing-resumption attempt shall record the blocking condition. |
| N-111 | WetMechanismTravel | open | After each N-044 exposure, external mechanisms shall complete their full commanded travel without seizure. |
| N-112 | WetJointIntegrity | open | After each N-044 exposure, structural joints shall show no separation or through-cracks on visual inspection at 5 times magnification. |
| N-113 | WetConductorResistance | open | After each N-045 exposure, end-to-end conductor resistance shall be no more than 10 percent above its pre-test value. |
| N-114 | WetInsulationResistance | open | After each N-045 exposure, conductor-to-conductor and conductor-to-case insulation resistance shall be at least 1 megohm at 50 V DC. |
| N-115 | HotSunElectronicsOperation | open | Powered electronics shall retain operational functions throughout the N-046 exposure. |
| N-116 | HotSunBatteryTemperature | open | Battery temperatures shall remain within manufacturer operating limits throughout the N-046 exposure. |
| N-117 | BatteryChargeTemperatureInhibition | open | Battery charging shall remain inhibited whenever measured battery temperature is outside the manufacturer permitted charge range. |
| N-118 | RightingDeadline | open | The vessel shall self-right within 60 seconds of each N-051 release. |
| N-119 | CapsizeRigRetention | open | The vessel shall retain its rig through every N-051 release. |
| N-120 | CapsizeBallastRetention | open | The vessel shall retain its ballast through every N-051 release. |
| N-121 | CapsizeElectronicsSealing | open | No water shall reach electronics during any N-051 release. |
| N-122 | ControlRecoveryDeadline | open | The vessel shall restore mode-appropriate autonomous sail/steering control within 120 seconds from each N-051 release. |
| N-123 | CapsizeGateProgressRetention | open | Gate progress shall be preserved through every N-051 release. |
| N-124 | CapsizeQualificationRetention | open | Qualification status shall be preserved through every N-051 release absent an independently disqualifying event. |
| N-125 | CapsizeRestrictionRetention | open | Control restoration after each N-051 release shall preserve every active survival, low-energy, recovery and motor-inhibition restriction. |
| N-126 | WeedPassageSpeed | open | During each N-053 patch passage, mean water-relative sailing speed shall be at least 50 percent of the weed-free reference speed. |
| N-127 | WeedPassageSteering | open | After each N-053 patch passage, full commanded rudder travel shall be regained within 5 minutes. |
| N-128 | WeedSnagSpeedRecovery | open | Within 5 minutes of each N-054 snag, water-relative sailing speed shall recover to at least 50 percent of unobstructed reference speed. |
| N-129 | WeedSnagSteeringRecovery | open | Within 5 minutes of each N-054 snag, full commanded rudder travel shall be regained. |
| N-130 | WeedBlockageFault | open | A suspected-fouling fault shall be logged within 10 seconds after the N-055 trigger. |
| N-131 | WeedBlockageContingency | open | The vessel shall enter fouling-contingency state within 10 seconds after the N-055 trigger. |
| N-132 | WeedBlockageLocation | open | Location reporting shall continue at the active telemetry cadence during fouling contingency whenever a link is available. |
| N-133 | PoweredWeedSpeed | open | Mean water-relative powered speed through each N-056 patch passage shall be at least 50 percent of weed-free reference speed. |
| N-134 | PoweredWeedCurrent | open | Motor and controller currents shall remain within their respective rated limits during each N-056 patch passage. |
| N-135 | PoweredWeedTemperature | open | Motor and controller temperatures shall remain within their respective rated limits during each N-056 patch passage. |
| N-136 | LockedPropulsorShutdown | open | A locked propulsor shall cause motor shutdown within 2 seconds. |
| R-101 | MotorQualificationInvariant | open | Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown. |
| R-102 | FreshRecoveryCommand | open | After restart, motor enable shall remain inhibited until a fresh authenticated recovery command is accepted. |
| E-144 | IngressEventDeadline | open | In the E-006 injection test, an ingress event record shall exist within 60 seconds of injection starting. |
| E-145 | QualificationRestoration | open | Within 30 seconds after a watchdog reset under E-003 preconditions, qualification status shall equal the valid persisted status, or be nonqualifying when persisted status is absent or inconsistent. |
| E-200 | SustainedEnergyFeasibility | open | The installed energy architecture shall support the selected bounded repeating profile without external charging, meeting the derived reserve, cycle-balance and peak-supply criteria. |
| E-201 | SustainedReserveProtection | open | Conservative stored energy shall remain strictly above the R-002 protected reserve throughout the selected sustained-operation profile. |
| E-202 | RepeatableCycleBalance | open | Stored energy at the end of the complete repeating profile shall be at least its initial value at the same profile phase. |
| E-203 | PeakSupplyCapability | open | The battery supply shall support each selected mode’s coincident peak withdrawal power without harvesting. |
| E-204 | HarvestCampaignCoverage | open | The qualification energy profile shall contain at least three consecutive 24-hour days, each with harvesting enabled for no more than 6 hours. |
| E-205 | EnergyEvidenceReadiness | open | An energy case shall be accepted only after its installed-load coverage, resource bounds, battery derating and interval-resolution evidence have been accepted. |

## Derivations

| Original | Derived | Status | Rationale |
| --- | --- | --- | --- |
| transGorgeChallenge | courseCompletion | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | repeatedOperation | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | unassistedAttempt | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | sailingPropulsion | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | liveObservation | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | emergencyIntervention | open | This rule refines the overall Trans-Gorge challenge. |
| courseCompletion | roundTrip | open | The vehicle mission implements the independently defined challenge course. |
| repeatedOperation | multiDayEndurance | open | Repeated autonomous journeys motivate the existing endurance and harvesting requirement; M-002 defines an initial 72-hour campaign; indefinite operation remains an objective. |
| unassistedAttempt | navigationAndControl | open | The vessel needs onboard guidance and control to complete an unassisted attempt. |
| sailingPropulsion | roundTrip | open | Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. |
| liveObservation | communications | open | Vehicle communications implement live observation and outage data retention. |
| emergencyIntervention | communications | open | Vehicle communications provide emergency commands whose use ends attempt qualification. |
| hawaiiVoyage | multiDayEndurance | open | An ocean passage motivates sustained energy autonomy; multi-day operation is an interim capability, not an ocean endurance sizing result. |
| hawaiiVoyage | navigationAndControl | open | An autonomous Hawaii passage needs ocean guidance and sailing control; N-001 specifies its environmental design envelope. |
| hawaiiVoyage | communications | open | The long-term ocean mission motivates review of monitoring coverage and outage behavior without selecting a radio technology. |
| hawaiiVoyage | resetRecovery | open | Extended unattended operation motivates recovery from onboard resets. |
| hawaiiVoyage | missionEvidence | open | Ocean mission assessment requires retained voyage evidence; E-007 specifies recording and retention acceptance criteria. |
| roundTrip | navigationAndControl | open | Autonomous completion of the route needs observations, guidance, and actuation. |
| roundTrip | resetRecovery | open | A reset during an autonomous journey must not leave mission behavior undefined. |
| roundTrip | communications | open | Mission supervision and recovery need an agreed operator communication policy. |
| roundTrip | ingressResponse | open | Recovering the boat after the journey motivates a defined response to small leaks. |
| roundTrip | missionEvidence | open | Assessing route completion and learning from the mission requires recorded evidence. |
| multiDayEndurance | energyAwareness | open | Multi-day operation with variable harvesting needs energy estimation and load management. |
| multiDayEndurance | lowEnergyRecovery | open | Harvest shortfalls need an explicit degraded operating mode. |
| energyAwareness | lowEnergyRecovery | open | Available-energy estimates and reserve policy must drive low-energy transitions. |
| roundTrip | transportability | open | Transportability refines the responsibilities needed for roundTrip. |
| roundTrip | desktopManufacture | open | David specified desktop manufacture and a 250 mm usable build cube as a project constraint on the vehicle; this is an imposed stakeholder constraint, not a consequence of one-person handling. |
| repeatedOperation | serviceability | open | Repeated deployment motivates maintainability between attempts; the timed service target is an engineering allocation, not implied by printer size. |
| navigationAndControl | trafficSafety | open | TrafficSafety refines the responsibilities needed for navigationAndControl. |
| roundTrip | operatingBoundary | open | OperatingBoundary refines the responsibilities needed for roundTrip. |
| emergencyIntervention | safeRecovery | open | Permitted emergency intervention requires explicit abort, qualification, isolation and control-loss behavior. |
| trafficSafety | navigationConspicuity | open | NavigationConspicuity refines the responsibilities needed for trafficSafety. |
| roundTrip | regulatoryClassification | open | RegulatoryClassification refines the responsibilities needed for roundTrip. |
| roundTrip | environmentalEnvelope | open | EnvironmentalEnvelope refines the responsibilities needed for roundTrip. |
| environmentalEnvelope | marineDurability | open | MarineDurability refines the responsibilities needed for environmentalEnvelope. |
| environmentalEnvelope | stabilityAndFouling | open | StabilityAndFouling refines the responsibilities needed for environmentalEnvelope. |
| safeRecovery | recoveryPropulsion | open | RecoveryPropulsion refines the responsibilities needed for safeRecovery. |
| recoveryPropulsion | recoveryEnergy | open | RecoveryEnergy refines the responsibilities needed for recoveryPropulsion. |
| communications | telemetryEquipment | open | TelemetryEquipment refines the responsibilities needed for communications. |
| communications | commandIntegrity | open | CommandIntegrity refines the responsibilities needed for communications. |
| hawaiiVoyage | environmentalEnvelope | open | Ocean operation requires its own environmental envelope; Gorge success does not establish it. |
| roundTrip | gorgeEnvironment | open | The Gorge mission sets the river environment; it does not impose the ocean profile. |
| hawaiiVoyage | oceanEnvironment | open | The Hawaii mission sets the ocean environment; this profile is not a Gorge acceptance prerequisite. |
| gorgeEnvironment | gorgeWind | open | GorgeWind provides a separately verifiable criterion for gorgeEnvironment. |
| gorgeEnvironment | gorgeWaves | open | GorgeWaves provides a separately verifiable criterion for gorgeEnvironment. |
| gorgeEnvironment | gorgeCurrent | open | GorgeCurrent provides a separately verifiable criterion for gorgeEnvironment. |
| gorgeEnvironment | gorgeSurvivalWind | open | GorgeSurvivalWind provides a separately verifiable criterion for gorgeEnvironment. |
| gorgeEnvironment | gorgeSurvivalWaves | open | GorgeSurvivalWaves provides a separately verifiable criterion for gorgeEnvironment. |
| oceanEnvironment | oceanWind | open | OceanWind provides a separately verifiable criterion for oceanEnvironment. |
| oceanEnvironment | oceanWaves | open | OceanWaves provides a separately verifiable criterion for oceanEnvironment. |
| oceanEnvironment | oceanCurrent | open | OceanCurrent provides a separately verifiable criterion for oceanEnvironment. |
| oceanEnvironment | oceanSurvivalWind | open | OceanSurvivalWind provides a separately verifiable criterion for oceanEnvironment. |
| oceanEnvironment | oceanSurvivalWaves | open | OceanSurvivalWaves provides a separately verifiable criterion for oceanEnvironment. |
| environmentalEnvelope | airTemperature | open | AirTemperature provides a separately verifiable criterion for environmentalEnvelope. |
| environmentalEnvelope | waterTemperature | open | WaterTemperature provides a separately verifiable criterion for environmentalEnvelope. |
| environmentalEnvelope | humidity | open | Humidity provides a separately verifiable criterion for environmentalEnvelope. |
| environmentalEnvelope | visibility | open | Visibility provides a separately verifiable criterion for environmentalEnvelope. |
| environmentalEnvelope | calmOperation | open | CalmOperation provides a separately verifiable criterion for environmentalEnvelope. |
| environmentalEnvelope | envelopeTransition | open | EnvelopeTransition provides a separately verifiable criterion for environmentalEnvelope. |
| marineDurability | freshwaterExposure | open | FreshwaterExposure provides a separately verifiable criterion for marineDurability. |
| marineDurability | saltwaterExposure | open | SaltwaterExposure provides a separately verifiable criterion for marineDurability. |
| marineDurability | enclosureSealing | open | EnclosureSealing provides a separately verifiable criterion for marineDurability. |
| marineDurability | wetMechanicalIntegrity | open | WetMechanicalIntegrity provides a separately verifiable criterion for marineDurability. |
| marineDurability | wetElectricalIntegrity | open | WetElectricalIntegrity provides a separately verifiable criterion for marineDurability. |
| marineDurability | solarHeating | open | SolarHeating provides a separately verifiable criterion for marineDurability. |
| marineDurability | printedMaterialAging | open | PrintedMaterialAging provides a separately verifiable criterion for marineDurability. |
| stabilityAndFouling | selfRighting | open | SelfRighting provides a separately verifiable criterion for stabilityAndFouling. |
| stabilityAndFouling | capsizeControlRecovery | open | CapsizeControlRecovery provides a separately verifiable criterion for stabilityAndFouling. |
| stabilityAndFouling | submergedWeedPassage | open | SubmergedWeedPassage provides a separately verifiable criterion for stabilityAndFouling. |
| stabilityAndFouling | weedSnagShedding | open | WeedSnagShedding provides a separately verifiable criterion for stabilityAndFouling. |
| stabilityAndFouling | weedBlockageResponse | open | WeedBlockageResponse provides a separately verifiable criterion for stabilityAndFouling. |
| stabilityAndFouling | recoveryPropulsorWeeds | open | RecoveryPropulsorWeeds provides a separately verifiable criterion for stabilityAndFouling. |
| recoveryPropulsion | recoveryPropulsorWeeds | open | The recovery propulsor must remain usable in the vegetation encountered by the sailing vessel. |
| navigationAndControl | navigationAvailability | open | NavigationAvailability isolates a separately verifiable consequence of navigationAndControl. |
| recoveryEnergy | launchEnergyAdmission | open | LaunchEnergyAdmission isolates a separately verifiable consequence of recoveryEnergy. |
| sailingPropulsion | challengeMotorInhibition | open | ChallengeMotorInhibition isolates a separately verifiable consequence of GorgeChallenge::sailingPropulsion. |
| unassistedAttempt | challengeMotorInhibition | open | No-intervention qualification must survive resets and motor-mode transitions. |
| unassistedAttempt | commandIntegrity | open | Accepted external control changes the attempt qualification; communications alone does not supply this rule. |
| emergencyIntervention | commandIntegrity | open | The emergency control channel needs authenticated, fresh commands and persistent qualification changes. |
| hawaiiVoyage | operatingBoundary | open | An ocean route also needs configured boundaries and no-feasible-route behavior; its boundaries differ from the Gorge course. |
| hawaiiVoyage | regulatoryClassification | open | Deployment permissions and applicable rules depend on the ocean route as well as the Gorge mission. |
| hawaiiVoyage | serviceability | open | Unattended ocean preparation and post-voyage maintenance motivate replaceable modules; this is not at-sea servicing during qualification. |
| gorgeEnvironment | freshwaterExposure | open | The river profile supplies the freshwater exposure medium. |
| oceanEnvironment | saltwaterExposure | open | The ocean profile supplies the saltwater exposure medium. |
| gorgeEnvironment | submergedWeedPassage | open | David identified Columbia River milfoil as a Gorge design condition. |
| gorgeEnvironment | weedSnagShedding | open | Appendage snags are a consequence of the Gorge submerged-vegetation exposure. |
| energyAwareness | energyEstimateCadence | open | This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. |
| energyAwareness | reserveEstimateCadence | open | This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. |
| energyAwareness | energyEstimateAccuracy | open | This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. |
| energyAwareness | conservativeEnergyEstimate | open | This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. |
| navigationAndControl | guidanceUpdateCadence | open | This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. |
| navigationAndControl | sailCommandCadence | open | This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. |
| navigationAndControl | steeringCommandCadence | open | This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. |
| navigationAndControl | positionAccuracy | open | This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. |
| navigationAndControl | headingAccuracy | open | This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. |
| resetRecovery | restartDeadline | open | This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. |
| resetRecovery | missionStateRestoration | open | This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. |
| resetRecovery | gateProgressRestoration | open | This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. |
| resetRecovery | resetRestrictionPreservation | open | This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. |
| lowEnergyRecovery | lowEnergyEntry | open | This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. |
| lowEnergyRecovery | lowEnergyPayloadInhibition | open | This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. |
| lowEnergyRecovery | lowEnergyNavigationContinuity | open | This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. |
| lowEnergyRecovery | lowEnergyCollisionContinuity | open | This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. |
| lowEnergyRecovery | lowEnergyExit | open | This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. |
| lowEnergyRecovery | payloadRestartPermission | open | This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. |
| communications | telemetryDeliveryCadence | open | This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. |
| communications | outageAutonomy | open | This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. |
| communications | reconnectCurrentRecord | open | This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. |
| communications | backlogOrdering | open | This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. |
| communications | backlogCurrentPriority | open | This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. |
| ingressResponse | ingressDetection | open | This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. |
| ingressResponse | ingressRecoveryRequest | open | This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. |
| ingressResponse | ingressFlotation | open | This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. |
| ingressResponse | ingressElectronicsProtection | open | This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. |
| ingressResponse | ingressPositionContinuity | open | This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. |
| missionEvidence | periodicLogCadence | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | logRetention | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | criticalEventRecording | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | logTimestampAccuracy | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | invalidTimestampMarking | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | logGapIndication | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | logInterruptionDurability | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | reconnectLogPreservation | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | qualificationPersistence | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| missionEvidence | unknownQualificationFallback | open | This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. |
| navigationAvailability | navigationValidEpochs | open | This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. |
| navigationAvailability | staleNavigationInvalidation | open | This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. |
| navigationAvailability | navigationDegradedTransition | open | This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. |
| navigationAvailability | staleNavigationUseInhibition | open | This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. |
| transportability | soloTransport | open | This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. |
| transportability | liftMass | open | This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. |
| transportability | setupDuration | open | This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. |
| transportability | packDuration | open | This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. |
| transportability | soloLaunch | open | This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. |
| transportability | soloRetrieval | open | This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. |
| serviceability | replacementDuration | open | This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. |
| serviceability | nondestructiveService | open | This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. |
| serviceability | postServiceSealing | open | This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. |
| serviceability | postServiceActuation | open | This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. |
| trafficSafety | trafficTracking | open | This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. |
| trafficSafety | collisionAssessmentCadence | open | This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. |
| trafficSafety | avoidanceCommandDeadline | open | This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. |
| trafficSafety | trafficAwarenessFault | open | This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. |
| operatingBoundary | boundaryEvaluationCadence | open | This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. |
| operatingBoundary | boundaryAvoidanceDeadline | open | This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. |
| operatingBoundary | boundaryAvoidanceRecording | open | This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. |
| operatingBoundary | boundaryStartInhibition | open | This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. |
| operatingBoundary | boundaryDegradedEvidence | open | This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. |
| safeRecovery | abortLatchDeadline | open | This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. |
| safeRecovery | recoveryTelemetryCadence | open | This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. |
| safeRecovery | motorIsolationDeadline | open | This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. |
| safeRecovery | isolationRestartInhibition | open | This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. |
| safeRecovery | manualControlLossShutdown | open | This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. |
| safeRecovery | controlLossLocationContinuity | open | This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. |
| navigationConspicuity | navigationLightPresentation | open | This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. |
| navigationConspicuity | navigationShapePresentation | open | This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. |
| navigationConspicuity | navigationSoundPresentation | open | This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. |
| navigationConspicuity | signalingModeDeadline | open | This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. |
| navigationConspicuity | signalingFaultRecording | open | This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. |
| navigationConspicuity | signalingFaultReporting | open | This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. |
| regulatoryClassification | deploymentComplianceRecord | open | This leaf isolates one acceptance outcome of S-005; the parent supplies shared verification conditions. |
| regulatoryClassification | deploymentReleaseGate | open | This leaf isolates one acceptance outcome of S-005; the parent supplies shared verification conditions. |
| telemetryEquipment | telemetryDisplayContent | open | This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. |
| telemetryEquipment | telemetryStaleIndication | open | This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. |
| telemetryEquipment | telemetryIdentityPreservation | open | This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. |
| telemetryEquipment | telemetryDuplicateSuppression | open | This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. |
| commandIntegrity | unauthenticatedCommandRejection | open | This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. |
| commandIntegrity | replayCommandRejection | open | This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. |
| commandIntegrity | expiredCommandRejection | open | This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. |
| commandIntegrity | acceptedCommandDeadline | open | This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. |
| commandIntegrity | onboardAcknowledgmentDeadline | open | This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. |
| commandIntegrity | acknowledgmentQueueing | open | This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. |
| commandIntegrity | externalControlDisqualification | open | This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. |
| visibility | visibilityNavigationCapability | open | This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. |
| visibility | visibilityTrafficCapability | open | This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. |
| visibility | restrictedVisibilityEntry | open | This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. |
| visibility | restrictedVisibilityEvidence | open | This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. |
| visibility | restrictedVisibilityCollisionAssessment | open | This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. |
| envelopeTransition | survivalEntryDeadline | open | This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. |
| envelopeTransition | survivalTransitionRecording | open | This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. |
| envelopeTransition | sailingResumptionDeadline | open | This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. |
| envelopeTransition | sailingResumptionInhibition | open | This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. |
| envelopeTransition | resumptionBlockEvidence | open | This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. |
| wetMechanicalIntegrity | wetMechanismTravel | open | This leaf isolates one acceptance outcome of N-044; the parent supplies shared verification conditions. |
| wetMechanicalIntegrity | wetJointIntegrity | open | This leaf isolates one acceptance outcome of N-044; the parent supplies shared verification conditions. |
| wetElectricalIntegrity | wetConductorResistance | open | This leaf isolates one acceptance outcome of N-045; the parent supplies shared verification conditions. |
| wetElectricalIntegrity | wetInsulationResistance | open | This leaf isolates one acceptance outcome of N-045; the parent supplies shared verification conditions. |
| solarHeating | hotSunElectronicsOperation | open | This leaf isolates one acceptance outcome of N-046; the parent supplies shared verification conditions. |
| solarHeating | hotSunBatteryTemperature | open | This leaf isolates one acceptance outcome of N-046; the parent supplies shared verification conditions. |
| solarHeating | batteryChargeTemperatureInhibition | open | This leaf isolates one acceptance outcome of N-046; the parent supplies shared verification conditions. |
| selfRighting | rightingDeadline | open | This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. |
| selfRighting | capsizeRigRetention | open | This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. |
| selfRighting | capsizeBallastRetention | open | This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. |
| selfRighting | capsizeElectronicsSealing | open | This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. |
| capsizeControlRecovery | controlRecoveryDeadline | open | This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. |
| capsizeControlRecovery | capsizeGateProgressRetention | open | This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. |
| capsizeControlRecovery | capsizeQualificationRetention | open | This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. |
| capsizeControlRecovery | capsizeRestrictionRetention | open | This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. |
| submergedWeedPassage | weedPassageSpeed | open | This leaf isolates one acceptance outcome of N-053; the parent supplies shared verification conditions. |
| submergedWeedPassage | weedPassageSteering | open | This leaf isolates one acceptance outcome of N-053; the parent supplies shared verification conditions. |
| weedSnagShedding | weedSnagSpeedRecovery | open | This leaf isolates one acceptance outcome of N-054; the parent supplies shared verification conditions. |
| weedSnagShedding | weedSnagSteeringRecovery | open | This leaf isolates one acceptance outcome of N-054; the parent supplies shared verification conditions. |
| weedBlockageResponse | weedBlockageFault | open | This leaf isolates one acceptance outcome of N-055; the parent supplies shared verification conditions. |
| weedBlockageResponse | weedBlockageContingency | open | This leaf isolates one acceptance outcome of N-055; the parent supplies shared verification conditions. |
| weedBlockageResponse | weedBlockageLocation | open | This leaf isolates one acceptance outcome of N-055; the parent supplies shared verification conditions. |
| recoveryPropulsorWeeds | poweredWeedSpeed | open | This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. |
| recoveryPropulsorWeeds | poweredWeedCurrent | open | This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. |
| recoveryPropulsorWeeds | poweredWeedTemperature | open | This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. |
| recoveryPropulsorWeeds | lockedPropulsorShutdown | open | This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. |
| challengeMotorInhibition | motorQualificationInvariant | open | This leaf isolates one acceptance outcome of R-004; the parent supplies shared verification conditions. |
| challengeMotorInhibition | freshRecoveryCommand | open | This leaf isolates one acceptance outcome of R-004; the parent supplies shared verification conditions. |
| ingressResponse | ingressEventDeadline | open | This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. |
| resetRecovery | qualificationRestoration | open | This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. |
| resetRecovery | logInterruptionDurability | open | resetRecovery also requires the shared logInterruptionDurability outcome; one normative leaf avoids duplicate obligations. |
| resetRecovery | unknownQualificationFallback | open | resetRecovery also requires the shared unknownQualificationFallback outcome; one normative leaf avoids duplicate obligations. |
| resetRecovery | qualificationPersistence | open | resetRecovery also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. |
| resetRecovery | freshRecoveryCommand | open | resetRecovery also requires the shared freshRecoveryCommand outcome; one normative leaf avoids duplicate obligations. |
| resetRecovery | motorQualificationInvariant | open | resetRecovery also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. |
| commandIntegrity | criticalEventRecording | open | commandIntegrity also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. |
| commandIntegrity | qualificationPersistence | open | commandIntegrity also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. |
| safeRecovery | qualificationPersistence | open | safeRecovery also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. |
| safeRecovery | motorQualificationInvariant | open | safeRecovery also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. |
| safeRecovery | periodicLogCadence | open | safeRecovery also requires the shared periodicLogCadence outcome; one normative leaf avoids duplicate obligations. |
| challengeMotorInhibition | qualificationPersistence | open | challengeMotorInhibition also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. |
| challengeMotorInhibition | criticalEventRecording | open | challengeMotorInhibition also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. |
| lowEnergyRecovery | periodicLogCadence | open | lowEnergyRecovery also requires the shared periodicLogCadence outcome; one normative leaf avoids duplicate obligations. |
| lowEnergyRecovery | telemetryDeliveryCadence | open | lowEnergyRecovery also requires the shared telemetryDeliveryCadence outcome; one normative leaf avoids duplicate obligations. |
| lowEnergyRecovery | criticalEventRecording | open | lowEnergyRecovery also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. |
| lowEnergyRecovery | motorQualificationInvariant | open | lowEnergyRecovery also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. |
| ingressResponse | criticalEventRecording | open | ingressResponse also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. |
| ingressResponse | motorQualificationInvariant | open | ingressResponse also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. |
| communications | logRetention | open | communications also requires the shared logRetention outcome; one normative leaf avoids duplicate obligations. |
| communications | reconnectLogPreservation | open | communications also requires the shared reconnectLogPreservation outcome; one normative leaf avoids duplicate obligations. |
| navigationAvailability | criticalEventRecording | open | navigationAvailability also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. |
| envelopeTransition | periodicLogCadence | open | envelopeTransition also requires the shared periodicLogCadence outcome; one normative leaf avoids duplicate obligations. |
| envelopeTransition | motorQualificationInvariant | open | envelopeTransition also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. |
| weedBlockageResponse | motorQualificationInvariant | open | weedBlockageResponse also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. |
| recoveryPropulsorWeeds | motorQualificationInvariant | open | recoveryPropulsorWeeds also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. |
| repeatedOperation | sustainedEnergyFeasibility | open | Repeated journeys motivate a repeatable energy cycle, beyond a one-off endurance run. |
| hawaiiVoyage | sustainedEnergyFeasibility | open | The ocean ambition requires sustained energy autonomy; route-specific resources remain unresolved. |
| sustainedEnergyFeasibility | sustainedReserveProtection | open | This leaf isolates one acceptance outcome of sustained energy feasibility. |
| sustainedEnergyFeasibility | repeatableCycleBalance | open | This leaf isolates one acceptance outcome of sustained energy feasibility. |
| sustainedEnergyFeasibility | peakSupplyCapability | open | This leaf isolates one acceptance outcome of sustained energy feasibility. |
| sustainedEnergyFeasibility | energyEvidenceReadiness | open | This leaf isolates one acceptance outcome of sustained energy feasibility. |
| multiDayEndurance | sustainedReserveProtection | open | The M-002 campaign requires this separately evaluated energy outcome. |
| multiDayEndurance | peakSupplyCapability | open | The M-002 campaign requires this separately evaluated energy outcome. |
| multiDayEndurance | harvestCampaignCoverage | open | The M-002 campaign requires this separately evaluated energy outcome. |
| multiDayEndurance | energyEvidenceReadiness | open | The M-002 campaign requires this separately evaluated energy outcome. |
| recoveryEnergy | sustainedReserveProtection | open | Sustained operation protects the recovery reserve sized by the existing R-002 policy. |
