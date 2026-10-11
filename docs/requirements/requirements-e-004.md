# E-004 Low energy recovery: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

## Breakdown 1

```sysml-view Page_requirements_e_004_0::thread direction=BT statements=true
package Page_requirements_e_004_0 {
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
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::lowEnergyCollisionContinuity;
        expose BlueDogRequirements::lowEnergyEntry;
        expose BlueDogRequirements::lowEnergyExit;
        expose BlueDogRequirements::lowEnergyNavigationContinuity;
        expose BlueDogRequirements::lowEnergyPayloadInhibition;
        expose BlueDogRequirements::payloadRestartPermission;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::motorQualificationInvariant;
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
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 1380; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 320; y = 1380; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 1380; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 960; y = 1380; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 1780; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::lowEnergyCollisionContinuity { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::lowEnergyEntry { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::lowEnergyExit { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::lowEnergyNavigationContinuity { x = 0; y = 2180; }
        metadata Layout about BlueDogRequirements::lowEnergyPayloadInhibition { x = 320; y = 2180; }
        metadata Layout about BlueDogRequirements::payloadRestartPermission { x = 640; y = 2180; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 960; y = 2180; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 2360; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 2400; }
    }
}
```

## Breakdown 2

```sysml-view Page_requirements_e_004_1::thread direction=BT statements=true
package Page_requirements_e_004_1 {
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
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 580; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 320; y = 2000; }
    }
}
```
