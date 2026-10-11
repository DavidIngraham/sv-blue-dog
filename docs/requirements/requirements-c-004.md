# C-004 SailingPropulsion relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the challenge propulsion rule and motor-related relationships from the authoritative model and informs the separation of qualifying sailing from powered testing and recovery. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_c_004::obligation direction=BT statements=true
package Page_c_004 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::sailingPropulsion;
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 0; }
    }
}
```
