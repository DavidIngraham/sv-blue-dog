# C-005 LiveObservation relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the live-observation obligation and communications relationships from the authoritative model and informs shore monitoring and evidence collection without dependence on operator control. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_c_005_0::liveObservation1 direction=BT statements=true
package Page_requirements_requirements_c_005_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view liveObservation1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::liveObservation;
        expose BlueDogRequirements::communications;
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 0; y = 200; }
    }
}
```
