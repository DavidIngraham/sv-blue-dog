# Declarative SysML/Python runtime

This package is being extracted from SV Blue Dog. It is not yet the completed reusable interface. The independent thermal example proves scalar calculation discovery, typed generated results, model-owned defaults, explicit batching and stale-source checks without importing Blue Dog code. Blue Dog now consumes generated mass, operating-performance, structural-margin, passage-feasibility, route, surface/wave, recovery-segment, resistance and hydrostatic exports instead of handwritten adapters.

```python
from sysml_python import Project
Project("pyproject.toml", executable="/path/to/pinned/sysml").prepare()
from generated import joule_heat
result = joule_heat(current=2, resistance=10)
print(result.power)
```

Exports are declared under `[tool.sysml_python.exports.<name>]` with a `definition` qualified name. Source discovery uses `models` glob patterns. `generated_package` selects the generated Python package. The caller supplies a pinned executable explicitly or through `OPENSYSML_BINARY`; no tool download or search is hidden in execution.

## Current supported slice

Scalar and fixed-vector Real inputs, named scalar or explicit tuple returns (including a one-element vector), Linux/GCC native execution, generated immutable input/output records, scalar and shared/per-case batching, model-evaluated default bindings, separately compiled physical input checks, source/compiler provenance in portable generated manifests, and rejection of stale sources. Explicit record bindings preserve model field order independently of Python mapping order. Aliases support existing models with abbreviated parameter names; schemas, dimensions and record fields are never repeated in configuration.

The pinned OpenSysML compiler rejects parameter defaults. The backend preserves scalar literal defaults in the generated Python API and compiles a semantic API projection with only those exported parameter defaults removed. The original model remains unchanged; Python supplies every C argument. Nonliteral defaults still require model evaluation and currently fail explicitly. Inline native assertions, nonliteral parameter-default expressions and generalized external bindings are not supported. Evaluated defaults can already be bound declaratively to named analysis outputs. Do not use this slice as evidence that the entire project goal is complete.

## Current migration boundary

Mass, operating performance, structural margins, passage feasibility, route screening, surface/wave helpers, recovery segments, hull resistance and hydrostatics use generated exports. All native execution shares this package's backend; the project's old schema reader, adapter hierarchy and duplicate native runtime have been removed. Resistance screening remains project-owned engineering policy over generated results. Hydrostatic mesh integration uses generated batch calls and a project-owned sum; its custom C shim is removed. Interpreter reference experiments remain project-owned and do not compile kernels.

The [package-less uv template](../../examples/thermal/README.md) has application tests and a CI check that installs a built wheel into a fresh environment outside this repository. Prepared manifests use project-relative source paths and verify the configuration, model-file set, generated sources and runtime implementation. Record inheritance and non-Real record fields are explicitly unsupported; field names that collide with the runtime API are rejected. The model's equations and schemas belong in SysML; geometry, reference experiments and engineering interpretation remain project-owned.

Generated packages contain rebuildable artifacts. Numerical execution is not physical qualification. Project evidence interpretation is intentionally outside this library.

Project-owned numerical providers can call an export's `prepare_inputs(**inputs)` to apply the same named record packing, defaults, shape checks and physical preconditions as scalar execution. It returns a dictionary of arrays keyed by public input name. This is useful when a project assembles forces or geometry outside SysML; the provider remains responsible for its external algorithm and result interpretation.

Generated results expose named fields and `to_mapping()`. Use `as_array()` when a numerical algorithm needs model-ordered values; it returns a copy. Preparing exports discovers return names from the model rather than maintaining Python output-label lists.

## Repeated execution

Use `with execution_session():` (imported from `sysml_python`) around a solve or campaign, or apply `@execution_session()` to its ordinary function. The first calculation validates the prepared model and generated sources; nested calls share that snapshot. The session validates again before returning and raises if the manifest or sources changed. Treat results as accepted only after the session exits successfully. Standalone calls retain per-call freshness checks. A session does not skip input shapes, finite-value checks or model-defined physical checks, and it does not create workers. Do not decorate a generator function: consume its results inside a session instead.


## Execution evidence

```python
from sysml_python import execution_session
with execution_session() as run:
    result = joule_heat(current=2, resistance=10)
evidence = run.to_mapping()
assert evidence["status"] == "complete"
```

A report records successful scalar calls, batch row counts (including collected
failures), input-validation-only calls, and the exact prepared manifest, model,
configuration, runtime implementation, SysML compiler and loaded native build.
A failed or stale session has status `failed`; its outputs are not accepted
execution evidence. `joule_heat.provenance()` identifies the currently loaded
calculation without claiming that an analysis was run. Reports describe software
execution, not physical validation, and do not store application inputs/results.
Projects should archive those alongside the report when they need full replay.

Generated calculations are callable objects with typed keyword arguments, typed
shared/per-case dictionaries, and a typed batch result. Records validate finite
Real values at construction. Model-defined physical checks are still applied at
execution. Moving a prepared project with its model/configuration/generated files
preserves its identity; the runtime builds a native library for the current host.
Changing configuration, adding a matched model file, or upgrading the runtime
requires preparation again.
