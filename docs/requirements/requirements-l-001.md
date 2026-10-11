# L-001 MissionReliability relationships

Reference view for [virtual design and PDR](../development-plan.md#virtual-design). Follow the model links below for the obligation, its derivation and planned evidence. A relationship records intent, not a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_l_001_0::missionReliability1 direction=BT statements=true
package Page_requirements_requirements_l_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view missionReliability1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::failureRateBudget;
        expose BlueDogRequirements::reliabilityEvidence;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::failureRateBudget { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::reliabilityEvidence { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_l_001_1::missionReliability2 direction=BT statements=true
package Page_requirements_requirements_l_001_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view missionReliability2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::criticalFailureDisposition;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalFailureDisposition { x = 0; y = 200; }
    }
}
```
