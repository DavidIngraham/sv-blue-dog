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
2. Use the pinned sysmlpy environment, then extend validation as the model grows.
3. Add mission sequencing, continuous supporting behavior, and recovery paths.
4. Agree on measurable requirements and introduce typed quantities/units and constraints.
5. Define ports, exchanged information, and power interfaces; allocate behavior to logical parts.
6. Refine logical responsibilities into hardware/software alternatives and a physical design.
7. Add verification cases, evidence, and requirement traceability as the design develops.

Do not use satisfaction relationships as a substitute for verification results. No satisfaction assertions are included in this starting model.

## Reproducible tooling

The root `pyproject.toml` defines a **package-free uv project** (`[tool.uv] package = false`). `uv.lock` fixes the dependency resolution, including sysmlpy 0.96.4. The project is not installed as a Python package; scripts run directly. Python 3.12 or 3.13 is supported.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and [Graphviz](https://graphviz.org/download/) with `dot` on PATH, then run from the repository root:

```sh
uv sync --locked
uv run python scripts/render_requirements.py
uv run python -m unittest discover -s tests -v
uv run python scripts/render_requirements.py --check
```

The renderer writes SVG, PNG, and DOT to `docs/figures/` and the readable requirement/derivation register to `docs/requirements-register.md`. Commit these with model changes so GitHub and the website can display them without a Python runtime. `--check` checks DOT and register freshness; it does not compare rendered image pixels. Graphviz is a system dependency outside the uv lockfile, so its version and fonts can affect layout.

## Renderer scope and validation limits

Testing sysmlpy 0.96.4 showed that its higher-level `ConnectionUsage` conversion and built-in general view omit the metadata-tagged derivation ends. The generator therefore reads **sysmlpy's concrete ANTLR parse tree**, before that lossy conversion, and renders the extracted graph with local Graphviz. It does not parse SysML with regular expressions or keep a separate handwritten edge list. No hosted renderer receives the model.

The adapter intentionally supports one flat Requirements package, requirement definitions with short IDs and maturity documentation, local typed requirement usages, and explicit derivation usages with one original and one derived end. Unsupported patterns fail. It checks duplicate IDs/edges, endpoint resolution, role metadata, and cycles. Both project SysML files are syntax-checked with parser rescue disabled. Tests exercise direction, unresolved endpoints, missing roles, cycles, and invalid syntax.

These checks are not full SysML semantic validation. In particular, they do not establish complete standard-library metadata semantics, system feasibility, numerical acceptance criteria, or requirement satisfaction. The built-in analyzer on the earlier nine-requirement baseline reported nine expected `REQUIREMENT_UNCOVERED` warnings and no errors; that result predates the explicit derivations and is not claimed as validation of this revision. No satisfaction assertions have been added to silence those warnings.

sysmlpy may emit a nonfatal DFA cache-save `RecursionError` warning; parsing continues. Do not edit these models through a sysmlpy high-level dump/format round trip until derivation-end preservation has been verified.

## References

- [sysmlpy](https://github.com/mycr0ft/sysmlpy), pinned to PyPI 0.96.4 in this project.
- [Official SysML v2 release repository](https://github.com/Systems-Modeling/SysML-v2-Release).
- [Official requirement derivation example](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml/src/examples/Requirements%20Examples/RequirementDerivationExample.sysml).
- The pinned sysmlpy distribution includes the `RequirementDerivation` domain library used as syntax guidance.
