# N-051 SelfRighting relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes self-righting obligations and their derived recovery criteria from the authoritative model and informs ballast, rig buoyancy and capsize analysis before controlled physical recovery trials. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_051_0::selfRighting1 direction=BT statements=true
package Page_requirements_requirements_n_051_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view selfRighting1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::rightingDeadline;
        expose BlueDogRequirements::capsizeRigRetention;
        expose BlueDogRequirements::capsizeBallastRetention;
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::rightingDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeRigRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeBallastRetention { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_051_1::selfRighting2 direction=BT statements=true
package Page_requirements_requirements_n_051_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view selfRighting2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeElectronicsSealing;
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeElectronicsSealing { x = 0; y = 200; }
    }
}
```
