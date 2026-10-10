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
        doc /* Aggregate requirement for EnergyAwareness. Acceptance requires all applicable derived leaf results (E-101, E-102, E-103, E-104); this parent has no independent executable pass/fail predicate. Shared verification context: Energy estimation and conservative decision inputs; accuracy uses calibrated energy integration across operating battery temperatures. */
    }
    requirement def <'E-002'> NavigationAndControl {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Aggregate requirement for NavigationAndControl. Acceptance requires all applicable derived leaf results (E-105, E-106, E-107, E-108, E-109); this parent has no independent executable pass/fail predicate. Shared verification context: Qualification uses the selected mission profile. Accuracy trials contain 1800 scheduled one-second epochs in 30 minutes; invalid or missing epochs fail. Position and heading criteria use the same set of at least 1710 qualifying epochs, preventing separate selection of different good samples. Fault-injection runs are separate. */
    }
    requirement def <'E-003'> ResetRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Aggregate requirement for ResetRecovery. Acceptance requires all applicable derived leaf results (E-110, E-111, E-112, E-113, E-145, E-136, E-139, E-138, R-102, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: Watchdog-reset tests start above protected reserve with valid navigation observations. Normal sailing remains subject to N-035; data and qualification persistence have shared leaf criteria. */
    }
    requirement def <'E-004'> LowEnergyRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Aggregate requirement for LowEnergyRecovery. Acceptance requires all applicable derived leaf results (E-114, E-115, E-116, E-117, E-118, E-119, E-130, E-120, E-132, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: Reserve means R-002. Emergency/recovery cadence takes precedence; clearing low-energy state is independent of other modes, while payload enabling respects all restrictions. */
    }
    requirement def <'E-005'> Communications {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Aggregate requirement for Communications. Acceptance requires all applicable derived leaf results (E-120, E-121, E-122, E-123, E-124, E-131, E-137); this parent has no independent executable pass/fail predicate. Shared verification context: Link availability is a delivery-test precondition, not a coverage guarantee. Normal cadence is 60 seconds; low-energy alone permits 300 seconds; emergency/powered recovery takes precedence at 60 seconds. Outage tests last 24 hours. */
    }
    requirement def <'E-006'> IngressResponse {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Aggregate requirement for IngressResponse. Acceptance requires all applicable derived leaf results (E-125, E-126, E-127, E-128, E-129, E-144, E-132, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: All leaves use a 30-minute freshwater injection at 10 mL/min into the normally dry hull. No pump technology is prescribed; R-004 remains applicable. */
    }
    requirement def <'E-007'> MissionEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Aggregate requirement for MissionEvidence. Acceptance requires all applicable derived leaf results (E-130, E-131, E-132, E-133, E-134, E-135, E-136, E-137, E-138, E-139); this parent has no independent executable pass/fail predicate. Shared verification context: Periodic records contain position, heading, mode, gate progress, battery energy and fault state. Critical events are independent of periodic cadence. Timestamp accuracy is assessed with valid GNSS time. */
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
        doc /* Aggregate requirement for Transportability. Acceptance requires all applicable derived leaf results (P-101, P-102, P-103, P-104, P-105, P-106); this parent has no independent executable pass/fail predicate. Shared verification context: Demonstrate with one adult, no powered lift, a firm bank or ramp of slope at most 1:12, wind at most 5 m/s and waves at most 0.2 m. This is not a survival-envelope recovery claim. */
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
        doc /* Aggregate requirement for Serviceability. Acceptance requires all applicable derived leaf results (P-107, P-108, P-109, P-110); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise individual replacement of the battery, every electronics module, every actuator and every serviceable enclosure seal by one operator using hand tools. */
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
        doc /* Aggregate requirement for TrafficSafety. Acceptance requires all applicable derived leaf results (S-101, S-102, S-103, S-104); this parent has no independent executable pass/fail predicate. Shared verification context: Use independently recorded head-on, crossing and overtaking AIS and non-AIS targets, day and night in the selected operational profile. Detection ranges, target signatures, closest-approach margins and maneuver feasibility remain unresolved acceptance parameters; tracking and avoidance cannot receive complete passes until these are frozen. */
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
        doc /* Aggregate requirement for OperatingBoundary. Acceptance requires all applicable derived leaf results (S-105, S-106, S-107, S-108, S-109); this parent has no independent executable pass/fail predicate. Shared verification context: Use uploaded permitted-water and exclusion polygons, with a 60-second prediction horizon. Inject approaches to every boundary, navigation loss and no-feasible-maneuver cases. Coordinates and uncertainty/clearance margins are controlled mission inputs with no default values. */
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
        doc /* Aggregate requirement for SafeRecovery. Acceptance requires all applicable derived leaf results (S-110, S-111, S-112, S-113, S-114, S-115, E-138, R-101, E-130); this parent has no independent executable pass/fail predicate. Shared verification context: Emergency intervention ends attempt qualification. Exercise active emergency, powered recovery, local isolation and remote-control loss, including coexisting low-energy flags. */
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
        doc /* Aggregate requirement for NavigationConspicuity. Acceptance requires all applicable derived leaf results (S-116, S-117, S-118, S-119, S-120, S-121); this parent has no independent executable pass/fail predicate. Shared verification context: Use the deployment-specific compliance matrix for sailing, powered-recovery and stationary modes, including its visibility, arcs, colors and sound criteria. The matrix remains a deployment hold point under S-005. */
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
        doc /* Aggregate requirement for RegulatoryClassification. Acceptance requires all applicable derived leaf results (S-122, S-123); this parent has no independent executable pass/fail predicate. Shared verification context: Acceptance is deployment document review, not onboard behavior or an assertion of buoy status. */
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
        doc /* Aggregate requirement for TelemetryEquipment. Acceptance requires all applicable derived leaf results (C-201, C-202, C-203, C-204); this parent has no independent executable pass/fail predicate. Shared verification context: Freshness threshold is 120 seconds for normal, emergency, powered recovery or unknown mode, and 600 seconds only for explicitly reported low energy without emergency or powered recovery. Staleness describes data age, not diagnosed link failure. Exercise a 24-hour outage and reconnection. */
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
        doc /* Aggregate requirement for CommandIntegrity. Acceptance requires all applicable derived leaf results (C-205, C-206, C-207, C-208, C-209, C-210, C-211, E-132, E-138); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise complete command receipt, authentication failure, replayed sequence numbers, age greater than 30 seconds, and external control during a qualifying attempt. */
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
        doc /* Aggregate requirement for Visibility. Acceptance requires all applicable derived leaf results (N-101, N-102, N-103, N-104, N-105); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise daylight and darkness at meteorological visibility of at least 1 km, and detected visibility below 1 km. Traffic performance remains subject to unresolved S-001 scenarios. */
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
        doc /* Aggregate requirement for EnvelopeTransition. Acceptance requires all applicable derived leaf results (N-106, N-107, N-108, N-109, N-110, E-130, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: The trigger is a detected upper operational wind or wave limit exceedance for the selected profile; calm invokes N-034. Resumption eligibility requires 10 continuous minutes inside the selected wind/wave limits, valid navigation and no low-energy, emergency-recovery or isolation restriction. */
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
        doc /* Aggregate requirement for WetMechanicalIntegrity. Acceptance requires all applicable derived leaf results (N-111, N-112); this parent has no independent executable pass/fail predicate. Shared verification context: Evaluate after each selected profile wet-exposure campaign under N-002. */
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
        doc /* Aggregate requirement for WetElectricalIntegrity. Acceptance requires all applicable derived leaf results (N-113, N-114); this parent has no independent executable pass/fail predicate. Shared verification context: Evaluate disconnected cable assemblies after each selected profile wet-exposure campaign under N-002; disconnect electronics for insulation measurement. */
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
        doc /* Aggregate requirement for SolarHeating. Acceptance requires all applicable derived leaf results (N-115, N-116, N-117); this parent has no independent executable pass/fail predicate. Shared verification context: Expose the powered vessel to 40 degC ambient air and 1000 W/m2 incident solar irradiance for 8 hours; use the installed battery manufacturer temperature limits. */
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
        doc /* Aggregate requirement for SelfRighting. Acceptance requires all applicable derived leaf results (N-118, N-119, N-120, N-121); this parent has no independent executable pass/fail predicate. Shared verification context: Use minimum and maximum mission loading, five releases at each angle of 90 and 180 degrees toward each side, without external action or motor thrust. Use freshwater for Gorge or 35 g/kg saltwater for ocean; dual qualification requires both media. All leaves apply to every release. */
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
        doc /* Aggregate requirement for CapsizeControlRecovery. Acceptance requires all applicable derived leaf results (N-122, N-123, N-124, N-125); this parent has no independent executable pass/fail predicate. Shared verification context: Apply to every N-051 release without operator input. Mode-appropriate control does not mean normal sailing before the N-035 resumption gate permits it. */
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
        doc /* Aggregate requirement for SubmergedWeedPassage. Acceptance requires all applicable derived leaf results (N-126, N-127); this parent has no independent executable pass/fail predicate. Shared verification context: Gorge campaign: five consecutive sailing passes without manual clearing or motor use through a 5 m by 1 m patch of 20 flexible branched stems per square metre, each 0.5-1.0 m long, extending from below the deepest appendage to within 0.1 m of the surface. Use 5 m/s mean wind and the weed-free reference heading. Record material, branch geometry, wet bending stiffness and anchoring; equivalence to local milfoil remains a physical-test validation task. */
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
        doc /* Aggregate requirement for WeedSnagShedding. Acceptance requires all applicable derived leaf results (N-128, N-129); this parent has no independent executable pass/fail predicate. Shared verification context: Gorge campaign: drape one wet 1 m branched stem over one appendage leading edge at a time, five repetitions per appendage, with N-053 surrogate characteristics, 5 m/s mean wind and the unobstructed reference heading. No manual assistance or motor use. Both leaf criteria apply to every repetition; visible stem removal alone is insufficient. */
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
        doc /* Aggregate requirement for WeedBlockageResponse. Acceptance requires all applicable derived leaf results (N-130, N-131, N-132, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: Gorge trigger: vegetation prevents completion of commanded rudder motion for 5 seconds, or keeps water-relative speed below 25 percent of the preceding weed-free 60-second mean for 60 seconds with mean wind at least 3 m/s. Dense mats are a blockage/avoidance case, not a pass-through claim. */
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
        doc /* Aggregate requirement for RecoveryPropulsorWeeds. Acceptance requires all applicable derived leaf results (N-133, N-134, N-135, N-136, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: Use a separately designated Gorge powered-recovery test with five passes through the N-053 patch without manual propulsor clearing, on the weed-free powered reference heading. Exercise locked propulsor separately. */
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
        doc /* Aggregate requirement for NavigationAvailability. Acceptance requires all applicable derived leaf results (E-140, E-141, E-142, E-143, E-132); this parent has no independent executable pass/fail predicate. Shared verification context: Campaigns use 1800 scheduled one-second epochs in 30 minutes, with missing/invalid epochs counted as failures. Fault injection is separate. */
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
        doc /* Aggregate requirement for ChallengeMotorInhibition. Acceptance requires all applicable derived leaf results (R-101, R-102, E-138, E-132); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise qualifying, nonqualifying and unknown qualification states, restart, link loss, power loss during transitions and conflicting/stale commands. Shared qualification persistence applies before enabling intervention. */
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

    // Independently verifiable acceptance leaves.
    requirement def <'E-101'> EnergyEstimateCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall refresh usable battery-energy estimates at least once per second. Verification uses the shared context of E-001. */
    }
    requirement energyEstimateCadence : EnergyEstimateCadence;

    #derivation connection decomposeEnergyEstimateCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. */
        end #original source ::> energyAwareness;
        end #derive target ::> energyEstimateCadence;
    }

    requirement def <'E-102'> ReserveEstimateCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall refresh protected recovery-reserve estimates at least once per second. Verification uses the shared context of E-001. */
    }
    requirement reserveEstimateCadence : ReserveEstimateCadence;

    #derivation connection decomposeReserveEstimateCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. */
        end #original source ::> energyAwareness;
        end #derive target ::> reserveEstimateCadence;
    }

    requirement def <'E-103'> EnergyEstimateAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Usable-energy estimation error shall not exceed 10 percent of measured usable full-charge energy relative to calibrated charge/discharge integration across operating battery temperatures. Verification uses the shared context of E-001. */
    }
    requirement energyEstimateAccuracy : EnergyEstimateAccuracy;

    #derivation connection decomposeEnergyEstimateAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. */
        end #original source ::> energyAwareness;
        end #derive target ::> energyEstimateAccuracy;
    }

    requirement def <'E-104'> ConservativeEnergyEstimate {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The usable-energy input to admission and low-energy decisions shall equal estimated usable energy minus the EnergyEstimateAccuracy error allowance. Verification uses the shared context of E-001. */
    }
    requirement conservativeEnergyEstimate : ConservativeEnergyEstimate;

    #derivation connection decomposeConservativeEnergyEstimate {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-001; the parent supplies shared verification conditions. */
        end #original source ::> energyAwareness;
        end #derive target ::> conservativeEnergyEstimate;
    }

    requirement def <'E-105'> GuidanceUpdateCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During operational qualification, mission guidance shall update at least once per second. Verification uses the shared context of E-002. */
    }
    requirement guidanceUpdateCadence : GuidanceUpdateCadence;

    #derivation connection decomposeGuidanceUpdateCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. */
        end #original source ::> navigationAndControl;
        end #derive target ::> guidanceUpdateCadence;
    }

    requirement def <'E-106'> SailCommandCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During operational qualification, commanded sail position shall update at least once per second. Verification uses the shared context of E-002. */
    }
    requirement sailCommandCadence : SailCommandCadence;

    #derivation connection decomposeSailCommandCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. */
        end #original source ::> navigationAndControl;
        end #derive target ::> sailCommandCadence;
    }

    requirement def <'E-107'> SteeringCommandCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During operational qualification, commanded steering position shall update at least once per second. Verification uses the shared context of E-002. */
    }
    requirement steeringCommandCadence : SteeringCommandCadence;

    #derivation connection decomposeSteeringCommandCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. */
        end #original source ::> navigationAndControl;
        end #derive target ::> steeringCommandCadence;
    }

    requirement def <'E-108'> PositionAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* At every epoch in the common E-002 acceptance set, valid position error shall be at most 10 m against an independent reference. Verification uses the shared context of E-002. */
    }
    requirement positionAccuracy : PositionAccuracy;

    #derivation connection decomposePositionAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. */
        end #original source ::> navigationAndControl;
        end #derive target ::> positionAccuracy;
    }

    requirement def <'E-109'> HeadingAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* At every epoch in the common E-002 acceptance set, valid heading error shall be at most 10 degrees against an independent reference. Verification uses the shared context of E-002. */
    }
    requirement headingAccuracy : HeadingAccuracy;

    #derivation connection decomposeHeadingAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-002; the parent supplies shared verification conditions. */
        end #original source ::> navigationAndControl;
        end #derive target ::> headingAccuracy;
    }

    requirement def <'E-110'> RestartDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After a watchdog reset under E-003 preconditions, the vessel shall restore mode-appropriate autonomous control within 30 seconds. Verification uses the shared context of E-003. */
        attribute measuredRestartTime : TimeValue;
        require constraint restartDeadline {
            measuredRestartTime >= 0 [s] and measuredRestartTime <= 30 [s]
        }
    }
    requirement restartDeadline : RestartDeadline;

    #derivation connection decomposeRestartDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. */
        end #original source ::> resetRecovery;
        end #derive target ::> restartDeadline;
    }

    requirement def <'E-111'> MissionStateRestoration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Within 30 seconds after a watchdog reset under E-003 preconditions, restored mission mode shall equal the last persisted mode. Verification uses the shared context of E-003. */
    }
    requirement missionStateRestoration : MissionStateRestoration;

    #derivation connection decomposeMissionStateRestoration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. */
        end #original source ::> resetRecovery;
        end #derive target ::> missionStateRestoration;
    }

    requirement def <'E-112'> GateProgressRestoration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Within 30 seconds after a watchdog reset under E-003 preconditions, restored gate progress shall equal the last persisted gate progress. Verification uses the shared context of E-003. */
    }
    requirement gateProgressRestoration : GateProgressRestoration;

    #derivation connection decomposeGateProgressRestoration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. */
        end #original source ::> resetRecovery;
        end #derive target ::> gateProgressRestoration;
    }

    requirement def <'E-113'> ResetRestrictionPreservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After watchdog reset, each active survival, low-energy, recovery and isolation restriction shall remain effective until its own release condition is met. Verification uses the shared context of E-003. */
    }
    requirement resetRestrictionPreservation : ResetRestrictionPreservation;

    #derivation connection decomposeResetRestrictionPreservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. */
        end #original source ::> resetRecovery;
        end #derive target ::> resetRestrictionPreservation;
    }

    requirement def <'E-114'> LowEnergyEntry {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* When conservative usable energy reaches or falls below protected reserve, the vessel shall set the low-energy flag within 5 seconds. Verification uses the shared context of E-004. */
    }
    requirement lowEnergyEntry : LowEnergyEntry;

    #derivation connection decomposeLowEnergyEntry {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> lowEnergyEntry;
    }

    requirement def <'E-115'> LowEnergyPayloadInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* While the low-energy flag is set, the optional observation payload shall be disabled. Verification uses the shared context of E-004. */
    }
    requirement lowEnergyPayloadInhibition : LowEnergyPayloadInhibition;

    #derivation connection decomposeLowEnergyPayloadInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> lowEnergyPayloadInhibition;
    }

    requirement def <'E-116'> LowEnergyNavigationContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* While the low-energy flag is set, autonomous navigation shall remain active. Verification uses the shared context of E-004. */
    }
    requirement lowEnergyNavigationContinuity : LowEnergyNavigationContinuity;

    #derivation connection decomposeLowEnergyNavigationContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> lowEnergyNavigationContinuity;
    }

    requirement def <'E-117'> LowEnergyCollisionContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* While the low-energy flag is set, collision-response behavior shall remain active. Verification uses the shared context of E-004. */
    }
    requirement lowEnergyCollisionContinuity : LowEnergyCollisionContinuity;

    #derivation connection decomposeLowEnergyCollisionContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> lowEnergyCollisionContinuity;
    }

    requirement def <'E-118'> LowEnergyExit {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After conservative usable energy exceeds 1.2 times protected reserve for 10 continuous minutes, the vessel shall clear the low-energy flag independently of survival/recovery flags. Verification uses the shared context of E-004. */
    }
    requirement lowEnergyExit : LowEnergyExit;

    #derivation connection decomposeLowEnergyExit {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> lowEnergyExit;
    }

    requirement def <'E-119'> PayloadRestartPermission {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Payload operation shall remain inhibited whenever a low-energy, survival or recovery restriction is active. Verification uses the shared context of E-004. */
    }
    requirement payloadRestartPermission : PayloadRestartPermission;

    #derivation connection decomposePayloadRestartPermission {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-004; the parent supplies shared verification conditions. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> payloadRestartPermission;
    }

    requirement def <'E-120'> TelemetryDeliveryCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* With a functioning link, current telemetry delivery intervals shall not exceed 60 seconds, except that low-energy operation without emergency/powered recovery permits 300 seconds. Verification uses the shared context of E-005. */
    }
    requirement telemetryDeliveryCadence : TelemetryDeliveryCadence;

    #derivation connection decomposeTelemetryDeliveryCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. */
        end #original source ::> communications;
        end #derive target ::> telemetryDeliveryCadence;
    }

    requirement def <'E-121'> OutageAutonomy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Through a 24-hour telemetry-link outage, autonomous mission control shall continue without operator intervention. Verification uses the shared context of E-005. */
    }
    requirement outageAutonomy : OutageAutonomy;

    #derivation connection decomposeOutageAutonomy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. */
        end #original source ::> communications;
        end #derive target ::> outageAutonomy;
    }

    requirement def <'E-122'> ReconnectCurrentRecord {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After link restoration, a current telemetry record shall arrive within the active TelemetryDeliveryCadence interval. Verification uses the shared context of E-005. */
    }
    requirement reconnectCurrentRecord : ReconnectCurrentRecord;

    #derivation connection decomposeReconnectCurrentRecord {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. */
        end #original source ::> communications;
        end #derive target ::> reconnectCurrentRecord;
    }

    requirement def <'E-123'> BacklogOrdering {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After reconnection, retained backlog records shall be transmitted in ascending acquisition sequence order. Verification uses the shared context of E-005. */
    }
    requirement backlogOrdering : BacklogOrdering;

    #derivation connection decomposeBacklogOrdering {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. */
        end #original source ::> communications;
        end #derive target ::> backlogOrdering;
    }

    requirement def <'E-124'> BacklogCurrentPriority {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During backlog transfer, current telemetry shall continue to meet TelemetryDeliveryCadence. Verification uses the shared context of E-005. */
    }
    requirement backlogCurrentPriority : BacklogCurrentPriority;

    #derivation connection decomposeBacklogCurrentPriority {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-005; the parent supplies shared verification conditions. */
        end #original source ::> communications;
        end #derive target ::> backlogCurrentPriority;
    }

    requirement def <'E-125'> IngressDetection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* In the E-006 injection test, ingress detection shall occur within 60 seconds of injection starting. Verification uses the shared context of E-006. */
    }
    requirement ingressDetection : IngressDetection;

    #derivation connection decomposeIngressDetection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. */
        end #original source ::> ingressResponse;
        end #derive target ::> ingressDetection;
    }

    requirement def <'E-126'> IngressRecoveryRequest {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* In the E-006 test, ingress detection shall set the recovery-request state. Verification uses the shared context of E-006. */
    }
    requirement ingressRecoveryRequest : IngressRecoveryRequest;

    #derivation connection decomposeIngressRecoveryRequest {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. */
        end #original source ::> ingressResponse;
        end #derive target ::> ingressRecoveryRequest;
    }

    requirement def <'E-127'> IngressFlotation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* In the E-006 test, the vessel shall remain afloat for the full 30 minutes. Verification uses the shared context of E-006. */
    }
    requirement ingressFlotation : IngressFlotation;

    #derivation connection decomposeIngressFlotation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. */
        end #original source ::> ingressResponse;
        end #derive target ::> ingressFlotation;
    }

    requirement def <'E-128'> IngressElectronicsProtection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After the E-006 test, enclosed-electronics water-sensitive indicators shall show no liquid ingress. Verification uses the shared context of E-006. */
    }
    requirement ingressElectronicsProtection : IngressElectronicsProtection;

    #derivation connection decomposeIngressElectronicsProtection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. */
        end #original source ::> ingressResponse;
        end #derive target ::> ingressElectronicsProtection;
    }

    requirement def <'E-129'> IngressPositionContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Throughout the E-006 test with a functioning link, position reporting shall meet the active TelemetryDeliveryCadence. Verification uses the shared context of E-006. */
    }
    requirement ingressPositionContinuity : IngressPositionContinuity;

    #derivation connection decomposeIngressPositionContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. */
        end #original source ::> ingressResponse;
        end #derive target ::> ingressPositionContinuity;
    }

    requirement def <'E-130'> PeriodicLogCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Periodic mission records shall be acquired at least once per second normally and once per minute in low-energy or survival operation. Verification uses the shared context of E-007. */
    }
    requirement periodicLogCadence : PeriodicLogCadence;

    #derivation connection decomposePeriodicLogCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> periodicLogCadence;
    }

    requirement def <'E-131'> LogRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Acquired mission records shall remain retrievable onboard for at least 30 days. Verification uses the shared context of E-007. */
    }
    requirement logRetention : LogRetention;

    #derivation connection decomposeLogRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> logRetention;
    }

    requirement def <'E-132'> CriticalEventRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence. Verification uses the shared context of E-007. */
    }
    requirement criticalEventRecording : CriticalEventRecording;

    #derivation connection decomposeCriticalEventRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> criticalEventRecording;
    }

    requirement def <'E-133'> LogTimestampAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* With valid GNSS time, mission-record timestamps shall differ from reference UTC by at most 1 second. Verification uses the shared context of E-007. */
    }
    requirement logTimestampAccuracy : LogTimestampAccuracy;

    #derivation connection decomposeLogTimestampAccuracy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> logTimestampAccuracy;
    }

    requirement def <'E-134'> InvalidTimestampMarking {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each record acquired without valid time shall carry an invalid-time indication. Verification uses the shared context of E-007. */
    }
    requirement invalidTimestampMarking : InvalidTimestampMarking;

    #derivation connection decomposeInvalidTimestampMarking {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> invalidTimestampMarking;
    }

    requirement def <'E-135'> LogGapIndication {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each detected missing sequence of scheduled records shall have a gap indication in retrieved data. Verification uses the shared context of E-007. */
    }
    requirement logGapIndication : LogGapIndication;

    #derivation connection decomposeLogGapIndication {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> logGapIndication;
    }

    requirement def <'E-136'> LogInterruptionDurability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After watchdog reset or abrupt power removal, every record older than 5 seconds before interruption shall remain readable. Verification uses the shared context of E-007. */
    }
    requirement logInterruptionDurability : LogInterruptionDurability;

    #derivation connection decomposeLogInterruptionDurability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> logInterruptionDurability;
    }

    requirement def <'E-137'> ReconnectLogPreservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Communication reconnection shall not delete retained mission records. Verification uses the shared context of E-007. */
    }
    requirement reconnectLogPreservation : ReconnectLogPreservation;

    #derivation connection decomposeReconnectLogPreservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> reconnectLogPreservation;
    }

    requirement def <'E-138'> QualificationPersistence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable. Verification uses the shared context of E-007. */
    }
    requirement qualificationPersistence : QualificationPersistence;

    #derivation connection decomposeQualificationPersistence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> qualificationPersistence;
    }

    requirement def <'E-139'> UnknownQualificationFallback {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* On restart with absent or inconsistent persisted qualification state, the vessel shall adopt nonqualifying status. Verification uses the shared context of E-007. */
    }
    requirement unknownQualificationFallback : UnknownQualificationFallback;

    #derivation connection decomposeUnknownQualificationFallback {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-007; the parent supplies shared verification conditions. */
        end #original source ::> missionEvidence;
        end #derive target ::> unknownQualificationFallback;
    }

    requirement def <'E-140'> NavigationValidEpochs {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* In each E-008 campaign, at least 1710 of 1800 scheduled epochs shall contain valid position and heading observations. Verification uses the shared context of E-008. */
        attribute validEpochs : Integer;
        require constraint availabilityFraction {
            validEpochs >= 1710 and validEpochs <= 1800
        }
    }
    requirement navigationValidEpochs : NavigationValidEpochs;

    #derivation connection decomposeNavigationValidEpochs {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. */
        end #original source ::> navigationAvailability;
        end #derive target ::> navigationValidEpochs;
    }

    requirement def <'E-141'> StaleNavigationInvalidation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Navigation observations older than 5 seconds shall be marked invalid. Verification uses the shared context of E-008. */
    }
    requirement staleNavigationInvalidation : StaleNavigationInvalidation;

    #derivation connection decomposeStaleNavigationInvalidation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. */
        end #original source ::> navigationAvailability;
        end #derive target ::> staleNavigationInvalidation;
    }

    requirement def <'E-142'> NavigationDegradedTransition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* When position or heading becomes invalid due to age, the vessel shall enter navigation-degraded state within 1 second. Verification uses the shared context of E-008. */
    }
    requirement navigationDegradedTransition : NavigationDegradedTransition;

    #derivation connection decomposeNavigationDegradedTransition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. */
        end #original source ::> navigationAvailability;
        end #derive target ::> navigationDegradedTransition;
    }

    requirement def <'E-143'> StaleNavigationUseInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The controller shall not use observations marked invalid as current navigation inputs. Verification uses the shared context of E-008. */
    }
    requirement staleNavigationUseInhibition : StaleNavigationUseInhibition;

    #derivation connection decomposeStaleNavigationUseInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-008; the parent supplies shared verification conditions. */
        end #original source ::> navigationAvailability;
        end #derive target ::> staleNavigationUseInhibition;
    }

    requirement def <'P-101'> SoloTransport {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One adult shall move all mission equipment 100 m without assistance. Verification uses the shared context of P-001. */
    }
    requirement soloTransport : SoloTransport;

    #derivation connection decomposeSoloTransport {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. */
        end #original source ::> transportability;
        end #derive target ::> soloTransport;
    }

    requirement def <'P-102'> LiftMass {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each separately lifted assembly shall have a mass no greater than 15 kg. Verification uses the shared context of P-001. */
    }
    requirement liftMass : LiftMass;

    #derivation connection decomposeLiftMass {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. */
        end #original source ::> transportability;
        end #derive target ::> liftMass;
    }

    requirement def <'P-103'> SetupDuration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One adult shall assemble the vessel from its transport configuration within 30 minutes. Verification uses the shared context of P-001. */
    }
    requirement setupDuration : SetupDuration;

    #derivation connection decomposeSetupDuration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. */
        end #original source ::> transportability;
        end #derive target ::> setupDuration;
    }

    requirement def <'P-104'> PackDuration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One adult shall pack the vessel into its transport configuration within 30 minutes. Verification uses the shared context of P-001. */
    }
    requirement packDuration : PackDuration;

    #derivation connection decomposePackDuration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. */
        end #original source ::> transportability;
        end #derive target ::> packDuration;
    }

    requirement def <'P-105'> SoloLaunch {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One adult shall launch the assembled vessel without assistance. Verification uses the shared context of P-001. */
    }
    requirement soloLaunch : SoloLaunch;

    #derivation connection decomposeSoloLaunch {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. */
        end #original source ::> transportability;
        end #derive target ::> soloLaunch;
    }

    requirement def <'P-106'> SoloRetrieval {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* One adult shall retrieve the vessel from the water without assistance. Verification uses the shared context of P-001. */
    }
    requirement soloRetrieval : SoloRetrieval;

    #derivation connection decomposeSoloRetrieval {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-001; the parent supplies shared verification conditions. */
        end #original source ::> transportability;
        end #derive target ::> soloRetrieval;
    }

    requirement def <'P-107'> ReplacementDuration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each P-003 replacement shall take no more than 30 minutes. Verification uses the shared context of P-003. */
    }
    requirement replacementDuration : ReplacementDuration;

    #derivation connection decomposeReplacementDuration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. */
        end #original source ::> serviceability;
        end #derive target ::> replacementDuration;
    }

    requirement def <'P-108'> NondestructiveService {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each P-003 replacement shall leave bonded structural joints and adjacent parts intact. Verification uses the shared context of P-003. */
    }
    requirement nondestructiveService : NondestructiveService;

    #derivation connection decomposeNondestructiveService {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. */
        end #original source ::> serviceability;
        end #derive target ::> nondestructiveService;
    }

    requirement def <'P-109'> PostServiceSealing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each P-003 replacement, the assembly shall meet the N-043 immersion criterion. Verification uses the shared context of P-003. */
    }
    requirement postServiceSealing : PostServiceSealing;

    #derivation connection decomposePostServiceSealing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. */
        end #original source ::> serviceability;
        end #derive target ::> postServiceSealing;
    }

    requirement def <'P-110'> PostServiceActuation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each P-003 replacement, affected actuators shall complete their full commanded travel. Verification uses the shared context of P-003. */
    }
    requirement postServiceActuation : PostServiceActuation;

    #derivation connection decomposePostServiceActuation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of P-003; the parent supplies shared verification conditions. */
        end #original source ::> serviceability;
        end #derive target ::> postServiceActuation;
    }

    requirement def <'S-101'> TrafficTracking {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall maintain a track for every encounter target within the frozen S-001 detection envelope. Verification uses the shared context of S-001. */
    }
    requirement trafficTracking : TrafficTracking;

    #derivation connection decomposeTrafficTracking {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. */
        end #original source ::> trafficSafety;
        end #derive target ::> trafficTracking;
    }

    requirement def <'S-102'> CollisionAssessmentCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall update collision-risk estimates at least once per second. Verification uses the shared context of S-001. */
    }
    requirement collisionAssessmentCadence : CollisionAssessmentCadence;

    #derivation connection decomposeCollisionAssessmentCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. */
        end #original source ::> trafficSafety;
        end #derive target ::> collisionAssessmentCadence;
    }

    requirement def <'S-103'> AvoidanceCommandDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall issue the prescribed avoiding-action command within 2 seconds of each S-001 collision-risk trigger. Verification uses the shared context of S-001. */
    }
    requirement avoidanceCommandDeadline : AvoidanceCommandDeadline;

    #derivation connection decomposeAvoidanceCommandDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. */
        end #original source ::> trafficSafety;
        end #derive target ::> avoidanceCommandDeadline;
    }

    requirement def <'S-104'> TrafficAwarenessFault {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After traffic assessment has been invalid for more than 5 seconds, the vessel shall log a traffic-awareness fault within 1 second. Verification uses the shared context of S-001. */
    }
    requirement trafficAwarenessFault : TrafficAwarenessFault;

    #derivation connection decomposeTrafficAwarenessFault {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-001; the parent supplies shared verification conditions. */
        end #original source ::> trafficSafety;
        end #derive target ::> trafficAwarenessFault;
    }

    requirement def <'S-105'> BoundaryEvaluationCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall evaluate its current position and predicted trajectory against the S-002 polygons at least once per second. Verification uses the shared context of S-002. */
    }
    requirement boundaryEvaluationCadence : BoundaryEvaluationCadence;

    #derivation connection decomposeBoundaryEvaluationCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. */
        end #original source ::> operatingBoundary;
        end #derive target ::> boundaryEvaluationCadence;
    }

    requirement def <'S-106'> BoundaryAvoidanceDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall issue an avoidance command within 2 seconds of predicting a boundary crossing. Verification uses the shared context of S-002. */
    }
    requirement boundaryAvoidanceDeadline : BoundaryAvoidanceDeadline;

    #derivation connection decomposeBoundaryAvoidanceDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. */
        end #original source ::> operatingBoundary;
        end #derive target ::> boundaryAvoidanceDeadline;
    }

    requirement def <'S-107'> BoundaryAvoidanceRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Every boundary-avoidance command shall have a corresponding event record. Verification uses the shared context of S-002. */
    }
    requirement boundaryAvoidanceRecording : BoundaryAvoidanceRecording;

    #derivation connection decomposeBoundaryAvoidanceRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. */
        end #original source ::> operatingBoundary;
        end #derive target ::> boundaryAvoidanceRecording;
    }

    requirement def <'S-108'> BoundaryStartInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Missing or geometrically invalid boundaries shall inhibit mission start. Verification uses the shared context of S-002. */
    }
    requirement boundaryStartInhibition : BoundaryStartInhibition;

    #derivation connection decomposeBoundaryStartInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. */
        end #original source ::> operatingBoundary;
        end #derive target ::> boundaryStartInhibition;
    }

    requirement def <'S-109'> BoundaryDegradedEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Navigation loss or absence of a feasible maneuver shall produce an explicit degraded-route verdict instead of a safe-route verdict. Verification uses the shared context of S-002. */
    }
    requirement boundaryDegradedEvidence : BoundaryDegradedEvidence;

    #derivation connection decomposeBoundaryDegradedEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-002; the parent supplies shared verification conditions. */
        end #original source ::> operatingBoundary;
        end #derive target ::> boundaryDegradedEvidence;
    }

    requirement def <'S-110'> AbortLatchDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After accepting emergency abort, the vessel shall latch the attempt as disqualified within 1 second. Verification uses the shared context of S-003. */
    }
    requirement abortLatchDeadline : AbortLatchDeadline;

    #derivation connection decomposeAbortLatchDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. */
        end #original source ::> safeRecovery;
        end #derive target ::> abortLatchDeadline;
    }

    requirement def <'S-111'> RecoveryTelemetryCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During active emergency or powered recovery with a functioning link, the vessel shall deliver position telemetry at least once per 60 seconds, including low-energy operation. Verification uses the shared context of S-003. */
    }
    requirement recoveryTelemetryCadence : RecoveryTelemetryCadence;

    #derivation connection decomposeRecoveryTelemetryCadence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. */
        end #original source ::> safeRecovery;
        end #derive target ::> recoveryTelemetryCadence;
    }

    requirement def <'S-112'> MotorIsolationDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A physically accessible local isolation control shall remove motor power within 1 second of activation. Verification uses the shared context of S-003. */
    }
    requirement motorIsolationDeadline : MotorIsolationDeadline;

    #derivation connection decomposeMotorIsolationDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. */
        end #original source ::> safeRecovery;
        end #derive target ::> motorIsolationDeadline;
    }

    requirement def <'S-113'> IsolationRestartInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Motor restart shall remain inhibited after local isolation until deliberate local reset. Verification uses the shared context of S-003. */
    }
    requirement isolationRestartInhibition : IsolationRestartInhibition;

    #derivation connection decomposeIsolationRestartInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. */
        end #original source ::> safeRecovery;
        end #derive target ::> isolationRestartInhibition;
    }

    requirement def <'S-114'> ManualControlLossShutdown {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After remote control has been lost for 5 seconds during manual powered recovery, the vessel shall command zero thrust within a further 1 second. Verification uses the shared context of S-003. */
    }
    requirement manualControlLossShutdown : ManualControlLossShutdown;

    #derivation connection decomposeManualControlLossShutdown {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. */
        end #original source ::> safeRecovery;
        end #derive target ::> manualControlLossShutdown;
    }

    requirement def <'S-115'> ControlLossLocationContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Location reporting shall continue at the active telemetry cadence after remote-control loss whenever a telemetry link is available. Verification uses the shared context of S-003. */
    }
    requirement controlLossLocationContinuity : ControlLossLocationContinuity;

    #derivation connection decomposeControlLossLocationContinuity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-003; the parent supplies shared verification conditions. */
        end #original source ::> safeRecovery;
        end #derive target ::> controlLossLocationContinuity;
    }

    requirement def <'S-116'> NavigationLightPresentation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall present the lights prescribed for its current mode by the S-004 compliance matrix without a person aboard. Verification uses the shared context of S-004. */
    }
    requirement navigationLightPresentation : NavigationLightPresentation;

    #derivation connection decomposeNavigationLightPresentation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. */
        end #original source ::> navigationConspicuity;
        end #derive target ::> navigationLightPresentation;
    }

    requirement def <'S-117'> NavigationShapePresentation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall present the shapes prescribed for its current mode by the S-004 compliance matrix without a person aboard. Verification uses the shared context of S-004. */
    }
    requirement navigationShapePresentation : NavigationShapePresentation;

    #derivation connection decomposeNavigationShapePresentation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. */
        end #original source ::> navigationConspicuity;
        end #derive target ::> navigationShapePresentation;
    }

    requirement def <'S-118'> NavigationSoundPresentation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall present the sound signals prescribed for its current mode by the S-004 compliance matrix without a person aboard. Verification uses the shared context of S-004. */
    }
    requirement navigationSoundPresentation : NavigationSoundPresentation;

    #derivation connection decomposeNavigationSoundPresentation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. */
        end #original source ::> navigationConspicuity;
        end #derive target ::> navigationSoundPresentation;
    }

    requirement def <'S-119'> SignalingModeDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A commanded mode change shall select the corresponding signaling configuration within 1 second. Verification uses the shared context of S-004. */
    }
    requirement signalingModeDeadline : SignalingModeDeadline;

    #derivation connection decomposeSignalingModeDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. */
        end #original source ::> navigationConspicuity;
        end #derive target ::> signalingModeDeadline;
    }

    requirement def <'S-120'> SignalingFaultRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each detectable signaling failure shall be logged within 5 seconds of detection. Verification uses the shared context of S-004. */
    }
    requirement signalingFaultRecording : SignalingFaultRecording;

    #derivation connection decomposeSignalingFaultRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. */
        end #original source ::> navigationConspicuity;
        end #derive target ::> signalingFaultRecording;
    }

    requirement def <'S-121'> SignalingFaultReporting {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* With a functioning link, each detected signaling failure shall be reported to shore within 5 seconds. Verification uses the shared context of S-004. */
    }
    requirement signalingFaultReporting : SignalingFaultReporting;

    #derivation connection decomposeSignalingFaultReporting {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-004; the parent supplies shared verification conditions. */
        end #original source ::> navigationConspicuity;
        end #derive target ::> signalingFaultReporting;
    }

    requirement def <'S-122'> DeploymentComplianceRecord {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each deployment shall have a dated compliance record identifying the craft, dimensions, waters, operating modes, applicable navigation and radio obligations, and permission evidence. Verification uses the shared context of S-005. */
    }
    requirement deploymentComplianceRecord : DeploymentComplianceRecord;

    #derivation connection decomposeDeploymentComplianceRecord {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-005; the parent supplies shared verification conditions. */
        end #original source ::> regulatoryClassification;
        end #derive target ::> deploymentComplianceRecord;
    }

    requirement def <'S-123'> DeploymentReleaseGate {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Deployment release shall be withheld while any mandatory authorization is absent, expired or unresolved. Verification uses the shared context of S-005. */
    }
    requirement deploymentReleaseGate : DeploymentReleaseGate;

    #derivation connection decomposeDeploymentReleaseGate {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of S-005; the parent supplies shared verification conditions. */
        end #original source ::> regulatoryClassification;
        end #derive target ::> deploymentReleaseGate;
    }

    requirement def <'C-201'> TelemetryDisplayContent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The shore endpoint shall display UTC sample time, position, mode, conservative usable energy, reserve, faults and age from each current telemetry record. Verification uses the shared context of C-101. */
    }
    requirement telemetryDisplayContent : TelemetryDisplayContent;

    #derivation connection decomposeTelemetryDisplayContent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. */
        end #original source ::> telemetryEquipment;
        end #derive target ::> telemetryDisplayContent;
    }

    requirement def <'C-202'> TelemetryStaleIndication {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The shore endpoint shall indicate stale data when record age exceeds its C-101 mode threshold until receipt of a record within its applicable threshold. Verification uses the shared context of C-101. */
    }
    requirement telemetryStaleIndication : TelemetryStaleIndication;

    #derivation connection decomposeTelemetryStaleIndication {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. */
        end #original source ::> telemetryEquipment;
        end #derive target ::> telemetryStaleIndication;
    }

    requirement def <'C-203'> TelemetryIdentityPreservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The shore endpoint shall preserve received record identity and sequence numbers across the C-101 outage/reconnection test. Verification uses the shared context of C-101. */
    }
    requirement telemetryIdentityPreservation : TelemetryIdentityPreservation;

    #derivation connection decomposeTelemetryIdentityPreservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. */
        end #original source ::> telemetryEquipment;
        end #derive target ::> telemetryIdentityPreservation;
    }

    requirement def <'C-204'> TelemetryDuplicateSuppression {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The shore endpoint shall not present a duplicate telemetry record as a new observation. Verification uses the shared context of C-101. */
    }
    requirement telemetryDuplicateSuppression : TelemetryDuplicateSuppression;

    #derivation connection decomposeTelemetryDuplicateSuppression {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-101; the parent supplies shared verification conditions. */
        end #original source ::> telemetryEquipment;
        end #derive target ::> telemetryDuplicateSuppression;
    }

    requirement def <'C-205'> UnauthenticatedCommandRejection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Commands failing authentication shall cause zero accepted actuator or mission-state changes. Verification uses the shared context of C-102. */
    }
    requirement unauthenticatedCommandRejection : UnauthenticatedCommandRejection;

    #derivation connection decomposeUnauthenticatedCommandRejection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. */
        end #original source ::> commandIntegrity;
        end #derive target ::> unauthenticatedCommandRejection;
    }

    requirement def <'C-206'> ReplayCommandRejection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Commands with previously used sequence numbers shall cause zero accepted actuator or mission-state changes. Verification uses the shared context of C-102. */
    }
    requirement replayCommandRejection : ReplayCommandRejection;

    #derivation connection decomposeReplayCommandRejection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. */
        end #original source ::> commandIntegrity;
        end #derive target ::> replayCommandRejection;
    }

    requirement def <'C-207'> ExpiredCommandRejection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Commands older than 30 seconds shall cause zero accepted actuator or mission-state changes. Verification uses the shared context of C-102. */
    }
    requirement expiredCommandRejection : ExpiredCommandRejection;

    #derivation connection decomposeExpiredCommandRejection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. */
        end #original source ::> commandIntegrity;
        end #derive target ::> expiredCommandRejection;
    }

    requirement def <'C-208'> AcceptedCommandDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An accepted abort or mode-change command shall be applied within 1 second of complete receipt. Verification uses the shared context of C-102. */
    }
    requirement acceptedCommandDeadline : AcceptedCommandDeadline;

    #derivation connection decomposeAcceptedCommandDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. */
        end #original source ::> commandIntegrity;
        end #derive target ::> acceptedCommandDeadline;
    }

    requirement def <'C-209'> OnboardAcknowledgmentDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An accepted abort or mode-change command shall be acknowledged onboard within 1 second of complete receipt. Verification uses the shared context of C-102. */
    }
    requirement onboardAcknowledgmentDeadline : OnboardAcknowledgmentDeadline;

    #derivation connection decomposeOnboardAcknowledgmentDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. */
        end #original source ::> commandIntegrity;
        end #derive target ::> onboardAcknowledgmentDeadline;
    }

    requirement def <'C-210'> AcknowledgmentQueueing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An accepted command acknowledgment shall enter the transmit queue in the same command-processing cycle when a link is available. Verification uses the shared context of C-102. */
    }
    requirement acknowledgmentQueueing : AcknowledgmentQueueing;

    #derivation connection decomposeAcknowledgmentQueueing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. */
        end #original source ::> commandIntegrity;
        end #derive target ::> acknowledgmentQueueing;
    }

    requirement def <'C-211'> ExternalControlDisqualification {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Acceptance of external mission or steering control during a qualifying attempt shall permanently disqualify that attempt. Verification uses the shared context of C-102. */
    }
    requirement externalControlDisqualification : ExternalControlDisqualification;

    #derivation connection decomposeExternalControlDisqualification {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of C-102; the parent supplies shared verification conditions. */
        end #original source ::> commandIntegrity;
        end #derive target ::> externalControlDisqualification;
    }

    requirement def <'N-101'> VisibilityNavigationCapability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Navigation shall meet E-002 and E-008 acceptance criteria at visibility of at least 1 km in daylight and darkness. Verification uses the shared context of N-033. */
    }
    requirement visibilityNavigationCapability : VisibilityNavigationCapability;

    #derivation connection decomposeVisibilityNavigationCapability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. */
        end #original source ::> visibility;
        end #derive target ::> visibilityNavigationCapability;
    }

    requirement def <'N-102'> VisibilityTrafficCapability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Traffic assessment shall meet the frozen S-001 criteria at visibility of at least 1 km in daylight and darkness. Verification uses the shared context of N-033. */
    }
    requirement visibilityTrafficCapability : VisibilityTrafficCapability;

    #derivation connection decomposeVisibilityTrafficCapability {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. */
        end #original source ::> visibility;
        end #derive target ::> visibilityTrafficCapability;
    }

    requirement def <'N-103'> RestrictedVisibilityEntry {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* On detecting visibility below 1 km, the vessel shall enter restricted-visibility state within 60 seconds. Verification uses the shared context of N-033. */
    }
    requirement restrictedVisibilityEntry : RestrictedVisibilityEntry;

    #derivation connection decomposeRestrictedVisibilityEntry {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. */
        end #original source ::> visibility;
        end #derive target ::> restrictedVisibilityEntry;
    }

    requirement def <'N-104'> RestrictedVisibilityEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Restricted-visibility operation shall be recorded as outside the normal operational envelope. Verification uses the shared context of N-033. */
    }
    requirement restrictedVisibilityEvidence : RestrictedVisibilityEvidence;

    #derivation connection decomposeRestrictedVisibilityEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. */
        end #original source ::> visibility;
        end #derive target ::> restrictedVisibilityEvidence;
    }

    requirement def <'N-105'> RestrictedVisibilityCollisionAssessment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Collision assessment shall remain active during restricted-visibility operation. Verification uses the shared context of N-033. */
    }
    requirement restrictedVisibilityCollisionAssessment : RestrictedVisibilityCollisionAssessment;

    #derivation connection decomposeRestrictedVisibilityCollisionAssessment {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-033; the parent supplies shared verification conditions. */
        end #original source ::> visibility;
        end #derive target ::> restrictedVisibilityCollisionAssessment;
    }

    requirement def <'N-106'> SurvivalEntryDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall enter survival mode within 60 seconds of the N-035 upper-limit trigger. Verification uses the shared context of N-035. */
    }
    requirement survivalEntryDeadline : SurvivalEntryDeadline;

    #derivation connection decomposeSurvivalEntryDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. */
        end #original source ::> envelopeTransition;
        end #derive target ::> survivalEntryDeadline;
    }

    requirement def <'N-107'> SurvivalTransitionRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Every survival-mode entry shall have a corresponding event record. Verification uses the shared context of N-035. */
    }
    requirement survivalTransitionRecording : SurvivalTransitionRecording;

    #derivation connection decomposeSurvivalTransitionRecording {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. */
        end #original source ::> envelopeTransition;
        end #derive target ::> survivalTransitionRecording;
    }

    requirement def <'N-108'> SailingResumptionDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Full autonomous sailing shall resume within 5 minutes of N-035 resumption eligibility becoming continuously true. Verification uses the shared context of N-035. */
    }
    requirement sailingResumptionDeadline : SailingResumptionDeadline;

    #derivation connection decomposeSailingResumptionDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. */
        end #original source ::> envelopeTransition;
        end #derive target ::> sailingResumptionDeadline;
    }

    requirement def <'N-109'> SailingResumptionInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Full autonomous sailing shall remain inhibited while N-035 resumption eligibility is false. Verification uses the shared context of N-035. */
    }
    requirement sailingResumptionInhibition : SailingResumptionInhibition;

    #derivation connection decomposeSailingResumptionInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. */
        end #original source ::> envelopeTransition;
        end #derive target ::> sailingResumptionInhibition;
    }

    requirement def <'N-110'> ResumptionBlockEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Every blocked sailing-resumption attempt shall record the blocking condition. Verification uses the shared context of N-035. */
    }
    requirement resumptionBlockEvidence : ResumptionBlockEvidence;

    #derivation connection decomposeResumptionBlockEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-035; the parent supplies shared verification conditions. */
        end #original source ::> envelopeTransition;
        end #derive target ::> resumptionBlockEvidence;
    }

    requirement def <'N-111'> WetMechanismTravel {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each N-044 exposure, external mechanisms shall complete their full commanded travel without seizure. Verification uses the shared context of N-044. */
    }
    requirement wetMechanismTravel : WetMechanismTravel;

    #derivation connection decomposeWetMechanismTravel {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-044; the parent supplies shared verification conditions. */
        end #original source ::> wetMechanicalIntegrity;
        end #derive target ::> wetMechanismTravel;
    }

    requirement def <'N-112'> WetJointIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each N-044 exposure, structural joints shall show no separation or through-cracks on visual inspection at 5 times magnification. Verification uses the shared context of N-044. */
    }
    requirement wetJointIntegrity : WetJointIntegrity;

    #derivation connection decomposeWetJointIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-044; the parent supplies shared verification conditions. */
        end #original source ::> wetMechanicalIntegrity;
        end #derive target ::> wetJointIntegrity;
    }

    requirement def <'N-113'> WetConductorResistance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each N-045 exposure, end-to-end conductor resistance shall be no more than 10 percent above its pre-test value. Verification uses the shared context of N-045. */
    }
    requirement wetConductorResistance : WetConductorResistance;

    #derivation connection decomposeWetConductorResistance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-045; the parent supplies shared verification conditions. */
        end #original source ::> wetElectricalIntegrity;
        end #derive target ::> wetConductorResistance;
    }

    requirement def <'N-114'> WetInsulationResistance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each N-045 exposure, conductor-to-conductor and conductor-to-case insulation resistance shall be at least 1 megohm at 50 V DC. Verification uses the shared context of N-045. */
    }
    requirement wetInsulationResistance : WetInsulationResistance;

    #derivation connection decomposeWetInsulationResistance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-045; the parent supplies shared verification conditions. */
        end #original source ::> wetElectricalIntegrity;
        end #derive target ::> wetInsulationResistance;
    }

    requirement def <'N-115'> HotSunElectronicsOperation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Powered electronics shall retain operational functions throughout the N-046 exposure. Verification uses the shared context of N-046. */
    }
    requirement hotSunElectronicsOperation : HotSunElectronicsOperation;

    #derivation connection decomposeHotSunElectronicsOperation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-046; the parent supplies shared verification conditions. */
        end #original source ::> solarHeating;
        end #derive target ::> hotSunElectronicsOperation;
    }

    requirement def <'N-116'> HotSunBatteryTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Battery temperatures shall remain within manufacturer operating limits throughout the N-046 exposure. Verification uses the shared context of N-046. */
    }
    requirement hotSunBatteryTemperature : HotSunBatteryTemperature;

    #derivation connection decomposeHotSunBatteryTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-046; the parent supplies shared verification conditions. */
        end #original source ::> solarHeating;
        end #derive target ::> hotSunBatteryTemperature;
    }

    requirement def <'N-117'> BatteryChargeTemperatureInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Battery charging shall remain inhibited whenever measured battery temperature is outside the manufacturer permitted charge range. Verification uses the shared context of N-046. */
    }
    requirement batteryChargeTemperatureInhibition : BatteryChargeTemperatureInhibition;

    #derivation connection decomposeBatteryChargeTemperatureInhibition {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-046; the parent supplies shared verification conditions. */
        end #original source ::> solarHeating;
        end #derive target ::> batteryChargeTemperatureInhibition;
    }

    requirement def <'N-118'> RightingDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall self-right within 60 seconds of each N-051 release. Verification uses the shared context of N-051. */
        attribute measuredRightingTime : TimeValue;
        require constraint rightingDeadline {
            measuredRightingTime >= 0 [s] and measuredRightingTime <= 60 [s]
        }
    }
    requirement rightingDeadline : RightingDeadline;

    #derivation connection decomposeRightingDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. */
        end #original source ::> selfRighting;
        end #derive target ::> rightingDeadline;
    }

    requirement def <'N-119'> CapsizeRigRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain its rig through every N-051 release. Verification uses the shared context of N-051. */
    }
    requirement capsizeRigRetention : CapsizeRigRetention;

    #derivation connection decomposeCapsizeRigRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. */
        end #original source ::> selfRighting;
        end #derive target ::> capsizeRigRetention;
    }

    requirement def <'N-120'> CapsizeBallastRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall retain its ballast through every N-051 release. Verification uses the shared context of N-051. */
    }
    requirement capsizeBallastRetention : CapsizeBallastRetention;

    #derivation connection decomposeCapsizeBallastRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. */
        end #original source ::> selfRighting;
        end #derive target ::> capsizeBallastRetention;
    }

    requirement def <'N-121'> CapsizeElectronicsSealing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* No water shall reach electronics during any N-051 release. Verification uses the shared context of N-051. */
    }
    requirement capsizeElectronicsSealing : CapsizeElectronicsSealing;

    #derivation connection decomposeCapsizeElectronicsSealing {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-051; the parent supplies shared verification conditions. */
        end #original source ::> selfRighting;
        end #derive target ::> capsizeElectronicsSealing;
    }

    requirement def <'N-122'> ControlRecoveryDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall restore mode-appropriate autonomous sail/steering control within 120 seconds from each N-051 release. Verification uses the shared context of N-052. */
        attribute measuredControlRecoveryTime : TimeValue;
        require constraint controlRecoveryDeadline {
            measuredControlRecoveryTime >= 0 [s] and measuredControlRecoveryTime <= 120 [s]
        }
    }
    requirement controlRecoveryDeadline : ControlRecoveryDeadline;

    #derivation connection decomposeControlRecoveryDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. */
        end #original source ::> capsizeControlRecovery;
        end #derive target ::> controlRecoveryDeadline;
    }

    requirement def <'N-123'> CapsizeGateProgressRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Gate progress shall be preserved through every N-051 release. Verification uses the shared context of N-052. */
    }
    requirement capsizeGateProgressRetention : CapsizeGateProgressRetention;

    #derivation connection decomposeCapsizeGateProgressRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. */
        end #original source ::> capsizeControlRecovery;
        end #derive target ::> capsizeGateProgressRetention;
    }

    requirement def <'N-124'> CapsizeQualificationRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Qualification status shall be preserved through every N-051 release absent an independently disqualifying event. Verification uses the shared context of N-052. */
    }
    requirement capsizeQualificationRetention : CapsizeQualificationRetention;

    #derivation connection decomposeCapsizeQualificationRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. */
        end #original source ::> capsizeControlRecovery;
        end #derive target ::> capsizeQualificationRetention;
    }

    requirement def <'N-125'> CapsizeRestrictionRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Control restoration after each N-051 release shall preserve every active survival, low-energy, recovery and motor-inhibition restriction. Verification uses the shared context of N-052. */
    }
    requirement capsizeRestrictionRetention : CapsizeRestrictionRetention;

    #derivation connection decomposeCapsizeRestrictionRetention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-052; the parent supplies shared verification conditions. */
        end #original source ::> capsizeControlRecovery;
        end #derive target ::> capsizeRestrictionRetention;
    }

    requirement def <'N-126'> WeedPassageSpeed {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* During each N-053 patch passage, mean water-relative sailing speed shall be at least 50 percent of the weed-free reference speed. Verification uses the shared context of N-053. */
    }
    requirement weedPassageSpeed : WeedPassageSpeed;

    #derivation connection decomposeWeedPassageSpeed {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-053; the parent supplies shared verification conditions. */
        end #original source ::> submergedWeedPassage;
        end #derive target ::> weedPassageSpeed;
    }

    requirement def <'N-127'> WeedPassageSteering {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After each N-053 patch passage, full commanded rudder travel shall be regained within 5 minutes. Verification uses the shared context of N-053. */
    }
    requirement weedPassageSteering : WeedPassageSteering;

    #derivation connection decomposeWeedPassageSteering {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-053; the parent supplies shared verification conditions. */
        end #original source ::> submergedWeedPassage;
        end #derive target ::> weedPassageSteering;
    }

    requirement def <'N-128'> WeedSnagSpeedRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Within 5 minutes of each N-054 snag, water-relative sailing speed shall recover to at least 50 percent of unobstructed reference speed. Verification uses the shared context of N-054. */
    }
    requirement weedSnagSpeedRecovery : WeedSnagSpeedRecovery;

    #derivation connection decomposeWeedSnagSpeedRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-054; the parent supplies shared verification conditions. */
        end #original source ::> weedSnagShedding;
        end #derive target ::> weedSnagSpeedRecovery;
    }

    requirement def <'N-129'> WeedSnagSteeringRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Within 5 minutes of each N-054 snag, full commanded rudder travel shall be regained. Verification uses the shared context of N-054. */
    }
    requirement weedSnagSteeringRecovery : WeedSnagSteeringRecovery;

    #derivation connection decomposeWeedSnagSteeringRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-054; the parent supplies shared verification conditions. */
        end #original source ::> weedSnagShedding;
        end #derive target ::> weedSnagSteeringRecovery;
    }

    requirement def <'N-130'> WeedBlockageFault {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A suspected-fouling fault shall be logged within 10 seconds after the N-055 trigger. Verification uses the shared context of N-055. */
    }
    requirement weedBlockageFault : WeedBlockageFault;

    #derivation connection decomposeWeedBlockageFault {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-055; the parent supplies shared verification conditions. */
        end #original source ::> weedBlockageResponse;
        end #derive target ::> weedBlockageFault;
    }

    requirement def <'N-131'> WeedBlockageContingency {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall enter fouling-contingency state within 10 seconds after the N-055 trigger. Verification uses the shared context of N-055. */
    }
    requirement weedBlockageContingency : WeedBlockageContingency;

    #derivation connection decomposeWeedBlockageContingency {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-055; the parent supplies shared verification conditions. */
        end #original source ::> weedBlockageResponse;
        end #derive target ::> weedBlockageContingency;
    }

    requirement def <'N-132'> WeedBlockageLocation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Location reporting shall continue at the active telemetry cadence during fouling contingency whenever a link is available. Verification uses the shared context of N-055. */
    }
    requirement weedBlockageLocation : WeedBlockageLocation;

    #derivation connection decomposeWeedBlockageLocation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-055; the parent supplies shared verification conditions. */
        end #original source ::> weedBlockageResponse;
        end #derive target ::> weedBlockageLocation;
    }

    requirement def <'N-133'> PoweredWeedSpeed {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Mean water-relative powered speed through each N-056 patch passage shall be at least 50 percent of weed-free reference speed. Verification uses the shared context of N-056. */
    }
    requirement poweredWeedSpeed : PoweredWeedSpeed;

    #derivation connection decomposePoweredWeedSpeed {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. */
        end #original source ::> recoveryPropulsorWeeds;
        end #derive target ::> poweredWeedSpeed;
    }

    requirement def <'N-134'> PoweredWeedCurrent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Motor and controller currents shall remain within their respective rated limits during each N-056 patch passage. Verification uses the shared context of N-056. */
    }
    requirement poweredWeedCurrent : PoweredWeedCurrent;

    #derivation connection decomposePoweredWeedCurrent {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. */
        end #original source ::> recoveryPropulsorWeeds;
        end #derive target ::> poweredWeedCurrent;
    }

    requirement def <'N-135'> PoweredWeedTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Motor and controller temperatures shall remain within their respective rated limits during each N-056 patch passage. Verification uses the shared context of N-056. */
    }
    requirement poweredWeedTemperature : PoweredWeedTemperature;

    #derivation connection decomposePoweredWeedTemperature {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. */
        end #original source ::> recoveryPropulsorWeeds;
        end #derive target ::> poweredWeedTemperature;
    }

    requirement def <'N-136'> LockedPropulsorShutdown {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A locked propulsor shall cause motor shutdown within 2 seconds. Verification uses the shared context of N-056. */
    }
    requirement lockedPropulsorShutdown : LockedPropulsorShutdown;

    #derivation connection decomposeLockedPropulsorShutdown {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of N-056; the parent supplies shared verification conditions. */
        end #original source ::> recoveryPropulsorWeeds;
        end #derive target ::> lockedPropulsorShutdown;
    }

    requirement def <'R-101'> MotorQualificationInvariant {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown. Verification uses the shared context of R-004. */
        attribute qualifying : Boolean;
        attribute qualificationStateKnown : Boolean;
        attribute motorEnabled : Boolean;
        require constraint motorQualificationInvariant {
            not motorEnabled or (qualificationStateKnown and not qualifying)
        }
    }
    requirement motorQualificationInvariant : MotorQualificationInvariant;

    #derivation connection decomposeMotorQualificationInvariant {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of R-004; the parent supplies shared verification conditions. */
        end #original source ::> challengeMotorInhibition;
        end #derive target ::> motorQualificationInvariant;
    }

    requirement def <'R-102'> FreshRecoveryCommand {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After restart, motor enable shall remain inhibited until a fresh authenticated recovery command is accepted. Verification uses the shared context of R-004. */
    }
    requirement freshRecoveryCommand : FreshRecoveryCommand;

    #derivation connection decomposeFreshRecoveryCommand {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of R-004; the parent supplies shared verification conditions. */
        end #original source ::> challengeMotorInhibition;
        end #derive target ::> freshRecoveryCommand;
    }

    requirement def <'E-144'> IngressEventDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* In the E-006 injection test, an ingress event record shall exist within 60 seconds of injection starting. Verification uses the shared context of E-006. */
    }
    requirement ingressEventDeadline : IngressEventDeadline;

    #derivation connection decomposeIngressEventDeadline {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-006; the parent supplies shared verification conditions. */
        end #original source ::> ingressResponse;
        end #derive target ::> ingressEventDeadline;
    }

    requirement def <'E-145'> QualificationRestoration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Within 30 seconds after a watchdog reset under E-003 preconditions, qualification status shall equal the valid persisted status, or be nonqualifying when persisted status is absent or inconsistent. Verification uses the shared context of E-003. */
    }
    requirement qualificationRestoration : QualificationRestoration;

    #derivation connection decomposeQualificationRestoration {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* This leaf isolates one acceptance outcome of E-003; the parent supplies shared verification conditions. */
        end #original source ::> resetRecovery;
        end #derive target ::> qualificationRestoration;
    }

    #derivation connection sharedAcceptance1 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* resetRecovery also requires the shared logInterruptionDurability outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> resetRecovery;
        end #derive target ::> logInterruptionDurability;
    }

    #derivation connection sharedAcceptance2 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* resetRecovery also requires the shared unknownQualificationFallback outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> resetRecovery;
        end #derive target ::> unknownQualificationFallback;
    }

    #derivation connection sharedAcceptance3 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* resetRecovery also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> resetRecovery;
        end #derive target ::> qualificationPersistence;
    }

    #derivation connection sharedAcceptance4 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* resetRecovery also requires the shared freshRecoveryCommand outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> resetRecovery;
        end #derive target ::> freshRecoveryCommand;
    }

    #derivation connection sharedAcceptance5 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* resetRecovery also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> resetRecovery;
        end #derive target ::> motorQualificationInvariant;
    }

    #derivation connection sharedAcceptance6 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* commandIntegrity also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> commandIntegrity;
        end #derive target ::> criticalEventRecording;
    }

    #derivation connection sharedAcceptance7 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* commandIntegrity also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> commandIntegrity;
        end #derive target ::> qualificationPersistence;
    }

    #derivation connection sharedAcceptance8 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* safeRecovery also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> safeRecovery;
        end #derive target ::> qualificationPersistence;
    }

    #derivation connection sharedAcceptance9 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* safeRecovery also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> safeRecovery;
        end #derive target ::> motorQualificationInvariant;
    }

    #derivation connection sharedAcceptance10 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* safeRecovery also requires the shared periodicLogCadence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> safeRecovery;
        end #derive target ::> periodicLogCadence;
    }

    #derivation connection sharedAcceptance11 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* challengeMotorInhibition also requires the shared qualificationPersistence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> challengeMotorInhibition;
        end #derive target ::> qualificationPersistence;
    }

    #derivation connection sharedAcceptance12 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* challengeMotorInhibition also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> challengeMotorInhibition;
        end #derive target ::> criticalEventRecording;
    }

    #derivation connection sharedAcceptance13 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* lowEnergyRecovery also requires the shared periodicLogCadence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> periodicLogCadence;
    }

    #derivation connection sharedAcceptance14 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* lowEnergyRecovery also requires the shared telemetryDeliveryCadence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> telemetryDeliveryCadence;
    }

    #derivation connection sharedAcceptance15 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* lowEnergyRecovery also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> criticalEventRecording;
    }

    #derivation connection sharedAcceptance16 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* lowEnergyRecovery also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> lowEnergyRecovery;
        end #derive target ::> motorQualificationInvariant;
    }

    #derivation connection sharedAcceptance17 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* ingressResponse also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> ingressResponse;
        end #derive target ::> criticalEventRecording;
    }

    #derivation connection sharedAcceptance18 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* ingressResponse also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> ingressResponse;
        end #derive target ::> motorQualificationInvariant;
    }

    #derivation connection sharedAcceptance19 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* communications also requires the shared logRetention outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> communications;
        end #derive target ::> logRetention;
    }

    #derivation connection sharedAcceptance20 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* communications also requires the shared reconnectLogPreservation outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> communications;
        end #derive target ::> reconnectLogPreservation;
    }

    #derivation connection sharedAcceptance21 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* navigationAvailability also requires the shared criticalEventRecording outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> navigationAvailability;
        end #derive target ::> criticalEventRecording;
    }

    #derivation connection sharedAcceptance22 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* envelopeTransition also requires the shared periodicLogCadence outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> envelopeTransition;
        end #derive target ::> periodicLogCadence;
    }

    #derivation connection sharedAcceptance23 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* envelopeTransition also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> envelopeTransition;
        end #derive target ::> motorQualificationInvariant;
    }

    #derivation connection sharedAcceptance24 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* weedBlockageResponse also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> weedBlockageResponse;
        end #derive target ::> motorQualificationInvariant;
    }

    #derivation connection sharedAcceptance25 {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* recoveryPropulsorWeeds also requires the shared motorQualificationInvariant outcome; one normative leaf avoids duplicate obligations. */
        end #original source ::> recoveryPropulsorWeeds;
        end #derive target ::> motorQualificationInvariant;
    }
}
