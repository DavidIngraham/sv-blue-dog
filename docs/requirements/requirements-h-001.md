# H-001 Hawaii voyage: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

## Breakdown 1

```sysml-view Page_requirements_h_001_0::thread direction=BT statements=true
package Page_requirements_h_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose BlueDogRequirements::oceanEnvironment;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::navigationAndControl;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 580; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 580; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 580; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 1380; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 320; y = 1380; }
    }
}
```

## Breakdown 2

```sysml-view Page_requirements_h_001_1::thread direction=BT statements=true
package Page_requirements_h_001_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose BlueDogRequirements::serviceability;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::regulatoryClassification;
        expose BlueDogRequirements::resetRecovery;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 640; y = 1200; }
    }
}
```

## Continue the breakdown

- [Communications](requirements-e-005.md)
- [Cruise performance](requirements-q-001.md)
- [Environmental envelope](requirements-n-001.md)
- [Mission evidence](requirements-e-007.md)
- [Mission reliability](requirements-l-001.md)
- [Multi day endurance](requirements-m-002.md)
- [Navigation and control](requirements-e-002.md)
- [Ocean environment](requirements-n-020.md)
- [Operating boundary](requirements-s-002.md)
- [Regulatory classification](requirements-s-005.md)
- [Reset recovery](requirements-e-003.md)
- [Serviceability](requirements-p-003.md)
- [Sustained energy feasibility](requirements-e-200.md)
