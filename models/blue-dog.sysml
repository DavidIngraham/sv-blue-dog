package BlueDog {
    doc /* Working architecture model, 2026-10-09.
     * Confirmed threshold: The Dalles-Bonneville-The Dalles round trip.
     * Objective: autonomously repeat the round trip for as long as practical.
     * Qualifying round trips require no operator intervention; live monitoring is required.
     * Two top-level drivers: GorgeChallenge::transGorgeChallenge and Goals::hawaiiVoyage.
     * Hawaii is the end goal; the Gorge is the torture test, not proof of ocean readiness.
     * Multi-day endurance with energy harvesting remains an earlier intent. SysML v2 learning is a project goal.
     * Proposed decomposition below is for discussion, not a selected design.
     * Tool checks are recorded in the modeling guide; satisfaction is not claimed.
     */

    private import GorgeChallenge::*;

    package Goals {
        requirement def <'H-001'> HawaiiVoyage {
            doc /* CONFIRMED INTENT: Develop SV Blue Dog toward completing an
             * autonomous sailing voyage to Hawaii. The Gorge challenge is a
             * proving ground for that end goal, not evidence of ocean readiness.
             * Departure point, destination gate, route, duration, environmental
             * envelope, assistance/propulsion rules, and acceptance evidence
             * remain to be agreed; Gorge-specific rules are not automatically
             * ocean mission rules.
             */
        }
        requirement hawaiiVoyage : HawaiiVoyage;
    }

    package Mission {
        action def HawaiiMission {
            doc /* Proposed decomposition supporting Goals::hawaiiVoyage.
             * This is not an executable sequence or a verified mission plan.
             * Route, landfall, endurance, and recovery criteria remain open.
             */
            action prepareAndLaunch;
            action sailOceanPassage;
            action approachDestination;
            action recoverBoatAndData;
            action manageEnergy;
            action monitorHealthAndRecover;
            action communicateWithOperator;
            action recordMissionData;
        }
        action def TransGorgeMission {
            doc /* Proposed activity decomposition, not execution order.
             * Departure/turnaround coordinates, duration, operating envelope,
             * recovery criteria, and monitoring service levels are TBD.
             * No operator intervention is permitted during a qualifying round trip.
             */
            action prepareAndLaunch;
            action sailOutbound;
            action turnAround;
            action sailHome;
            action repeatCourse;
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
             * Shared candidate architecture for the Gorge and Hawaii missions.
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
