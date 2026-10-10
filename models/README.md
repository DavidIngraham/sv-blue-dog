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

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run from the repository root:

```sh
uv sync --locked
uv run python scripts/install_renderer.py
uv run python scripts/render_requirements.py
uv run pytest -v
uv run python scripts/render_requirements.py --check
```

Pytest is a development dependency managed by uv. Run `uv run pytest` for the full suite or select cases with `-k`. Parametrized tests report individual boundary and invalid-input cases; fixtures share the native CLI runner and cache publication outputs for their test module.

The official Python client automatically downloads a matching `sysml-grpc`
runtime on first use, checks it against its packaged SHA-256 digest, and starts a
private local service for the Python process. First use requires network access;
subsequent runs use the cached runtime. `uv.lock` pins Python packages; the client
release pins the runtime download. For offline setup and explicit runtime paths,
see the [OpenSysML client guide](https://opensysml.org/guide/09-clients/).
No model is sent to a hosted analysis service by this workflow.

The renderer writes native Mermaid Markdown and standalone HTML to `docs/figures/`, updates marked diagram blocks in the authored articles, and regenerates the reports and analysis JSON. Commit these with model changes. GitHub renders the fenced Mermaid blocks; the blog loads a pinned Mermaid renderer. Standalone HTML uses OpenSysML's pinned CDN renderer and falls back to source when unavailable. `--check` compares all generated text, including embedded diagrams. Graphviz is no longer required for publishing.

## Native requirements view

`requirements-view.sysml` declares bounded native views, grouped by original
requirement. Each drawing includes one parent and at most three immediate children.
The [requirements view index](../docs/requirements-views.md) links 47 parent pages,
including separate Trans-Gorge and Hawaii entry points, environment, weed tolerance,
energy, safety, communications and practicality.

`DiagramLayout::Layout` annotations bound the native rendering's membership:
OpenSysML otherwise expands a requirement view through related elements. Mermaid
preserves that node selection but computes its own layout. Documents explicitly
request Mermaid and `BT` direction, keeping original requirements above derived
ones. Omitted-node notices describe intentional view boundaries, not missing model
relationships. Satisfaction is available separately in the traceability register.

The all-encompassing view remains solely as the regression oracle. It is not
published or embedded in articles. A coverage test checks that the small views
together preserve every one of the 249 derivations and contain at most four nodes.
The native documents also provide requirement statements and next-level links.

The native CLI is pinned separately to `nightly-20261009-28106371e`. Release 0.9.2
renders this view as a containment tree without derivation links; the dated nightly
supports requirement graphs. `scripts/install_renderer.py` downloads the CLI to
`.tools/`, verifies a committed SHA-256 archive digest, and extracts only its executable.
The installer supports Windows x64 and Linux/macOS x64/ARM64; Windows was exercised
for this migration. Nothing is installed globally and no moving nightly tag is used.
The Python client remains pinned to 0.9.2 for interactive modeling; publishing uses the native CLI.

Native dashed `derive` arrows point **from derived to original**, opposite the earlier
custom diagram convention. All 199 requirements and 249 derivation relationships are regression-checked
against the source model. Short IDs remain in the linked register; the
native diagram uses its default monochrome style without our former maturity colors.
The renderer reports two exposed standard-library elements as intentionally not drawn.

The Markdown register is rendered natively from `requirements-document.sysml`
using `-render-document BlueDogDocuments::RequirementsRegister`. Its
`DocumentQueries` queries select requirements and derivations, read the named
`workStatus` metadata, and resolve endpoints through their original/derive roles.
DocumentQueries is an OpenSysML tooling library, not an OMG standard library.
The CLI writes Markdown directly; Python does not construct table rows or cells.

The publishing script wraps native validation, document rendering and analyses,
then replaces only explicitly marked diagram blocks in authored Markdown.
Publishing needs Python and the pinned native CLI. Regression tests retain native
DOT inspection as an independent check of derivation endpoints; DOT is no longer
a published artifact. Browser checks verify Mermaid rendering separately from
model correctness. Run `uv run pytest` and the publishing freshness check before pushing.

Passing analysis does not establish mission feasibility or requirement satisfaction.
Thirteen requirement definitions contain native numeric or state acceptance predicates. Synthetic boundary tests exercise them; they do not establish physical compliance. See [verification plan](../docs/verification-plan.md). The mission decomposition does not yet define an executable sequence.

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

The [decomposition map](../docs/requirement-decomposition.md) explains the 127 acceptance leaves beneath 29 retained parent IDs. Parents supply common test context and link to individual outcomes; derivation is not executable aggregation. The atomicity pass moved five existing native predicates from bundled parents to the corresponding leaves; the later energy framework adds its own criteria. Use the focused requirement views to follow one parent at a time. Use the native register for readable statements.

## Sustained-operation energy framework

[energy.sysml](energy.sysml) defines extensible electrical load collections, mode budgets, battery storage, chronological resource intervals, a native analysis case and an evidence-gated verification case. [energy-examples.sysml](energy-examples.sysml) holds the synthetic 72-hour input set separately from the reusable definitions. All accounting and requirement predicates execute in SysML, including collection summation and recursive energy propagation. `ordered nonunique` preserves repeated values in sampled histories.

The [native load table](../docs/energy-budget.md), [analysis JSON](../docs/analysis/sustained-energy.json) and [framework guide](../docs/sustained-operations.md) distinguish conditional numerical feasibility from accepted evidence. Publishing regenerates the table and analysis; `--check` detects stale outputs. The verification case explicitly verifies E-200 and returns inconclusive for the unaccepted synthetic inputs.

## Concise requirements and supporting information

Keep `doc` on a requirement definition to one concise obligation. Put qualification
conditions in a named `comment conditions`; those definitions remain normative.
Use `comment notes` for explanatory limitations, `ModelingMetadata::Rationale`
for justification, and `ModelingMetadata::Issue` for open questions. These are
native SysML constructs; no project metadata library is needed. Formal `assume`
and `require` predicates remain in the requirement where already modeled.

`requirement-verification.sysml` owns planned procedures and native `verify`
links to the parent and applicable leaves, including shared leaves. Its cases
return inconclusive pending evidence-backed implementation. Do not treat a prose
parent or an unimplemented case as an executable pass.

The [register](../docs/requirements-register.md) and focused views show concise
statements. The separate [context report](../docs/requirements-context.md) publishes
conditions, rationale, notes, issues and verification specifications. Derivation
rationale is standard metadata on each connection. Publishing renders the native
document set once per format; HTML files share `figures/sysml-document.css`.
