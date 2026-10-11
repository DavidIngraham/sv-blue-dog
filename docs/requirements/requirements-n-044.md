# N-044 WetMechanicalIntegrity relationships

This focused view supports [detailed design and build readiness](../development-plan.md#detailed-design). It takes wet-mechanical-integrity obligations and their derived criteria from the authoritative model and informs structural details, joints and representative wet-condition testing. The relationships define the design and evidence obligations; they do not record a completed test.

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
