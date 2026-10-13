# Declarative SysML/Python runtime

This package is being extracted from SV Blue Dog. It is not yet the completed reusable interface. The independent thermal example proves scalar calculation discovery, typed generated results, model-owned defaults, explicit batching and stale-source checks without importing Blue Dog code. Blue Dog now consumes a generated mass export instead of a handwritten mass adapter.

```python
from sysml_python import Project
Project("pyproject.toml", executable="/path/to/pinned/sysml").prepare()
from generated import joule_heat
result = joule_heat(current=2, resistance=10)
print(result.power)
```

Exports are declared under `[tool.sysml_python.exports.<name>]` with a `definition` qualified name. Source discovery uses `models` glob patterns. `generated_package` selects the generated Python package. The caller supplies a pinned executable explicitly or through `OPENSYSML_BINARY`; no tool download or search is hidden in execution.

## Current supported slice

Scalar and fixed-vector Real inputs, named scalar or explicit tuple returns, Linux/GCC native execution, generated immutable input/output records, scalar and shared/per-case batching, model-evaluated default bindings, separately compiled physical input checks, source/compiler provenance in generated manifests, and rejection of stale sources. Explicit record bindings preserve model field order independently of Python mapping order. Aliases support existing models with abbreviated parameter names; schemas, dimensions and record fields are never repeated in configuration.

The pinned OpenSysML compiler rejects parameter defaults. The backend preserves scalar literal defaults in the generated Python API and compiles a semantic API projection with only those exported parameter defaults removed. The original model remains unchanged; Python supplies every C argument. Nonliteral defaults still require model evaluation and currently fail explicitly. Inline native assertions, nonliteral parameter-default expressions, generalized external bindings and portable manifests still need work. Evaluated defaults can already be bound declaratively to named analysis outputs. Do not use this slice as evidence that the entire project goal is complete.

## Remaining migration

1. Define model-owned export/binding metadata and lower defaults and physical checks explicitly.
2. Generate typed inputs/outputs and named vector packing from semantic model information; reject unsupported schemas.
3. Mass is migrated; continue separating project reference experiments from generic preparation.
4. Migrate other supported calculations; delete duplicate runtime and preparation plumbing.
5. Package the independent uv template, CI and validation examples; verify installed-package behavior outside the repository.

Generated packages contain rebuildable artifacts. Numerical execution is not physical qualification. Project evidence interpretation is intentionally outside this library.
