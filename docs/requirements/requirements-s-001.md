# S-001 Traffic safety: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_s_001_0::thread direction=BT statements=true
package Page_requirements_s_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::avoidanceCommandDeadline;
        expose BlueDogRequirements::collisionAssessmentCadence;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::trafficAwarenessFault;
        expose BlueDogRequirements::trafficTracking;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::avoidanceCommandDeadline { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::collisionAssessmentCadence { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::trafficAwarenessFault { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::trafficTracking { x = 0; y = 2180; }
    }
}
```

## Continue the breakdown

- [Navigation conspicuity](requirements-s-004.md)
