package BlueDogRequirements {
    private import RequirementDerivation::*;
    private import GorgeChallenge::*;
    private import BlueDog::Goals::*;
    requirement def <'M-001'> RoundTrip {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* SV Blue Dog shall complete the imported Gorge
         * challenge threshold and pursue its repeated-operation objective,
         * observing the imported autonomy, propulsion, monitoring, and emergency
         * intervention rules. Challenge rules are owned by challenge.sysml.
         */
    }
    requirement def <'M-002'> MultiDayEndurance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The boat shall support multi-day missions
         * using onboard energy storage and energy harvesting.
         * Duration, harvest conditions, and energy reserve TBD.
         */
    }
    requirement def <'E-001'> EnergyAwareness {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Estimate available energy and manage electrical
         * loads so recovery functions retain an agreed reserve.
         * Estimation accuracy, reserve, and load priorities TBD.
         */
    }
    requirement def <'E-002'> NavigationAndControl {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Acquire navigation and sailing observations,
         * execute mission guidance, and command sail/steering actuators.
         * Accuracy, rates and actuation interfaces remain open; the environmental envelope is N-001.
         */
    }
    requirement def <'E-003'> ResetRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Recover from software reset.
         * Restore a defined operating mode and
         * retained mission state with controlled actuator outputs.
         * Restart time and acceptance criteria TBD.
         */
    }
    requirement def <'E-004'> LowEnergyRecovery {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Provide a low-energy limp mode.
         * Trigger, remaining functions, and mission response TBD.
         */
    }
    requirement def <'E-005'> Communications {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Provide live operator monitoring during
         * autonomous operation. Monitoring shall not require operator
         * intervention in completing a qualifying round trip.
         * Loss of the monitoring link shall not interrupt autonomous mission
         * execution. The vessel shall retain telemetry onboard during an outage
         * and transmit the retained data when contact returns.
         * The operator shall have a remote emergency override for mission
         * abort or manual control when a command link is available.
         * Using this override ends the attempt's qualification as unassisted.
         * Link coverage, displayed data, update interval, outage retention
         * duration, and backlog transmission priority remain to be agreed.
         */
    }
    requirement def <'E-006'> IngressResponse {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Tolerate a small hull breach; a bilge pump
         * was proposed. Detection method, tolerable leak, response,
         * and energy allocation remain TBD.
         */
    }
    requirement def <'E-007'> MissionEvidence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Record time-correlated navigation, energy,
         * commands, and faults for mission assessment and learning.
         * Rates, retention, and tolerated data loss TBD.
         */
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
        doc /* Repeated autonomous journeys motivate the existing endurance and harvesting requirement; quantitative sizing remains open. */
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
        doc /* Ocean mission assessment requires retained voyage evidence; acceptance criteria remain open. */
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
        doc /* The complete vessel, disassembled where needed, shall be transportable, launched, and recovered by one person using a documented handling procedure. Packed dimensions, lift mass, lifting points, setup time, and launch/recovery conditions shall be specified and demonstrated; numerical limits remain open. */
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
        doc /* Printed components shall fit an agreed desktop 3D-printer build envelope and support assembly, sealing, inspection, and replacement with accessible tools. Printer dimensions, material, tolerances, joints, print orientation, and material/process qualification remain open; a typical printer is not a fixed dimensional standard. */
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
        doc /* Energy storage, seals, electronics, and actuators shall be accessible for inspection and replacement between attempts. Define service intervals, spares, leak checks, cost and build-time budgets before accepting the design. */
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
        doc /* The vessel shall detect and assess collision risk, maintain an effective lookout, and take appropriate avoiding action within its approved operational envelope. Define detection performance for non-AIS craft, reaction time, maneuvering capability, and loss-of-awareness response; AIS alone is not the lookout solution. */
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
        doc /* The vessel shall enforce mission boundaries and respond autonomously to loss of progress, grounding risk, or boundary approach using a defined contingency plan. Course gates, chart margins, prohibited areas, traffic corridors, and recovery areas remain open. No dam transit is assumed. */
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
        doc /* The vessel shall support emergency abort, location reporting, and one-person recovery with controlled propulsion and actuator states. Define remote/local authority, communications-loss behavior, reserve energy, accessible isolation, and recovery conditions. Safety intervention ends qualifying challenge operation. */
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
        doc /* The vessel shall carry and operate lights, shapes, and sound-signaling arrangements applicable to its measured dimensions, operating waters, visibility, and sailing, powered, or anchored mode. Assess automatic presentation for unattended operation. Selection and legal applicability remain open; no universal small-size exemption is assumed. */
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
        doc /* Before deployment, determine applicable vessel classification, Inland or International navigation rules, registration, radio authorization, and any permissions for a stationary observation or buoy mode. Record dimensions and mode-dependent obligations. Unattended operation or small size shall not be treated as a COLREG exemption or proof of buoy classification. */
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
        doc /* The vessel shall retain navigation, autonomous sail/steering control, mission recording, and available-link telemetry throughout these operating envelopes: Gorge wind 3-15 m/s with 20 m/s gusts, significant wave height up to 1.0 m with peak periods 2-5 s, and current up to 1.5 m/s; ocean wind 3-15 m/s with 20 m/s gusts, significant wave height up to 3.0 m with peak periods 5-20 s, and current up to 1.0 m/s. Wind is true wind referenced to 10 m above water, with 10-minute means and 3-second gusts; wave statistics use 20-minute records. Both profiles include air 0-40 degC, water 2-30 degC, relative humidity 0-100 percent with condensation, day/night, and visibility at least 1 km. Function shall be retained for 72 continuous hours in Gorge qualification and 30 continuous days in ocean qualification without maintenance or operator intervention, with onboard harvesting permitted. Below 3 m/s wind, the vessel shall retain navigation, recording and autonomous contingency behavior; positive progress or station keeping is not guaranteed. Current limits do not guarantee upstream progress at every wind angle. At an observed operating-limit exceedance, the vessel shall log the event and enter autonomous survival behavior within 60 s; visibility below 1 km shall trigger that behavior within 60 s of detection. Survival shall preserve flotation, attached ballast and rig, sealed electronics, mission state, and at least one time-stamped position record per minute for 24 h in wind up to 25 m/s with 35 m/s gusts, Gorge significant waves up to 2 m (peak periods 3-7 s), or ocean significant waves up to 6 m (peak periods 6-20 s). Qualification shall include individual waves up to twice the respective significant wave height, with wind/waves/current from adverse relative directions. After 10 continuous minutes back inside operating limits, autonomous sailing shall resume within 5 minutes without repair. The respective current, temperature and humidity limits also apply during survival. Survival does not require course progress and does not authorize motor use in a qualifying challenge. These are engineering design targets, not measured route extremes or demonstrated capability. */
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
        doc /* The assembled vessel shall meet N-001 following 72 h continuous freshwater exposure for Gorge service and 30 days continuous 35 g/kg saltwater exposure for ocean service, including continuous wetting of underwater parts and at least one complete topside spray wetting per hour. Electronics enclosures, installed connectors and cable penetrations shall admit no detectable liquid water using dry internal indicators after 30 minutes with their highest point 1 m below the water surface, before and after each exposure campaign. External mechanisms shall complete commanded travel without seizure, structural joints shall show no separation or through-cracks, and exposed electrical connections shall retain continuity and insulation resistance of at least 1 megohm when isolated from electronics. With ambient air 40 degC and incident solar irradiance 1000 W/m2 for 8 h, powered electronics shall retain N-001 functions and every battery shall remain within its manufacturer-rated operating temperatures, including automatic charge inhibition outside permitted charging temperatures. Printed structural parts shall retain at least 80 percent of unaged coupon failure load after a recorded cumulative 300 MJ/m2 exposure in the 300-400 nm UV band and the ocean wet-exposure campaign; this is a qualification dose, not an asserted calendar lifetime. */
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
        doc /* At each declared minimum and maximum mission loading condition, the vessel shall self-right from 90 and 180 degrees heel within 60 s of release without external action or motor thrust, and restore autonomous sail/steering control within 120 s. Qualification shall include five releases at each angle to each side, in fresh and 35 g/kg salt water, without water reaching electronics or loss of rig or ballast. After a flexible wet vegetation surrogate 1 m long and 20 mm wide, anchored only by its contact with the vessel, is draped once across each appendage leading edge, the vessel shall autonomously clear it or retain at least 50 percent of its unobstructed speed and full commanded rudder travel within 5 minutes in 5 m/s wind. If this criterion is not met, it shall detect loss of progress and log/enter contingency behavior within a further 60 s without automatically enabling the recovery motor. Floating-log impact, fishing-line entanglement, ice and surf-zone operation are outside this initial qualification envelope; avoidance and recovery remain necessary. */
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
        doc /* Provide auxiliary motor propulsion for development testing and vessel recovery. Interlock challenge mode against propulsive motor commands; entering powered recovery shall terminate and log the qualifying attempt. Define thrust/current envelope, runtime, protected propulsor, isolation, and energy reserve. Recovery thrust is not yet sized for Gorge currents. */
    }
    requirement recoveryPropulsion : RecoveryPropulsion;
    #derivation connection deriveRecoveryPropulsion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* RecoveryPropulsion refines the responsibilities needed for safeRecovery. */
        end #original source ::> safeRecovery;
        end #derive target ::> recoveryPropulsion;
    }

    requirement def <'R-002'> RecoveryEnergy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Allocate and monitor energy reserved for communications, safe control, and the specified powered recovery scenario. Define trigger thresholds and verify recovery demand against available battery energy; a motor alone does not guarantee recovery. */
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
        doc /* Provide onboard telemetry equipment and a shore monitoring endpoint reporting timestamped position, mission mode, energy, faults, and link/data age. Retain observations through outages and resume transfer. Determine Gorge and ocean coverage, update rates, antenna installation, power demand, and service costs before selecting cellular or satellite equipment. */
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
        doc /* Emergency command equipment shall authenticate commands, reject stale or replayed requests, acknowledge accepted mode changes, and record interventions. Link loss shall leave autonomous safety functions operating. Command latency, authority handover, and recovery procedure remain open. */
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
}
