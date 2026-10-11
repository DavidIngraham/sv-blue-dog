# E-009 Wind observation: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_e_009_0::thread direction=BT statements=true
package Page_requirements_e_009_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::windObservation;
        expose BlueDogRequirements::invalidWindUseInhibition;
        expose BlueDogRequirements::windDirectionAccuracy;
        expose BlueDogRequirements::windLossResponse;
        expose BlueDogRequirements::windSampleCadence;
        expose BlueDogRequirements::windSensingEndurance;
        expose BlueDogRequirements::windSpeedAccuracy;
        expose BlueDogRequirements::windStaleInvalidation;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::windObservation { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::invalidWindUseInhibition { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::windDirectionAccuracy { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::windLossResponse { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::windSampleCadence { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::windSensingEndurance { x = 0; y = 2180; }
        metadata Layout about BlueDogRequirements::windSpeedAccuracy { x = 320; y = 2180; }
        metadata Layout about BlueDogRequirements::windStaleInvalidation { x = 640; y = 2180; }
    }
}
```

## Hardware and budgets

The testbed uses the owned Bluetooth Portable Mini; the challenge uses the provisional ULP Wired Mini. [Sensor configurations and rollup](../energy.md#wind-sensing-configurations) connect these requirements to power, installed mass and endurance.
