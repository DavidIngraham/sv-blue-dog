# R-002 RecoveryEnergy relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes recovery-energy obligations and recovery-task relationships from the authoritative model and informs battery reserve allocation and the measurements needed to verify usable recovery energy. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_r_002::obligation direction=BT statements=true
package Page_r_002 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::recoveryEnergy;
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 0; y = 0; }
    }
}
```
