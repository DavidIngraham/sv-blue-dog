package BlueDog {
    doc /* Working architecture model, 2026-10-09.
     * Confirmed mission: Bonneville-The Dalles round trip, multi-day
     * endurance with energy harvesting. SysML v2 learning is a project goal.
     * Proposed decomposition below is for discussion, not a selected design.
     * No tool validation or requirement satisfaction is claimed.
     */

    package Mission {
        action def TransGorgeMission {
            doc /* Proposed activity decomposition, not execution order.
             * Departure/turnaround coordinates, duration, operating envelope,
             * recovery criteria, and operator intervention policy are TBD.
             */
            action prepareAndLaunch;
            action sailOutbound;
            action turnAround;
            action sailHome;
            action recoverBoatAndData;
            action manageEnergy;
            action monitorHealthAndRecover;
            action communicateWithOperator;
            action recordMissionData;
        }
        action def SwellMonitoringMission {
            doc /* Stretch mission, not required for the initial round trip.
             * Station-keeping area, measurement products, and accuracy TBD.
             */
            action reachObservationArea;
            action maintainObservationArea;
            action measureAndRecordConditions;
            action returnForRecovery;
        }
    }

    package Architecture {
        part def Operator;
        part def ShoreSupport;
        part def Environment;
        part def HullAndRig;
        part def EnergySubsystem;
        part def NavigationAndSensing;
        part def GuidanceAndControl;
        part def SailAndSteeringActuation;
        part def Communications;
        part def HealthAndRecovery;
        part def DataRecording;
        part def ObservationPayload;

        part def Boat {
            doc /* Logical responsibilities, not separate PCB commitments.
             * Interfaces, behavior allocation, and physical realization TBD.
             */
            part hullAndRig : HullAndRig;
            part energy : EnergySubsystem;
            part navigation : NavigationAndSensing;
            part control : GuidanceAndControl;
            part actuation : SailAndSteeringActuation;
            part communications : Communications;
            part recovery : HealthAndRecovery;
            part recording : DataRecording;
            part observationPayload : ObservationPayload [0..1];
        }
        part missionContext {
            part boat : Boat;
            part operator : Operator;
            part shoreSupport : ShoreSupport;
            part environment : Environment;
        }
    }

    package Requirements {
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
    }
}
