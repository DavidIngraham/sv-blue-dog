# Declarative analysis refactor — local validation

Implemented in `/home/david/repos/sv-blue-dog-declarative`, branch
`refactor/declarative-analyses`. Refactor commit: `3d9280d2d97051af1ea5c2d18e36ae9d239dd193`.
No push, PR, merge, deployment, dependency publishing or SysPresent integration.

## Source and preservation

The authoritative source was `/home/david/repos/sv-blue-dog-editorial` on
`refactor/oosem-system-model` at `b94b6e0`, with extensive pending model,
audit, analysis and editorial work. The Windows checkout was older (`f59cf12`).
Snapshot `9c8878f` preserves all 860 tracked/non-ignored source files, including pending work,
separately from this refactor, with repository-owner attribution. The original
branch, HEAD, dirty status and source bytes were verified unchanged; see
[preservation evidence](original-preservation.json) and [baseline](baseline.json).
The isolated environment reuses only the pinned tool installation by symlink;
mutable preparation outputs and the Python environment belong to this worktree.

## Architecture and migrated scope

`studies/config.py` validates safe YAML with a strict, versioned Pydantic schema
before model loading. `studies/runner.py` resolves exact native IDs and semantic
type/owner/general queries, rejects empty or ambiguous selections, preflights
bindings and delegates every calculation/objective to native OpenSysML. Scenario
overrides require explicit rationale. Native reports retain objective verdicts,
diagnostics, outputs, selected/tied trade evaluations and available evidence
strength. Execution errors and failed objectives remain different outcomes.

Provenance records raw and validated configuration hashes, selected IDs, subjects,
native attribute facts/defaults/units, external assumptions, model/source/driver
hashes and pinned runtime/executable identity. Changed source/configuration or an
injected snapshot on another native connection is rejected. JSON projects native
results; native AnalysisRecords remain the recording mechanism.

The recovery demonstration discovers configured RecoveryScreen usages from
`examples/studies/recovery.yaml`. Its API/CLI, old native-report shape, supervisor
traces and optional records remain available; the old CASES tuple is import
compatibility only. Sail-trade YAML discovers typed assessments and selects the
independent buoyancy sensitivity. A third example supplies explicit hypothetical
scalar recovery assumptions. New CLI: `python -m tools.boat_analysis.cli study`.

The numerical search discovers model-exported design/parameter names, generated
state fields and operating-case counts. It replaces fixed dimensions and several
positional indices while preserving its numerical procedure. Existing generated
calculation exports and Python numerical kernels remain in place. No SysML
formula, acceptance constraint or physical operating policy changed.

## Validation

| Check | Actual result |
| --- | --- |
| Preserved-baseline preparation and representative tests | 94 passed; 509.90 s for tests |
| New focused schema/discovery/CLI/search checks | 49 passed |
| Full repository attempt in one process | 829 passed, 40 failed, 277 errors, 0 skipped; 1454.48 s; native service killed by OS for memory use |
| Fresh serial reruns of affected modules | All seven modules pass with GOMEMLIMIT=3GiB and GOGC=50; 1145 distinct checks pass across the full run and reruns, with one unchanged assertion remaining |
| Migrated real native studies | Nine study runs match all eight baseline case projections exactly |
| Recovery demonstration | Numerical outputs, configuration inputs and behavior traces exactly match baseline |
| Real search initialization/evaluation | Zero difference in bounds, initial state, operating results, routes and 297 constraints; tested rtol=1e-13, atol=1e-12 |
| Synthetic extension | Same YAML selector discovers an added native configuration and analysis usage; no registry/kernel edits |
| Native preparation and publishing build | Passed; logs retained alongside this report |

The long-run native service was killed by the OS at approximately 8.26 GiB RSS,
invalidating subsequent checks. [Kernel evidence](long-run-oom.txt) records the
actual kill; earlier repository logs also showed the resulting connection-refused
pattern. No unrelated process was stopped and no dependency/runtime patch was
introduced. The seven affected modules pass in fresh serial processes using a
3 GiB Go heap target and GOGC=50. See [rerun evidence](affected-reruns.json).
The monolithic default-memory run is not green; bounded process lifetime remains
necessary until the native service's retention behavior is addressed separately.

The one persistent assertion failure is
`tests/test_inline_views.py::test_inline_view_resolves_actual_refinement_and_statements`:
its expected requirement wording is stale. The baseline control verifies the
test, authored page, model files and publishing/runtime sources against `9c8878f`
and reproduces the same assertion from that baseline implementation. See
[control](baseline-inline-control.json), [full log](refactor-full-tests.log) and
[JUnit](refactor-full-tests.xml). It is left separate from this analysis refactor.

| Native numerical result | Before | After |
| --- | ---: | ---: |
| Upright recovery required energy (Wh) | 12.545454545454543 | 12.545454545454543 |
| Inverted recovery required energy (Wh) | 98 | 98 |
| Positive buoyancy moment (Nm) | 98.0665 | 98.0665 |
| Negative buoyancy moment (Nm) | -98.0665 | -98.0665 |

All comparisons are software/model regression evidence. They add no measured
model validation or physical qualification. The generated native record snapshot
is `.tools/demonstration-refactor.sysml`, with its provenance companion. The
runtime is `23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2` (Go 1.25.11); see
[actual runtime version](runtime-version.txt). Pydantic remains locked at 2.14.0;
the only added package is PyYAML 6.0.3. No project type-checker configuration was
present; schema/runtime types and Python imports were exercised by tests.

## Reproduce

Use the locked environment and pinned tool bootstrap in AGENTS.md. In this
prepared worktree, `.venv/bin/python` is sufficient; the cached uv executable is
`/home/david/repos/sv-blue-dog-editorial/.tools/uv`.

```sh
cd /home/david/repos/sv-blue-dog-declarative
.venv/bin/python -m tools.boat_analysis.cli prepare
.venv/bin/python -m tools.boat_analysis.cli study examples/studies/recovery.yaml --output build/analysis/recovery-study.json
.venv/bin/python -m tools.boat_analysis.cli study examples/studies/sail-trade.yaml --output build/analysis/sail-trade-study.json
.venv/bin/python -m tools.boat_analysis.cli study examples/studies/recovery-scenarios.yaml --output build/analysis/recovery-scenarios-study.json
.venv/bin/python -m tools.boat_analysis.cli study --schema --output build/analysis/study.schema.json
.venv/bin/python -m pytest --durations=30 --junitxml=.tools/refactor-full-tests.xml
.venv/bin/python reviews/declarative-analysis-refactor/rerun_affected.py
.venv/bin/python -m tools.publishing.build
PYTHONPATH=. .venv/bin/python reviews/declarative-analysis-refactor/compare_search.py
PYTHONPATH=. .venv/bin/python reviews/declarative-analysis-refactor/demonstrate_addition.py
PYTHONPATH=. .venv/bin/python reviews/declarative-analysis-refactor/baseline_inline_control.py
```

`validate_migration.py` compares the real studies against
`.tools/numerical-baseline.json` and `.tools/demonstration-baseline.json`; the
original captured copies are retained here for replay if those cache files are
missing. Full reports/schema are in `build/analysis`; compact numerical evidence
and comparison drivers are committed in this folder.

## Remaining limits

- Scalar YAML overrides only; vectors/records, custom/native dimensional values
  remain in model configurations/generated interfaces. Unit labels on plain Real
  inputs are provenance, with no inferred conversion or dimensional validation.
- Native reflection lacks a complete direction/required-input contract. Native
  execution validates actual argument direction and missing/default bindings.
- Route arity, direction/tack topology, some geometry/route vector positions and
  state-bound semantics still require stronger native contracts before safe reuse.
- Solver controls, seed adjustments, diagnostic scaling, hypothetical supervisor
  events and legacy campaign orchestration remain Python responsibilities. No
  measured uncertainty or absent metadata has been invented.
- The stale inline-view assertion above remains a pre-existing suite failure.
- A single long default-cache native service can exhaust available memory. Fresh
  serial processes with the recorded Go memory settings pass the affected tests;
  service memory retention is an unresolved dependency/test-runtime limitation.

See [schema/migration documentation](../../docs/reference/declarative-studies.md)
for extension points, defaults, examples and the explicit hard-coded boundaries.
