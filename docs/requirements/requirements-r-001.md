# R-001 RecoveryPropulsion relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes recovery-propulsion obligations and installed recovery needs from the authoritative model and informs air-versus-water propulsor comparisons and the associated bench and water tests. The relationships define the design and evidence obligations; they do not record a completed test.

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
