# P-003 Serviceability relationships

Reference view for [detailed design and build readiness](../development-plan.md#detailed-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_p_003_0::serviceability1 direction=BT statements=true
package Page_requirements_requirements_p_003_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view serviceability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::replacementDuration;
        expose BlueDogRequirements::nondestructiveService;
        expose BlueDogRequirements::postServiceSealing;
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::replacementDuration { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::nondestructiveService { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::postServiceSealing { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_p_003_1::serviceability2 direction=BT statements=true
package Page_requirements_requirements_p_003_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view serviceability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::postServiceActuation;
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::postServiceActuation { x = 0; y = 200; }
    }
}
```
