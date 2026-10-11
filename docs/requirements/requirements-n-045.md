# N-045 WetElectricalIntegrity relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_045_0::wetElectricalIntegrity1 direction=BT statements=true
package Page_requirements_requirements_n_045_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view wetElectricalIntegrity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::wetElectricalIntegrity;
        expose BlueDogRequirements::wetConductorResistance;
        expose BlueDogRequirements::wetInsulationResistance;
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetConductorResistance { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetInsulationResistance { x = 300; y = 200; }
    }
}
```
