# C-101 Telemetry equipment: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_c_101_0::thread direction=BT statements=true
package Page_requirements_c_101_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryDisplayContent;
        expose BlueDogRequirements::telemetryDuplicateSuppression;
        expose BlueDogRequirements::telemetryIdentityPreservation;
        expose BlueDogRequirements::telemetryStaleIndication;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::telemetryDisplayContent { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::telemetryDuplicateSuppression { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::telemetryIdentityPreservation { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::telemetryStaleIndication { x = 960; y = 2000; }
    }
}
```
