# Learning SysML v2 through SV Blue Dog

Start with [blue-dog.sysml](blue-dog.sysml), [requirements.sysml](requirements.sysml) and the [mission decision record](../docs/mission-and-requirements.md).

The textual model is the editable architecture source in Git. It currently contains mission action decomposition, a logical parts hierarchy, and textual requirement definitions/usages. It is a discussion model, not a complete executable mission or verified design.

## Read the first model

- `package` groups related concepts: mission, architecture, and requirements.
- `part def Boat` defines a type; `part boat : Boat` uses that type in a mission context.
- Nested parts decompose responsibility. They do not require one circuit board per part.
- `action def TransGorgeMission` decomposes mission behavior. Nested actions alone do not establish a timeline or concurrent execution.
- `requirement def` defines a requirement type; `requirement` creates a usage. Short identifiers such as M-001 keep references stable.
- `doc` carries intent and unresolved questions. Those statements are not executable acceptance constraints.

## Learning sequence

1. Review system boundary and mission decomposition together.
2. Use the pinned OpenSysML environment, then extend validation as the model grows.
3. Add mission sequencing, continuous supporting behavior, and recovery paths.
4. Agree on measurable requirements and introduce typed quantities/units and constraints.
5. Define ports, exchanged information, and power interfaces; allocate behavior to logical parts.
6. Refine logical responsibilities into hardware/software alternatives and a physical design.
7. Add verification cases, evidence, and requirement traceability as the design develops.

Do not use satisfaction relationships as a substitute for verification results. No satisfaction assertions are included in this starting model.

## Reproducible tooling

The root `pyproject.toml` defines a **package-free uv project** (`[tool.uv] package = false`). `uv.lock` fixes the dependency resolution, including OpenSysML 0.9.2. The project is not installed as a Python package; scripts run directly. Python 3.12 or 3.13 is supported.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and [Graphviz](https://graphviz.org/download/) with `dot` on PATH, then run from the repository root:

```sh
uv sync --locked
uv run python scripts/render_requirements.py
uv run python -m unittest discover -s tests -v
uv run python scripts/render_requirements.py --check
```

The official Python client automatically downloads a matching `sysml-grpc`
runtime on first use, checks it against its packaged SHA-256 digest, and starts a
private local service for the Python process. First use requires network access;
subsequent runs use the cached runtime. `uv.lock` pins Python packages; the client
release pins the runtime download. For offline setup and explicit runtime paths,
see the [OpenSysML client guide](https://opensysml.org/guide/09-clients/).
No model is sent to a hosted analysis service by this workflow.

The renderer writes SVG, PNG, and DOT to `docs/figures/` and the readable requirement/derivation register to `docs/requirements-register.md`. Commit these with model changes so GitHub and the website can display them without a Python runtime. `--check` checks DOT and register freshness; it does not compare rendered image pixels. Graphviz is a system dependency outside the uv lockfile, so its version and fonts can affect layout.

## Renderer scope and validation limits

OpenSysML loads and analyzes both project models. Error diagnostics stop generation.
The project renderer reads the engine's public API-JSON export: requirement IDs,
documentation, resolved metadata types, and reference-subsetting targets. It keeps
Graphviz for the existing project-specific layout and generates the Markdown register
from those same model elements. There is no handwritten edge list or source-text parser.

The API-JSON mapping is experimental upstream and emits an explicit warning. We pin
OpenSysML 0.9.2 and check the complete project graph when upgrading. This renderer
supports one flat Requirements package, locally typed requirement usages, and explicit
metadata-tagged connections with one original and one derived end. It rejects missing
roles, unresolved endpoints, duplicate IDs/edges, and cycles. This is a narrow project
publishing adapter, not a general implementation of Requirement Derivation semantics.

The migration preserved all nine requirement usages and eight links, and both models
loaded without OpenSysML diagnostics. The generated SVG, PNG, and DOT stayed unchanged;
the register only lost redundant whitespace. Model source files were not rewritten.

Passing analysis does not establish mission feasibility or requirement satisfaction.
Requirements currently carry prose and unresolved thresholds, not executable acceptance
constraints. The mission decomposition does not yet define an executable sequence.

## References

- [OpenMBEE/OpenSysML](https://github.com/Open-MBEE/OpenSysML), pinned to 0.9.2.
- [Official SysML v2 release repository](https://github.com/Systems-Modeling/SysML-v2-Release).
- [Official requirement derivation example](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml/src/examples/Requirements%20Examples/RequirementDerivationExample.sysml).

The earlier sysmlpy fork work is retained separately and is no longer a dependency
of this project.
