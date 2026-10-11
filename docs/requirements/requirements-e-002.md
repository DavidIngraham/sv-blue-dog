# E-002 NavigationAndControl relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_002_0::navigationAndControl1 direction=BT statements=true
package Page_requirements_requirements_e_002_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view navigationAndControl1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::guidanceUpdateCadence;
        expose BlueDogRequirements::sailCommandCadence;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::guidanceUpdateCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::sailCommandCadence { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_002_1::navigationAndControl2 direction=BT statements=true
package Page_requirements_requirements_e_002_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view navigationAndControl2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::steeringCommandCadence;
        expose BlueDogRequirements::positionAccuracy;
        expose BlueDogRequirements::headingAccuracy;
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::steeringCommandCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::positionAccuracy { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::headingAccuracy { x = 600; y = 200; }
    }
}
```
