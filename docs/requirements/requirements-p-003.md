# P-003 Serviceability: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

This thread starts with an owner-imposed project constraint. It applies alongside the mission goals.

```sysml-view Page_requirements_p_003_0::thread direction=BT statements=true
package Page_requirements_p_003_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::nondestructiveService;
        expose BlueDogRequirements::postServiceActuation;
        expose BlueDogRequirements::postServiceSealing;
        expose BlueDogRequirements::replacementDuration;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::nondestructiveService { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::postServiceActuation { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::postServiceSealing { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::replacementDuration { x = 960; y = 800; }
    }
}
```
