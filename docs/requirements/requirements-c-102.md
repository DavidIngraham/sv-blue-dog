# C-102 Command integrity: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

## Breakdown 1

```sysml-view Page_requirements_c_102_0::thread direction=BT statements=true
package Page_requirements_c_102_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::acceptedCommandDeadline;
        expose BlueDogRequirements::acknowledgmentQueueing;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::expiredCommandRejection;
        expose BlueDogRequirements::externalControlDisqualification;
        expose BlueDogRequirements::onboardAcknowledgmentDeadline;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::replayCommandRejection;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 580; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 580; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 1380; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 320; y = 1380; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::acceptedCommandDeadline { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::acknowledgmentQueueing { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::expiredCommandRejection { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::externalControlDisqualification { x = 0; y = 2180; }
        metadata Layout about BlueDogRequirements::onboardAcknowledgmentDeadline { x = 320; y = 2180; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 640; y = 2180; }
        metadata Layout about BlueDogRequirements::replayCommandRejection { x = 960; y = 2180; }
    }
}
```

## Breakdown 2

```sysml-view Page_requirements_c_102_1::thread direction=BT statements=true
package Page_requirements_c_102_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::unauthenticatedCommandRejection;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 580; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::unauthenticatedCommandRejection { x = 0; y = 2000; }
    }
}
```
