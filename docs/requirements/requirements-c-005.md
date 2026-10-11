# C-005 LiveObservation relationships

Reference view for [mission definition and SRR](../development-plan.md#mission-definition). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

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
