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
         * Accuracy, rates, actuation interfaces, and envelope TBD.
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
        doc /* An autonomous Hawaii passage needs ocean guidance and sailing control; its operating envelope remains open. */
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
        doc /* Define separate Gorge and ocean operating and survival envelopes for wind, gusts, current, waves, water/air temperature, visibility, and debris. Launch readiness and autonomous contingency decisions shall use the applicable envelope; numerical limits require site evidence and testing. */
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
        doc /* Hull, seals, connectors, electronics, and exposed materials shall withstand the specified immersion, spray, UV, corrosion, and fatigue exposure. Include freshwater Gorge trials and saltwater ocean service. Specify test severity, duration, inspection criteria, and tolerable ingress. */
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
        doc /* The vessel shall recover a defined sailing condition after the specified capsize event and tolerate the agreed weed/debris exposure without unacceptable control loss. Establish ballast, stability, recovery time, fouling loads, and test conditions before acceptance. */
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
