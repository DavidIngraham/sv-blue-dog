# Independent Gorge Challenge

`GorgeChallenge` is a standalone top-level namespace in
`models/gorge-challenge.sysml`. Blue Dog adopts its rules through native
references. The independent challenge does not depend on a particular boat.

The correction starts from published main `e73d45624e9eedafc79f22f8559219195e9b313d`
in isolated worktree `/home/david/repos/sv-blue-dog-gorge-challenge`, branch
`fix/standalone-gorge-challenge`. The original dirty editorial checkout and all
completed declarative and namespace worktrees remain preserved.

| Scope | Ownership |
| --- | --- |
| `GorgeChallenge` | Independent entry and qualification requirements, their derivations, nonbinding guidance and the 1.2 m maximum vessel length |
| `BlueDog::Mission::Course` | Boat-project course proposal, chart snapshot, gate offsets, routing margins/grid and sizing-distance binding; not an accepted organizer course or universal entrant policy |
| `BlueDog::Mission::Scope` | Blue Dog mission choice and current/future applicability annotations |
| `BlueDog::Requirements` | Boat allocations and interpretations, including the provisional LTE-M technology issue moved out of the independent rule |
| `BlueDog::Verification::Challenge` | Planned boat qualification cases, not accepted evidence |
| `BlueDog::Analyses` | Project-specific engineering studies and bindings |
| `Analysis` and five mixed/domain libraries | Existing shared numerical and domain contracts, unchanged |

All **14,933 native elements** survive under their mapped identities with the
same native kind, mapped owner, type and generalization. No declaration is added,
lost or duplicated. Total package count remains **115**; top-level packages are
now **8**, across eight sources. All six shared library files retain their exact
bytes, including the `Analysis` grouping.

The [prefix mapping](namespace-map.json) and [complete element mapping](element-id-map.json)
cover 401 moved identities. The exceptional mapping moves the existing
`LiveObservation::issue` metadata and its child to
`BlueDog::Requirements::Communications::monitoringTechnologyIssue`; it is a
boat technology assumption, not a challenge technology mandate. No old namespace
alias remains. Native export keys and project YAML study selectors retain their
identities; active references in queries, Python, fixtures and publication views
are rebound to `GorgeChallenge`.

Explanatory references from the challenge back to Blue Dog's course and
verification cases are expressed in entrant/attempt terms. The concrete boat
verification explanation stays in the existing Blue Dog verification package.
Normative rule statements, identifiers, thresholds, qualification behavior and
acceptance flags are preserved. No independent course geometry is invented from
the boat's still-unaccepted proposal. Organizer acceptance and actual physical
verification remain outstanding engineering work.

The pinned native editor cannot rewrite secondary documents. The migration
stages the full model in a single in-memory primary source, moves and renames the
existing declarations natively, then splits the eight roots through native edit
ranges and reparses them strictly before installation. It does not introduce a
second SysML parser or relationship engine. The complete standalone challenge
parses strictly without a fake `BlueDog` wrapper or any marine library source.

Verification includes:

- Native identity, owner/type/generalization and normative rule-statement comparisons.
- Standalone challenge loading, native length checks and missing-input behavior.
- A realistic unresolved boat-reference probe that the native parser rejects.
- Native dependency tables proving challenge dependencies stay internal and boat
  dependencies point toward challenge requirements.
- Nine study runs, the configured mission demonstration and all 297 search
  constraints: exact report equality after ID mapping and maximum absolute
  numerical delta **0** (`rtol=1e-13`, `atol=1e-12`).
- Complete normalized tables from seven audits: **zero differences**, diagnostics
  or errors. Changed source/model hashes are recorded as provenance, not hidden
  as unchanged numerical facts.

The numerical/audit baseline reuses the validated published source only after
checking all seven original source SHA-256 hashes against its recorded results.
Historical evidence and previous review reports remain frozen. The isolated suite passes **1,169 tests in 81 modules**, and all **33 reusable
runtime tests** pass with the pinned native compiler, without skips. Generator
freshness, the seeded mission campaign, five figure generators, Python compilation
and the **38-page** publishing build pass. Detailed local results are recorded in
`validation-summary.json`; exact main CI/Pages results are in the external
publication handoff.

Reproduce with the repository's pinned runtime and locked environment:

```sh
uv run python -m tools.boat_analysis.cli prepare
PYTHONPATH=. uv run python reviews/standalone-gorge-challenge/validate_native.py
PYTHONPATH=. uv run python reviews/standalone-gorge-challenge/validate_numerics.py
PYTHONPATH=. uv run python reviews/standalone-gorge-challenge/capture_audits.py
uv run python reviews/standalone-gorge-challenge/compare_audit_tables.py
uv run python -m tools.testing
PYTHONPATH=. uv run python reviews/standalone-gorge-challenge/run_publication_checks.py
```

Use `GOMEMLIMIT=3GiB GOGC=50` for native checks. The regression driver supplies
these defaults and isolates each module's native service. There is no configured
separate static type checker; Python compilation and tested runtime contracts
provide the applicable checks.

For SysPresent integration, use the complete eight-file payload: replace
`models/blue-dog.sysml`, add `models/gorge-challenge.sysml` and retain all six shared
library files. Apply the explicit ID mapping to external consumers. This task
does not modify SysPresent. The payload and model hashes are stable before its
independent integration, and any later model-byte change requires coordination.

The first complete local run found one stale assertion in
`test_namespace_structure.py`: it classified every non-library source as a boat
source. The corrected test explicitly checks separate `BlueDog` and
`GorgeChallenge` source roots. Its three tests pass on rerun; the other 80 modules
passed in the complete run. Original failure evidence is retained under
`initial-regression/`, with the rerun in `targeted-rerun.json`. No model or runtime
change was needed. Main CI subsequently provides the clean complete-run gate.
