# H-001 HawaiiVoyage relationships

Reference view for [mission definition and SRR](../development-plan.md#mission-definition). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

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
