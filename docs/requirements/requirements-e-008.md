# E-008 NavigationAvailability relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_008_0::navigationAvailability1 direction=BT statements=true
package Page_requirements_requirements_e_008_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view navigationAvailability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::navigationValidEpochs;
        expose BlueDogRequirements::staleNavigationInvalidation;
        expose BlueDogRequirements::navigationDegradedTransition;
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::navigationValidEpochs { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::staleNavigationInvalidation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::navigationDegradedTransition { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_008_1::navigationAvailability2 direction=BT statements=true
package Page_requirements_requirements_e_008_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view navigationAvailability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::staleNavigationUseInhibition;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::staleNavigationUseInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 300; y = 200; }
    }
}
```
