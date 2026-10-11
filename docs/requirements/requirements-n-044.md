# N-044 WetMechanicalIntegrity relationships

Reference view for [detailed design and build readiness](../development-plan.md#detailed-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_044_0::wetMechanicalIntegrity1 direction=BT statements=true
package Page_requirements_requirements_n_044_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view wetMechanicalIntegrity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetMechanismTravel;
        expose BlueDogRequirements::wetJointIntegrity;
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::wetMechanismTravel { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::wetJointIntegrity { x = 300; y = 200; }
    }
}
```
