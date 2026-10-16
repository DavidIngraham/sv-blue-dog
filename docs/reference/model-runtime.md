# Running the model calculations

I use a pinned development revision of OpenSysML for the model engine, Python client and agent MCP server. Native analysis calls return typed values. The simulator executes the model's supervisory actions during the voyage and its outcome calculation when classifying the result. The numerical optimizer remains in SciPy, while the equations and acceptance criteria stay in SysML.

The same native engine supplies document queries and renders the scoped views in these articles. The publishing code handles narrative pages, navigation, interactive plots and the existing blog import. The numerical batch adapter remains useful for repeated compiled evaluations; it is a specialized bridge, rather than a second modeling framework.

For repeatable model analyses, I can save a standalone model snapshot with OpenSysML's native `AnalysisRecords`. Each record identifies its case, execution time, tool and outputs. The source models remain unchanged. For example:

```sh
uv run python -m tools.boat_analysis.cli record \
  --case BlueDogEnvironmentReview::FetchSensitivity \
  --case BlueDogEncounterReview::Acquisition \
  --output build/analysis/review.sysml
```

The saved model can be reopened with the same engine and queried through its Python client or MCP server. These records supplement the immutable archives for external simulations and optimizer campaigns; a recorded execution does not imply that a vessel requirement has been physically verified.

SysML owns the equations. Python assembles geometry, chooses operating cases and coordinates the optimizer. All native calculations use the reusable library’s [execution backend](../../packages/sysml-python/sysml_python/backends/native.py). Mass, operating performance, structural margins, passage feasibility, route screening, surface/wave helpers, recovery segments, hull resistance and hydrostatics have declarative exports. Preparation reads argument order, Real types, dimensions and named output tuples from OpenSysML's API element export. Application wiring supplies friendly argument aliases and selects model-exported defaults; the generated interface supplies vector widths and output labels.

Mass, operating performance, structural margins, passage feasibility and route screening use declarative exports in [pyproject.toml](../../pyproject.toml). The [reusable SysML/Python library](../../packages/sysml-python/README.md) discovers their vector dimensions, delegates input-record generation to OpenSysML, evaluates model-owned defaults and compiles declared input checks. It still generates calculation-result wrappers for named return tuples. Surface and wave providers assemble external geometry and quadrature around generated calculations; the shared backend compiles those calculations. Named model results can be copied to arrays for NumPy operations. Geometry and interpreter reference experiments remain project-owned in the [reference preparation](../../tools/boat_analysis/model/preparation.py). Hydrostatic meshes use the same explicit batch API; the project sums the returned tetrahedron moments. Generated code and manifests remain build artifacts; fingerprints cover model and runtime sources.

OpenSysML generates frozen, slotted dataclass snapshots from `MarineDesign` for operating state, aerodynamic coefficients, hydrostatic inputs, appendage loads, mass properties and passage conditions, alongside `Design` and `Parameters`. These input records expose named fields and `to_mapping()`; NumPy conversion uses `as_array(record)` and `from_array(RecordType, values)` from `sysml_python.records`. The model declares the numerical field order; the boundary packs by field name, including for batches. Mass dictionaries are also packed by name, so insertion order cannot alter the physics. The surface-wind provider uses the same packing contract. Optimizer coordinates, mesh geometry and low-level numerical arrays remain arrays; these records describe quantities exchanged between domain calculations.

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

Wing-strip load integration uses this path. Independent operating-condition sweeps can use it too. A nonlinear solver's next trial still depends on the previous result, and a mission trajectory still advances chronologically; batching does not remove those dependencies. Parallel studies can use separate worker processes, each with its own native state. The runtime itself does not create workers. Solves and mission operations use an execution session: model and generated-source fingerprints are checked before the first calculation and before the operation returns. Nested calculations share the snapshot, while numerical input checks still run on each call. Source edits invalidate the operation at exit. This avoids checking every source file for every wind strip or recovery segment.

Adding a supported calculation to the declarative library requires its SysML definition and an export declaration. It does not require a handwritten adapter or preparation function. The contract reader supports Real scalars, fixed vectors, and unbounded vectors whose size comes from a model-exported default. Unsupported schemas fail preparation. Physical preconditions are explicitly connected to their calculation; the generator does not infer engineering meaning. Hydrostatics uses the shared native batch loop, with mesh assembly and reduction in project geometry code. Resistance-domain screening is a project-owned policy over generated, named model results; it contains no compiler or ABI setup.


[Modeling method](../methods/modeling.md) · [Contributor guide](authoring.md)

## Mission actions and records

The [mission supervisor](../../models/vehicle/mission-logic.sysml) executes through OpenSysML's native action API. `HandleEvent` determines the response to an observation or intervention. `SupervisoryCycle` determines sailing permission, operating mode, abort latching and whether an abort alert is attempted or queued. `RecoveryAuthority` permits recovery after primary steering or power loss only when an explicitly independent, powered path is supplied. `FallbackPolicy` decides whether the available, permitted recovery path can be attempted or the vessel must continue drifting. Dependencies connect these actions to the normal-sailing, traffic-encounter and abort/recovery scenarios; the supervisor is allocated to the onboard mission manager.

Python supplies observations, computes chart and traffic geometry, ranks feasible headings and integrates motion and energy. It dispatches the action outputs to those mechanisms. The supervisor's traffic mode identifies a predicted encounter; avoidance geometry and maneuver selection remain conceptual Python calculations. This is a partial executable logical architecture, not a complete autopilot or a verified sensing system.

The capsize path requires explicit observations: safety functions remain available
while inverted, then unassisted righting restores upright operation. Between
those observations the simulated boat drifts with the current, consumes energy
and remains exposed to chart and traffic hazards. It cannot sail, score gate
crossings or collect solar energy. Missing safety evidence triggers abort. This
tests the qualification policy; it does not predict righting dynamics or supply
evidence that the physical boat can recover.

Each result includes `logic_trace`, with the action name, simulation time, input facts and output decisions for events and changed supervisory decisions. The abort latch and memoized pure action results are scoped to one simulation. Execution sessions check model provenance, and campaign records include the source hashes. These records support explaining a simulated decision; they do not establish physical capability.


## Reproducing mission campaigns

Run the original conceptual campaign with `uv run python -m tools.boat_analysis.mission.campaign --count 32`, or add `--candidate build/analysis/sizing-continuation.json` for a freshly checked sizing result. It records the model inputs, source hashes, seeds, generated traffic counts, gate events and chronological histories. The numerical horizon can be extended without turning incomplete observations into failures.

Forecast-service loss and forecast invalidity are separate scenario events. A service outage alone preserves the qualifying attempt; a forecast declared no longer applicable triggers autonomous recovery. A manually supplied weather update disqualifies the attempt. These cases exercise mission policy; they do not yet validate a forecast-applicability estimator or an operational weather-service integration.


## Reproducing the IC-01 integration

Prepare the pinned model/runtime inputs, then run the allocated sizing and mission phases:

```sh
uv run python -m tools.boat_analysis.cli prepare
uv run python -m tools.boat_analysis.mission.integrated --phase all
```

The sizing phase supplies a freshly evaluated candidate to the mission phase. Records retain model and driver hashes, trajectories, both energy accounts and acceptance facts. An explicitly supplied warm start can accelerate the solve; it is reevaluated before becoming acceptance evidence.

For installed sensing inputs, the [measurement format and importer](sensing-measurements.md) records the pipeline identity, synchronized observations and power, source hashes and any base electronics load replaced by shared compute. Synthetic regression fixtures remain labeled `synthetic-test`; they do not qualify hardware.
