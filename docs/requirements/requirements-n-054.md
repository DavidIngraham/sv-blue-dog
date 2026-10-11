# N-054 WeedSnagShedding relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes weed-snag-shedding obligations and their derived criteria from the authoritative model and informs appendage details, clearing behavior and repeatable snag tests. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_054_0::weedSnagShedding1 direction=BT statements=true
package Page_requirements_requirements_n_054_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view weedSnagShedding1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::weedSnagShedding;
        expose BlueDogRequirements::weedSnagSpeedRecovery;
        expose BlueDogRequirements::weedSnagSteeringRecovery;
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedSnagSpeedRecovery { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedSnagSteeringRecovery { x = 300; y = 200; }
    }
}
```
