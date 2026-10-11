# R-001 RecoveryPropulsion relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_r_001::obligation direction=BT statements=true
package Page_r_001 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::recoveryPropulsion;
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 0; y = 0; }
    }
}
```
