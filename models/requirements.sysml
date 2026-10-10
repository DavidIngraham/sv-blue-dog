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
        doc /* The vessel shall operate for 72 continuous hours without servicing or external charging while meeting the Gorge operational functions under N-010 and the applicable shared N-001 conditions. A qualification run shall include three consecutive 24-hour cycles, each with at most 6 hours of harvesting and at least 18 hours with harvesting disabled. Harvest input shall be limited to the installed harvester output measured under a frozen, recorded resource profile; a test supply may replay that profile but shall not exceed its measured power or accumulated energy. The conservative usable-energy estimate shall remain above the R-002 recovery reserve throughout. Acceptance requires the initial battery state, harvester configuration, replay profile, actual harvested energy and loads in the test record; absent profile evidence invalidates the test. Passing does not establish indefinite energy balance. */
    }
    requirement def <'E-001'> EnergyAwareness {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall update usable battery-energy and recovery-reserve estimates at least once per second. Against calibrated charge/discharge integration across the operating battery temperature range, usable-energy estimation error shall not exceed 10 percent of measured usable full-charge energy. The low-energy transition shall use a conservative estimate equal to estimated usable energy minus that error allowance. */
    }
    requirement def <'E-002'> NavigationAndControl {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Under the selected operational profile N-010 or N-020 and its shared conditions, the vessel shall update mission guidance and sail/steering commands at least once per second. In each 30-minute qualification run, at least 1710 of the 1800 scheduled one-second epochs shall have a valid position within 10 m and a valid heading within 10 degrees of an independent reference. Missing or invalid epochs count as failures, not excluded samples. Deliberately injected navigation failures shall be assessed separately under E-008 and shall not be mixed into an accuracy run. */
    }
    requirement def <'E-003'> ResetRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After a software watchdog reset with conservative usable battery energy above the recovery reserve and valid navigation observations available, the vessel shall restore mode-appropriate autonomous control, persisted mission mode, gate progress and qualification status within 30 seconds. Reset shall preserve survival and low-energy restrictions; full sailing resumption shall obey N-035. Motor enabling shall obey R-004 and require a fresh authenticated recovery command after restart. Records older than 5 seconds before reset shall persist. An absent or inconsistent persisted qualification state shall force nonqualifying status, never infer a qualifying attempt. */
        attribute measuredRestartTime : TimeValue;
        require constraint restartDeadline {
            measuredRestartTime >= 0 [s] and measuredRestartTime <= 30 [s]
        }
    }
    requirement def <'E-004'> LowEnergyRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* When the conservative usable-energy estimate reaches the R-002 reserve, the vessel shall enter a logged low-energy state within 5 seconds and disable the optional observation payload. Position recording shall continue at least once per minute. Telemetry cadence shall be at most 300 seconds except during active emergency or powered recovery, when the S-003 60-second cadence takes precedence. Autonomous navigation, collision response and R-004 motor inhibition shall remain active. The low-energy flag shall clear after conservative usable energy exceeds 1.2 times the reserve for 10 continuous minutes, independently of survival or recovery flags. Payload operation shall resume only when that flag has cleared and no survival or recovery restriction remains. */
    }
    requirement def <'E-005'> Communications {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* With a functioning link, the vessel shall deliver a current telemetry record to the shore endpoint at least once per 60 seconds in normal operation; E-004 permits 300 seconds in low-energy mode outside active emergency/powered recovery. A 24-hour link outage shall not require operator intervention, erase mission data or stop autonomous control. After reconnection it shall deliver a current record within the active cadence and transfer oldest-first backlog without delaying current records beyond that cadence. Onboard retention shall meet E-007; command handling shall meet C-102. */
    }
    requirement def <'E-006'> IngressResponse {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* In a 30-minute qualification test injecting freshwater into the normally dry hull at 10 mL/min, the vessel shall detect and record ingress within 60 seconds of injection starting, enter a logged recovery-request state, and retain flotation, dry electronics and position reporting for the full test. Detection shall not automatically enable motor propulsion in challenge mode. A pump is one possible implementation, not a prescribed solution. */
    }
    requirement def <'E-007'> MissionEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain at least 30 days of timestamped position, heading, mission mode, gate progress, battery energy and fault state at 1 Hz in normal operation and at least once per minute in low-energy or survival operation. Every external-command disposition, reset, motor-enable transition and qualification change shall be recorded regardless of periodic sampling cadence. Timestamps shall be UTC within 1 second while GNSS time is valid; invalid time and gaps shall be flagged. After abrupt power removal, all records older than 5 seconds before removal shall remain readable. Reconnection shall not delete retained records. Disqualifying transitions shall be persisted before commanded intervention or motor enable; unknown qualification state on restart shall be nonqualifying. */
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
        doc /* David specified desktop manufacture and a 250 mm usable build cube as a project constraint on the vehicle; this is an imposed stakeholder constraint, not a consequence of one-person handling. */
        end #original source ::> roundTrip;
        end #derive target ::> desktopManufacture;
    }

    requirement def <'P-003'> Serviceability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One operator shall be able to replace the battery, each electronics module, each actuator and each serviceable enclosure seal individually within 30 minutes using hand tools, without cutting bonded structural joints or destroying adjacent parts. Following each replacement, the assembly shall pass the N-043 enclosure immersion criterion and a complete commanded-travel check for affected actuators. */
    }
    requirement serviceability : Serviceability;
    #derivation connection deriveServiceability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Repeated deployment motivates maintainability between attempts; the timed service target is an engineering allocation, not implied by printer size. */
        end #original source ::> GorgeChallenge::repeatedOperation;
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
        doc /* After accepting an emergency abort, the vessel shall persistently latch the attempt as disqualified within 1 second, before performing the commanded intervention. During active emergency or powered recovery it shall provide position telemetry at least once per 60 seconds while a link is available, taking precedence over low-energy cadence. A physically accessible local isolation control shall remove motor power within 1 second and prevent restart until deliberately reset. Loss of remote control for 5 seconds during manual powered recovery shall command zero thrust within a further 1 second while retaining recording and location reporting; R-004 remains applicable. */
    }
    requirement safeRecovery : SafeRecovery;
    #derivation connection deriveSafeRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Permitted emergency intervention requires explicit abort, qualification, isolation and control-loss behavior. */
        end #original source ::> GorgeChallenge::emergencyIntervention;
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
        doc /* The vessel shall retain the common environmental capabilities specified by the shared exposure requirements in both mission environments, with distinct operational and survival outcomes. Gorge acceptance uses N-010 and its profile leaves; ocean acceptance uses N-020 and its profile leaves. These mission-specific profiles are not interchangeable, and a Gorge release does not require ocean qualification. Qualification shall exercise navigation, sail/steering control, recording and available-link telemetry concurrently; survival acceptance permits loss of course progress but requires flotation, attached rig/ballast, dry electronics and retained mission state. Passing the Gorge profile alone shall not establish ocean capability. */
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
        doc /* The vessel shall retain its required functions and structural integrity during repeated freshwater Gorge service and prolonged saltwater ocean exposure. Qualification uses N-041 freshwater for the Gorge profile and N-042 saltwater for the ocean profile; dual-profile qualification requires both campaigns. Shared sealing, material aging and thermal checks use that selected campaign. Acceptance shall include post-exposure functional checks for the selected profile. Derivation edges indicate reasoning, not unconditional applicability of every descendant to every mission. */
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
        doc /* At maximum mission load, auxiliary powered recovery shall sustain at least 0.5 m/s speed over ground for 30 minutes directly against a 1.5 m/s current, with wind no greater than 5 m/s and waves no greater than 0.2 m. Acceptance shall measure track, current and electrical power. This sheltered recovery target is not a storm-recovery guarantee; motor enable and challenge qualification shall comply with R-004, and isolation/control-loss behavior with S-003. */
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
        doc /* The protected recovery reserve shall be at least 1.2 times the sum of 30 minutes of worst-case electrical motor power measured in the R-001 recovery test and 2 hours of essential navigation/control/recording/telemetry electrical power measured at the S-003 recovery cadence. Motor and essential powers shall be separate, non-overlapping measurements. Reserve sizing shall use the selected installed configuration; available battery energy shall be characterized at the lowest operating battery temperature and end-of-service capacity. Launch admission is R-003; in-mission reserve crossing invokes E-004. */
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
        doc /* The shore endpoint shall display UTC sample time, position, mission mode, conservative usable battery energy, reserve, faults and age of each current telemetry record. It shall mark records stale above 120 seconds age in normal/emergency/powered-recovery modes and above 600 seconds in explicitly reported low-energy mode only when neither emergency nor powered recovery is active. Emergency or powered-recovery flags take precedence if flags coexist. Missing or unrecognized mode shall use 120 seconds. Stale denotes data age, not a diagnosis of link failure; it clears only upon receipt of a record within its mode threshold. A 24-hour outage/reconnection test shall restore reception, preserve identity/sequence numbers and suppress duplicate presentation as new observations. Delivery cadence shall meet E-005 and S-003. */
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
        doc /* The Gorge mission sets the river environment; it does not impose the ocean profile. */
        end #original source ::> roundTrip;
        end #derive target ::> gorgeEnvironment;
    }

    requirement def <'N-020'> OceanEnvironment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall operate on a northeast Pacific passage toward Hawaii in saltwater, ocean swell, wind seas and prolonged unattended exposure. Ocean-derived parameter requirements and the shared exposure requirements apply together. The baseline is not a hurricane-survival claim or a completed route/season qualification. */
    }
    requirement oceanEnvironment : OceanEnvironment;
    #derivation connection deriveOceanEnvironment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The Hawaii mission sets the ocean environment; this profile is not a Gorge acceptance prerequisite. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
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
        doc /* The vessel shall retain navigation and control in currents from 0 to 1.5 m/s from any direction relative to wind and waves. Qualification shall include opposing current. Predicted boundary risk shall invoke S-002; current tolerance alone does not ensure progress or station keeping. Positive upstream speed is not required at every wind speed or heading. */
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
        doc /* The vessel shall retain navigation and control in currents from 0 to 1.0 m/s from any direction relative to wind and waves. Qualification shall include opposing current. Predicted boundary risk shall invoke S-002; current tolerance alone does not ensure progress or station keeping. Positive upstream speed is not required at every wind speed or heading. */
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
        doc /* The vessel shall retain operational functions from 0 to 40 degC ambient air temperature. Qualification shall include powered cold and hot endpoints with internal temperatures stabilized to less than 1 degC change per hour, followed by 2 hours of operation at each endpoint. The same temperature range applies during survival, with only the mode-appropriate retained functions required by N-001/N-035. */
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
        doc /* The immersed hull, appendages and installed equipment shall retain operational functions in water from 2 to 30 degC, including 2 hours at each endpoint after thermal stabilization. The same temperature range applies during survival, with only the mode-appropriate retained functions required by N-001/N-035. */
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
        doc /* With harvesting disabled, the vessel shall retain navigation, recording and autonomous boundary/traffic contingency functions for 24 continuous hours in mean wind below 3 m/s, without drawing conservative usable energy below the R-002 reserve. Initial conservative usable energy shall cover the reserve plus 24 hours of the measured worst-case electrical load for those calm-mode functions. Acceptance shall record the initial energy, load measurement and full energy history. Neither progress nor station keeping is required; R-004 prohibits automatic motor activation in a qualifying attempt. */
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
        doc /* Within 60 seconds of detecting an upper operational wind or wave limit exceedance for the selected profile, the vessel shall enter and log survival mode with position recording at least once per minute. Calm conditions invoke N-034, not this upper-limit trigger. After 10 continuous minutes inside the selected operational wind/wave limits, full autonomous sailing shall resume within 5 minutes if navigation is valid and no low-energy, emergency-recovery or isolation restriction remains. Otherwise the vessel shall retain and log the blocking mode. Restoration of mode-appropriate control after capsize under N-052 does not bypass this resumption gate or R-004. */
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
        doc /* For Gorge qualification, following 72 hours continuous freshwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its Gorge functional checks without repair or servicing. */
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
        doc /* For ocean qualification, following 30 days continuous 35 g/kg saltwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its ocean functional checks without repair or servicing. This campaign is an exposure qualification, not proof of the eventual passage duration. */
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
        doc /* Printed structural material shall retain at least 80 percent of unaged failure load after 300 MJ/m2 cumulative UV exposure in the 300-400 nm band followed by the selected profile wet-exposure campaign (N-041 for Gorge; N-042 for ocean). Dual-profile qualification shall evaluate both aging/exposure sequences. Acceptance shall compare the lowest failure load of five aged coupons with the lowest of five unaged coupons of identical geometry, material, print orientation and process under the same loading fixture and rate. */
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
        doc /* At minimum and maximum mission loading, the vessel shall self-right from 90 and 180 degrees heel within 60 seconds of release without external action or motor thrust. Acceptance shall include five releases at each angle toward each side in freshwater for Gorge qualification or 35 g/kg saltwater for ocean qualification; dual qualification requires both media; every release shall meet the time limit without loss of rig or ballast or water reaching electronics. */
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
        doc /* For every N-051 release, the vessel shall restore mode-appropriate autonomous sail/steering control within 120 seconds from release without operator input, preserving gate progress and qualification status. Restoration shall retain active survival, low-energy, recovery and motor-inhibition restrictions. This deadline is not permission to resume normal sailing before N-035 permits it. */
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
        doc /* For Gorge qualification, the vessel shall complete five consecutive sailing passes through a 5 m long by 1 m wide submerged milfoil-like vegetation test patch without manual clearing or motor use. The patch shall contain 20 flexible branched stems per square metre, each 0.5-1.0 m long, reaching from below the deepest appendage to within 0.1 m of the surface. In 5 m/s mean wind on the same heading as a weed-free reference run, the vessel shall retain at least 50 percent of reference mean water-relative speed through the patch and regain full commanded rudder travel within 5 minutes after each pass. Qualification records shall identify stem material, branch geometry, wet bending stiffness and anchoring so repeated campaigns use the same patch properties; surrogate equivalence to collected local milfoil remains a physical-test validation task. */
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
        doc /* For Gorge qualification, after one wet 1 m branched vegetation stem is draped across each appendage leading edge in separate tests, the vessel shall regain both at least 50 percent of unobstructed reference sailing speed and full commanded rudder travel within 5 minutes in 5 m/s mean wind, without manual assistance or motor use. Removing visible weed alone is not acceptance. Five repetitions per appendage shall pass, using the same heading and water-relative speed reference; stem characteristics shall match the N-053 qualified weed surrogate. */
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
        doc /* For Gorge qualification, when a vegetation blockage causes commanded rudder motion to remain incomplete for 5 seconds, or speed through water to remain below 25 percent of the preceding weed-free 60-second mean for 60 seconds with mean wind at least 3 m/s, the vessel shall log a suspected fouling fault and enter contingency behavior within a further 10 seconds. It shall retain location reporting and shall not automatically enable the recovery motor during a qualifying attempt. Dense mats are a blockage/avoidance case, not a claimed pass-through capability. */
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
        doc /* During a separately designated Gorge powered-recovery test, the vessel shall traverse the N-053 patch five times without manual propulsor clearing, retain at least 50 percent of its weed-free mean water-relative powered speed on the same heading and remain within the motor/controller rated current and temperature limits. A locked propulsor shall cause motor shutdown within 2 seconds; recovery-mode weed clearing shall never bypass challenge-mode motor inhibition. */
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
    requirement def <'E-008'> NavigationAvailability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall provide valid position and heading observations at at least 1710 of the 1800 scheduled one-second epochs in each 30-minute operational qualification run. Missing and invalid epochs count against availability. Observations older than 5 seconds shall be marked invalid and trigger a logged navigation-degraded state within 1 second; stale values shall not be presented as current. Fault-injection tests shall verify the degraded transition separately from the availability run. */
        attribute validEpochs : Integer;
        require constraint availabilityFraction {
            validEpochs >= 1710 and validEpochs <= 1800
        }
    }
    requirement navigationAvailability : NavigationAvailability;
    requirement def <'R-003'> LaunchEnergyAdmission {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall inhibit mission start unless the conservative usable battery-energy estimate is strictly greater than the protected reserve sized under R-002. A missing, stale or invalid energy estimate or reserve configuration shall inhibit start. The estimate shall be no older than 1 second at admission. Acceptance shall inject values below, equal to and above the reserve and missing/invalid/stale inputs. */
        attribute conservativeStartEnergy : EnergyValue;
        attribute protectedReserve : EnergyValue;
        attribute estimateAge : TimeValue;
        attribute estimateValid : Boolean;
        attribute reserveValid : Boolean;
        attribute missionStartEnabled : Boolean;
        attribute admissionEligible : Boolean =
            estimateValid and reserveValid and protectedReserve > 0 [J] and
            estimateAge >= 0 [s] and estimateAge <= 1 [s] and
            conservativeStartEnergy > protectedReserve;
        require constraint launchEnergyGate {
            not missionStartEnabled or admissionEligible
        }
    }
    requirement launchEnergyAdmission : LaunchEnergyAdmission;
    requirement def <'R-004'> ChallengeMotorInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown, including restart and link loss. On an accepted powered-recovery request, nonqualifying status shall be persisted and logged before motor enable. Restart shall require a fresh authenticated recovery command before any motor enable. Tests shall cover qualifying, nonqualifying and unknown status, power loss at the transition and conflicting/stale commands. */
        attribute qualifying : Boolean;
        attribute qualificationStateKnown : Boolean;
        attribute motorEnabled : Boolean;
        require constraint motorQualificationInvariant {
            not motorEnabled or (qualificationStateKnown and not qualifying)
        }
    }
    requirement challengeMotorInhibition : ChallengeMotorInhibition;
    #derivation connection auditDerivation1 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* NavigationAvailability isolates a separately verifiable consequence of navigationAndControl. */
        end #original source ::> navigationAndControl;
        end #derive target ::> navigationAvailability;
    }
    #derivation connection auditDerivation2 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* LaunchEnergyAdmission isolates a separately verifiable consequence of recoveryEnergy. */
        end #original source ::> recoveryEnergy;
        end #derive target ::> launchEnergyAdmission;
    }
    #derivation connection auditDerivation3 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* ChallengeMotorInhibition isolates a separately verifiable consequence of GorgeChallenge::sailingPropulsion. */
        end #original source ::> GorgeChallenge::sailingPropulsion;
        end #derive target ::> challengeMotorInhibition;
    }
    #derivation connection auditDerivation4 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* No-intervention qualification must survive resets and motor-mode transitions. */
        end #original source ::> GorgeChallenge::unassistedAttempt;
        end #derive target ::> challengeMotorInhibition;
    }
    #derivation connection auditDerivation5 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Accepted external control changes the attempt qualification; communications alone does not supply this rule. */
        end #original source ::> GorgeChallenge::unassistedAttempt;
        end #derive target ::> commandIntegrity;
    }
    #derivation connection auditDerivation6 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The emergency control channel needs authenticated, fresh commands and persistent qualification changes. */
        end #original source ::> GorgeChallenge::emergencyIntervention;
        end #derive target ::> commandIntegrity;
    }
    #derivation connection auditDerivation7 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An ocean route also needs configured boundaries and no-feasible-route behavior; its boundaries differ from the Gorge course. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> operatingBoundary;
    }
    #derivation connection auditDerivation8 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Deployment permissions and applicable rules depend on the ocean route as well as the Gorge mission. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> regulatoryClassification;
    }
    #derivation connection auditDerivation9 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Unattended ocean preparation and post-voyage maintenance motivate replaceable modules; this is not at-sea servicing during qualification. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> serviceability;
    }
    #derivation connection auditDerivation10 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The river profile supplies the freshwater exposure medium. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> freshwaterExposure;
    }
    #derivation connection auditDerivation11 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The ocean profile supplies the saltwater exposure medium. */
        end #original source ::> oceanEnvironment;
        end #derive target ::> saltwaterExposure;
    }
    #derivation connection auditDerivation12 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* David identified Columbia River milfoil as a Gorge design condition. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> submergedWeedPassage;
    }
    #derivation connection auditDerivation13 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Appendage snags are a consequence of the Gorge submerged-vegetation exposure. */
        end #original source ::> gorgeEnvironment;
        end #derive target ::> weedSnagShedding;
    }
}
