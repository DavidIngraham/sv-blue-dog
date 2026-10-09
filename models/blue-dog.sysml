package BlueDog {
    doc /* Working architecture model, 2026-10-09.
     * Confirmed mission: Bonneville-The Dalles round trip, multi-day
     * endurance with energy harvesting. SysML v2 learning is a project goal.
     * Proposed decomposition below is for discussion, not a selected design.
     * Tool checks are recorded in the modeling guide; satisfaction is not claimed.
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

}
