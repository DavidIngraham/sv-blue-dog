# N-046 SolarHeating relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_046_0::solarHeating1 direction=BT statements=true
package Page_requirements_requirements_n_046_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view solarHeating1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::solarHeating;
        expose BlueDogRequirements::hotSunElectronicsOperation;
        expose BlueDogRequirements::hotSunBatteryTemperature;
        expose BlueDogRequirements::batteryChargeTemperatureInhibition;
        metadata Layout about BlueDogRequirements::solarHeating { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::hotSunElectronicsOperation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::hotSunBatteryTemperature { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::batteryChargeTemperatureInhibition { x = 600; y = 200; }
    }
}
```
