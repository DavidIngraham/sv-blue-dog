# C-003 UnassistedAttempt relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the unassisted-attempt rule and autonomy relationships from the authoritative model and informs the boundary between autonomous control, observation and operator intervention. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_c_003::obligation direction=BT statements=true
package Page_c_003 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 0; }
    }
}
```
