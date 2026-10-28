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
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Requirements::roundTrip;
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 0; y = 200; }
    }
}
```

Derivation, refinement and design motivation answer different questions. A requirement derivation asserts that satisfaction of the original requirement implies satisfaction of its derived requirements under the stated conditions; passing the children alone does not prove the parent. A refinement makes a referenced obligation more precise. A dependency with rationale records a design motivation without claiming that satisfying it proves the originating requirement.

Architecture satisfaction links assert that their subject satisfies the referenced requirement. At this stage they record an intended design claim that still needs evidence. Allocations separately map logical responsibilities to candidate equipment. Verification cases identify the evidence needed to establish compliance. An optimizer's converged candidate is analysis evidence under its assumptions; it is not a completed physical verification.

The Markdown source owns this explanation and the scope of each view. The imported SysML owns the requirements, relationships and rationale. The publisher validates temporary view definitions and generates the completed page without editing this source.

Read the normative conditions and supporting metadata in the [vehicle requirements](../../models/blue-dog.sysml), [independent challenge](../../models/blue-dog.sysml), and [verification plans](../../models/blue-dog.sysml). The [design decisions](../../models/blue-dog.sysml) and [source evidence](../../models/blue-dog.sysml) preserve the rationale behind the analysis choices.


## Requirements versus design assumptions

A challenge obligation motivates a function; it does not uniquely determine a material modulus, laminate thickness or sensor accuracy. I keep explicit owner constraints, functional acceptance, provisional performance allocations and selected strategies distinct with [requirement-basis metadata](../../models/blue-dog.sysml). Each numerical allocation has an attached review annotation identifying its source, applicability, owner, needed measurements, margin basis and closure action. An unrecorded value-selection justification remains open; retaining a limit does not accept it. Assessment and release obligations identify the responsible role and work product. The two provisional reliability objectives are explicitly marked as studies, so their numerical comparisons cannot silently become binding mission obligations. A dependency records a selected design basis; a derivation records an implied obligation under explicit conditions.

Engineering decision records use a shared [item definition](../../models/libraries/decision-records.sysml). SysML items can represent identifiable information acted on over time; parts represent systems or components that can perform actions. The decision register includes working policies, baselines, preferences, mixed design-basis statements and unresolved questions. Its record states describe existing content without claiming approval or implementation. Value-allocation and procedure-choice reviews remain metadata on the requirements and procedures they concern. The element choice follows [SysML 2.0 Part 1, §7.10](https://www.omg.org/spec/SysML/2.0/Language/PDF); the record content is project tailoring.

The material and geometric constants used in preliminary sizing live in the [structural analysis basis](../../models/blue-dog.sysml). They let me explore a candidate before measurements exist. Qualification instead checks supported material bounds and applicable load, functional and site limits. Missing evidence cannot produce a passing executable requirement. Lower measured stiffness or strength means revisiting the geometry or reinforcement, not rejecting a material for missing an assumed property.

```sysml-report BlueDogRequirementBasisDocuments::Summary
```

<details>
<summary>Current allocation justification, process responsibilities and closure plans</summary>

```sysml-report BlueDogRequirementBasisDocuments::ClosurePlans
```

</details>

Archived runs retain their original inputs and claims. A passing numerical screen supports a candidate under those assumptions; measured stiffness, strength and operating loads are needed to establish physical compliance.

## Following executable decisions

The [mission supervisor](../mission-simulation.md#executable-supervisory-logic) connects logical scenarios to decisions during a simulated voyage. Its actions govern event responses, sailing permission and abort latching. The resulting trace records the input facts and decisions, so a trajectory can be read alongside the behavior that produced it. Scenario dependencies and the logical-supervision allocation identify the architectural responsibility being exercised.

For example, a loss of communications can coexist with continued autonomous sailing, while a safety abort queues its alert and proceeds toward recovery. Regression scenarios check these distinctions, including the persistence of an abort after observations recover. A separate model calculation classifies the observed mission outcome. Behavioral execution and outcome assessment answer different questions, and neither supplies the physical evidence for an installed controller.

The [simulation studies and their limits](../simulation-studies.md) describe the vessel, environment and behavior assumptions used in each assessment.

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

The architecture uses the pinned [OpenSysML OOSEM library](https://github.com/DavidIngraham/OpenSysML/blob/23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2/docs/project/oosem-library.md) for system context, actors, logical responsibilities, hardware, nodes and logical scenarios. This is an OpenSysML method library expressed in SysML, not a separate Blue Dog workflow engine. The [method model](../../models/blue-dog.sysml) holds package classifications, scenario refinements and allocations; diagrams import that model through native `LogicalScenarioView` definitions.

I connect each function's use case to a logical scenario, allocate its actions to responsibilities, then describe the candidate physical realization and its verification evidence. Typed items describe information crossing action boundaries. Model links identify intended scope; the executable subset is described separately from behavior awaiting implementation.

Requirements packages carry OOSEM roles. Individual requirements express derivation, refinement and independent owner constraints through their relationships. I classify requirements at package level because the pinned library's direct parent-level derivation checks do not cover every same-level decomposition or independent owner constraint used here.


## Reusing failure-analysis views

The [reliability analysis](../reliability.md#how-avoidance-can-fail) uses library
event and gate types, standard causal connections and review records. A new
failure tree declares its inputs and connections, then exposes the relevant
events in a `FaultTreeView`. A new DFMEA review owns its rows; the reusable
`ReviewRows` query selects those rows by type. Neither needs project-specific
Python diagram or table code.

The [redundant-power example](https://github.com/DavidIngraham/OpenSysML/blob/23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2/examples/fault-tree.sysml)
shows the same definitions applied outside Blue Dog. The
[library guide](https://github.com/DavidIngraham/OpenSysML/blob/23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2/docs/guide/failure-analysis.md)
describes the supported qualitative subset and rendering limits. The reusable
view controls presentation; it does not establish that the causal argument is
complete or that its safeguards work on the boat.
