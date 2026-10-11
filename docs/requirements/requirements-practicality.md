# Manufacturing, handling and serviceability

One-person handling and a 250 mm cubic printer are owner-imposed project constraints. They shape the build and maintenance approach alongside the mission goals.

[Requirements overview](../requirements.md) · [Modeling method](../methods/modeling.md)

Arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision, and **dependency** records a design basis. Each view retains its upstream context; statements are rendered from the model.

- [Transport and manufacture](#transport-and-manufacture)
- [Serviceability](#serviceability)

## Transport and manufacture

```sysml-view Page_practicality_23::thread direction=BT statements=true
package Page_practicality_23 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::liftMass;
        expose BlueDogRequirements::packDuration;
        expose BlueDogRequirements::setupDuration;
        expose BlueDogRequirements::soloLaunch;
        expose BlueDogRequirements::soloRetrieval;
        expose BlueDogRequirements::soloTransport;
        expose BlueDogRequirements::transportability;
        metadata Layout about BlueDogRequirements::liftMass { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::packDuration { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::setupDuration { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::soloLaunch { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::soloRetrieval { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::soloTransport { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::transportability { x = 640; y = 400; }
    }
}
```


## Serviceability

```sysml-view Page_practicality_24::thread direction=BT statements=true
package Page_practicality_24 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::nondestructiveService;
        expose BlueDogRequirements::postServiceActuation;
        expose BlueDogRequirements::postServiceSealing;
        expose BlueDogRequirements::replacementDuration;
        expose BlueDogRequirements::serviceability;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::nondestructiveService { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::postServiceActuation { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::postServiceSealing { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::replacementDuration { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::serviceability { x = 320; y = 400; }
    }
}
```
