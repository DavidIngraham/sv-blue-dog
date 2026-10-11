# E-005 Communications: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

## Breakdown 1

```sysml-view Page_requirements_e_005_0::thread direction=BT statements=true
package Page_requirements_e_005_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::backlogCurrentPriority;
        expose BlueDogRequirements::backlogOrdering;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::logRetention;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::outageAutonomy;
        expose BlueDogRequirements::reconnectCurrentRecord;
        expose BlueDogRequirements::reconnectLogPreservation;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 580; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 580; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::backlogCurrentPriority { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::backlogOrdering { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::logRetention { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 1780; }
        metadata Layout about BlueDogRequirements::outageAutonomy { x = 320; y = 1780; }
        metadata Layout about BlueDogRequirements::reconnectCurrentRecord { x = 640; y = 1780; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 960; y = 1780; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 0; y = 2000; }
    }
}
```

## Breakdown 2

```sysml-view Page_requirements_e_005_1::thread direction=BT statements=true
package Page_requirements_e_005_1 {
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
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 1600; }
    }
}
```

## Continue the breakdown

- [Command integrity](requirements-c-102.md)
- [Telemetry equipment](requirements-c-101.md)
