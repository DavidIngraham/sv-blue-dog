# C-006 EmergencyIntervention relationships

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
