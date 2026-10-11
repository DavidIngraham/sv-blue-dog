# N-010 Gorge environment: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_010_0::thread direction=BT statements=true
package Page_requirements_n_010_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeCurrent;
        expose BlueDogRequirements::gorgeSurvivalWaves;
        expose BlueDogRequirements::gorgeSurvivalWind;
        expose BlueDogRequirements::gorgeWaves;
        expose BlueDogRequirements::gorgeWind;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::freshwaterExposure;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedSnagShedding;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::gorgeCurrent { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWaves { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWind { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::gorgeWaves { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::gorgeWind { x = 0; y = 1780; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 320; y = 1780; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 640; y = 1780; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 640; y = 2000; }
    }
}
```

## Continue the breakdown

- [Submerged weed passage](requirements-n-053.md)
- [Weed snag shedding](requirements-n-054.md)
