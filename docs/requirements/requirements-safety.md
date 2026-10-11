# Traffic safety, communications and monitoring

Other river users are part of the operating context. The vessel must remain observable, respect its operating boundary and distinguish monitoring from intervention that ends a qualifying attempt.

[Requirements overview](../requirements.md) · [Modeling method](../methods/modeling.md)

Arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision, and **dependency** records a design basis. Each view retains its upstream context; statements are rendered from the model.

- [Traffic and operating boundary](#traffic-and-operating-boundary)
- [Conspicuity, classification and recovery](#conspicuity-classification-and-recovery)
- [Live monitoring and telemetry](#live-monitoring-and-telemetry)
- [Command integrity](#command-integrity)

## Traffic and operating boundary

```sysml-view Page_safety_18::thread direction=BT statements=true
package Page_safety_18 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::avoidanceCommandDeadline;
        expose BlueDogRequirements::boundaryAvoidanceDeadline;
        expose BlueDogRequirements::boundaryAvoidanceRecording;
        expose BlueDogRequirements::boundaryDegradedEvidence;
        expose BlueDogRequirements::boundaryEvaluationCadence;
        expose BlueDogRequirements::boundaryStartInhibition;
        expose BlueDogRequirements::collisionAssessmentCadence;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::trafficAwarenessFault;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::trafficTracking;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::avoidanceCommandDeadline { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceDeadline { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceRecording { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryDegradedEvidence { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::boundaryEvaluationCadence { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::boundaryStartInhibition { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::collisionAssessmentCadence { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::trafficAwarenessFault { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::trafficTracking { x = 640; y = 1200; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 1200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 1600; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 1600; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 1600; }
    }
}
```


## Conspicuity, classification and recovery

### Deployment release and safe recovery

```sysml-view Page_safety_19::thread direction=BT statements=true
package Page_safety_19 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::abortLatchDeadline { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::controlLossLocationContinuity { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::deploymentComplianceRecord { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::deploymentReleaseGate { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::isolationRestartInhibition { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::manualControlLossShutdown { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::motorIsolationDeadline { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryTelemetryCadence { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 2800; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 3200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 3200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 3600; }
    }
}
```

### Navigation signals and signaling faults

```sysml-view Page_safety_20::thread direction=BT statements=true
package Page_safety_20 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::navigationLightPresentation;
        expose BlueDogRequirements::navigationShapePresentation;
        expose BlueDogRequirements::navigationSoundPresentation;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::signalingFaultRecording;
        expose BlueDogRequirements::signalingFaultReporting;
        expose BlueDogRequirements::signalingModeDeadline;
        expose BlueDogRequirements::trafficSafety;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::navigationLightPresentation { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::navigationShapePresentation { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::navigationSoundPresentation { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::signalingFaultRecording { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::signalingFaultReporting { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::signalingModeDeadline { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 640; y = 800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 1200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 1200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 1200; }
    }
}
```


## Live monitoring and telemetry

```sysml-view Page_safety_21::thread direction=BT statements=true
package Page_safety_21 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::backlogCurrentPriority { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::backlogOrdering { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::logRetention { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::outageAutonomy { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::reconnectCurrentRecord { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryDisplayContent { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryDuplicateSuppression { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::telemetryIdentityPreservation { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::telemetryStaleIndication { x = 960; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 2400; }
    }
}
```


## Command integrity

```sysml-view Page_safety_22::thread direction=BT statements=true
package Page_safety_22 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::acceptedCommandDeadline { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::acknowledgmentQueueing { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::communications { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::expiredCommandRejection { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::externalControlDisqualification { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::onboardAcknowledgmentDeadline { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::replayCommandRejection { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::unauthenticatedCommandRejection { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 2800; }
    }
}
```
