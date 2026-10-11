# E-006 IngressResponse relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes ingress-response obligations and health-management relationships from the authoritative model and informs leak detection, autonomous response and controlled fault testing. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_e_006_0::ingressResponse1 direction=BT statements=true
package Page_requirements_requirements_e_006_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view ingressResponse1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::ingressDetection;
        expose BlueDogRequirements::ingressRecoveryRequest;
        expose BlueDogRequirements::ingressFlotation;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::ingressDetection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::ingressRecoveryRequest { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::ingressFlotation { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_006_1::ingressResponse2 direction=BT statements=true
package Page_requirements_requirements_e_006_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view ingressResponse2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::ingressElectronicsProtection;
        expose BlueDogRequirements::ingressPositionContinuity;
        expose BlueDogRequirements::ingressEventDeadline;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::ingressElectronicsProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::ingressPositionContinuity { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::ingressEventDeadline { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_e_006_2::ingressResponse3 direction=BT statements=true
package Page_requirements_requirements_e_006_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view ingressResponse3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 300; y = 200; }
    }
}
```
