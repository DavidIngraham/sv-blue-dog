# Reading the design through the model

**Design phase:** Appendix Ã‚Â· [Development plan](../development-plan.md)

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


## Requirements versus design assumptions

A challenge obligation motivates a function; it does not uniquely determine a material modulus, laminate thickness or sensor accuracy. I keep explicit owner constraints, functional acceptance, provisional performance allocations and selected strategies distinct with [requirement-basis metadata](../../models/vehicle/requirement-basis.sysml). A dependency records a selected design basis; a derivation identifies an obligation needed to meet its parent.

The material and geometric constants used in preliminary sizing live in the [structural analysis basis](../../models/analyses/structural-basis.sysml). They let us explore a candidate before measurements exist. Qualification instead checks supported material bounds and applicable load, functional and site limits. Missing evidence cannot produce a passing executable requirement. Lower measured stiffness or strength means revisiting the geometry or reinforcement, not rejecting a material for missing an assumed property.

```sysml-report BlueDogRequirementBasisDocuments::Summary
```

The numerical screening inputs have not changed in this clarification. Archived runs retain their original revision and claims; their passing screens are not converted into evidence that the current acceptance requirements have been verified. The next sizing refinement should vary the provisional inputs and replace them with evidence-backed values.

## Running the calculations

SysML owns the equations. Python assembles geometry, chooses operating cases and coordinates the optimizer. All native calculations use the reusable library’s [execution backend](../../packages/sysml-python/sysml_python/backends/native.py). Mass, operating performance, structural margins, passage feasibility, route screening, surface/wave helpers, recovery segments, hull resistance and hydrostatics have declarative exports. The old shared adapter layer, duplicate runtime and custom hydrostatic C shim have been removed. Preparation reads argument order, Real types, dimensions and named output tuples from OpenSysML's API element export. Application wiring supplies friendly argument aliases and selects model-exported defaults; adapters no longer repeat vector widths or output labels.

Mass, operating performance, structural margins, passage feasibility and route screening now use declarative exports in [pyproject.toml](../../pyproject.toml). The [reusable SysML/Python library](../../packages/sysml-python/README.md) discovers their vector dimensions, generates named records, evaluates model-owned defaults and compiles declared input checks. Their handwritten adapters are gone. Surface and wave providers assemble external geometry and quadrature around generated calculations; they no longer compile calculations themselves. Named model results can be copied to arrays for NumPy operations. Geometry and interpreter reference experiments remain project-owned in the [reference preparation](../../tools/boat_analysis/model/preparation.py). Hydrostatic meshes use the same explicit batch API; the project sums the returned tetrahedron moments. Generated code and manifests remain build artifacts; fingerprints cover model and runtime sources.

Named Python records for operating state, aerodynamic coefficients, hydrostatic inputs, appendage loads, mass properties and passage conditions are generated from `MarineDesign` alongside `Design` and `Parameters`. The model declares the numerical field order; the boundary packs by field name, including for batches. Mass dictionaries are also packed by name, so insertion order cannot alter the physics. The surface-wind provider uses the same packing contract. Optimizer coordinates, mesh geometry and low-level numerical arrays remain arrays; these records describe quantities exchanged between domain calculations.

Scalar and batch calls share shape, finite-value, default and typed-record handling. Physical mass and operating preconditions are explicit SysML `InputChecks` calculations; the boundary executes them before evaluating the requested calculation. The pinned C generator omits assertions inside calculations, so these checks are compiled and called explicitly. A failed input group produces its model-defined name and, for per-case inputs, its batch index. These numerical preconditions are separate from vessel qualification requirements.

Meson builds all exported calculations and input checks together as separate shared libraries, selecting the host compiler, linker and library filenames. The runtime caches immutable build snapshots using the generated sources, wrappers, Meson recipe, compiler identity and flags. Calls sharing a loaded library use the same lock because OpenSysML's generated evaluator owns mutable execution state. Results are copied before that state can be reused. Hydrostatics uses the generated batch calculations with project-owned mesh reduction.

Independent cases can run in a native batch. Shared inputs and per-case inputs are explicit; there is no implicit broadcasting:

```python
result = operation.batch(
    shared={"design": design, "parameters": parameters,
            "aero": aero, "mass": mass, "hydro": hydro},
    cases={"state": states},  # (number of cases, 9)
    chunk_size=256,
)
# result.values columns follow the fields of generated OperationResult.
```

The C wrapper calls the same generated calculation for each row and copies its output immediately. It processes bounded chunks, preserves case order and reports the original case index on failure. With `errors="collect"`, native failures produce an error message and a NaN row; those rows must never count as feasible results. Malformed inputs and adapter precondition failures reject the batch before execution. A shared vector has shape `(width,)`; a per-case vector has shape `(cases, width)`. Scalar inputs use a scalar or a `(cases,)` array respectively.

Wing-strip load integration now uses this path. Independent operating-condition sweeps can use it too. A nonlinear solver's next trial still depends on the previous result, and a mission trajectory still advances chronologically; batching does not remove those dependencies. Parallel studies can use separate worker processes, each with its own native state. The runtime itself does not create workers. Solves and mission operations use an execution session: model and generated-source fingerprints are checked before the first calculation and before the operation returns. Nested calculations share the snapshot, while numerical input checks still run on each call. Source edits invalidate the operation at exit. This avoids checking every source file for every wind strip or recovery segment.

Adding a supported calculation to the declarative library requires its SysML definition and an export declaration. It does not require a handwritten adapter or preparation function. The contract reader supports Real scalars, fixed vectors, and unbounded vectors whose size comes from a model-exported default. Unsupported schemas fail preparation. Physical preconditions are explicitly connected to their calculation; the generator does not infer engineering meaning. Hydrostatics uses the shared native batch loop, with mesh assembly and reduction in project geometry code. Resistance-domain screening is a project-owned policy over generated, named model results; it contains no compiler or ABI setup.
