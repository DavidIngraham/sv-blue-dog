# Q-001 CruisePerformance relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes cruise-performance obligations and their derived progress criteria from the authoritative model and informs required sailing polars, coupled sizing and eventual sailing measurements. The relationships define the design and evidence obligations; they do not record a completed test.

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
