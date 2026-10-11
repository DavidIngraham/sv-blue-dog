# N-044 Wet mechanical integrity: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_044_0::thread direction=BT statements=true
package Page_requirements_n_044_0 {
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
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetJointIntegrity;
        expose BlueDogRequirements::wetMechanismTravel;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::wetJointIntegrity { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::wetMechanismTravel { x = 320; y = 2400; }
    }
}
```
