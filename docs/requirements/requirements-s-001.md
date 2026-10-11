# S-001 TrafficSafety relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes traffic-safety obligations and traffic-context relationships from the authoritative model and informs encounter scenarios, sensing assumptions and collision-avoidance behavior. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_s_001_0::trafficSafety1 direction=BT statements=true
package Page_requirements_requirements_s_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view trafficSafety1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::trafficTracking;
        expose BlueDogRequirements::collisionAssessmentCadence;
        expose BlueDogRequirements::avoidanceCommandDeadline;
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::trafficTracking { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::collisionAssessmentCadence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::avoidanceCommandDeadline { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_s_001_1::trafficSafety2 direction=BT statements=true
package Page_requirements_requirements_s_001_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view trafficSafety2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::trafficSafety;
        expose BlueDogRequirements::trafficAwarenessFault;
        metadata Layout about BlueDogRequirements::trafficSafety { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::trafficAwarenessFault { x = 0; y = 200; }
    }
}
```
