# P-001 Transportability: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

This thread starts with an owner-imposed project constraint. It applies alongside the mission goals.

```sysml-view Page_requirements_p_001_0::thread direction=BT statements=true
package Page_requirements_p_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::transportability;
        expose BlueDogRequirements::liftMass;
        expose BlueDogRequirements::packDuration;
        expose BlueDogRequirements::setupDuration;
        expose BlueDogRequirements::soloLaunch;
        expose BlueDogRequirements::soloRetrieval;
        expose BlueDogRequirements::soloTransport;
        metadata Layout about BlueDogRequirements::transportability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::liftMass { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::packDuration { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::setupDuration { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::soloLaunch { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::soloRetrieval { x = 0; y = 580; }
        metadata Layout about BlueDogRequirements::soloTransport { x = 320; y = 580; }
    }
}
```
