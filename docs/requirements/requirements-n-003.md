# N-003 StabilityAndFouling relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes stability and fouling obligations and their derived requirements from the authoritative model and informs recovery, appendage and weed-tolerance concepts and representative failure scenarios. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_003_0::stabilityAndFouling1 direction=BT statements=true
package Page_requirements_requirements_n_003_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view stabilityAndFouling1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::submergedWeedPassage;
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_003_1::stabilityAndFouling2 direction=BT statements=true
package Page_requirements_requirements_n_003_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view stabilityAndFouling2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::weedSnagShedding;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 600; y = 200; }
    }
}
```
