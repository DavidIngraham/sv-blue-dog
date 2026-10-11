# M-001 RoundTrip relationships

Reference view for [mission definition and SRR](../development-plan.md#mission-definition). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_m_001::obligation direction=BT statements=true
package Page_m_001 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::roundTrip;
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 0; }
    }
}
```
