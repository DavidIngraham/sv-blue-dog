# H-001 HawaiiVoyage relationships

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_h_001::obligation direction=BT statements=true
package Page_h_001 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
    }
}
```
