# E-001 EnergyAwareness relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes energy-awareness obligations and their derived checks from the authoritative model and informs energy sensing, estimation and the control decisions driven by available energy. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_001_0::energyAwareness1 direction=BT statements=true
package Page_requirements_requirements_e_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view energyAwareness1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::energyEstimateCadence;
        expose BlueDogRequirements::reserveEstimateCadence;
        expose BlueDogRequirements::energyEstimateAccuracy;
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEstimateCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::reserveEstimateCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::energyEstimateAccuracy { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_001_1::energyAwareness2 direction=BT statements=true
package Page_requirements_requirements_e_001_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view energyAwareness2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::conservativeEnergyEstimate;
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::conservativeEnergyEstimate { x = 0; y = 200; }
    }
}
```
