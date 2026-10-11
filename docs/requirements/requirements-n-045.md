# N-045 WetElectricalIntegrity relationships

This focused view supports [detailed design and build readiness](../development-plan.md#detailed-design). It takes wet-electrical-integrity obligations and their derived criteria from the authoritative model and informs enclosures, connections, protection and electrical exposure tests. The relationships define the design and evidence obligations; they do not record a completed test.

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
