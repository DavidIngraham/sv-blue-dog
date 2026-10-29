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

Reusable calculation-only libraries share the independent `Analysis` root:

```text
Analysis
├── Marine
│   ├── Appendages, Concept, Course
│   ├── Hydrostatics, Propulsion, Recovery, Resistance
│   └── Sailing, Surface, WavePerformance, Weather
├── Mechanics
│   ├── Mass
│   └── Structures
├── Energy
│   └── Actuation
└── Reliability
```

These packages own numerical calculations and their documentation. For example,
`Analysis::Marine::Resistance::Evaluate` is a reusable resistance kernel and
`Analysis::Mechanics::Mass::MassProperties` computes mass properties. Project
studies and configuration bindings stay under `BlueDog::Analyses`.

Five mixed/domain roots remain separate. `MarineDesign` owns named design,
parameter, operating-state and result schemas; its vector adapters belong with
that contract. `MarineEnergy` owns electrical loads, batteries, budget/interval
types, their derived properties and rollup. `InlandExtended` and
`InlandNavigationExperiment` own navigation-domain enums, contexts and conditional
rule assessments. `EngineeringDecisions` owns decision and review records.
Owning a calculation or an analysis case does not by itself make such a library
calculation-only, and package ownership does not create physical composition.

The loaded model has **7 top-level packages and 115 packages in total**, including
108 nested packages, in seven source documents. These are native namespace counts,
not counts of view roots or boat components. Shared calculations have no Blue Dog
dependencies. Their SI/vector boundary conventions and existing numerical limits
remain part of the contract; grouping them adds no new engineering capability.

## Adding or selecting model elements

Put a project definition under the area that owns its engineering meaning. Keep
the IC-01 candidate under `BlueDog::Configurations::IC01`, reusable calculations
under the appropriate `Analysis` domain and project bindings under `BlueDog::Analyses`. Use
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
`BlueDog` root is not an extension mechanism. The shared `Analysis` package is likewise canonical in
`models/libraries/analysis.sysml`; do not reopen it across independent files.
The five mixed/domain libraries remain separate source documents. Use the pinned
native editor and semantic validation when changing declarations and references. When editing
a shared calculation through the native client, select the calculation document
as the primary source; the pinned editor cannot rewrite secondary documents.
A new reusable calculation can be discovered and executed through the native API
without adding a Python dispatch list.

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
bindings (for example, `MarineSailing::Core` becomes
`Analysis::Marine::Sailing::Core`); the active model has no old-root alias facade. Historical replay
against an archived source revision continues to use that revision's names.

After model changes, run `uv run python -m tools.boat_analysis.cli prepare`, the
relevant checks and the full regression suite as required by
[AGENTS.md](../../AGENTS.md). Build the publication with
`uv run python -m tools.publishing.build` before publishing. Namespace validation
establishes resolution and ownership; it adds no physical qualification evidence.
