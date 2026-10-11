# C-002 RepeatedOperation relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the repeated-operation objective and endurance relationships from the authoritative model and informs the progression from one qualifying trip to sustained autonomous operation. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_c_002::obligation direction=BT statements=true
package Page_c_002 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::repeatedOperation;
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 0; }
    }
}
```
