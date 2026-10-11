# E-002 Navigation and control: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_e_002_0::thread direction=BT statements=true
package Page_requirements_e_002_0 {
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
        expose BlueDogRequirements::guidanceUpdateCadence;
        expose BlueDogRequirements::headingAccuracy;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::positionAccuracy;
        expose BlueDogRequirements::sailCommandCadence;
        expose BlueDogRequirements::steeringCommandCadence;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::windObservation;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::guidanceUpdateCadence { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::headingAccuracy { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::positionAccuracy { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::sailCommandCadence { x = 0; y = 1780; }
        metadata Layout about BlueDogRequirements::steeringCommandCadence { x = 320; y = 1780; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 640; y = 1780; }
        metadata Layout about BlueDogRequirements::windObservation { x = 960; y = 1780; }
    }
}
```

## Continue the breakdown

- [Navigation availability](requirements-e-008.md)
- [Traffic safety](requirements-s-001.md)
- [Wind observation](requirements-e-009.md)
