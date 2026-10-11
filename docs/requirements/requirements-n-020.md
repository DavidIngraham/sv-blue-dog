# N-020 OceanEnvironment relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_020_0::oceanEnvironment1 direction=BT statements=true
package Page_requirements_requirements_n_020_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view oceanEnvironment1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanWind;
        expose BlueDogRequirements::oceanWaves;
        expose BlueDogRequirements::oceanCurrent;
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::oceanWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::oceanCurrent { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_020_1::oceanEnvironment2 direction=BT statements=true
package Page_requirements_requirements_n_020_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view oceanEnvironment2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanSurvivalWind;
        expose BlueDogRequirements::oceanSurvivalWaves;
        expose BlueDogRequirements::saltwaterExposure;
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWind { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWaves { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 600; y = 200; }
    }
}
```
