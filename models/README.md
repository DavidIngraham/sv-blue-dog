# Learning SysML v2 through SV Blue Dog

Start with the independent [challenge.sysml](challenge.sysml) and [challenge brief](../docs/challenge-brief.md), then [blue-dog.sysml](blue-dog.sysml), [requirements.sysml](requirements.sysml) and the [mission decision record](../docs/mission-and-requirements.md).

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
uv run python scripts/install_renderer.py
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

## Native requirements view

`requirements-view.sysml` declares `BlueDogViews::requirements` as an OMG
`GeneralView` filtered to requirement usages. It exposes both the independent
`GorgeChallenge` package and the vehicle requirements. `requirements.sysml` imports
`GorgeChallenge`; the tooling loads both source files together, resolving cross-file
derivation endpoints. The challenge can also be analyzed by itself. The combined source set also includes
`blue-dog.sysml`, which defines the Hawaii goal and both mission decompositions.
The two graph roots are C-000 (Trans-Gorge challenge) and H-001 (Hawaii voyage).
Vehicle requirements live in the distinct `BlueDogRequirements` package; files
do not reopen or merge separate declarations of the `BlueDog` package. OpenSysML selects the nodes and
relationships and writes DOT; Python no longer constructs diagram nodes or edges.
Graphviz converts that unmodified DOT to SVG/PNG with a left-to-right layout.

The native CLI is pinned separately to `nightly-20261009-28106371e`. Release 0.9.2
renders this view as a containment tree without derivation links; the dated nightly
supports requirement graphs. `scripts/install_renderer.py` downloads the CLI to
`.tools/`, verifies a committed SHA-256 archive digest, and extracts only its executable.
The installer supports Windows x64 and Linux/macOS x64/ARM64; Windows was exercised
for this migration. Nothing is installed globally and no moving nightly tag is used.
The Python client and its analysis service remain pinned to 0.9.2 for register generation.

Native dashed `derive` arrows point **from derived to original**, opposite the earlier
custom diagram convention. All seventeen nodes and twenty-five relationships are regression-checked
against the source model. Maturity and short IDs remain in the linked register; the
native diagram uses its default monochrome style without our former maturity colors.
The renderer reports two exposed standard-library elements as intentionally not drawn.

The Markdown register still uses the Python client's experimental API-JSON export,
which retains IDs, documentation, metadata types and reference bindings. Its narrow
project adapter checks missing roles, unresolved endpoints, duplicate IDs/edges and
cycles. That adapter no longer drives diagram construction. `--check` regenerates
native DOT for comparison as well as checking register freshness.

Passing analysis does not establish mission feasibility or requirement satisfaction.
Requirements currently carry prose and unresolved thresholds, not executable acceptance
constraints. The mission decomposition does not yet define an executable sequence.

## References

- [OpenMBEE/OpenSysML](https://github.com/Open-MBEE/OpenSysML), Python client 0.9.2; native renderer `nightly-20261009-28106371e`.
- [Official SysML v2 release repository](https://github.com/Systems-Modeling/SysML-v2-Release).
- [Official requirement derivation example](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml/src/examples/Requirements%20Examples/RequirementDerivationExample.sysml).

The earlier sysmlpy fork work is retained separately and is no longer a dependency
of this project.
