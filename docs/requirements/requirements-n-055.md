# N-055 Weed blockage response: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_055_0::thread direction=BT statements=true
package Page_requirements_n_055_0 {
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
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::weedBlockageContingency;
        expose BlueDogRequirements::weedBlockageFault;
        expose BlueDogRequirements::weedBlockageLocation;
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
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 1380; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::weedBlockageContingency { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::weedBlockageFault { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::weedBlockageLocation { x = 960; y = 2400; }
    }
}
```
