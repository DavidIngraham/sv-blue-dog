# C-101 TelemetryEquipment relationships

Reference view for [detailed design and build readiness](../development-plan.md#detailed-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_c_101_0::telemetryEquipment1 direction=BT statements=true
package Page_requirements_requirements_c_101_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view telemetryEquipment1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryDisplayContent;
        expose BlueDogRequirements::telemetryStaleIndication;
        expose BlueDogRequirements::telemetryIdentityPreservation;
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDisplayContent { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryStaleIndication { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::telemetryIdentityPreservation { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_c_101_1::telemetryEquipment2 direction=BT statements=true
package Page_requirements_requirements_c_101_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view telemetryEquipment2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::telemetryEquipment;
        expose BlueDogRequirements::telemetryDuplicateSuppression;
        metadata Layout about BlueDogRequirements::telemetryEquipment { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDuplicateSuppression { x = 0; y = 200; }
    }
}
```
