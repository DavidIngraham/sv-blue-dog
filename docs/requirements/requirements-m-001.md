# M-001 RoundTrip relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the vehicle round-trip obligation and challenge relationships from the authoritative model and informs ordered route behavior and verification of a completed journey. The relationships define the design and evidence obligations; they do not record a completed test.

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
