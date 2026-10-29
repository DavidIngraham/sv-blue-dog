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
        expose BlueDog::Requirements::avoidanceCommandDeadline;
        expose BlueDog::Requirements::boundaryAvoidanceDeadline;
        expose BlueDog::Requirements::boundaryAvoidanceRecording;
        expose BlueDog::Requirements::boundaryDegradedEvidence;
        expose BlueDog::Requirements::boundaryEvaluationCadence;
        expose BlueDog::Requirements::boundaryStartInhibition;
        expose BlueDog::Requirements::collisionAssessmentCadence;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationConspicuity;
        expose GorgeChallenge::navigationRules;
        expose BlueDog::Requirements::operatingBoundary;
        expose GorgeChallenge::restrictedWaters;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::trafficAwarenessFault;
        expose BlueDog::Requirements::trafficSafety;
        expose GorgeChallenge::trafficCoexistence;
        expose BlueDog::Requirements::trafficTracking;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::avoidanceCommandDeadline { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::boundaryAvoidanceDeadline { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::boundaryAvoidanceRecording { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::boundaryDegradedEvidence { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::boundaryEvaluationCadence { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::boundaryStartInhibition { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::collisionAssessmentCadence { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::navigationConspicuity { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::operatingBoundary { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::trafficAwarenessFault { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::trafficSafety { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::trafficTracking { x = 320; y = 1200; }
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
        expose BlueDog::Requirements::abortLatchDeadline;
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::controlLossLocationContinuity;
        expose BlueDog::Requirements::deploymentComplianceRecord;
        expose BlueDog::Requirements::deploymentReleaseGate;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::isolationRestartInhibition;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::manualControlLossShutdown;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::motorIsolationDeadline;
        expose BlueDog::Requirements::motorQualificationInvariant;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::periodicLogCadence;
        expose BlueDog::Requirements::qualificationPersistence;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::recoveryTelemetryCadence;
        expose BlueDog::Requirements::regulatoryClassification;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::weedBlockageResponse;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::abortLatchDeadline { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::challengeMotorInhibition { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::commandIntegrity { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::communications { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::controlLossLocationContinuity { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::deploymentComplianceRecord { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::deploymentReleaseGate { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::envelopeTransition { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::isolationRestartInhibition { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::manualControlLossShutdown { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::motorIsolationDeadline { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::motorQualificationInvariant { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::periodicLogCadence { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::qualificationPersistence { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::recoveryTelemetryCadence { x = 640; y = 2000; }
        metadata Layout about BlueDog::Requirements::regulatoryClassification { x = 960; y = 2000; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 0; y = 2400; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 2400; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 640; y = 2400; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 960; y = 2400; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 1120; y = 2580; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 0; y = 2800; }
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
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationConspicuity;
        expose GorgeChallenge::navigationRules;
        expose BlueDog::Requirements::navigationLightPresentation;
        expose BlueDog::Requirements::navigationShapePresentation;
        expose BlueDog::Requirements::navigationSoundPresentation;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::signalingFaultRecording;
        expose BlueDog::Requirements::signalingFaultReporting;
        expose BlueDog::Requirements::signalingModeDeadline;
        expose BlueDog::Requirements::trafficSafety;
        expose GorgeChallenge::trafficCoexistence;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::navigationConspicuity { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::navigationLightPresentation { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::navigationShapePresentation { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::navigationSoundPresentation { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::signalingFaultRecording { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::signalingFaultReporting { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::signalingModeDeadline { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::trafficSafety { x = 320; y = 800; }
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
        expose BlueDog::Requirements::backlogCurrentPriority;
        expose BlueDog::Requirements::backlogOrdering;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::logRetention;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::outageAutonomy;
        expose BlueDog::Requirements::reconnectCurrentRecord;
        expose BlueDog::Requirements::reconnectLogPreservation;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::telemetryDeliveryCadence;
        expose BlueDog::Requirements::telemetryDisplayContent;
        expose BlueDog::Requirements::telemetryDuplicateSuppression;
        expose BlueDog::Requirements::telemetryEquipment;
        expose BlueDog::Requirements::telemetryIdentityPreservation;
        expose BlueDog::Requirements::telemetryStaleIndication;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::backlogCurrentPriority { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::backlogOrdering { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::commandIntegrity { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::communications { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::logRetention { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::outageAutonomy { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::reconnectCurrentRecord { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::reconnectLogPreservation { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::telemetryDeliveryCadence { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::telemetryDisplayContent { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::telemetryDuplicateSuppression { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::telemetryEquipment { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::telemetryIdentityPreservation { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::telemetryStaleIndication { x = 640; y = 1600; }
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
        expose BlueDog::Requirements::acceptedCommandDeadline;
        expose BlueDog::Requirements::acknowledgmentQueueing;
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::criticalEventRecording;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::expiredCommandRejection;
        expose BlueDog::Requirements::externalControlDisqualification;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationAvailability;
        expose BlueDog::Requirements::onboardAcknowledgmentDeadline;
        expose BlueDog::Requirements::qualificationPersistence;
        expose BlueDog::Requirements::replayCommandRejection;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::unauthenticatedCommandRejection;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::acceptedCommandDeadline { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::acknowledgmentQueueing { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::challengeMotorInhibition { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::commandIntegrity { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::communications { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::criticalEventRecording { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::expiredCommandRejection { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::externalControlDisqualification { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::navigationAvailability { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::onboardAcknowledgmentDeadline { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::qualificationPersistence { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::replayCommandRejection { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::unauthenticatedCommandRejection { x = 320; y = 2000; }
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

## Entry review and qualification decisions

C-007 governs vessel navigation compliance. C-028 through C-032 identify the entrant, organizer and operator duties needed to review entry and adjudicate an attempt. Their process records remain subject to the planned review; traceability does not establish compliance.

<details>
<summary>Model process obligations and their source</summary>

```sysml-view Page_safety_process::thread direction=BT statements=true
package Page_safety_process {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::navigationRules;
        expose GorgeChallenge::navigationRuleApplicability;
        expose GorgeChallenge::navigationRuleBaseline;
        expose GorgeChallenge::navigationEntryEvidence;
        expose GorgeChallenge::operatorSafetyIntervention;
        expose GorgeChallenge::navigationAdjudication;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::navigationRules { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::navigationRuleApplicability { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::navigationRuleBaseline { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::navigationEntryEvidence { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::operatorSafetyIntervention { x = 0; y = 800; }
        metadata Layout about GorgeChallenge::navigationAdjudication { x = 320; y = 800; }
    }
}
```

</details>
