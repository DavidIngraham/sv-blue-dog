# E-001 Energy awareness: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_e_001_0::thread direction=BT statements=true
package Page_requirements_e_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::repeatedOperation;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::conservativeEnergyEstimate;
        expose BlueDogRequirements::energyEstimateAccuracy;
        expose BlueDogRequirements::energyEstimateCadence;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::reserveEstimateCadence;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::conservativeEnergyEstimate { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::energyEstimateAccuracy { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::energyEstimateCadence { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::reserveEstimateCadence { x = 0; y = 1780; }
    }
}
```

## Continue the breakdown

- [Low energy recovery](requirements-e-004.md)
