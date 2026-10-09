package BlueDog {
    package Requirements {
        private import RequirementDerivation::*;
        requirement def <'M-001'> RoundTrip {
            doc /* CONFIRMED INTENT: The system shall support an autonomous
             * sailing mission from the Bonneville area to The Dalles area
             * and back. Exact endpoints and completion criteria TBD.
             */
        }
        requirement def <'M-002'> MultiDayEndurance {
            doc /* CONFIRMED INTENT: The boat shall support multi-day missions
             * using onboard energy storage and energy harvesting.
             * Duration, harvest conditions, and energy reserve TBD.
             */
        }
        requirement def <'E-001'> EnergyAwareness {
            doc /* PROPOSED: Estimate available energy and manage electrical
             * loads so recovery functions retain an agreed reserve.
             * Estimation accuracy, reserve, and load priorities TBD.
             */
        }
        requirement def <'E-002'> NavigationAndControl {
            doc /* PROPOSED: Acquire navigation and sailing observations,
             * execute mission guidance, and command sail/steering actuators.
             * Accuracy, rates, actuation interfaces, and envelope TBD.
             */
        }
        requirement def <'E-003'> ResetRecovery {
            doc /* LEGACY INTENT: Recover from software reset.
             * Proposed refinement: restore a defined operating mode and
             * retained mission state with controlled actuator outputs.
             * Restart time and acceptance criteria TBD.
             */
        }
        requirement def <'E-004'> LowEnergyRecovery {
            doc /* LEGACY INTENT: Provide a low-energy limp mode.
             * Trigger, remaining functions, and mission response TBD.
             */
        }
        requirement def <'E-005'> Communications {
            doc /* LEGACY INTENT: Communicate with an operator.
             * Link coverage, data products, command authority, reporting
             * interval, and behavior during loss of contact TBD.
             */
        }
        requirement def <'E-006'> IngressResponse {
            doc /* LEGACY INTENT: Tolerate a small hull breach; a bilge pump
             * was proposed. Detection method, tolerable leak, response,
             * and energy allocation remain TBD.
             */
        }
        requirement def <'E-007'> MissionEvidence {
            doc /* PROPOSED: Record time-correlated navigation, energy,
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

        // Proposed derivations: direction is original requirement to derived requirement.
        #derivation connection roundTripNavigation {
            doc /* PROPOSED: Autonomous completion of the route needs observations, guidance, and actuation. */
            end #original source ::> roundTrip;
            end #derive target ::> navigationAndControl;
        }
        #derivation connection roundTripReset {
            doc /* PROPOSED: A reset during an autonomous journey must not leave mission behavior undefined. */
            end #original source ::> roundTrip;
            end #derive target ::> resetRecovery;
        }
        #derivation connection roundTripCommunications {
            doc /* PROPOSED: Mission supervision and recovery need an agreed operator communication policy. */
            end #original source ::> roundTrip;
            end #derive target ::> communications;
        }
        #derivation connection roundTripIngress {
            doc /* PROPOSED: Recovering the boat after the journey motivates a defined response to small leaks. */
            end #original source ::> roundTrip;
            end #derive target ::> ingressResponse;
        }
        #derivation connection roundTripEvidence {
            doc /* PROPOSED: Assessing route completion and learning from the mission requires recorded evidence. */
            end #original source ::> roundTrip;
            end #derive target ::> missionEvidence;
        }
        #derivation connection enduranceEnergy {
            doc /* PROPOSED: Multi-day operation with variable harvesting needs energy estimation and load management. */
            end #original source ::> multiDayEndurance;
            end #derive target ::> energyAwareness;
        }
        #derivation connection enduranceLimpMode {
            doc /* PROPOSED: Harvest shortfalls need an explicit degraded operating mode. */
            end #original source ::> multiDayEndurance;
            end #derive target ::> lowEnergyRecovery;
        }
        #derivation connection energyLimpMode {
            doc /* PROPOSED: Available-energy estimates and reserve policy must drive low-energy transitions. */
            end #original source ::> energyAwareness;
            end #derive target ::> lowEnergyRecovery;
        }
    }
}
