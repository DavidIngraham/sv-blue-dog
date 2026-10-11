# N-020 Ocean environment: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_020_0::thread direction=BT statements=true
package Page_requirements_n_020_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose BlueDogRequirements::oceanEnvironment;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDogRequirements::oceanCurrent;
        expose BlueDogRequirements::oceanSurvivalWaves;
        expose BlueDogRequirements::oceanSurvivalWind;
        expose BlueDogRequirements::oceanWaves;
        expose BlueDogRequirements::oceanWind;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::saltwaterExposure;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::oceanCurrent { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWaves { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWind { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::oceanWaves { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::oceanWind { x = 0; y = 980; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 980; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 0; y = 2000; }
    }
}
```
