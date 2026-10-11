# S-003 SafeRecovery relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_s_003_0::safeRecovery1 direction=BT statements=true
package Page_requirements_requirements_s_003_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view safeRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::abortLatchDeadline;
        expose BlueDogRequirements::recoveryTelemetryCadence;
        expose BlueDogRequirements::motorIsolationDeadline;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::abortLatchDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::recoveryTelemetryCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::motorIsolationDeadline { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_s_003_1::safeRecovery2 direction=BT statements=true
package Page_requirements_requirements_s_003_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view safeRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::isolationRestartInhibition;
        expose BlueDogRequirements::manualControlLossShutdown;
        expose BlueDogRequirements::controlLossLocationContinuity;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::isolationRestartInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::manualControlLossShutdown { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::controlLossLocationContinuity { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_s_003_2::safeRecovery3 direction=BT statements=true
package Page_requirements_requirements_s_003_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view safeRecovery3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::periodicLogCadence;
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 600; y = 200; }
    }
}
```
