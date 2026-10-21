# Traffic safety, communications and monitoring

[Requirements overview](../requirements.md) · [Current assessment](../current-assessment.md)

Finishing the course cannot take priority over other river users. The boat needs onboard traffic assessment, conspicuous behavior and a recovery response when a required safety capability is lost. Shore telemetry lets me observe the attempt; intervention ends qualification.

## Traffic and operating boundary

The boat must observe relevant traffic, assess conflicts and act within its timing and maneuvering capability. Distance depends on target class, relative motion, uncertainty, reviewed clearance and achieved response, including hazards arriving during an occupied maneuver. Timely acquisition and track reliability are separate evidence obligations. Occupied kayaks, stand-up paddleboards, people in the water and unoccupied craft remain distinct cases; uncertain occupancy must not receive a presumed low-consequence treatment. The [allocation reference](../reference/encounter-envelope.md) identifies the still-unresolved acceptance criteria.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_safety_18::thread direction=BT statements=true
package Page_safety_18 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::avoidanceCommandDeadline;
        expose BlueDogRequirements::boundaryAvoidanceDeadline;
        expose BlueDogRequirements::boundaryAvoidanceRecording;
        expose BlueDogRequirements::boundaryDegradedEvidence;
        expose BlueDogRequirements::boundaryEvaluationCadence;
        expose BlueDogRequirements::boundaryStartInhibition;
        expose BlueDogRequirements::collisionAssessmentCadence;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationConspicuity;
        expose GorgeChallenge::navigationRules;
        expose BlueDogRequirements::operatingBoundary;
        expose GorgeChallenge::restrictedWaters;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::trafficAwarenessFault;
        expose BlueDogRequirements::trafficSafety;
        expose GorgeChallenge::trafficCoexistence;
        expose BlueDogRequirements::trafficTracking;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::avoidanceCommandDeadline { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceDeadline { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceRecording { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryDegradedEvidence { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryEvaluationCadence { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::boundaryStartInhibition { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::collisionAssessmentCadence { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::trafficAwarenessFault { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::trafficTracking { x = 320; y = 1200; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 1200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 1200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 1600; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 1600; }
        metadata Layout about GorgeChallenge::navigationRules { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::restrictedWaters { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::trafficCoexistence { x = 640; y = 2000; }
    }
}
```

</details>


## Conspicuity, classification and recovery

Navigation signals and operating applicability depend on the actual vessel and mode. The model records obligations and release criteria; the site and installation evidence must support them.

### Deployment release and safe recovery

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_safety_19::thread direction=BT statements=true
package Page_safety_19 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::abortLatchDeadline;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::controlLossLocationContinuity;
        expose BlueDogRequirements::deploymentComplianceRecord;
        expose BlueDogRequirements::deploymentReleaseGate;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::isolationRestartInhibition;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::manualControlLossShutdown;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::motorIsolationDeadline;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::recoveryTelemetryCadence;
        expose BlueDogRequirements::regulatoryClassification;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::weedBlockageResponse;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::abortLatchDeadline { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::controlLossLocationContinuity { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::deploymentComplianceRecord { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::deploymentReleaseGate { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::isolationRestartInhibition { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::manualControlLossShutdown { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::motorIsolationDeadline { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryTelemetryCadence { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::liveObservation { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 3200; }
    }
}
```

</details>

### Navigation signals and signaling faults

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_safety_20::thread direction=BT statements=true
package Page_safety_20 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationConspicuity;
        expose GorgeChallenge::navigationRules;
        expose BlueDogRequirements::navigationLightPresentation;
        expose BlueDogRequirements::navigationShapePresentation;
        expose BlueDogRequirements::navigationSoundPresentation;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::signalingFaultRecording;
        expose BlueDogRequirements::signalingFaultReporting;
        expose BlueDogRequirements::signalingModeDeadline;
        expose BlueDogRequirements::trafficSafety;
        expose GorgeChallenge::trafficCoexistence;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::navigationLightPresentation { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::navigationShapePresentation { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::navigationSoundPresentation { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::signalingFaultRecording { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::signalingFaultReporting { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::signalingModeDeadline { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 320; y = 800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 1200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 1200; }
        metadata Layout about GorgeChallenge::navigationRules { x = 0; y = 1600; }
        metadata Layout about GorgeChallenge::trafficCoexistence { x = 320; y = 1600; }
    }
}
```

</details>


## Live monitoring and telemetry

Telemetry supports observation without becoming a required control link. Lost communications must preserve autonomous decisions, and important events must remain available after reconnection.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_safety_21::thread direction=BT statements=true
package Page_safety_21 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::backlogCurrentPriority;
        expose BlueDogRequirements::backlogOrdering;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::logRetention;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::outageAutonomy;
        expose BlueDogRequirements::reconnectCurrentRecord;
        expose BlueDogRequirements::reconnectLogPreservation;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        expose BlueDogRequirements::telemetryDisplayContent;
        expose BlueDogRequirements::telemetryDuplicateSuppression;
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryIdentityPreservation;
        expose BlueDogRequirements::telemetryStaleIndication;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::backlogCurrentPriority { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::backlogOrdering { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::logRetention { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::outageAutonomy { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::reconnectCurrentRecord { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryDisplayContent { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryDuplicateSuppression { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::telemetryIdentityPreservation { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::telemetryStaleIndication { x = 640; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 1600; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::liveObservation { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 2400; }
    }
}
```

</details>


## Command integrity

Commands need validity, freshness and preserved restrictions so stale messages or a restart cannot trigger an unsafe action or restore qualification.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_safety_22::thread direction=BT statements=true
package Page_safety_22 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::acceptedCommandDeadline;
        expose BlueDogRequirements::acknowledgmentQueueing;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::expiredCommandRejection;
        expose BlueDogRequirements::externalControlDisqualification;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::onboardAcknowledgmentDeadline;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::replayCommandRejection;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::unauthenticatedCommandRejection;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::acceptedCommandDeadline { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::acknowledgmentQueueing { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::expiredCommandRejection { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::externalControlDisqualification { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::onboardAcknowledgmentDeadline { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::replayCommandRejection { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::unauthenticatedCommandRejection { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 960; y = 2400; }
    }
}
```

</details>

## Autonomous abort and shore recovery

When continuing is unsafe, the boat must end qualification and act onboard. Alert delivery or operator acknowledgment cannot be a prerequisite for attempting recovery.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view SRR_Thread_safety::thread direction=BT statements=true
package SRR_Thread_safety {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::navigationRules;
        expose GorgeChallenge::safetyCapabilityAbort;
        expose GorgeChallenge::autonomousShoreRecovery;
        expose GorgeChallenge::abortAlert;
        expose GorgeChallenge::courseRecoveryReserve;
        expose GorgeChallenge::reserveAbort;
        expose GorgeChallenge::recoveryConspicuity;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::navigationRules { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::safetyCapabilityAbort { x = 640; y = 0; }
        metadata Layout about GorgeChallenge::autonomousShoreRecovery { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::abortAlert { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::courseRecoveryReserve { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::reserveAbort { x = 0; y = 800; }
        metadata Layout about GorgeChallenge::recoveryConspicuity { x = 320; y = 800; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
