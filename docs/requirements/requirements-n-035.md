# N-035 Envelope transition: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_035_0::thread direction=BT statements=true
package Page_requirements_n_035_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::resumptionBlockEvidence;
        expose BlueDogRequirements::sailingResumptionDeadline;
        expose BlueDogRequirements::sailingResumptionInhibition;
        expose BlueDogRequirements::survivalEntryDeadline;
        expose BlueDogRequirements::survivalTransitionRecording;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 580; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 0; y = 1380; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 320; y = 1380; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::resumptionBlockEvidence { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::sailingResumptionDeadline { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::sailingResumptionInhibition { x = 0; y = 2180; }
        metadata Layout about BlueDogRequirements::survivalEntryDeadline { x = 320; y = 2180; }
        metadata Layout about BlueDogRequirements::survivalTransitionRecording { x = 640; y = 2180; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 960; y = 2180; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 2400; }
    }
}
```
