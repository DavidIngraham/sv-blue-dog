# E-008 Navigation availability: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_e_008_0::thread direction=BT statements=true
package Page_requirements_e_008_0 {
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
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::navigationDegradedTransition;
        expose BlueDogRequirements::navigationValidEpochs;
        expose BlueDogRequirements::staleNavigationInvalidation;
        expose BlueDogRequirements::staleNavigationUseInhibition;
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
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 1380; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::navigationDegradedTransition { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::navigationValidEpochs { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::staleNavigationInvalidation { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::staleNavigationUseInhibition { x = 0; y = 2180; }
    }
}
```
