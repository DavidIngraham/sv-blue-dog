# Model namespaces and source maintenance

[Blue Dog's project model](../../models/blue-dog.sysml) has one native root,
`BlueDog`. Packages group related engineering definitions. A component's owning
package does not make it a component of the boat: part composition, interfaces,
allocations, satisfaction and verification relationships state those meanings.
The [modeling conventions](../../models/README.md) explain their use.

## Ownership

```text
BlueDog
├── Mission
│   ├── Challenge
│   ├── Course
│   ├── Scope
│   └── UseCases
├── Requirements
│   ├── Basis
│   └── Structure
├── Architecture
│   ├── Logical
│   ├── Physical
│   ├── Interfaces
│   ├── Contracts
│   └── Correspondence
├── Behavior
│   ├── Contracts
│   ├── MissionLogic
│   └── Navigation
├── Analyses
│   ├── Sizing (including Uncertainty, Credibility and Evidence)
│   ├── Operating
│   ├── Safety (including DFMEA and AvoidanceFailures)
│   └── other project studies
├── Configurations
│   ├── IC01
│   ├── Management
│   ├── Examples (Energy, Sailing and Reliability)
│   └── shared input and equipment configurations
├── Decisions
│   ├── Context
│   ├── Design
│   ├── OpenQuestions
│   └── TradeCriteria
├── Verification
│   ├── Challenge
│   ├── Requirements
│   ├── Planning
│   └── Satisfaction
├── Evidence
│   ├── Sources
│   └── generated recorded-result projections
├── Method (including Scenarios)
├── Goals
└── DesignIntent
```

This outline shows ownership areas and selected children, rather than every
analysis. Native semantic queries provide the full inventory. Mission actions
also live directly in `Mission`, and system composition and context directly
in `Architecture`.

Twenty reusable packages remain separate in `models/libraries/`. Marine
calculations, energy/reliability calculations and shared decision-record types
have independent roots and no Blue Dog dependencies. Project configurations bind
their inputs; project analyses identify the question, subject and applicability.
The loaded model has 21 top-level packages and 111 packages in total, including
the 90 nested packages. This is a namespace count, not a count of view roots or
boat components.

## Adding or selecting model elements

Put a project definition under the area that owns its engineering meaning. Keep
the IC-01 candidate under `BlueDog::Configurations::IC01`, reusable calculations
in an independent library and project bindings under `BlueDog::Analyses`. Use
native references for relationships between areas; importing a package does not
establish traceability or engineering authority.

Use exact qualified IDs or supported native types/ownership queries in Python,
YAML and publication views. For example, a sail-trade usage selector has owner
`BlueDog::Analyses::SailTrade` and type
`BlueDog::Analyses::SailTrade::TradeAssessment`. The
[declarative study contract](declarative-studies.md) specifies direct ownership,
cardinality, defaults, missing inputs and provenance. Add a typed usage under the
selected owner to extend that study without adding a Python selection list.
Do not infer meaning from a package's display name or source filename.

## Canonical source and generated evidence

`models/blue-dog.sysml` contains the complete native project package. The pinned
runtime does not resolve independent files as reopened fragments of the same
package. Keep the project document canonical; a second file declaring another
`BlueDog` root is not an extension mechanism. Reusable libraries remain separate
source documents. Use the pinned native editor and semantic validation when
changing declarations and references.

Seven evidence sections inside the canonical document have explicit
`BEGIN GENERATED PROJECTION` / `END GENERATED PROJECTION` comment boundaries.
Generators own only the bytes between their matching markers and preserve the
rest of the document. Do not hand-edit their payloads or restore old standalone
projection files under `models/`.

| Section | Native package in `BlueDog::Evidence` | Generator |
| --- | --- | --- |
| `coupled-2026-10-10` | `RecordedSizing` | `tools.boat_analysis.evidence.model` |
| `current-sizing` | `CurrentSizing` | `tools.boat_analysis.evidence.model --current` |
| `sizing-continuation` | `SizingContinuation` | `tools.boat_analysis.evidence.continuation 2026-10-12-continuation` |
| `finite-passage-sizing` | `FinitePassageSizing` | `tools.boat_analysis.evidence.continuation 2026-10-12-finite-passage --package BlueDog::Evidence::FinitePassageSizing` |
| `srr-current` | `SRRCurrent` | `tools.publishing.srr --run 2026-10-13-srr-readiness` |
| `srr-frontier` | `SRRFrontier` | `tools.publishing.frontier --run 2026-10-13-srr-frontier` |
| `gorge-wind` | `WindObservations` | `tools.boat_analysis.environment.climatology` |

Run these modules with `uv run python -m`. Append `--check` to compare the
section with its recorded or frozen inputs without writing model sources or
plots. The weather check uses frozen observations and cannot be combined with
`--fetch`. The section helper validates unique, ordered, nonoverlapping marker
pairs before writing.

Historical `evidence/runs/` records retain their original source revisions, names
and hashes. Their model projections do not turn those records into current
physical evidence. Current execution reports record the actual qualified IDs,
source hashes and runtime. Consumers of older qualified IDs must update their
bindings; the active model has no old-root alias facade. Historical replay
against an archived source revision continues to use that revision's names.

After model changes, run `uv run python -m tools.boat_analysis.cli prepare`, the
relevant checks and the full regression suite as required by
[AGENTS.md](../../AGENTS.md). Build the publication with
`uv run python -m tools.publishing.build` before publishing. Namespace validation
establishes resolution and ownership; it adds no physical qualification evidence.
