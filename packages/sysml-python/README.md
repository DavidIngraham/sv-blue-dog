# Declarative SysML/Python runtime

This package is being extracted from SV Blue Dog. It is not yet the completed reusable interface. The independent thermal example proves scalar calculation discovery, typed generated results, explicit batching and stale-source checks without importing Blue Dog code.

```python
from sysml_python import Project
Project("pyproject.toml", executable="/path/to/pinned/sysml").prepare()
from generated import joule_heat
result = joule_heat(current=2, resistance=10)
print(result.power)
```

Exports are declared under `[tool.sysml_python.exports.<name>]` with a `definition` qualified name. Source discovery uses `models` glob patterns. `generated_package` selects the generated Python package. The caller supplies a pinned executable explicitly or through `OPENSYSML_BINARY`; no tool download or search is hidden in execution.

## Current supported slice

Named scalar Real inputs and a named scalar Real result, Linux/GCC native execution, generated immutable output records, shared/per-case scalar batching, source/compiler provenance in the generated manifest, and rejection of stale sources. The extracted low-level backend also retains its existing vector ABI support; the public semantic export has not yet exposed that support.

The pinned OpenSysML compiler rejects parameter defaults. The backend preserves scalar literal defaults in the generated Python API and compiles a semantic API projection with only those exported parameter defaults removed. The original model remains unchanged; Python supplies every C argument. Nonliteral defaults still require model evaluation and currently fail explicitly. Native assertions, typed vector/record boundaries, nonliteral model-evaluated defaults, external bindings and portable manifests still need the planned migration. Do not use this slice as evidence that the entire project goal is complete.

## Remaining migration

1. Define model-owned export/binding metadata and lower defaults and physical checks explicitly.
2. Generate typed inputs/outputs and named vector packing from semantic model information; reject unsupported schemas.
3. Migrate Blue Dog mass end-to-end, keeping boat geometry and reference experiments project-owned.
4. Migrate other supported calculations; delete duplicate runtime and preparation plumbing.
5. Package the independent uv template, CI and validation examples; verify installed-package behavior outside the repository.

Generated packages contain rebuildable artifacts. Numerical execution is not physical qualification. Project evidence interpretation is intentionally outside this library.
