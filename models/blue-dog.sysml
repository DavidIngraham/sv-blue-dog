package BlueDog {
    doc /* Working architecture model, 2026-10-09.
     * Confirmed threshold: The Dalles-Bonneville-The Dalles round trip.
     * Objective: autonomously repeat the round trip for as long as practical.
     * Qualifying round trips require no operator intervention; live monitoring is required.
     * Two top-level drivers: GorgeChallenge::transGorgeChallenge and Goals::hawaiiVoyage.
     * Hawaii is the end goal; the Gorge is the torture test, not proof of ocean readiness.
     * Multi-day endurance with energy harvesting remains an earlier intent. SysML v2 learning is a project goal.
     * Decomposition identifies responsibilities; physical design remains open.
     * Tool checks are recorded in the modeling guide; design satisfaction links
     * are maintained separately and do not establish verification.
     */

    private import GorgeChallenge::*;

    package Goals {
        requirement def <'H-001'> HawaiiVoyage {
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            doc /* The vessel shall complete an autonomous sailing voyage to Hawaii. */
        comment notes /* Gorge-specific challenge rules do not automatically apply to the ocean mission. */
        metadata rationale : ModelingMetadata::Rationale { text = "The Gorge is a proving ground for the ocean objective, not evidence of ocean readiness."; }
        metadata issue : ModelingMetadata::Issue { text = "Departure point, destination gate, route, duration, route/season suitability of the candidate ocean envelope, assistance/propulsion rules and acceptance evidence remain to be agreed."; }
        }
        requirement hawaiiVoyage : HawaiiVoyage;
    }

    package Mission {
        action def HawaiiMission {
            doc /* Mission decomposition supporting Goals::hawaiiVoyage.
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
            doc /* Activity decomposition, not execution order.
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
        part def MonitoringStation;
        part def ShoreSupport {
            part monitoringStation : MonitoringStation;
        }
        part def Environment;
        part def OtherVessel {
            doc /* External traffic, including commercial ships, barges, fishing and recreational craft, with or without AIS. Behavior and cooperation are outside Blue Dog control. */
        }
        part def PrintedHull;
        part def SealedEnclosure;
        part def KeelAndBallast;
        part def HandlingInterfaces;
        part def HullAndRig {
            part printedHull : PrintedHull;
            part enclosure : SealedEnclosure;
            part keelAndBallast : KeelAndBallast;
            part handling : HandlingInterfaces;
        }
        part def EnergyStorage;
        part def HarvestingInterface;
        part def PowerManagement;
        part def EnergySubsystem {
            part storage : EnergyStorage;
            part harvesting : HarvestingInterface;
            part powerManagement : PowerManagement;
        }
        part def PositionAndAttitude;
        part def WindSensing;
        part def TrafficSensing;
        part def NavigationAndSensing {
            part positionAndAttitude : PositionAndAttitude;
            part wind : WindSensing;
            part traffic : TrafficSensing;
        }
        part def MissionManager;
        part def CollisionAvoidance;
        part def BoundarySupervisor;
        part def GuidanceAndControl {
            part missionManager : MissionManager;
            part collisionAvoidance : CollisionAvoidance;
            part boundarySupervisor : BoundarySupervisor;
        }
        part def SailAndSteeringActuation;
        part def TelemetryRadio;
        part def AntennaSystem;
        part def CommandGateway;
        part def Communications {
            part telemetryRadio : TelemetryRadio;
            part antenna : AntennaSystem;
            part commandGateway : CommandGateway;
        }
        part def RecoveryPropulsion;
        part def RecoveryController;
        part def IngressMonitor;
        part def HealthAndRecovery {
            part motorSystem : RecoveryPropulsion;
            part recoveryController : RecoveryController;
            part ingressMonitor : IngressMonitor;
        }
        part def NavigationSignaling;
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
            part signaling : NavigationSignaling;
            part observationPayload : ObservationPayload [0..1];
        }
        part missionContext {
            part boat : Boat;
            part operator : Operator;
            part shoreSupport : ShoreSupport;
            part environment : Environment;
            part traffic : OtherVessel [0..*];
        }
    }

}
