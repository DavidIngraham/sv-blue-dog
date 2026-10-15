# Declarative SysML/Python runtime

This library generates typed Python calculation APIs from explicitly exported SysML definitions. It handles input validation, model defaults, native compilation, scalar and batch execution, freshness checks and execution evidence. Application geometry, scenarios, solvers and engineering interpretation stay in the application. The independent thermal template demonstrates use outside SV Blue Dog.

```python
from sysml_python import Project
Project("pyproject.toml", executable="/path/to/pinned/sysml").prepare()
from generated import joule_heat
result = joule_heat(current=2, resistance=10)
print(result.power)
```

Exports are declared under `[tool.sysml_python.exports.<name>]` with a `definition` qualified name. Source discovery uses `models` glob patterns. `generated_package` selects the generated Python package. The caller supplies a pinned executable explicitly or through `OPENSYSML_BINARY`; no tool download or search is hidden in execution.

## Supported models

Scalar and fixed-vector Real inputs, named scalar or explicit tuple returns (including a one-element vector), Meson-managed native execution, generated immutable input/output records, scalar and shared/per-case batching, model-evaluated default bindings, separately compiled physical input checks, source/compiler provenance in portable generated manifests, and rejection of stale sources. Explicit record bindings preserve model field order independently of Python mapping order. Aliases support existing models with abbreviated parameter names; schemas, dimensions and record fields are never repeated in configuration.

The pinned OpenSysML compiler rejects parameter defaults. The backend preserves scalar literal defaults in the generated Python API and compiles a semantic API projection with only those exported parameter defaults removed. The original model remains unchanged; Python supplies every C argument. Nonliteral defaults still require model evaluation and currently fail explicitly. Inline native assertions, nonliteral parameter-default expressions and generalized external bindings are not supported. Evaluated defaults can already be bound declaratively to named analysis outputs.

## SV Blue Dog integration

Mass, operating performance, structural margins, passage feasibility, route screening, surface/wave helpers, recovery segments, hull resistance and hydrostatics use generated exports. All native execution shares this package's backend; the project's old schema reader, adapter hierarchy and duplicate native runtime have been removed. Resistance screening remains project-owned engineering policy over generated results. Hydrostatic mesh integration uses generated batch calls and a project-owned sum; its custom C shim is removed. Interpreter reference experiments remain project-owned and do not compile kernels.

The [package-less uv template](../../examples/thermal/README.md) has application tests and a CI check that installs a built wheel into a fresh environment outside this repository. Prepared manifests use project-relative source paths and verify the configuration, model-file set, generated sources and runtime implementation. Record inheritance, nested features, bound record values and non-Real fields are explicitly unsupported; field names that collide with the runtime API are rejected. Records are direct part or attribute definitions containing scalar Real attributes. Literal record defaults are preserved as keyword-only dataclass defaults and apply to mapping inputs too. Nonliteral record defaults are rejected. Bind nonliteral calculation defaults to analysis outputs. The model's equations and schemas belong in SysML; geometry, reference experiments and engineering interpretation remain project-owned.

Generated packages contain rebuildable artifacts. Numerical execution is not physical qualification. Project evidence interpretation is intentionally outside this library.

Project-owned numerical providers can call an export's `prepare_inputs(**inputs)` to apply the same named record packing, defaults, shape checks and physical preconditions as scalar execution. It returns a dictionary of arrays keyed by public input name. This is useful when a project assembles forces or geometry outside SysML; the provider remains responsible for its external algorithm and result interpretation.

Generated records expose named fields and `to_mapping()`. Use `as_array()` when a numerical algorithm needs model-ordered values; it returns a copy. Convert its result back with `RecordType.from_array(values)`, which checks the vector shape and finite Real values using the generated field order. Preparing exports discovers return names from the model rather than maintaining Python output-label lists.

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


## Configuration

Each export names its `definition`. Optional `aliases` rename model arguments;
`records` bind vector arguments to named scalar records; `defaults` bind arguments
to model-evaluated `Analysis.output` values; and `checks` names a calculation whose
outputs must all equal one. `output_record` verifies a result against a record;
`output_definition` supplies the named result schema of a delegating calculation.
No vector widths or output-label lists belong in configuration.

The generated package is rebuildable and should be ignored by version control.
Preparation refuses to overwrite a Python package without its generated marker.
Use a new import/process after changing an exported signature. Existing callables
can reload rebuilt equations with the same signature, but cannot acquire new
Python argument or result fields without reimporting the generated code.

`errors="collect"` collects native batch execution failures with their row index;
invalid input shapes, nonfinite values and failed physical preconditions still
reject the call before numerical execution. Successful rows retain their order.
Native libraries use a content-addressed cache including source, compiler target,
compiler version and flags, and serialize calls into each loaded library.


## Native toolchains

The first call builds every exported calculation and input check in one Meson
project, with a separate shared library per target. Meson selects the compiler,
linker, math library and platform filename. It prefers GNU C11 for OpenSysML
generated code, with C11 as the fallback for other compilers. Python interfaces remain unchanged;
Cython is not needed because OpenSysML already produces C.

Install the runtime normally; Meson, Ninja and filelock are Python dependencies.
Install a C toolchain separately. Set `CC` before the first call to select one
(for example `CC=clang`). Meson honors `CFLAGS`, `CPPFLAGS` and `LDFLAGS`.
`SYSML_BUILD_JOBS` limits parallel compilation (default four). On Windows Meson
can activate Visual Studio automatically; OpenSysML's current generated code
requires GNU extensions, so use MinGW-w64 GCC for generated models. MSVC coverage
is limited to the runtime's portable C ABI fixtures, not OpenSysML-generated C.

CI exercises generated models on Linux/GCC, macOS/Clang and Windows/MinGW GCC,
plus portable ABI fixtures on Windows/MSVC. The selected OpenSysML executable
must itself support the host. The wheel includes neither OpenSysML nor a C
compiler; it builds host libraries locally and is not a precompiled model wheel.

Each immutable build snapshot is locked across processes. Its identity includes
source contents, recipe, compiler identity and executable hashes, environment
flags and Meson version. Receipts verify the resulting binary hashes before
loading. Execution provenance records Meson compiler/machine information,
resolved build options and target details. Compiler diagnostics are retained in
errors, with the failed build directory available for inspection.
