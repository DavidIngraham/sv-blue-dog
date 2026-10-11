# E-003 ResetRecovery relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes reset-recovery obligations and mission continuity needs from the authoritative model and informs restart behavior and software, controller and integrated fault-injection tests. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_003_0::resetRecovery1 direction=BT statements=true
package Page_requirements_requirements_e_003_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view resetRecovery1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::restartDeadline;
        expose BlueDogRequirements::missionStateRestoration;
        expose BlueDogRequirements::gateProgressRestoration;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::restartDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::missionStateRestoration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::gateProgressRestoration { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_003_1::resetRecovery2 direction=BT statements=true
package Page_requirements_requirements_e_003_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view resetRecovery2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::resetRestrictionPreservation;
        expose BlueDogRequirements::qualificationRestoration;
        expose BlueDogRequirements::logInterruptionDurability;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::resetRestrictionPreservation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationRestoration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_003_2::resetRecovery3 direction=BT statements=true
package Page_requirements_requirements_e_003_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view resetRecovery3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::unknownQualificationFallback;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::freshRecoveryCommand;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_003_3::resetRecovery4 direction=BT statements=true
package Page_requirements_requirements_e_003_3 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view resetRecovery4 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
}
```
