# Reading the design through the model

**OOSEM:** Methods · [Maturity assessment](../current-assessment.md)

I want to be able to follow a design decision back to the mission that caused it. This is how I use SysML to keep requirements, rationale, architecture and verification connected in the [current assessment](../current-assessment.md). It starts with mission intent and ends with links that make later design decisions and test results easier to interpret.

I begin with the finite Gorge challenge, then make the vehicle’s obligations precise enough to evaluate. The eventual ocean mission has separate applicability. A requirement statement states the obligation; its conditions identify the qualification context. Rationale explains why an obligation or design choice exists without becoming another acceptance criterion.

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

Read the normative conditions and supporting metadata in the [vehicle requirements](../../models/vehicle/requirements.sysml), [independent challenge](../../models/missions/transgorge.sysml), and [verification plans](../../models/vehicle/verification.sysml). The [design decisions](../../models/vehicle/decisions.sysml) and [source evidence](../../models/vehicle/source-evidence.sysml) preserve the rationale behind the analysis choices.


## Requirements versus design assumptions

A challenge obligation motivates a function; it does not uniquely determine a material modulus, laminate thickness or sensor accuracy. I keep explicit owner constraints, functional acceptance, provisional performance allocations and selected strategies distinct with [requirement-basis metadata](../../models/vehicle/requirement-basis.sysml). A dependency records a selected design basis; a derivation identifies an obligation needed to meet its parent.

The material and geometric constants used in preliminary sizing live in the [structural analysis basis](../../models/analyses/structural-basis.sysml). They let me explore a candidate before measurements exist. Qualification instead checks supported material bounds and applicable load, functional and site limits. Missing evidence cannot produce a passing executable requirement. Lower measured stiffness or strength means revisiting the geometry or reinforcement, not rejecting a material for missing an assumed property.

```sysml-report BlueDogRequirementBasisDocuments::Summary
```

Archived runs retain their original inputs and claims. A passing numerical screen supports a candidate under those assumptions; measured stiffness, strength and operating loads are needed to establish physical compliance.

## Following executable decisions

The [mission supervisor](../mission-simulation.md#executable-supervisory-logic) connects logical scenarios to decisions during a simulated voyage. Its actions govern event responses, sailing permission and abort latching. The resulting trace records the input facts and decisions, so a trajectory can be read alongside the behavior that produced it. Scenario dependencies and the mission-manager allocation identify the architectural responsibility being exercised.

For example, a loss of communications can coexist with continued autonomous sailing, while a safety abort queues its alert and proceeds toward recovery. Regression scenarios check these distinctions, including the persistence of an abort after observations recover. A separate model calculation classifies the observed mission outcome. Behavioral execution and outcome assessment answer different questions, and neither supplies the physical evidence for an installed controller.

The [development spirals](../simulation-spirals.md) place this behavior alongside the growth in vessel and environmental fidelity.

## Running and reading the model

OpenSysML parses and executes the model, supplies document queries and renders
the diagrams in these articles. Python coordinates geometry, external evidence
and the numerical search. The equations and acceptance criteria stay in SysML.

That separation lets me ask the same engineering question from a script, a
modeling tool or an agent. The result still depends on the declared inputs and
on whether the model represents the behavior that matters. A successful software
check establishes implementation consistency; physical evidence establishes
whether the boat behaves as predicted.

The [contributor guide](../reference/authoring.md) explains how to reproduce the
site. The [runtime reference](../reference/model-runtime.md) covers calculation
records, generated interfaces and numerical execution.

## Native OOSEM roles

The architecture uses the pinned [OpenSysML OOSEM library](https://github.com/DavidIngraham/OpenSysML/blob/e002f1668834f9409ee62200c8b89c0f5bf5e309/docs/project/oosem-library.md) for system context, actors, logical responsibilities, hardware, nodes and logical scenarios. This is an OpenSysML method library expressed in SysML, not a separate Blue Dog workflow engine. The [method model](../../models/vehicle/method.sysml) holds package classifications, scenario refinements and allocations; diagrams import that model through native `LogicalScenarioView` definitions.

When developing a function, connect its use case to a logical scenario, allocate its actions to responsibilities, then refine the physical realization and its verification evidence. Typed items describe information crossing action boundaries. Model links identify intended scope; they do not claim that a simulation already implements every linked behavior.

Requirements packages carry OOSEM roles. Individual requirements retain their existing derivation, refinement and owner-constraint semantics. I do not apply a blanket requirement-level classification: the pinned library's direct parent-level derivation checks do not express every same-level decomposition or independent owner constraint in this project. Adding an artificial derivation to silence a method warning would weaken traceability.
