# Declarative SysML/Python runtime

This package is being extracted from SV Blue Dog. It is not yet the completed reusable interface. The independent thermal example proves scalar calculation discovery, typed generated results, model-owned defaults, explicit batching and stale-source checks without importing Blue Dog code. Blue Dog now consumes generated mass, operating-performance, structural-margin, passage-feasibility, route, surface/wave and recovery-segment exports instead of handwritten adapters.

```python
from sysml_python import Project
Project("pyproject.toml", executable="/path/to/pinned/sysml").prepare()
from generated import joule_heat
result = joule_heat(current=2, resistance=10)
print(result.power)
```

Exports are declared under `[tool.sysml_python.exports.<name>]` with a `definition` qualified name. Source discovery uses `models` glob patterns. `generated_package` selects the generated Python package. The caller supplies a pinned executable explicitly or through `OPENSYSML_BINARY`; no tool download or search is hidden in execution.

## Current supported slice

Scalar and fixed-vector Real inputs, named scalar or explicit tuple returns (including a one-element vector), Linux/GCC native execution, generated immutable input/output records, scalar and shared/per-case batching, model-evaluated default bindings, separately compiled physical input checks, source/compiler provenance in generated manifests, and rejection of stale sources. Explicit record bindings preserve model field order independently of Python mapping order. Aliases support existing models with abbreviated parameter names; schemas, dimensions and record fields are never repeated in configuration.

The pinned OpenSysML compiler rejects parameter defaults. The backend preserves scalar literal defaults in the generated Python API and compiles a semantic API projection with only those exported parameter defaults removed. The original model remains unchanged; Python supplies every C argument. Nonliteral defaults still require model evaluation and currently fail explicitly. Inline native assertions, nonliteral parameter-default expressions, generalized external bindings and portable manifests still need work. Evaluated defaults can already be bound declaratively to named analysis outputs. Do not use this slice as evidence that the entire project goal is complete.

## Current migration boundary

Mass, operating performance, structural margins, passage feasibility, route screening, surface/wave helpers, recovery segments and hull resistance use generated exports. All native execution shares this package's backend; the project's old schema reader, adapter hierarchy and duplicate native runtime have been removed. Resistance screening remains project-owned engineering policy over generated results. Specialized hydrostatic mesh integration still has preparation and binding code to migrate.

The [package-less uv template](../../examples/thermal/README.md) has application tests and a CI check that installs a built wheel into a fresh environment outside this repository. Portable manifests, complete execution provenance, broader default lowering, and explicit handling of additional record schemas remain unfinished. The model's equations and schemas belong in SysML; geometry, reference experiments and engineering interpretation remain project-owned.

Generated packages contain rebuildable artifacts. Numerical execution is not physical qualification. Project evidence interpretation is intentionally outside this library.

Project-owned numerical providers can call an export's `prepare_inputs(**inputs)` to apply the same named record packing, defaults, shape checks and physical preconditions as scalar execution. It returns a dictionary of arrays keyed by public input name. This is useful when a project assembles forces or geometry outside SysML; the provider remains responsible for its external algorithm and result interpretation.

Generated results expose named fields and `to_mapping()`. Use `as_array()` when a numerical algorithm needs model-ordered values; it returns a copy. Preparing exports discovers return names from the model rather than maintaining Python output-label lists.

## Repeated execution

Use `with execution_session():` (imported from `sysml_python`) around a solve or campaign, or apply `@execution_session()` to its ordinary function. The first calculation validates the prepared model and generated sources; nested calls share that snapshot. The session validates again before returning and raises if the manifest or sources changed. Treat results as accepted only after the session exits successfully. Standalone calls retain per-call freshness checks. A session does not skip input shapes, finite-value checks or model-defined physical checks, and it does not create workers. Do not decorate a generator function: consume its results inside a session instead.
