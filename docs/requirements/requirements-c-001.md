# C-001 CourseCompletion relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the challenge course and its vehicle-level refinement from the authoritative model and informs route completion criteria, navigation behavior and mission evidence. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_c_001_0::courseCompletion1 direction=BT statements=true
package Page_requirements_requirements_c_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view courseCompletion1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::courseCompletion;
        expose BlueDogRequirements::roundTrip;
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 200; }
    }
}
```
