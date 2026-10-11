# C-102 CommandIntegrity relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_c_102_0::commandIntegrity1 direction=BT statements=true
package Page_requirements_requirements_c_102_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view commandIntegrity1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::unauthenticatedCommandRejection;
        expose BlueDogRequirements::replayCommandRejection;
        expose BlueDogRequirements::expiredCommandRejection;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::unauthenticatedCommandRejection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::replayCommandRejection { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::expiredCommandRejection { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_c_102_1::commandIntegrity2 direction=BT statements=true
package Page_requirements_requirements_c_102_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view commandIntegrity2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::acceptedCommandDeadline;
        expose BlueDogRequirements::onboardAcknowledgmentDeadline;
        expose BlueDogRequirements::acknowledgmentQueueing;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::acceptedCommandDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::onboardAcknowledgmentDeadline { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::acknowledgmentQueueing { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_c_102_2::commandIntegrity3 direction=BT statements=true
package Page_requirements_requirements_c_102_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view commandIntegrity3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::externalControlDisqualification;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::qualificationPersistence;
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::externalControlDisqualification { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
}
```
