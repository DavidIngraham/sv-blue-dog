# N-054 WeedSnagShedding relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

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
