# N-033 Visibility relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes visibility obligations and their scenario relationships from the authoritative model and informs the operating context for sensing, traffic interactions and later field trials. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_033_0::visibility1 direction=BT statements=true
package Page_requirements_requirements_n_033_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view visibility1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::visibilityNavigationCapability;
        expose BlueDogRequirements::visibilityTrafficCapability;
        expose BlueDogRequirements::restrictedVisibilityEntry;
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::visibilityNavigationCapability { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::visibilityTrafficCapability { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEntry { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_033_1::visibility2 direction=BT statements=true
package Page_requirements_requirements_n_033_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view visibility2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::restrictedVisibilityEvidence;
        expose BlueDogRequirements::restrictedVisibilityCollisionAssessment;
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEvidence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityCollisionAssessment { x = 300; y = 200; }
    }
}
```
