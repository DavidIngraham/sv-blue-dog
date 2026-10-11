# N-051 Self righting: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_051_0::thread direction=BT statements=true
package Page_requirements_n_051_0 {
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
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeBallastRetention;
        expose BlueDogRequirements::capsizeElectronicsSealing;
        expose BlueDogRequirements::capsizeRigRetention;
        expose BlueDogRequirements::rightingDeadline;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::capsizeBallastRetention { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::capsizeElectronicsSealing { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::capsizeRigRetention { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::rightingDeadline { x = 960; y = 2400; }
    }
}
```
