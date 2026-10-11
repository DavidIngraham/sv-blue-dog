# C-000 TransGorgeChallenge relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_c_000_0::transGorgeChallenge1 direction=BT statements=true
package Page_requirements_requirements_c_000_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view transGorgeChallenge1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 300; y = 200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_c_000_1::transGorgeChallenge2 direction=BT statements=true
package Page_requirements_requirements_c_000_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view transGorgeChallenge2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::emergencyIntervention;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 200; }
        metadata Layout about GorgeChallenge::liveObservation { x = 300; y = 200; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 600; y = 200; }
    }
}
```
