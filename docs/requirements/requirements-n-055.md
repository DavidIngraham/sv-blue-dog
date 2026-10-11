# N-055 WeedBlockageResponse relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_055_0::weedBlockageResponse1 direction=BT statements=true
package Page_requirements_requirements_n_055_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view weedBlockageResponse1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedBlockageFault;
        expose BlueDogRequirements::weedBlockageContingency;
        expose BlueDogRequirements::weedBlockageLocation;
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedBlockageFault { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageContingency { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::weedBlockageLocation { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_055_1::weedBlockageResponse2 direction=BT statements=true
package Page_requirements_requirements_n_055_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view weedBlockageResponse2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
}
```
