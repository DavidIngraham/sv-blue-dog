# E-004 LowEnergyRecovery relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_004_0::lowEnergyRecovery1 direction=BT statements=true
package Page_requirements_requirements_e_004_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view lowEnergyRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::lowEnergyEntry;
        expose BlueDogRequirements::lowEnergyPayloadInhibition;
        expose BlueDogRequirements::lowEnergyNavigationContinuity;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyEntry { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyPayloadInhibition { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyNavigationContinuity { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_004_1::lowEnergyRecovery2 direction=BT statements=true
package Page_requirements_requirements_e_004_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view lowEnergyRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::lowEnergyCollisionContinuity;
        expose BlueDogRequirements::lowEnergyExit;
        expose BlueDogRequirements::payloadRestartPermission;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyCollisionContinuity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::lowEnergyExit { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::payloadRestartPermission { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_004_2::lowEnergyRecovery3 direction=BT statements=true
package Page_requirements_requirements_e_004_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view lowEnergyRecovery3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_004_3::lowEnergyRecovery4 direction=BT statements=true
package Page_requirements_requirements_e_004_3 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view lowEnergyRecovery4 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
}
```
