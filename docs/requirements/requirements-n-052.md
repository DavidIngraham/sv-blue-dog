# N-052 CapsizeControlRecovery relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_052_0::capsizeControlRecovery1 direction=BT statements=true
package Page_requirements_requirements_n_052_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view capsizeControlRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::controlRecoveryDeadline;
        expose BlueDogRequirements::capsizeGateProgressRetention;
        expose BlueDogRequirements::capsizeQualificationRetention;
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::controlRecoveryDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeGateProgressRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeQualificationRetention { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_052_1::capsizeControlRecovery2 direction=BT statements=true
package Page_requirements_requirements_n_052_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view capsizeControlRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::capsizeRestrictionRetention;
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeRestrictionRetention { x = 0; y = 200; }
    }
}
```
