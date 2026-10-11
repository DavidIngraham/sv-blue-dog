# E-007 MissionEvidence relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_007_0::missionEvidence1 direction=BT statements=true
package Page_requirements_requirements_e_007_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view missionEvidence1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::logRetention;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::logRetention { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_007_1::missionEvidence2 direction=BT statements=true
package Page_requirements_requirements_e_007_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view missionEvidence2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::logTimestampAccuracy;
        expose BlueDogRequirements::invalidTimestampMarking;
        expose BlueDogRequirements::logGapIndication;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::logTimestampAccuracy { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::invalidTimestampMarking { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logGapIndication { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_007_2::missionEvidence3 direction=BT statements=true
package Page_requirements_requirements_e_007_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view missionEvidence3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::logInterruptionDurability;
        expose BlueDogRequirements::reconnectLogPreservation;
        expose BlueDogRequirements::qualificationPersistence;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_007_3::missionEvidence4 direction=BT statements=true
package Page_requirements_requirements_e_007_3 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view missionEvidence4 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::unknownQualificationFallback;
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 0; y = 200; }
    }
}
```
