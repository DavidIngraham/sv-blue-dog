# Blue Dog namespace structure

The active model now owns project definitions beneath one native `BlueDog`
package. Twenty reusable library roots remain independent. This is an actual
SysML ownership migration, with all live Python, YAML, publication and test
bindings updated to canonical qualified IDs.

| Native inventory | Before (`8f2dd80`) | After |
| --- | ---: | ---: |
| Source documents | 96 | 21 |
| Top-level packages | 100 | 21 |
| Nested packages | 5 | 90 |
| All packages | 105 | 111 |
| All native elements | 14,923 | 14,929 |

`Mission`, `Requirements`, `Architecture`, `Behavior`, `Analyses`,
`Configurations`, `Decisions`, `Verification` and `Evidence` organize engineering
ownership. Existing `Goals`, `DesignIntent`, `Method`, mission actions and system
composition remain. The six additional elements are organizing packages.
See [the current hierarchy](../../docs/reference/namespace-structure.md),
[the complete prefix/source mapping](namespace-mapping.md) and
[machine-readable mapping](namespace-map.json).

## Implementation and compatibility

The work starts from the completed declarative refactor at `8f2dd80`, in an
isolated local worktree and branch. Neither the original dirty editorial checkout
nor the clean declarative checkout is a work target. See
[preservation evidence](preservation.json).

The pinned native editor cannot move the existing project across documents: it
rejects respelling a step of the IC-01 battery-assumption feature chain. The
pinned runtime also does not merge independently reopened `BlueDog` fragments.
Therefore the actual project package is canonical in `models/blue-dog.sysml`;
the old 76 project files are removed. Native editor declaration ranges supplied
the complete declaration bytes for assembly, followed by strict native semantic
resolution and identity comparison. There is no replacement SysML parser,
relationship engine or alias facade.

Native comparison maps all 14,923 preexisting element IDs and compares kind,
owner, type and generalization. Only the expected package owners change. Native
audits compare requirement, allocation, scenario, configuration, analysis,
safety, decision and verification records. Query ordering and source hashes
necessarily change. Hazard-basis reporting keeps its original direct-owned
dependency boundary rather than absorbing the newly nested DFMEA and failure
analysis packages. Configuration inventory recognizes package ownership at any
depth, demonstrated by synthetic nested negative controls.

The analysis-use register discovers native analysis types under `BlueDog` and
the three existing external analysis roots, replacing its long per-package
selection list. A synthetic annotated nested analysis verifies extension without
a package-list edit. The pinned document-query vocabulary has no global-model
source operation: a new independent external root still needs an explicit
register scope. The native audit independently inventories loaded roots and
rejects unregistered or unannotated cases rather than silently omitting them.
The navigation adapter now loads the full model dependency closure instead of its
former two-file subset, which cannot resolve a canonical project document.
The challenge-independence test validates the actual native challenge declaration
under its canonical owner wrappers without vehicle or project-library sources.
Publication restores compact common-namespace labels only through unique native
identities; ambiguous suffixes fail explicitly, and queried dependency edges are
preserved without changing model relationships.

Seven generated evidence projections now update only their explicitly bounded
sections. The writer rejects duplicate, missing, reversed, overlapping or injected
markers, preserves surrounding bytes, and avoids rewriting unchanged content.
Each generator has a read-only `--check` path. Current bindings use canonical
IDs; accepted legacy generator arguments redirect to the appropriate section.
Standalone export containers remain available. Archived replay uses archived
source names deliberately, and recorded evidence retains its original provenance.

Consumers using old project qualified names or deleted source paths must migrate
using the mapping. No runtime aliases are supplied. Search/vector/solver limits
documented by the preceding declarative refactor remain; this change does not
claim total declarativity or new physical engineering evidence.

## Validation

The saved pre-migration native and numerical baselines were captured before
production assembly. Preparation passed before and after the migration. All nine
configured study runs and the named-configuration demonstration match exactly.
The initial real search problem retains all 297 inequality constraints, constraint
names, dimensions and state fields. Saved bounds, initial vector, equalities,
inequalities, design, states, routes and righting arrays have maximum absolute
difference **0**, checked at `rtol=1e-13`, `atol=1e-12`.

Seven audits have no errors and retain their baseline summaries: 257 requirements,
110 analysis cases, 100 verification definitions, 14 logical responsibilities,
28 logical exchanges and nine scenarios, with unchanged allocation counts.

Final results are **1,163 passed, one known baseline failure, zero errors and
zero skipped**, across all 80 isolated modules. The 38-page publication builds,
all seven projection freshness checks pass, all normalized native audit tables
match, and the positive nested-analysis discovery control passes. See
[the complete validation summary](validation-summary.json),
[final command results](checks-final/results.json) and
[the baseline wording control](../declarative-analysis-refactor/baseline-inline-control.json).
There are no unexpected failures. Initial failures and corrected reruns are both
retained; latest outcomes are aggregated per test identity.

The unchanged failure is
`tests/test_inline_views.py::test_inline_view_resolves_actual_refinement_and_statements`,
which expects the old “The vessel shall cross the configured Bingen departure”
wording. The preceding byte-verified baseline reproduces that assertion. The
isolated suite driver therefore returns failure until that unrelated assertion is
reconciled; it does not hide it as a pass or skip. The full suite runs in fresh
serial module processes with `GOMEMLIMIT=3GiB GOGC=50`, avoiding the prior
monolithic native-service out-of-memory failure. The preceding refactor review
already establishes the stale inline-view wording assertion as a baseline failure;
any present occurrence is distinguished from namespace regressions.

Reproduce from this worktree after the pinned tool bootstrap and locked sync:

```sh
uv run python -m tools.boat_analysis.cli prepare
uv run python -m tools.boat_analysis.cli study examples/studies/recovery.yaml
uv run python -m tools.boat_analysis.cli study examples/studies/sail-trade.yaml
uv run python -m tools.boat_analysis.cli study examples/studies/recovery-scenarios.yaml
uv run python reviews/namespace-restructure/validate_numerics.py
uv run python reviews/namespace-restructure/validate_native_identity.py
uv run python reviews/namespace-restructure/capture_audits.py
uv run python reviews/namespace-restructure/compare_audit_tables.py
uv run python reviews/namespace-restructure/run_isolated_suite.py
uv run python -m tools.publishing.build
```

Generator freshness commands are listed in the namespace reference. See saved
JUnit reports and timings for test execution, native audit artifacts for endpoint
tables, numerical comparisons for exact deltas, and baseline artifacts for the
original source fingerprints and values.

## Later SysPresent integration

No SysPresent files or bundled models were modified. A later explicit integration
must replace the old 76 project source documents with `models/blue-dog.sysml`,
retain the 20 library documents, and update dependent qualified IDs from the
mapping. Adding the canonical source alongside old project sources would create
duplicate declarations. Rebuild native exports and publication views after import.
No push, merge, deployment or upstream dependency publication was performed.


## Local worktree

The completed combined declarative refactor and namespace migration is in
`/home/david/repos/sv-blue-dog-namespaces`, branch `refactor/bluedog-namespaces`.
It descends from the clean `refactor/declarative-analyses` baseline. Existing
commits and authorship are retained; new work is committed as Codex. The original
editorial worktree and the clean declarative worktree remain untouched.

Namespace source commit: `ad26c68b7f01149cb207759cf390642c645ba514`. Validation records the tested working-tree
source fingerprints before this commit; model and runtime bytes are unchanged by
committing. The collection contains exactly 1,164 tests, matching the latest-result
aggregation. No production changes were made after the recorded passing checks.

Raw diagnostic logs and JUnit reports retain their original whitespace. The local
review attributes exempt those generated files from whitespace-only Git checks;
source and authored documentation still pass the normal whitespace checks.
