# H-001 HawaiiVoyage relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the Hawai‘i objective and related vehicle obligations from the authoritative model and informs ocean mission definition and which Gorge evidence may transfer to later development. The relationships define the design and evidence obligations; they do not record a completed test.

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
