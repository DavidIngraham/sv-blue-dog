package BlueDog {
    doc /* Working architecture model, 2026-10-09.
     * Confirmed threshold: Bingen-Stevenson-Bingen round trip.
     * Repeated operation is a future endurance objective, outside current acceptance.
     * Qualifying round trips require no operator intervention; live monitoring is required.
     * Current design driver: one finite GorgeChallenge::transGorgeChallenge round trip.
     * Goals::hawaiiVoyage is a separate future mission with its own constraints.
     * Multi-day endurance with energy harvesting remains an earlier intent. SysML v2 learning is a project goal.
     * Decomposition identifies responsibilities; physical design remains open.
     * Tool checks are recorded in the modeling guide; design satisfaction links
     * are maintained separately and do not establish verification.
     */

    private import GorgeChallenge::*;

    package DesignIntent {
        doc /* Owner-imposed project constraints: one-person transport, construction on a
         * 250 mm cubic desktop printer, and serviceability between deployments. These
         * remain binding alongside the finite Gorge mission, not consequences of sailing success.
         */
    }

    package Goals {
        requirement def <'H-001'> HawaiiVoyage {
            metadata applicability : BlueDogMissionScope::Applicability { mission = BlueDogMissionScope::MissionKind::futureOcean; }
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
             * TransGorgeCourse defines marker-referenced gates, subject to course release review.
             * The finite challenge has no completion deadline. GorgeChallenge defines
             * monitoring and recovery obligations; environmental allocations and
             * real recovery sites remain subject to review.
             * No operator intervention is permitted during a qualifying round trip.
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
             * Candidate architecture for the finite Gorge challenge. Future missions require separate allocation.
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
