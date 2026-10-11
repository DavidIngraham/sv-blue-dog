# Reading the design through the model

We begin with the challenge and the eventual ocean mission, then make the vehicle's obligations precise enough to evaluate. A requirement statement states the obligation; its conditions identify the qualification context. Rationale explains why an obligation or design choice exists without becoming another acceptance criterion.

For example, the vehicle's ordered gate crossings refine the challenge's course-completion obligation. The statement and relationship below are read from the model at publication time.

```sysml-view Page_methods_modeling_0::course direction=BT statements=true
package Page_methods_modeling_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view course : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::courseCompletion;
        expose BlueDogRequirements::roundTrip;
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 200; }
    }
}
```

Derivation, refinement and design motivation answer different questions. A derivation identifies an acceptance outcome under its parent's conditions. A refinement makes a referenced obligation more precise. A dependency with rationale records a design motivation without claiming that satisfying it proves the originating requirement.

Architecture satisfaction links express intended allocations. Verification cases identify the evidence needed to establish compliance. An optimizer's converged candidate is analysis evidence under its assumptions; it is not a completed physical verification.

The Markdown source owns this explanation and the scope of each view. The imported SysML owns the requirements, relationships and rationale. The publisher validates temporary view definitions and generates the completed page without editing this source.
