# E-001 EnergyAwareness relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

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
