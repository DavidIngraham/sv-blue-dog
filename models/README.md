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

Do not use satisfaction relationships as a substitute for verification results. The design satisfaction assertions in `satisfaction.sysml` record intended allocations; none is a verification result.

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
Graphviz converts the native DOT to SVG/PNG with high-level requirements above their derived requirements.
Graphviz uses `rankdir=BT` because native derive arrows point from derived to
original; the arrows therefore point upward while the hierarchy reads top-down.
A rendering-only rank constraint aligns both mission drivers on the top row;
the saved native DOT and all native nodes and edges remain unchanged.

The native CLI is pinned separately to `nightly-20261009-28106371e`. Release 0.9.2
renders this view as a containment tree without derivation links; the dated nightly
supports requirement graphs. `scripts/install_renderer.py` downloads the CLI to
`.tools/`, verifies a committed SHA-256 archive digest, and extracts only its executable.
The installer supports Windows x64 and Linux/macOS x64/ARM64; Windows was exercised
for this migration. Nothing is installed globally and no moving nightly tag is used.
The Python client remains pinned to 0.9.2 for interactive modeling; publishing uses the native CLI.

Native dashed `derive` arrows point **from derived to original**, opposite the earlier
custom diagram convention. All 193 requirements and 238 derivation relationships are regression-checked
against the source model. Short IDs remain in the linked register; the
native diagram uses its default monochrome style without our former maturity colors.
The renderer reports two exposed standard-library elements as intentionally not drawn.

The Markdown register is rendered natively from `requirements-document.sysml`
using `-render-document BlueDogDocuments::RequirementsRegister`. Its
`DocumentQueries` queries select requirements and derivations, read the named
`workStatus` metadata, and resolve endpoints through their original/derive roles.
DocumentQueries is an OpenSysML tooling library, not an OMG standard library.
The CLI writes Markdown directly; Python does not construct table rows or cells.

The publishing script is a thin CLI wrapper: native validation, native DOT and
Markdown rendering, Graphviz conversion, and generated-file freshness checks.
It does not use the Python client or experimental API-JSON export. The pinned
Python client remains available for interactive modeling, but publishing needs
only Python, the installed native CLI, and Graphviz.

Six integration tests cover native validation, standalone challenge loading,
the expected diagram relationships, the two top-level drivers, register IDs/statuses/relationships, and use-case/satisfaction traceability. The former generic custom duplicate-ID and cycle
validator has been removed; native validation and these project publication
checks are the checks we run. `--check` compares native DOT and Markdown without
rewriting them or comparing image pixels.

Passing analysis does not establish mission feasibility or requirement satisfaction.
Eight requirement definitions contain native numeric or state acceptance predicates. Synthetic boundary tests exercise them; they do not establish physical compliance. See [verification plan](../docs/verification-plan.md). The mission decomposition does not yet define an executable sequence.

## References

- [OpenMBEE/OpenSysML](https://github.com/Open-MBEE/OpenSysML), Python client 0.9.2; native renderer `nightly-20261009-28106371e`.
- [Official SysML v2 release repository](https://github.com/Systems-Modeling/SysML-v2-Release).
- [Official requirement derivation example](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml/src/examples/Requirements%20Examples/RequirementDerivationExample.sysml).

The earlier sysmlpy fork work is retained separately and is no longer a dependency
of this project.

## Model status metadata

Requirement documentation contains statements and rationale, not maturity tags.
The register does not infer lifecycle status from prose. Requirements and derivations now carry standard `StatusInfo` metadata with
`status = ModelingMetadata::StatusKind::open`. The native register queries the typed metadata field, not documentation text. Open means work remains on the model
element; it does not revoke the agreed mission intent.

The standard [ModelingMetadata library](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml.library/Domain%20Libraries/Metadata/ModelingMetadata.sysml)
defines `StatusInfo` with a typed `StatusKind`: `open`, `tbd` (to be determined),
`tbr` (to be resolved), `tbc` (to be confirmed), `done`, and `closed`.
It also provides optional owner, originator, and risk information. This metadata supplies work-status tracking. These values do not directly
encode the former confirmed/legacy/proposed categories or prove verification.

## Use cases and architecture allocations

`use-cases.sysml` declares requirement-linked objectives and a native case view.
`satisfaction.sysml` connects candidate design elements to requirements. The
native document includes these links in `docs/traceability.md`. The architecture
view includes overview, detailed composition, and mission context. All SVG and
PNG assets are generated by the publishing script. One-person handling and
printer construction are requirements; P-002 fixes the usable printer envelope at 250 Ãƒâ€” 250 Ãƒâ€” 250 mm, while P-001 proposes the per-lift mass limit.

Executable-criteria tests cover numeric boundaries, navigation epoch counts, launch-inhibition conditions, every motor/qualification Boolean combination, and missing observations.

## Recovery propulsion analysis

`recovery-trade.sysml` contains a native executable analysis case for water and air propeller candidates. The publishing command runs both examples and saves the CLI's unmodified JSON in `docs/analysis/recovery-trade.json`; `--check` also checks this output. All equations stay in SysML, including the shared R-002 reserve calculation. See the [trade study](../docs/recovery-propulsion-trade.md) for assumptions, commands, evidence gates and result interpretation.

## Atomic acceptance leaves

The [decomposition map](../docs/requirement-decomposition.md) explains the 127 acceptance leaves beneath 29 retained parent IDs. Parents supply common test context and link to individual outcomes; derivation is not executable aggregation. Eight native predicates remain, with five moved from bundled parents to the corresponding leaves. The full SVG is a zoomable trace graph; the PNG is a scaled overview because Graphviz limits bitmap width. Use the native register for readable statements.
