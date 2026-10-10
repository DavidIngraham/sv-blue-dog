package BlueDogRequirements {
    private import RequirementDerivation::*;
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    private import GorgeChallenge::*;
    private import BlueDog::Goals::*;
    requirement def <'M-001'> RoundTrip {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall cross the configured The Dalles departure gate, Bonneville turnaround gate and The Dalles return gate in that order during one attempt, satisfying C-003 through C-006. Acceptance shall use the timestamped trajectory and intervention/propulsion event log; a missing gate crossing or disqualifying event shall prevent a completion verdict. */
    }
    requirement def <'M-002'> MultiDayEndurance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall operate for 72 continuous hours without servicing or external charging while meeting the Gorge operational functions in N-001. A qualification run shall include three consecutive 24-hour cycles, each with no more than 6 hours of harvesting and at least 18 hours with harvesting disabled. The battery shall remain above the R-002 recovery reserve throughout. Actual harvested energy, loads and battery energy shall be recorded; passing this campaign does not establish indefinite energy balance. */
    }
    requirement def <'E-001'> EnergyAwareness {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall update usable battery-energy and recovery-reserve estimates at least once per second. Against calibrated charge/discharge integration across the operating battery temperature range, usable-energy estimation error shall not exceed 10 percent of measured usable full-charge energy. The low-energy transition shall use a conservative estimate equal to estimated usable energy minus that error allowance. */
    }
    requirement def <'E-002'> NavigationAndControl {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During N-001 operation the vessel shall update position, heading, mission guidance and sail/steering commands at least once per second. Position error shall be at most 10 m and heading error at most 10 degrees for at least 95 percent of valid samples in each 30-minute qualification run against an independent reference. Position or heading data older than 5 seconds shall be marked invalid and trigger a logged navigation-degraded state within 1 second; the controller shall not continue using stale observations as current measurements. */
    }
    requirement def <'E-003'> ResetRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After a software watchdog reset with usable battery energy above the recovery reserve and valid navigation observations available, the vessel shall restore autonomous control and its persisted mission mode, gate progress and qualification status within 30 seconds. Propulsive motor output shall remain inhibited throughout restart unless a fresh authenticated recovery command is accepted after restart. Loss of recorded data shall not exceed the last 5 seconds; a reset shall never restore a disqualified attempt to qualifying status. */
        attribute measuredRestartTime : TimeValue;
        require constraint restartDeadline {
            measuredRestartTime >= 0 [s] and measuredRestartTime <= 30 [s]
        }
    }
    requirement def <'E-004'> LowEnergyRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* When the conservative usable-energy estimate reaches the R-002 reserve, the vessel shall enter a logged low-energy state within 5 seconds and disable the optional observation payload. Position recording shall continue at least once per minute and live telemetry at least once per 5 minutes when a link is available. Autonomous navigation, collision response and challenge motor inhibition shall remain active. Normal payload operation shall resume only after energy exceeds 1.2 times the reserve for 10 continuous minutes. */
    }
    requirement def <'E-005'> Communications {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During normal operation with a functioning link, the vessel shall deliver a current telemetry record to the shore endpoint at least once per 60 seconds. A 24-hour link outage shall not require operator intervention, erase mission data or stop autonomous control. After reconnection it shall deliver a current record within 60 seconds and resume oldest-first backlog transfer without delaying current records beyond 60 seconds. Onboard retention shall meet E-007; command handling shall meet C-102. */
    }
    requirement def <'E-006'> IngressResponse {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* In a 30-minute qualification test injecting freshwater into the normally dry hull at 10 mL/min, the vessel shall detect and record ingress within 60 seconds of injection starting, enter a logged recovery-request state, and retain flotation, dry electronics and position reporting for the full test. Detection shall not automatically enable motor propulsion in challenge mode. A pump is one possible implementation, not a prescribed solution. */
    }
    requirement def <'E-007'> MissionEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain at least 30 days of timestamped position, heading, mission mode, gate progress, battery energy and fault state at 1 Hz during normal operation, and at the degraded rates required by E-004/N-001 in those modes. It shall record every accepted/rejected external command, reset, motor-enable transition and qualification change. Timestamps shall be UTC within 1 second while GNSS time is valid; invalid time and gaps shall be flagged. A power interruption shall lose no more than the last 5 seconds of committed logging activity, and reconnection shall not delete retained records. */
    }
    requirement roundTrip : RoundTrip;
    requirement multiDayEndurance : MultiDayEndurance;
    requirement energyAwareness : EnergyAwareness;
    requirement navigationAndControl : NavigationAndControl;
    requirement resetRecovery : ResetRecovery;
    requirement lowEnergyRecovery : LowEnergyRecovery;
    requirement communications : Communications;
    requirement ingressResponse : IngressResponse;
    requirement missionEvidence : MissionEvidence;

    #derivation connection challengeCourse {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vehicle mission implements the independently defined challenge course. */
        end #original source ::> GorgeChallenge::courseCompletion;
        end #derive target ::> roundTrip;
    }
    #derivation connection challengeEndurance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Repeated autonomous journeys motivate the existing endurance and harvesting requirement; M-002 defines an initial 72-hour campaign; indefinite operation remains an objective. */
        end #original source ::> GorgeChallenge::repeatedOperation;
        end #derive target ::> multiDayEndurance;
    }
    #derivation connection challengeAutonomy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel needs onboard guidance and control to complete an unassisted attempt. */
        end #original source ::> GorgeChallenge::unassistedAttempt;
        end #derive target ::> navigationAndControl;
    }
    #derivation connection challengePropulsion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. */
        end #original source ::> GorgeChallenge::sailingPropulsion;
        end #derive target ::> roundTrip;
    }
    #derivation connection challengeMonitoring {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Vehicle communications implement live observation and outage data retention. */
        end #original source ::> GorgeChallenge::liveObservation;
        end #derive target ::> communications;
    }
    #derivation connection challengeOverride {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Vehicle communications provide emergency commands whose use ends attempt qualification. */
        end #original source ::> GorgeChallenge::emergencyIntervention;
        end #derive target ::> communications;
    }

    #derivation connection hawaiiMultiDayEndurance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An ocean passage motivates sustained energy autonomy; multi-day operation is an interim capability, not an ocean endurance sizing result. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> multiDayEndurance;
    }

    #derivation connection hawaiiNavigationAndControl {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An autonomous Hawaii passage needs ocean guidance and sailing control; N-001 specifies its environmental design envelope. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> navigationAndControl;
    }

    #derivation connection hawaiiCommunications {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The long-term ocean mission motivates review of monitoring coverage and outage behavior without selecting a radio technology. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> communications;
    }

    #derivation connection hawaiiResetRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Extended unattended operation motivates recovery from onboard resets. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> resetRecovery;
    }

    #derivation connection hawaiiMissionEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Ocean mission assessment requires retained voyage evidence; E-007 specifies recording and retention acceptance criteria. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> missionEvidence;
    }

    // Derivations: direction is original requirement to derived requirement.
    #derivation connection roundTripNavigation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Autonomous completion of the route needs observations, guidance, and actuation. */
        end #original source ::> roundTrip;
        end #derive target ::> navigationAndControl;
    }
    #derivation connection roundTripReset {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A reset during an autonomous journey must not leave mission behavior undefined. */
        end #original source ::> roundTrip;
        end #derive target ::> resetRecovery;
    }
    #derivation connection roundTripCommunications {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Mission supervision and recovery need an agreed operator communication policy. */
        end #original source ::> roundTrip;
        end #derive target ::> communications;
    }
    #derivation connection roundTripIngress {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Recovering the boat after the journey motivates a defined response to small leaks. */
        end #original source ::> roundTrip;
        end #derive target ::> ingressResponse;
    }
    #derivation connection roundTripEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Assessing route completion and learning from the mission requires recorded evidence. */
        end #original source ::> roundTrip;
        end #derive target ::> missionEvidence;
    }
    #derivation connection enduranceEnergy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Multi-day operation with variable harvesting needs energy estimation and load management. */
        end #original source ::> multiDayEndurance;
        end #derive target ::> energyAwareness;
    }
    #derivation connection enduranceLimpMode {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Harvest shortfalls need an explicit degraded operating mode. */
        end #original source ::> multiDayEndurance;
        end #derive target ::> lowEnergyRecovery;
    }
    #derivation connection energyLimpMode {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Available-energy estimates and reserve policy must drive low-energy transitions. */
        end #original source ::> energyAwareness;
        end #derive target ::> lowEnergyRecovery;
    }

    requirement def <'P-001'> Transportability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One adult operator shall be able to move all mission equipment 100 m, assemble the vessel, launch it, recover it and pack it without another person or powered lifting equipment. Each separately lifted assembly shall have mass at most 15 kg. Setup and pack-down shall each take at most 30 minutes. Demonstration conditions shall be a firm bank or ramp with slope at most 1:12, wind at most 5 m/s and wave height at most 0.2 m; this handling envelope does not claim solo recovery in the sailing survival envelope. */
    }
    requirement transportability : Transportability;
    #derivation connection deriveTransportability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Transportability refines the responsibilities needed for roundTrip. */
        end #original source ::> roundTrip;
        end #derive target ::> transportability;
    }

    requirement def <'P-002'> DesktopManufacture {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Every printed component shall be producible as one or more print jobs on a printer with usable Cartesian travel of 250 mm by 250 mm by 250 mm. In the selected build orientation, the complete occupied envelope of each job, including supports, brim, raft and printer-required clearance, shall have positive X, Y and Z extents each no greater than 250 mm. Acceptance shall compare slicer/job-envelope measurements for every job with these limits; raw part volume alone is insufficient. */
        attribute jobX : LengthValue;
        attribute jobY : LengthValue;
        attribute jobZ : LengthValue;
        attribute buildLimit : LengthValue = 250 [mm];
        require constraint jobFits {
            jobX > 0 [mm] and jobY > 0 [mm] and jobZ > 0 [mm] and
            jobX <= buildLimit and jobY <= buildLimit and jobZ <= buildLimit
        }
    }
    requirement desktopManufacture : DesktopManufacture;
    #derivation connection deriveDesktopManufacture {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* DesktopManufacture refines the responsibilities needed for transportability. */
        end #original source ::> transportability;
        end #derive target ::> desktopManufacture;
    }

    requirement def <'P-003'> Serviceability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One operator shall be able to replace the battery, each electronics module, each actuator and each serviceable enclosure seal individually within 30 minutes using hand tools, without cutting bonded structural joints or destroying adjacent parts. Following each replacement, the assembly shall pass the N-043 enclosure immersion criterion and a complete commanded-travel check for affected actuators. */
    }
    requirement serviceability : Serviceability;
    #derivation connection deriveServiceability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Serviceability refines the responsibilities needed for desktopManufacture. */
        end #original source ::> desktopManufacture;
        end #derive target ::> serviceability;
    }

    requirement def <'S-001'> TrafficSafety {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Within the N-001 operating envelope, the vessel shall track encountered vessels, including non-AIS craft, update collision-risk estimates at least once per second and issue an avoiding-action command within 2 seconds of a collision-risk trigger. Qualification shall include head-on, crossing and overtaking encounters with AIS and non-AIS targets, day and night, using independently recorded target trajectories. Loss of a valid traffic assessment for more than 5 seconds shall trigger a logged traffic-awareness fault within 1 second. Detection range, target signatures, closest-approach margins and maneuver feasibility are unresolved acceptance parameters recorded in the verification plan; this requirement cannot receive a complete pass until those parameters and scenario results are supplied. */
    }
    requirement trafficSafety : TrafficSafety;
    #derivation connection deriveTrafficSafety {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* TrafficSafety refines the responsibilities needed for navigationAndControl. */
        end #original source ::> navigationAndControl;
        end #derive target ::> trafficSafety;
    }

    requirement def <'S-002'> OperatingBoundary {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall evaluate its position and predicted 60-second trajectory against the uploaded permitted-water polygon and exclusion polygons at least once per second. A predicted boundary crossing shall trigger a logged avoidance command within 2 seconds. Missing or geometrically invalid boundaries shall inhibit mission start. Qualification shall inject trajectories toward each boundary, navigation loss and a no-feasible-maneuver case; the latter two shall produce an explicit degraded-state event rather than a false safe-route verdict. Course coordinates and uncertainty/clearance margins are controlled mission inputs, not arbitrary defaults. */
    }
    requirement operatingBoundary : OperatingBoundary;
    #derivation connection deriveOperatingBoundary {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* OperatingBoundary refines the responsibilities needed for roundTrip. */
        end #original source ::> roundTrip;
        end #derive target ::> operatingBoundary;
    }

    requirement def <'S-003'> SafeRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An accepted emergency abort shall latch the attempt as disqualified within 1 second and retain that state through power cycling. The vessel shall provide position reports at least once per 60 seconds while the link is available. A physically accessible local isolation control shall remove motor power within 1 second and prevent restart until deliberately reset. Loss of remote control for 5 seconds during manual powered recovery shall command zero thrust within a further 1 second while retaining autonomous recording and location reporting. */
    }
    requirement safeRecovery : SafeRecovery;
    #derivation connection deriveSafeRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* SafeRecovery refines the responsibilities needed for transportability. */
        end #original source ::> transportability;
        end #derive target ::> safeRecovery;
    }

    requirement def <'S-004'> NavigationConspicuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall automatically present the lights, shapes and sound signals in the deployment-specific compliance matrix for sailing, powered recovery and stationary modes, without a person aboard. A commanded mode change shall select its corresponding signaling configuration within 1 second; detectable signaling failures shall be logged and reported within 5 seconds. Acceptance shall measure the applicable visibility, arcs, colors and sound performance from that matrix. The matrix remains a deployment hold point under S-005, not a presumed small-craft exemption. */
    }
    requirement navigationConspicuity : NavigationConspicuity;
    #derivation connection deriveNavigationConspicuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* NavigationConspicuity refines the responsibilities needed for trafficSafety. */
        end #original source ::> trafficSafety;
        end #derive target ::> navigationConspicuity;
    }

    requirement def <'S-005'> RegulatoryClassification {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each deployment shall have a dated compliance record identifying the craft, dimensions, operating waters and modes, applicable navigation and radio obligations, and required permissions with their evidence. Deployment release shall be withheld when a required authorization is absent, expired or unresolved. Acceptance is a document review with no unresolved mandatory items; this is a deployment/process requirement, not an onboard component behavior or an assertion of buoy status. */
    }
    requirement regulatoryClassification : RegulatoryClassification;
    #derivation connection deriveRegulatoryClassification {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* RegulatoryClassification refines the responsibilities needed for roundTrip. */
        end #original source ::> roundTrip;
        end #derive target ::> regulatoryClassification;
    }

    requirement def <'N-001'> EnvironmentalEnvelope {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall support autonomous operation in the Columbia River Gorge reservoir environment and the intended northeast Pacific passage environment, with separate operational and survival capabilities. The derived Gorge, ocean and shared exposure requirements specify acceptance conditions. Qualification shall exercise navigation, sail/steering control, recording and available-link telemetry concurrently; survival acceptance permits loss of course progress but requires flotation, attached rig/ballast, dry electronics and retained mission state. Passing the Gorge profile alone shall not establish ocean capability. */
    }
    requirement environmentalEnvelope : EnvironmentalEnvelope;
    #derivation connection deriveEnvironmentalEnvelope {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* EnvironmentalEnvelope refines the responsibilities needed for roundTrip. */
        end #original source ::> roundTrip;
        end #derive target ::> environmentalEnvelope;
    }

    requirement def <'N-002'> MarineDurability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain its required functions and structural integrity during repeated freshwater Gorge service and prolonged saltwater ocean exposure. Derived requirements specify wet exposure, sealing, material aging and thermal qualification. Acceptance shall include post-exposure functional checks against the affected operational requirements. */
    }
    requirement marineDurability : MarineDurability;
    #derivation connection deriveMarineDurability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* MarineDurability refines the responsibilities needed for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> marineDurability;
    }

    requirement def <'N-003'> StabilityAndFouling {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall autonomously recover from capsize and tolerate submerged aquatic vegetation, including milfoil-like stems, without reliance on operator intervention during a qualifying attempt. Derived requirements specify righting, control recovery, weed passage, snag shedding and blockage response. Dense floating mats and fishing-line entanglement are not covered by the submerged-weed passage qualification. */
    }
    requirement stabilityAndFouling : StabilityAndFouling;
    #derivation connection deriveStabilityAndFouling {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* StabilityAndFouling refines the responsibilities needed for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> stabilityAndFouling;
    }

    requirement def <'R-001'> RecoveryPropulsion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall provide auxiliary propulsion that is inhibited for every qualifying challenge state, including restart and link loss. Entering powered recovery shall disqualify and log the attempt before motor thrust is enabled. At maximum mission load, powered recovery shall sustain at least 0.5 m/s speed over ground for 30 minutes against a 1.5 m/s current in wind no greater than 5 m/s and waves no greater than 0.2 m. Acceptance shall measure the track, current and electrical power. This sheltered recovery target does not imply motor recovery in the full N-001 storm envelope; local isolation and control-loss response shall meet S-003. */
    }
    requirement recoveryPropulsion : RecoveryPropulsion;
    #derivation connection deriveRecoveryPropulsion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* RecoveryPropulsion refines the responsibilities needed for safeRecovery. */
        end #original source ::> safeRecovery;
        end #derive target ::> recoveryPropulsion;
    }

    calc def RecoveryReserveDemand {
        doc /* R-002 reserve policy: 30 minutes motor operation plus two hours essential loads, with a 20 percent allowance. Powers are non-overlapping electrical demands. */
        in motorPower : PowerValue;
        in essentialPower : PowerValue;
        return reserve : EnergyValue;
        1.2 * (motorPower * 1800 [s] + essentialPower * 7200 [s])
    }

    requirement def <'R-002'> RecoveryEnergy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Before starting an attempt, conservative usable battery energy shall exceed a protected reserve of at least 1.2 times the sum of 30 minutes of measured worst-case electrical motor power in the R-001 recovery test and 2 hours of essential navigation/control/recording/telemetry electrical power. Motor and essential power shall be separate, non-overlapping measurements. Throughout the attempt, reserve crossing shall trigger E-004. Acceptance shall evaluate the energy inequality using measured usable battery energy at the lowest operating battery temperature and end-of-service capacity. */
        attribute motorPower : PowerValue;
        attribute essentialPower : PowerValue;
        attribute reserveEnergy : EnergyValue;
        require constraint reserveSizing {
            motorPower > 0 [W] and essentialPower > 0 [W] and
            reserveEnergy >= RecoveryReserveDemand(motorPower, essentialPower)
        }
    }
    requirement recoveryEnergy : RecoveryEnergy;
    #derivation connection deriveRecoveryEnergy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* RecoveryEnergy refines the responsibilities needed for recoveryPropulsion. */
        end #original source ::> recoveryPropulsion;
        end #derive target ::> recoveryEnergy;
    }

    requirement def <'C-101'> TelemetryEquipment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The shore endpoint shall display UTC sample time, position, mission mode, usable battery energy, reserve, faults and time since the last received sample for every current telemetry record. It shall mark data stale once its age exceeds 120 seconds and retain that indication until a fresh record arrives. With injected 24-hour loss and subsequent reconnection, reception shall resume and records shall remain identifiable by vessel identity and sequence number without duplicate entries being presented as new observations. Delivery timing shall meet E-005, with the degraded-mode exception in E-004. */
    }
    requirement telemetryEquipment : TelemetryEquipment;
    #derivation connection deriveTelemetryEquipment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* TelemetryEquipment refines the responsibilities needed for communications. */
        end #original source ::> communications;
        end #derive target ::> telemetryEquipment;
    }

    requirement def <'C-102'> CommandIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall reject commands with failed authentication, an already-used sequence number or age greater than 30 seconds without changing actuator or mission state. Each command shall be logged with its disposition; an accepted abort/mode-change shall be applied and acknowledged onboard within 1 second of complete receipt, and transmitted acknowledgment shall be queued immediately when a link is available. Replayed, expired and unauthenticated command injections shall cause zero accepted mode changes. Acceptance of external mission/steering control during a qualifying attempt shall permanently disqualify that attempt. */
    }
    requirement commandIntegrity : CommandIntegrity;
    #derivation connection deriveCommandIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* CommandIntegrity refines the responsibilities needed for communications. */
        end #original source ::> communications;
        end #derive target ::> commandIntegrity;
    }
    #derivation connection hawaiiEnvironment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Ocean operation requires its own environmental envelope; Gorge success does not establish it. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> environmentalEnvelope;
    }

    requirement def <'N-010'> GorgeEnvironment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall operate on the Columbia River reach between The Dalles and Bonneville in freshwater, opposing wind/current, short-period chop, traffic and submerged aquatic vegetation. Gorge-derived parameter requirements and the shared exposure requirements apply together; no dam transit, ice or surf-zone launch is included. */
    }
    requirement gorgeEnvironment : GorgeEnvironment;
    #derivation connection deriveGorgeEnvironment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* GorgeEnvironment provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> gorgeEnvironment;
    }

    requirement def <'N-020'> OceanEnvironment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall operate on a northeast Pacific passage toward Hawaii in saltwater, ocean swell, wind seas and prolonged unattended exposure. Ocean-derived parameter requirements and the shared exposure requirements apply together. The baseline is not a hurricane-survival claim or a completed route/season qualification. */
    }
    requirement oceanEnvironment : OceanEnvironment;
    #derivation connection deriveOceanEnvironment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* OceanEnvironment provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> oceanEnvironment;
    }

    requirement def <'N-011'> GorgeWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain the N-001 operational functions in true wind from 3 to 15 m/s (10-minute mean referenced to 10 m above water), including 3-second gusts up to 20 m/s. Qualification shall include upwind, crosswind and downwind headings; this is a functional wind limit, not a guarantee of upstream progress. */
    }
    requirement gorgeWind : GorgeWind;
    #derivation connection deriveGorgeWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* GorgeWind provides a separately verifiable criterion for gorgeEnvironment. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> gorgeWind;
    }

    requirement def <'N-012'> GorgeWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain N-001 operational functions in significant wave heights up to 1 m with peak periods 2-5 s, including individual waves up to 2 m. Wave statistics shall use 20-minute records. Qualification shall include head, beam and following seas and physically realizable wind-wave-current combinations within the profile. */
    }
    requirement gorgeWaves : GorgeWaves;
    #derivation connection deriveGorgeWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* GorgeWaves provides a separately verifiable criterion for gorgeEnvironment. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> gorgeWaves;
    }

    requirement def <'N-013'> GorgeCurrent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain navigation and control in currents from 0 to 1.5 m/s from any direction relative to wind and waves. Qualification shall include opposing current. Failure to make progress shall invoke S-002 contingency behavior; positive upstream speed is not required at every wind speed or heading. */
    }
    requirement gorgeCurrent : GorgeCurrent;
    #derivation connection deriveGorgeCurrent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* GorgeCurrent provides a separately verifiable criterion for gorgeEnvironment. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> gorgeCurrent;
    }

    requirement def <'N-014'> GorgeSurvivalWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* For 24 continuous hours, the vessel shall meet the N-001 survival acceptance outcomes in mean wind up to 25 m/s and 3-second gusts up to 35 m/s, using the operational wind reference convention. The respective wave, current, temperature and humidity limits apply concurrently. */
    }
    requirement gorgeSurvivalWind : GorgeSurvivalWind;
    #derivation connection deriveGorgeSurvivalWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* GorgeSurvivalWind provides a separately verifiable criterion for gorgeEnvironment. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> gorgeSurvivalWind;
    }

    requirement def <'N-015'> GorgeSurvivalWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* For 24 continuous hours, the vessel shall meet the N-001 survival acceptance outcomes in significant wave heights up to 2 m, peak periods 3-7 s and individual waves up to 4 m. Qualification shall include adverse relative directions and physically realizable combinations with profile survival wind and current. */
    }
    requirement gorgeSurvivalWaves : GorgeSurvivalWaves;
    #derivation connection deriveGorgeSurvivalWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* GorgeSurvivalWaves provides a separately verifiable criterion for gorgeEnvironment. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> gorgeSurvivalWaves;
    }

    requirement def <'N-021'> OceanWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain the N-001 operational functions in true wind from 3 to 15 m/s (10-minute mean referenced to 10 m above water), including 3-second gusts up to 20 m/s. Qualification shall include upwind, crosswind and downwind headings; this is a functional wind limit, not a guarantee of upstream progress. */
    }
    requirement oceanWind : OceanWind;
    #derivation connection deriveOceanWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* OceanWind provides a separately verifiable criterion for oceanEnvironment. */
        end #original source ::> oceanEnvironment;
        end #derive target ::> oceanWind;
    }

    requirement def <'N-022'> OceanWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain N-001 operational functions in significant wave heights up to 3 m with peak periods 5-20 s, including individual waves up to 6 m. Wave statistics shall use 20-minute records. Qualification shall include head, beam and following seas and physically realizable wind-wave-current combinations within the profile. */
    }
    requirement oceanWaves : OceanWaves;
    #derivation connection deriveOceanWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* OceanWaves provides a separately verifiable criterion for oceanEnvironment. */
        end #original source ::> oceanEnvironment;
        end #derive target ::> oceanWaves;
    }

    requirement def <'N-023'> OceanCurrent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain navigation and control in currents from 0 to 1.0 m/s from any direction relative to wind and waves. Qualification shall include opposing current. Failure to make progress shall invoke S-002 contingency behavior; positive upstream speed is not required at every wind speed or heading. */
    }
    requirement oceanCurrent : OceanCurrent;
    #derivation connection deriveOceanCurrent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* OceanCurrent provides a separately verifiable criterion for oceanEnvironment. */
        end #original source ::> oceanEnvironment;
        end #derive target ::> oceanCurrent;
    }

    requirement def <'N-024'> OceanSurvivalWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* For 24 continuous hours, the vessel shall meet the N-001 survival acceptance outcomes in mean wind up to 25 m/s and 3-second gusts up to 35 m/s, using the operational wind reference convention. The respective wave, current, temperature and humidity limits apply concurrently. */
    }
    requirement oceanSurvivalWind : OceanSurvivalWind;
    #derivation connection deriveOceanSurvivalWind {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* OceanSurvivalWind provides a separately verifiable criterion for oceanEnvironment. */
        end #original source ::> oceanEnvironment;
        end #derive target ::> oceanSurvivalWind;
    }

    requirement def <'N-025'> OceanSurvivalWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* For 24 continuous hours, the vessel shall meet the N-001 survival acceptance outcomes in significant wave heights up to 6 m, peak periods 6-20 s and individual waves up to 12 m. Qualification shall include adverse relative directions and physically realizable combinations with profile survival wind and current. */
    }
    requirement oceanSurvivalWaves : OceanSurvivalWaves;
    #derivation connection deriveOceanSurvivalWaves {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* OceanSurvivalWaves provides a separately verifiable criterion for oceanEnvironment. */
        end #original source ::> oceanEnvironment;
        end #derive target ::> oceanSurvivalWaves;
    }

    requirement def <'N-030'> AirTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain operational functions from 0 to 40 degC ambient air temperature. Qualification shall include powered cold and hot endpoints with internal temperatures stabilized to less than 1 degC change per hour, followed by 2 hours of operation at each endpoint. The same range applies during survival. */
    }
    requirement airTemperature : AirTemperature;
    #derivation connection deriveAirTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* AirTemperature provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> airTemperature;
    }

    requirement def <'N-031'> WaterTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The immersed hull, appendages and installed equipment shall retain operational functions in water from 2 to 30 degC, including 2 hours at each endpoint after thermal stabilization. The same range applies during survival. */
    }
    requirement waterTemperature : WaterTemperature;
    #derivation connection deriveWaterTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* WaterTemperature provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> waterTemperature;
    }

    requirement def <'N-032'> Humidity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The installed equipment shall retain operational functions at 0-100 percent relative humidity, including condensation. Qualification shall include three powered 24-hour cycles between 10 and 40 degC at at least 95 percent relative humidity, with visible condensation on external surfaces during cooling and no liquid water reaching enclosed electronics. */
    }
    requirement humidity : Humidity;
    #derivation connection deriveHumidity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Humidity provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> humidity;
    }

    requirement def <'N-033'> Visibility {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain navigation and traffic-assessment functions in daylight and darkness at meteorological visibility of at least 1 km. On detecting visibility below 1 km it shall enter and log a restricted-visibility state within 60 seconds, retain collision assessment and avoid claiming normal-envelope availability. Traffic detection/avoidance acceptance remains subject to the unresolved scenario parameters in S-001. */
    }
    requirement visibility : Visibility;
    #derivation connection deriveVisibility {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Visibility provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> visibility;
    }

    requirement def <'N-034'> CalmOperation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* At mean wind below 3 m/s the vessel shall retain navigation, recording and autonomous boundary/traffic contingency functions for at least 24 hours with the energy reserve initially available. Neither progress nor station keeping is required in calm conditions. No automatic motor activation is permitted during a qualifying attempt. */
    }
    requirement calmOperation : CalmOperation;
    #derivation connection deriveCalmOperation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* CalmOperation provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> calmOperation;
    }

    requirement def <'N-035'> EnvelopeTransition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Within 60 seconds of detecting an operating wind or wave limit exceedance, the vessel shall enter and log survival mode and retain position recording at least once per minute. After 10 continuous minutes inside operating limits, autonomous sailing shall resume within 5 minutes without repair or operator commands. Entry into survival mode shall not enable the recovery motor. */
    }
    requirement envelopeTransition : EnvelopeTransition;
    #derivation connection deriveEnvelopeTransition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* EnvelopeTransition provides a separately verifiable criterion for environmentalEnvelope. */
        end #original source ::> environmentalEnvelope;
        end #derive target ::> envelopeTransition;
    }

    requirement def <'N-041'> FreshwaterExposure {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Following 72 hours continuous freshwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its Gorge functional checks without repair or servicing. */
    }
    requirement freshwaterExposure : FreshwaterExposure;
    #derivation connection deriveFreshwaterExposure {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* FreshwaterExposure provides a separately verifiable criterion for marineDurability. */
        end #original source ::> marineDurability;
        end #derive target ::> freshwaterExposure;
    }

    requirement def <'N-042'> SaltwaterExposure {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Following 30 days continuous 35 g/kg saltwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its ocean functional checks without repair or servicing. This campaign is an exposure qualification, not proof of the eventual passage duration. */
    }
    requirement saltwaterExposure : SaltwaterExposure;
    #derivation connection deriveSaltwaterExposure {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* SaltwaterExposure provides a separately verifiable criterion for marineDurability. */
        end #original source ::> marineDurability;
        end #derive target ::> saltwaterExposure;
    }

    requirement def <'N-043'> EnclosureSealing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Before and after each wet-exposure campaign, installed electronics enclosures, connectors and penetrations shall show no detectable liquid ingress on dry internal water-sensitive indicators after 30 minutes immersion with their highest point 1 m below the water surface. */
    }
    requirement enclosureSealing : EnclosureSealing;
    #derivation connection deriveEnclosureSealing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* EnclosureSealing provides a separately verifiable criterion for marineDurability. */
        end #original source ::> marineDurability;
        end #derive target ::> enclosureSealing;
    }

    requirement def <'N-044'> WetMechanicalIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each wet-exposure campaign, external mechanisms shall complete their full commanded travel without seizure, and structural joints shall show no separation or through-cracks on visual inspection at 5 times magnification. */
    }
    requirement wetMechanicalIntegrity : WetMechanicalIntegrity;
    #derivation connection deriveWetMechanicalIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* WetMechanicalIntegrity provides a separately verifiable criterion for marineDurability. */
        end #original source ::> marineDurability;
        end #derive target ::> wetMechanicalIntegrity;
    }

    requirement def <'N-045'> WetElectricalIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each wet-exposure campaign, disconnected cable assemblies shall have end-to-end conductor resistance no more than 10 percent above their pre-test value and conductor-to-conductor/conductor-to-case insulation resistance of at least 1 megohm at 50 V DC. Electronics shall be disconnected during insulation measurement. */
    }
    requirement wetElectricalIntegrity : WetElectricalIntegrity;
    #derivation connection deriveWetElectricalIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* WetElectricalIntegrity provides a separately verifiable criterion for marineDurability. */
        end #original source ::> marineDurability;
        end #derive target ::> wetElectricalIntegrity;
    }

    requirement def <'N-046'> SolarHeating {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* At 40 degC ambient air and 1000 W/m2 incident solar irradiance for 8 hours, powered electronics shall retain operational functions and battery temperatures shall remain within manufacturer operating limits. Charging shall be inhibited whenever measured battery temperature is outside its permitted charge range. */
    }
    requirement solarHeating : SolarHeating;
    #derivation connection deriveSolarHeating {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* SolarHeating provides a separately verifiable criterion for marineDurability. */
        end #original source ::> marineDurability;
        end #derive target ::> solarHeating;
    }

    requirement def <'N-047'> PrintedMaterialAging {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Printed structural material shall retain at least 80 percent of unaged failure load after 300 MJ/m2 cumulative UV exposure in the 300-400 nm band followed by the saltwater exposure campaign. Acceptance shall compare the lowest failure load of five aged coupons with the lowest of five unaged coupons of identical geometry, material, print orientation and process under the same loading fixture and rate. */
    }
    requirement printedMaterialAging : PrintedMaterialAging;
    #derivation connection derivePrintedMaterialAging {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* PrintedMaterialAging provides a separately verifiable criterion for marineDurability. */
        end #original source ::> marineDurability;
        end #derive target ::> printedMaterialAging;
    }

    requirement def <'N-051'> SelfRighting {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* At minimum and maximum mission loading, the vessel shall self-right from 90 and 180 degrees heel within 60 seconds of release without external action or motor thrust. Acceptance shall include five releases at each angle toward each side in freshwater and 35 g/kg saltwater; every release shall meet the time limit without loss of rig or ballast or water reaching electronics. */
        attribute measuredRightingTime : TimeValue;
        require constraint rightingDeadline {
            measuredRightingTime >= 0 [s] and measuredRightingTime <= 60 [s]
        }
    }
    requirement selfRighting : SelfRighting;
    #derivation connection deriveSelfRighting {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* SelfRighting provides a separately verifiable criterion for stabilityAndFouling. */
        end #original source ::> stabilityAndFouling;
        end #derive target ::> selfRighting;
    }

    requirement def <'N-052'> CapsizeControlRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* For every N-051 release, the vessel shall restore autonomous sail/steering control within 120 seconds of release, preserving qualification status and gate progress without operator input. */
        attribute measuredControlRecoveryTime : TimeValue;
        require constraint controlRecoveryDeadline {
            measuredControlRecoveryTime >= 0 [s] and measuredControlRecoveryTime <= 120 [s]
        }
    }
    requirement capsizeControlRecovery : CapsizeControlRecovery;
    #derivation connection deriveCapsizeControlRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* CapsizeControlRecovery provides a separately verifiable criterion for stabilityAndFouling. */
        end #original source ::> stabilityAndFouling;
        end #derive target ::> capsizeControlRecovery;
    }

    requirement def <'N-053'> SubmergedWeedPassage {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall complete five consecutive sailing passes through a 5 m long by 1 m wide submerged milfoil-like vegetation test patch without manual clearing or motor use. The patch shall contain 20 flexible branched stems per square metre, each 0.5-1.0 m long, reaching from below the deepest appendage to within 0.1 m of the surface. In 5 m/s mean wind on the same heading as a weed-free reference run, the vessel shall retain at least 50 percent of reference mean speed through the patch and regain full commanded rudder travel within 5 minutes after each pass. Qualification records shall identify stem material, branch geometry, wet bending stiffness and anchoring so repeated campaigns use the same patch properties; surrogate equivalence to collected local milfoil remains a physical-test validation task. */
    }
    requirement submergedWeedPassage : SubmergedWeedPassage;
    #derivation connection deriveSubmergedWeedPassage {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* SubmergedWeedPassage provides a separately verifiable criterion for stabilityAndFouling. */
        end #original source ::> stabilityAndFouling;
        end #derive target ::> submergedWeedPassage;
    }

    requirement def <'N-054'> WeedSnagShedding {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After one wet 1 m branched vegetation stem is draped across each appendage leading edge in separate tests, the vessel shall clear the snag or regain at least 50 percent of unobstructed sailing speed and full rudder travel within 5 minutes in 5 m/s mean wind, without manual assistance or motor use. Five repetitions per appendage shall pass; stem characteristics shall match the N-053 qualified weed surrogate. */
    }
    requirement weedSnagShedding : WeedSnagShedding;
    #derivation connection deriveWeedSnagShedding {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* WeedSnagShedding provides a separately verifiable criterion for stabilityAndFouling. */
        end #original source ::> stabilityAndFouling;
        end #derive target ::> weedSnagShedding;
    }

    requirement def <'N-055'> WeedBlockageResponse {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* When a vegetation blockage causes commanded rudder motion to remain incomplete for 5 seconds, or speed through water to remain below 25 percent of the preceding weed-free 60-second mean for 60 seconds with mean wind at least 3 m/s, the vessel shall log a suspected fouling fault and enter contingency behavior within a further 10 seconds. It shall retain location reporting and shall not automatically enable the recovery motor during a qualifying attempt. Dense mats are a blockage/avoidance case, not a claimed pass-through capability. */
    }
    requirement weedBlockageResponse : WeedBlockageResponse;
    #derivation connection deriveWeedBlockageResponse {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* WeedBlockageResponse provides a separately verifiable criterion for stabilityAndFouling. */
        end #original source ::> stabilityAndFouling;
        end #derive target ::> weedBlockageResponse;
    }

    requirement def <'N-056'> RecoveryPropulsorWeeds {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During a separately designated powered recovery test, the vessel shall traverse the N-053 patch five times without manual propulsor clearing, retain at least 50 percent of its weed-free powered speed and remain within the motor/controller rated current and temperature limits. A locked propulsor shall cause motor shutdown within 2 seconds; recovery-mode weed clearing shall never bypass challenge-mode motor inhibition. */
    }
    requirement recoveryPropulsorWeeds : RecoveryPropulsorWeeds;
    #derivation connection deriveRecoveryPropulsorWeeds {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* RecoveryPropulsorWeeds provides a separately verifiable criterion for stabilityAndFouling. */
        end #original source ::> stabilityAndFouling;
        end #derive target ::> recoveryPropulsorWeeds;
    }
    #derivation connection motorWeedTolerance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The recovery propulsor must remain usable in the vegetation encountered by the sailing vessel. */
        end #original source ::> recoveryPropulsion;
        end #derive target ::> recoveryPropulsorWeeds;
    }
}
