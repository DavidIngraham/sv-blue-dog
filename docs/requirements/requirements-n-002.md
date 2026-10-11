# N-002 MarineDurability relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_002_0::marineDurability1 direction=BT statements=true
package Page_requirements_requirements_n_002_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view marineDurability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::freshwaterExposure;
        expose BlueDogRequirements::saltwaterExposure;
        expose BlueDogRequirements::enclosureSealing;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::enclosureSealing { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_002_1::marineDurability2 direction=BT statements=true
package Page_requirements_requirements_n_002_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view marineDurability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetElectricalIntegrity;
        expose BlueDogRequirements::solarHeating;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::solarHeating { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_002_2::marineDurability3 direction=BT statements=true
package Page_requirements_requirements_n_002_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view marineDurability3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::printedMaterialAging;
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::printedMaterialAging { x = 0; y = 200; }
    }
}
```
