# C-006 EmergencyIntervention relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the emergency-intervention rule and recovery relationships from the authoritative model and informs how a challenge attempt ends and recovery takes precedence. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md)

This obligation also motivates design choices. A rationale-bearing dependency does not assert logical requirement derivation; follow the source model for those decisions.

```sysml-view Page_c_006::obligation direction=BT statements=true
package Page_c_006 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view obligation : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::emergencyIntervention;
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 0; }
    }
}
```
