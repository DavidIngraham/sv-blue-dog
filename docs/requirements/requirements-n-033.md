# N-033 Visibility: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_033_0::thread direction=BT statements=true
package Page_requirements_n_033_0 {
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
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::restrictedVisibilityCollisionAssessment;
        expose BlueDogRequirements::restrictedVisibilityEntry;
        expose BlueDogRequirements::restrictedVisibilityEvidence;
        expose BlueDogRequirements::visibilityNavigationCapability;
        expose BlueDogRequirements::visibilityTrafficCapability;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityCollisionAssessment { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEntry { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEvidence { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::visibilityNavigationCapability { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::visibilityTrafficCapability { x = 0; y = 2180; }
    }
}
```
