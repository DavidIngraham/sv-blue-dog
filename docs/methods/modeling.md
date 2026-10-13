# Reading the design through the model

**Design phase:** Appendix · [Development plan](../development-plan.md)

I want to be able to follow a design decision back to the mission that caused it. This is how I use SysML to keep requirements, rationale, architecture and verification connected in the [engineering record](../development-plan.md#engineering-record). It starts with mission intent and ends with links that make later design reviews and test results easier to interpret.

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

Read the normative conditions and supporting metadata in the [vehicle requirements](../../models/vehicle/requirements.sysml), [independent challenge](../../models/missions/transgorge.sysml), and [verification plans](../../models/vehicle/verification.sysml). The [design decisions](../../models/vehicle/decisions.sysml) and [source evidence](../../models/vehicle/source-evidence.sysml) preserve the rationale behind the analysis choices.


## Running the calculations

SysML owns the equations. Python assembles geometry, chooses operating cases and coordinates the optimizer. The generated C calculations run through one [native execution layer](../../tools/boat_analysis/model/native_kernel.py). Each adapter supplies a small `KernelSpec`: generated source, ordered argument names and expected output size. The runtime inspects the generated entry-point signature to identify scalar and vector arguments and the supported output type. Domain adapters retain their physical checks and named outputs.

The runtime caches builds using the generated source, wrapper, compiler identity and flags. Calls sharing a loaded library use the same lock because OpenSysML's generated evaluator owns mutable execution state. Results are copied before that state can be reused. Hydrostatics retains its specialized mesh reduction in C and uses the same build and locking machinery.

Independent cases can run in a native batch. Shared inputs and per-case inputs are explicit; there is no implicit broadcasting:

```python
result = operation.evaluate_batch(
    shared={"design": design, "parameters": parameters,
            "aero": aero, "mass": mass, "hydro": hydro},
    cases={"state": states},  # (number of cases, 9)
    chunk_size=256,
)
# result.values columns follow operation.contract["outputNames"].
```

The C wrapper calls the same generated calculation for each row and copies its output immediately. It processes bounded chunks, preserves case order and reports the original case index on failure. With `errors="collect"`, native failures produce an error message and a NaN row; those rows must never count as feasible results. Malformed inputs and adapter precondition failures reject the batch before execution. A shared vector has shape `(width,)`; a per-case vector has shape `(cases, width)`. Scalar inputs use a scalar or a `(cases,)` array respectively.

Wing-strip load integration now uses this path. Independent operating-condition sweeps can use it too. A nonlinear solver's next trial still depends on the previous result, and a mission trajectory still advances chronologically; batching does not remove those dependencies. Parallel studies can use separate worker processes, each with its own native state. The runtime itself does not create workers.

Adding a calculation requires an adapter specification, not another compiler/ctypes wrapper. Signature inspection checks the generated ABI; it does not automatically discover the model's physical preconditions or qualification meaning.
