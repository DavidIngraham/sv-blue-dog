# N-001 Environmental envelope: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_001_0::thread direction=BT statements=true
package Page_requirements_n_001_0 {
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
        expose BlueDogRequirements::airTemperature;
        expose BlueDogRequirements::calmOperation;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::humidity;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::waterTemperature;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::airTemperature { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::calmOperation { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::humidity { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 1780; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 320; y = 1780; }
        metadata Layout about BlueDogRequirements::visibility { x = 640; y = 1780; }
        metadata Layout about BlueDogRequirements::waterTemperature { x = 960; y = 1780; }
    }
}
```

## Continue the breakdown

- [Envelope transition](requirements-n-035.md)
- [Marine durability](requirements-n-002.md)
- [Stability and fouling](requirements-n-003.md)
- [Visibility](requirements-n-033.md)
