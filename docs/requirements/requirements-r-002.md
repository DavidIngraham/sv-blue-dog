# R-002 RecoveryEnergy relationships

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
