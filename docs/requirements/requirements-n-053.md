# N-053 SubmergedWeedPassage relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes submerged-weed-passage obligations and appendage relationships from the authoritative model and informs hull and appendage geometry and representative vegetation trials. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_053_0::submergedWeedPassage1 direction=BT statements=true
package Page_requirements_requirements_n_053_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view submergedWeedPassage1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedPassageSpeed;
        expose BlueDogRequirements::weedPassageSteering;
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedPassageSpeed { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedPassageSteering { x = 300; y = 200; }
    }
}
```
