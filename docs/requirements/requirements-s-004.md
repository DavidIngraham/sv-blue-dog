# S-004 NavigationConspicuity relationships

Reference view for [detailed design and build readiness](../development-plan.md#detailed-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_s_004_0::navigationConspicuity1 direction=BT statements=true
package Page_requirements_requirements_s_004_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view navigationConspicuity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::navigationLightPresentation;
        expose BlueDogRequirements::navigationShapePresentation;
        expose BlueDogRequirements::navigationSoundPresentation;
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationLightPresentation { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::navigationShapePresentation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::navigationSoundPresentation { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_s_004_1::navigationConspicuity2 direction=BT statements=true
package Page_requirements_requirements_s_004_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view navigationConspicuity2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationConspicuity;
        expose BlueDogRequirements::signalingModeDeadline;
        expose BlueDogRequirements::signalingFaultRecording;
        expose BlueDogRequirements::signalingFaultReporting;
        metadata Layout about BlueDogRequirements::navigationConspicuity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::signalingModeDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::signalingFaultRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::signalingFaultReporting { x = 600; y = 200; }
    }
}
```
