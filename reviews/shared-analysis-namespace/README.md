# Shared calculation namespace

Fifteen reusable calculation-only packages now share one native `Analysis` root,
organized into `Marine`, `Mechanics`, `Energy` and `Reliability`. Project-specific
studies remain under `BlueDog::Analyses`. The selection follows engineering
purpose and native declaration content, rather than the presence of a `calc` or
`analysis` keyword alone.

| Native inventory | Published baseline `556cd79` | This branch |
| --- | ---: | ---: |
| Model source files | 21 | 7 |
| Top-level packages | 21 | 7 |
| Total packages | 111 | 115 |
| Native elements | 14,929 | 14,933 |
| Moved calculation-only packages | — | 15 |
| Moved calculation definitions | — | 44 |

All 14,929 existing declarations survive under their mapped identities, with
unchanged native kind, mapped owner, type and generalization. The four added
elements are organizing packages: `Analysis`, `Analysis::Marine`,
`Analysis::Mechanics`, and `Analysis::Energy`. Native reference resolution and
complete audit-table comparisons also pass. The model changes are actual
namespace ownership, without old-root aliases or UI-only grouping.

## Scope and exceptions

The [machine-readable mapping](namespace-map.json) lists every moved qualified
prefix and source path. The current [namespace guide](../../docs/reference/namespace-structure.md)
describes the hierarchy and extension rules.

| Retained root | Reason |
| --- | --- |
| `MarineDesign` | Eight named design, parameter, operating-state and result schemas; its two vector adapters belong to the numerical contract. |
| `MarineEnergy` | Electrical loads, load budgets, batteries and intervals, including their derived properties and rollup. Storage-rate calculation and the analysis case remain cohesive with those types. |
| `InlandExtended` | Navigation-domain enums, context and conditional rule/equipment assessments. |
| `InlandNavigationExperiment` | Encounter/obligation enums, context and conditional pair assessment. |
| `EngineeringDecisions` | Decision-state, information-record and review schemas. |

These five source documents retain their exact original bytes. Calculations
inside mixed libraries are deliberately retained, and the project studies are
not treated as reusable generic kernels. Existing physical composition,
configuration values, qualification policy, acceptance flags and historical
evidence are unchanged. No new physics, metadata or missing facts are invented.

The shared calculation library is canonical in `models/libraries/analysis.sysml`.
The pinned runtime cannot combine independently reopened namespace fragments.
Its editor also cannot rewrite references in secondary documents. The migration
therefore staged the complete model in one in-memory primary document, used
native move/rename operations, partitioned the resulting roots through native
declaration ranges, then reparsed the seven resulting sources strictly. No
second SysML parser or relationship engine was introduced. Native comparison
ran before source installation and again after formatting and binding updates.

Native calculation IDs and old library source paths require the documented
migration. Python export names remain stable; their native definitions and checks
are rebound in `pyproject.toml`. Current project YAML selectors retain their
identities because `BlueDog::Analyses` and its cases remain in place. Existing
record schemas such as `MarineDesign::Design` are unchanged. Rebuild generated
native/C adapters with `prepare`; do not reuse stale generated symbol metadata.

## Verification

Fresh preparation, numerical and audit baselines were captured on `556cd79`
before mutation. After migration, native preparation passes. Nine configured
study runs, the named-configuration demonstration and the real search problem
retain exactly equal reports after qualified-ID normalization. Bounds, initial
vector, equalities, all 297 inequality constraints, design/state arrays, routes
and righting arrays have maximum absolute delta **0**, checked with
`rtol=1e-13`, `atol=1e-12`.

All seven audits have no diagnostics/errors and their normalized complete tables
match, including requirement, allocation, scenario, configuration, analysis,
safety, decision and verification records. Provenance hashes and source locations
change as expected; historical evidence and previous review reports are frozen.

Focused tests verify the seven real roots, retained domain/schema identities,
absence of old calculation aliases, standalone execution of the calculation
document, and native discovery/execution of a synthetic additional calculation
without a Python dispatch-list edit. The native editing fixture explicitly selects
the calculation document as its primary source. These are software consistency
checks, not physical validation or evidence acceptance.

The full isolated suite passes all **1,167 tests in 81 modules**, without skips.
All **33 unique reusable runtime tests** also pass with the pinned native compiler.
Seven generator freshness checks, the seeded four-run mission campaign, five
figure generators and the **38-page** publishing build pass. Python compilation
and `git diff --check` pass. Detailed local results are in
[validation-summary.json](validation-summary.json); exact branch-CI and portability
results are recorded in the final handoff.

Reproduce from the repository root with the pinned toolchain and locked environment:

```sh
uv run python -m tools.boat_analysis.cli prepare
PYTHONPATH=. uv run python reviews/shared-analysis-namespace/validate_native.py
PYTHONPATH=. uv run python reviews/shared-analysis-namespace/validate_numerics.py
PYTHONPATH=. uv run python reviews/shared-analysis-namespace/capture_audits.py
PYTHONPATH=. uv run python reviews/shared-analysis-namespace/compare_audit_tables.py
uv run python -m tools.testing
uv run python -m tools.publishing.build
```

Use `GOMEMLIMIT=3GiB GOGC=50` for native test processes. The regression driver
already supplies these defaults and runs each configured module in a separate
process. Generator `--check` commands remain in the namespace reference.
There is no separately configured static type checker; Python syntax/import and
runtime contracts are checked by compilation and the configured regression suite.

## Integration boundary

This work uses `/home/david/repos/sv-blue-dog-analysis-namespaces`, branch
`refactor/shared-analysis-namespace`, based on published `556cd79`. The original
dirty editorial checkout and completed declarative/namespace worktrees remain
preserved, including their commits and authorship.

Challenge remains `BlueDog::Mission::Challenge`; this migration does not change
its scope or mission policy.

Only this feature branch is authorized for pushing. Main remains unchanged;
feature-ref CI must skip deployment. No merge, Pages deployment or SysPresent
modification is authorized by this request.

Later integration must replace the 15 former calculation source files with
`models/libraries/analysis.sysml`, update `models/blue-dog.sysml` to its rebound
references, retain the five mixed library files and migrate external qualified
IDs with the mapping. Adding the grouped file alongside old roots would leave
the old roots visible. The hash-verified seven-file payload is supplied in the
handoff. Existing solver, fixed vector, route-topology and SI-scalar limits remain
documented; namespace organization does not claim universal numerical reuse.
