# Q-001 CruisePerformance relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_q_001_0::cruisePerformance1 direction=BT statements=true
package Page_requirements_requirements_q_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view cruisePerformance1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::legProgress;
        expose BlueDogRequirements::passageDuration;
        expose BlueDogRequirements::cruiseEvidence;
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::legProgress { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::passageDuration { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::cruiseEvidence { x = 600; y = 200; }
    }
}
```
