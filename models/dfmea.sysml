package BlueDogDFMEA {
    private import ScalarValues::*;
    doc /* Initial design failure-mode review. Rows are hypotheses, not exhaustive
     * hazard coverage or measured rates. No ordinal score is converted to probability.
     * Scope includes sailing, holds, recovery, and common-cause failures.
     */
    part def FailureMode {
        attribute identifier : String;
        ref part affected : Parts::Part;
        attribute intendedFunction : String;
        attribute failureMode : String;
        attribute cause : String;
        attribute localEffect : String;
        attribute missionEffect : String;
        attribute proposedDetection : String;
        attribute recommendedAction : String;
        attribute ownerRole : String;
        attribute safetyCritical : Boolean;
        attribute dispositionAccepted : Boolean default false;
        attribute actionEvidenceAccepted : Boolean default false;
        attribute evidenceReference : String default "Not yet available";
    }
    part def Review {
        ref part vessel : BlueDog::Architecture::Boat;
        part modes : FailureMode [1..*];
        attribute scopeReviewed : Boolean;
    }
    analysis def DesignFailureReview {
        subject review : Review;
        out attribute modeCount : Integer = SequenceFunctions::size(review.modes);
        out attribute safetyCriticalCount : Integer = SequenceFunctions::size(review.modes->ControlFunctions::select { in mode : FailureMode; mode.safetyCritical });
        out attribute unresolvedCriticalCount : Integer = SequenceFunctions::size(review.modes->ControlFunctions::select {
            in mode : FailureMode; mode.safetyCritical and not (mode.dispositionAccepted and mode.actionEvidenceAccepted and mode.evidenceReference != "Not yet available") });
        out attribute openActionCount : Integer = SequenceFunctions::size(review.modes->ControlFunctions::select { in mode : FailureMode; not mode.actionEvidenceAccepted });
        return reviewReady : Boolean = modeCount > 0 and review.scopeReviewed and unresolvedCriticalCount == 0;
        objective inventory { require constraint { modeCount > 0 } }
    }
    part starter : Review {
        ref part :>> vessel = BlueDog::Architecture::missionContext.boat;
        attribute :>> scopeReviewed default = false;
        part hullLeak : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.hullAndRig.printedHull;
            attribute :>> identifier = "FM-001";
            attribute :>> intendedFunction = "Retain buoyancy";
            attribute :>> failureMode = "Printed seam leaks";
            attribute :>> cause = "Cyclic wave load or print defect";
            attribute :>> localEffect = "Water enters hull";
            attribute :>> missionEffect = "Buoyancy or electrical function lost";
            attribute :>> proposedDetection = "Ingress sensing; acceptance unproven";
            attribute :>> recommendedAction = "Coupon fatigue, seam pressure test and flooded-compartment trial";
            attribute :>> ownerRole = "Hull/structure";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part keelLoss : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.hullAndRig.keelAndBallast;
            attribute :>> identifier = "FM-002";
            attribute :>> intendedFunction = "Maintain righting moment";
            attribute :>> failureMode = "Keel attachment fractures";
            attribute :>> cause = "Fatigue or impact";
            attribute :>> localEffect = "Ballast detached";
            attribute :>> missionEffect = "Persistent inversion or vessel loss";
            attribute :>> proposedDetection = "Attitude sensor; attachment inspection";
            attribute :>> recommendedAction = "Proof load and fatigue qualification of joint";
            attribute :>> ownerRole = "Hull/structure";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part steeringJam : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.actuation;
            attribute :>> identifier = "FM-003";
            attribute :>> intendedFunction = "Control heading";
            attribute :>> failureMode = "Rudder or linkage jams";
            attribute :>> cause = "Milfoil wrap, debris or actuator fault";
            attribute :>> localEffect = "Commanded rudder motion unavailable";
            attribute :>> missionEffect = "Reduced VMG; boundary excursion or collision";
            attribute :>> proposedDetection = "Position/current disagreement detection to be designed";
            attribute :>> recommendedAction = "Weed-jam injection and autonomous clearing trial";
            attribute :>> ownerRole = "Actuation";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part sailJam : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.actuation;
            attribute :>> identifier = "FM-004";
            attribute :>> intendedFunction = "Control sail force";
            attribute :>> failureMode = "Wing trim jams";
            attribute :>> cause = "Bearing wear, salt or drive failure";
            attribute :>> localEffect = "Trim fixed in unsafe position";
            attribute :>> missionEffect = "VMG loss or overpower/capsize";
            attribute :>> proposedDetection = "Command/response monitoring to be designed";
            attribute :>> recommendedAction = "Jam test at adverse trim; passive load limiting trade";
            attribute :>> ownerRole = "Actuation";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part batteryFault : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.energy.storage;
            attribute :>> identifier = "FM-005";
            attribute :>> intendedFunction = "Supply essential power";
            attribute :>> failureMode = "Battery disconnects or faults";
            attribute :>> cause = "Cell degradation, BMS trip or short";
            attribute :>> localEffect = "Bus power lost or overheating";
            attribute :>> missionEffect = "Mission loss; possible thermal damage";
            attribute :>> proposedDetection = "Voltage/temperature/current sensing to be verified";
            attribute :>> recommendedAction = "Cold/aged-cell loading and BMS fault injection";
            attribute :>> ownerRole = "Power";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part harvestLoss : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.energy.harvesting;
            attribute :>> identifier = "FM-006";
            attribute :>> intendedFunction = "Replenish stored energy";
            attribute :>> failureMode = "Harvesting stops";
            attribute :>> cause = "Connector corrosion or panel damage";
            attribute :>> localEffect = "Persistent energy deficit";
            attribute :>> missionEffect = "Long-hold exposure exhausts reserve";
            attribute :>> proposedDetection = "Harvest-current residual monitoring to be designed";
            attribute :>> recommendedAction = "No-harvest fault campaign and reserve policy validation";
            attribute :>> ownerRole = "Power";
            attribute :>> safetyCritical = false;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part powerCommonCause : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.energy.powerManagement;
            attribute :>> identifier = "FM-007";
            attribute :>> intendedFunction = "Keep essential services powered";
            attribute :>> failureMode = "Shared bus fault disables multiple functions";
            attribute :>> cause = "Regulator short or common water ingress";
            attribute :>> localEffect = "Navigation, actuation and telemetry lost together";
            attribute :>> missionEffect = "Mission and observation lost";
            attribute :>> proposedDetection = "Independent health path not yet designed";
            attribute :>> recommendedAction = "Assess isolation and independence; common-cause fault injection";
            attribute :>> ownerRole = "Power/system";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part navigationFault : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.navigation.positionAndAttitude;
            attribute :>> identifier = "FM-008";
            attribute :>> intendedFunction = "Estimate position and heading";
            attribute :>> failureMode = "Plausible wrong navigation solution";
            attribute :>> cause = "Bias, stale data or corrupted input";
            attribute :>> localEffect = "Guidance uses wrong state";
            attribute :>> missionEffect = "Boundary/traffic hazard and route failure";
            attribute :>> proposedDetection = "Plausibility checks; independent reference unresolved";
            attribute :>> recommendedAction = "Biased/stale-sensor injection across speed/current profiles";
            attribute :>> ownerRole = "Navigation";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part controlLockup : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.control.missionManager;
            attribute :>> identifier = "FM-009";
            attribute :>> intendedFunction = "Execute autonomous mission";
            attribute :>> failureMode = "Controller hangs or repeats invalid command";
            attribute :>> cause = "Systematic software fault or reset corruption";
            attribute :>> localEffect = "Mission logic stops or is unsafe";
            attribute :>> missionEffect = "No progress or unsafe actuation";
            attribute :>> proposedDetection = "Watchdog and restoration requirements; unverified";
            attribute :>> recommendedAction = "Fault injection and persisted-state consistency testing";
            attribute :>> ownerRole = "Autonomy";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part trafficMiss : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.control.collisionAvoidance;
            attribute :>> identifier = "FM-010";
            attribute :>> intendedFunction = "Avoid other vessels";
            attribute :>> failureMode = "Traffic conflict missed";
            attribute :>> cause = "Sensor blind spot or prediction error";
            attribute :>> localEffect = "Avoidance not commanded";
            attribute :>> missionEffect = "Collision risk";
            attribute :>> proposedDetection = "Independent lookout unavailable onboard";
            attribute :>> recommendedAction = "Non-AIS traffic scenarios and safe boundary strategies";
            attribute :>> ownerRole = "Autonomy/safety";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part radioLoss : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.communications.telemetryRadio;
            attribute :>> identifier = "FM-011";
            attribute :>> intendedFunction = "Provide live observation";
            attribute :>> failureMode = "Radio link unavailable";
            attribute :>> cause = "Antenna wetting, shadowing or radio fault";
            attribute :>> localEffect = "Live data cannot reach shore";
            attribute :>> missionEffect = "Observation outage; autonomy must continue";
            attribute :>> proposedDetection = "Contact-age monitoring and retained logs";
            attribute :>> recommendedAction = "Wet/inverted antenna trials and 24-hour outage/reconnect test";
            attribute :>> ownerRole = "Communications";
            attribute :>> safetyCritical = false;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
        part motorUncommanded : FailureMode subsets modes {
            ref part :>> affected = BlueDog::Architecture::missionContext.boat.recovery.motorSystem;
            attribute :>> identifier = "FM-012";
            attribute :>> intendedFunction = "Provide controlled recovery thrust";
            attribute :>> failureMode = "Motor energizes during qualifying sailing";
            attribute :>> cause = "Driver short or command gating fault";
            attribute :>> localEffect = "Unintended powered propulsion";
            attribute :>> missionEffect = "Challenge disqualification or contact hazard";
            attribute :>> proposedDetection = "Isolation and qualification latch; unverified";
            attribute :>> recommendedAction = "Stuck-driver test and independent propulsion isolation";
            attribute :>> ownerRole = "Recovery";
            attribute :>> safetyCritical = true;
            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
            metadata risk : RiskMetadata::Risk;
        }
    }
    dependency hullLeakDesign from starter::hullLeak to BlueDog::Architecture::missionContext::boat::hullAndRig::printedHull;
    dependency hullLeakCriterion from starter::hullLeak to BlueDogRequirements::enclosureSealing;
    dependency keelLossDesign from starter::keelLoss to BlueDog::Architecture::missionContext::boat::hullAndRig::keelAndBallast;
    dependency keelLossCriterion from starter::keelLoss to BlueDogRequirements::selfRighting;
    dependency steeringJamDesign from starter::steeringJam to BlueDog::Architecture::missionContext::boat::actuation;
    dependency steeringJamCriterion from starter::steeringJam to BlueDogRequirements::weedSnagSteeringRecovery;
    dependency sailJamDesign from starter::sailJam to BlueDog::Architecture::missionContext::boat::actuation;
    dependency sailJamCriterion from starter::sailJam to BlueDogRequirements::sailCommandCadence;
    dependency batteryFaultDesign from starter::batteryFault to BlueDog::Architecture::missionContext::boat::energy::storage;
    dependency batteryFaultCriterion from starter::batteryFault to BlueDogRequirements::sustainedReserveProtection;
    dependency harvestLossDesign from starter::harvestLoss to BlueDog::Architecture::missionContext::boat::energy::harvesting;
    dependency harvestLossCriterion from starter::harvestLoss to BlueDogRequirements::lowEnergyEntry;
    dependency powerCommonCauseDesign from starter::powerCommonCause to BlueDog::Architecture::missionContext::boat::energy::powerManagement;
    dependency powerCommonCauseCriterion from starter::powerCommonCause to BlueDogRequirements::missionReliability;
    dependency navigationFaultDesign from starter::navigationFault to BlueDog::Architecture::missionContext::boat::navigation::positionAndAttitude;
    dependency navigationFaultCriterion from starter::navigationFault to BlueDogRequirements::navigationAvailability;
    dependency controlLockupDesign from starter::controlLockup to BlueDog::Architecture::missionContext::boat::control::missionManager;
    dependency controlLockupCriterion from starter::controlLockup to BlueDogRequirements::resetRecovery;
    dependency trafficMissDesign from starter::trafficMiss to BlueDog::Architecture::missionContext::boat::control::collisionAvoidance;
    dependency trafficMissCriterion from starter::trafficMiss to BlueDogRequirements::trafficSafety;
    dependency radioLossDesign from starter::radioLoss to BlueDog::Architecture::missionContext::boat::communications::telemetryRadio;
    dependency radioLossCriterion from starter::radioLoss to BlueDogRequirements::outageAutonomy;
    dependency motorUncommandedDesign from starter::motorUncommanded to BlueDog::Architecture::missionContext::boat::recovery::motorSystem;
    dependency motorUncommandedCriterion from starter::motorUncommanded to BlueDogRequirements::challengeMotorInhibition;
    dependency dispositionCriterion from DesignFailureReview to BlueDogRequirements::criticalFailureDisposition;
    dependency speedExposureFeedback from DesignFailureReview to BlueDogReliability::CruiseReliability;
    dependency commonCauseBudget from starter::powerCommonCause to BlueDogRequirements::failureRateBudget;
}
