package BlueDogRequirements {
    private import RequirementDerivation::*;
    private import GorgeChallenge::*;
    private import BlueDog::Goals::*;
    requirement def <'M-001'> RoundTrip {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* SV Blue Dog shall complete the imported Gorge
         * challenge threshold and pursue its repeated-operation objective,
         * observing the imported autonomy, propulsion, monitoring, and emergency
         * intervention rules. Challenge rules are owned by challenge.sysml.
         */
    }
    requirement def <'M-002'> MultiDayEndurance {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The boat shall support multi-day missions
         * using onboard energy storage and energy harvesting.
         * Duration, harvest conditions, and energy reserve TBD.
         */
    }
    requirement def <'E-001'> EnergyAwareness {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Estimate available energy and manage electrical
         * loads so recovery functions retain an agreed reserve.
         * Estimation accuracy, reserve, and load priorities TBD.
         */
    }
    requirement def <'E-002'> NavigationAndControl {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Acquire navigation and sailing observations,
         * execute mission guidance, and command sail/steering actuators.
         * Accuracy, rates, actuation interfaces, and envelope TBD.
         */
    }
    requirement def <'E-003'> ResetRecovery {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Recover from software reset.
         * Restore a defined operating mode and
         * retained mission state with controlled actuator outputs.
         * Restart time and acceptance criteria TBD.
         */
    }
    requirement def <'E-004'> LowEnergyRecovery {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Provide a low-energy limp mode.
         * Trigger, remaining functions, and mission response TBD.
         */
    }
    requirement def <'E-005'> Communications {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
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
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Tolerate a small hull breach; a bilge pump
         * was proposed. Detection method, tolerable leak, response,
         * and energy allocation remain TBD.
         */
    }
    requirement def <'E-007'> MissionEvidence {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
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
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vehicle mission implements the independently defined challenge course. */
        end #original source ::> GorgeChallenge::courseCompletion;
        end #derive target ::> roundTrip;
    }
    #derivation connection challengeEndurance {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Repeated autonomous journeys motivate the existing endurance and harvesting requirement; quantitative sizing remains open. */
        end #original source ::> GorgeChallenge::repeatedOperation;
        end #derive target ::> multiDayEndurance;
    }
    #derivation connection challengeAutonomy {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel needs onboard guidance and control to complete an unassisted attempt. */
        end #original source ::> GorgeChallenge::unassistedAttempt;
        end #derive target ::> navigationAndControl;
    }
    #derivation connection challengePropulsion {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. */
        end #original source ::> GorgeChallenge::sailingPropulsion;
        end #derive target ::> roundTrip;
    }
    #derivation connection challengeMonitoring {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Vehicle communications implement live observation and outage data retention. */
        end #original source ::> GorgeChallenge::liveObservation;
        end #derive target ::> communications;
    }
    #derivation connection challengeOverride {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Vehicle communications provide emergency commands whose use ends attempt qualification. */
        end #original source ::> GorgeChallenge::emergencyIntervention;
        end #derive target ::> communications;
    }

    #derivation connection hawaiiMultiDayEndurance {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An ocean passage motivates sustained energy autonomy; multi-day operation is an interim capability, not an ocean endurance sizing result. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> multiDayEndurance;
    }

    #derivation connection hawaiiNavigationAndControl {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* An autonomous Hawaii passage needs ocean guidance and sailing control; its operating envelope remains open. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> navigationAndControl;
    }

    #derivation connection hawaiiCommunications {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The long-term ocean mission motivates review of monitoring coverage and outage behavior without selecting a radio technology. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> communications;
    }

    #derivation connection hawaiiResetRecovery {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Extended unattended operation motivates recovery from onboard resets. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> resetRecovery;
    }

    #derivation connection hawaiiMissionEvidence {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Ocean mission assessment requires retained voyage evidence; acceptance criteria remain open. */
        end #original source ::> BlueDog::Goals::hawaiiVoyage;
        end #derive target ::> missionEvidence;
    }

    // Derivations: direction is original requirement to derived requirement.
    #derivation connection roundTripNavigation {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Autonomous completion of the route needs observations, guidance, and actuation. */
        end #original source ::> roundTrip;
        end #derive target ::> navigationAndControl;
    }
    #derivation connection roundTripReset {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A reset during an autonomous journey must not leave mission behavior undefined. */
        end #original source ::> roundTrip;
        end #derive target ::> resetRecovery;
    }
    #derivation connection roundTripCommunications {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Mission supervision and recovery need an agreed operator communication policy. */
        end #original source ::> roundTrip;
        end #derive target ::> communications;
    }
    #derivation connection roundTripIngress {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Recovering the boat after the journey motivates a defined response to small leaks. */
        end #original source ::> roundTrip;
        end #derive target ::> ingressResponse;
    }
    #derivation connection roundTripEvidence {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Assessing route completion and learning from the mission requires recorded evidence. */
        end #original source ::> roundTrip;
        end #derive target ::> missionEvidence;
    }
    #derivation connection enduranceEnergy {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Multi-day operation with variable harvesting needs energy estimation and load management. */
        end #original source ::> multiDayEndurance;
        end #derive target ::> energyAwareness;
    }
    #derivation connection enduranceLimpMode {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Harvest shortfalls need an explicit degraded operating mode. */
        end #original source ::> multiDayEndurance;
        end #derive target ::> lowEnergyRecovery;
    }
    #derivation connection energyLimpMode {
        @ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Available-energy estimates and reserve policy must drive low-energy transitions. */
        end #original source ::> energyAwareness;
        end #derive target ::> lowEnergyRecovery;
    }
}
