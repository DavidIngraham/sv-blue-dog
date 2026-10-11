# E-005 Communications relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes communications obligations and monitoring relationships from the authoritative model and informs link-loss behavior, telemetry architecture and representative communication scenarios. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_005_0::communications1 direction=BT statements=true
package Page_requirements_requirements_e_005_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view communications1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        expose BlueDogRequirements::outageAutonomy;
        expose BlueDogRequirements::reconnectCurrentRecord;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::outageAutonomy { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::reconnectCurrentRecord { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_005_1::communications2 direction=BT statements=true
package Page_requirements_requirements_e_005_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view communications2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::backlogOrdering;
        expose BlueDogRequirements::backlogCurrentPriority;
        expose BlueDogRequirements::logRetention;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::backlogOrdering { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::backlogCurrentPriority { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::logRetention { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_005_2::communications3 direction=BT statements=true
package Page_requirements_requirements_e_005_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view communications3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::reconnectLogPreservation;
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 0; y = 200; }
    }
}
```
