# N-056 RecoveryPropulsorWeeds relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes recovery-propulsor weed obligations and recovery relationships from the authoritative model and informs drive installation, protection and comparative installed weed tests. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_056_0::recoveryPropulsorWeeds1 direction=BT statements=true
package Page_requirements_requirements_n_056_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view recoveryPropulsorWeeds1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::poweredWeedSpeed;
        expose BlueDogRequirements::poweredWeedCurrent;
        expose BlueDogRequirements::poweredWeedTemperature;
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::poweredWeedSpeed { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::poweredWeedCurrent { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::poweredWeedTemperature { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_056_1::recoveryPropulsorWeeds2 direction=BT statements=true
package Page_requirements_requirements_n_056_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view recoveryPropulsorWeeds2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::lockedPropulsorShutdown;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::lockedPropulsorShutdown { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
    }
}
```
