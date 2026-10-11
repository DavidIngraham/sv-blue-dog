# E-200 SustainedEnergyFeasibility relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_200_0::sustainedEnergyFeasibility1 direction=BT statements=true
package Page_requirements_requirements_e_200_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view sustainedEnergyFeasibility1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::repeatableCycleBalance;
        expose BlueDogRequirements::peakSupplyCapability;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::repeatableCycleBalance { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_200_1::sustainedEnergyFeasibility2 direction=BT statements=true
package Page_requirements_requirements_e_200_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view sustainedEnergyFeasibility2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::energyEvidenceReadiness;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 0; y = 200; }
    }
}
```
