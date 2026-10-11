# P-001 Transportability relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_p_001_0::transportability1 direction=BT statements=true
package Page_requirements_requirements_p_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view transportability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::transportability;
        expose BlueDogRequirements::soloTransport;
        expose BlueDogRequirements::liftMass;
        expose BlueDogRequirements::setupDuration;
        metadata Layout about BlueDogRequirements::transportability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::soloTransport { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::liftMass { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::setupDuration { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_p_001_1::transportability2 direction=BT statements=true
package Page_requirements_requirements_p_001_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view transportability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::transportability;
        expose BlueDogRequirements::packDuration;
        expose BlueDogRequirements::soloLaunch;
        expose BlueDogRequirements::soloRetrieval;
        metadata Layout about BlueDogRequirements::transportability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::packDuration { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::soloLaunch { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::soloRetrieval { x = 600; y = 200; }
    }
}
```
