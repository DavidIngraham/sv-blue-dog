# C-004 SailingPropulsion relationships

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
