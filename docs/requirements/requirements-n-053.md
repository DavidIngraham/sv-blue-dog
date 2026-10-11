# N-053 SubmergedWeedPassage relationships

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
