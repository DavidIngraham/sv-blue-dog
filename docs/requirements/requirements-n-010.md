# N-010 GorgeEnvironment relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_010_0::gorgeEnvironment1 direction=BT statements=true
package Page_requirements_requirements_n_010_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view gorgeEnvironment1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeWind;
        expose BlueDogRequirements::gorgeWaves;
        expose BlueDogRequirements::gorgeCurrent;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeCurrent { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_010_1::gorgeEnvironment2 direction=BT statements=true
package Page_requirements_requirements_n_010_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view gorgeEnvironment2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeSurvivalWind;
        expose BlueDogRequirements::gorgeSurvivalWaves;
        expose BlueDogRequirements::freshwaterExposure;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_010_2::gorgeEnvironment3 direction=BT statements=true
package Page_requirements_requirements_n_010_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view gorgeEnvironment3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedSnagShedding;
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 300; y = 200; }
    }
}
```
