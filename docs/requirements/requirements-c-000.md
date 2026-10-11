# C-000 Trans gorge challenge: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_c_000_0::thread direction=BT statements=true
package Page_requirements_c_000_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 580; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 580; }
    }
}
```

## Continue the breakdown

- [Course completion](requirements-c-001.md)
- [Emergency intervention](requirements-c-006.md)
- [Live observation](requirements-c-005.md)
- [Repeated operation](requirements-c-002.md)
- [Sailing propulsion](requirements-c-004.md)
- [Unassisted attempt](requirements-c-003.md)
