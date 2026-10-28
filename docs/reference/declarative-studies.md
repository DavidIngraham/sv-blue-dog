# Declarative native analyses

A study describes which model analyses to execute and, when needed, which named
subject and external scenario assumptions to supply. OpenSysML owns analysis
inputs, defaults, engineering equations, objectives and verdicts. The existing
`sysml-python` export declarations still own generated numerical adapters;
SciPy, geometry and quadrature remain reusable Python algorithms.

```sh
uv sync --locked
uv run python -m tools.boat_analysis.cli study examples/studies/recovery.yaml \
  --output build/analysis/recovery-study.json
uv run python -m tools.boat_analysis.cli study examples/studies/sail-trade.yaml \
  --output build/analysis/sail-trade-study.json
uv run python -m tools.boat_analysis.cli study examples/studies/recovery-scenarios.yaml \
  --output build/analysis/recovery-scenarios-study.json
uv run python -m tools.boat_analysis.cli study --schema \
  --output build/analysis/study.schema.json
```

The schema is generated directly from `StudyConfig`, with no hand-maintained
second schema. Pydantic validates the entire YAML before loading a model.
Unknown fields, unsupported schema versions, wrong scalar types, duplicate YAML
keys and unsafe YAML constructors fail. The loader includes the configuration
path and nested field location in validation errors.

## Selections and bindings

```yaml
schema_version: 1
name: Current rig assessments
groups:
  - name: contenders
    select:
      kind: AnalysisCaseUsage
      owner: BlueDogSailTrade
      type: BlueDogSailTrade::TradeAssessment
      cardinality: many
```

Selectors use exact native IDs or semantic native queries. An ID cannot be
combined with query filters. Query filters are combined with AND; `owner` is
the direct native owner, `type` is the resolved usage type and `general` is a
definition's specialization. They do not search source text or guess by name.
`cardinality: one` is the default and rejects ambiguity; `many` requires at
least one match. Results are sorted by native ID, so adding a new typed usage
under the selected owner includes it without changing Python or the YAML list.
Definition selectors intentionally execute the selected definition; usage
selectors retain their model bindings and defaults.

`subject` accepts the same selector with cardinality one. Omit it to preserve
the native subject binding. A new subject does not override model applicability
constraints: IC-01-only analyses still reject another vessel configuration.

Each group defaults to one scenario named `default`, with no overrides.
`examples/studies/recovery-scenarios.yaml` shows explicit scalar assumptions:

```yaml
scenarios:
  - name: diagnostic
    arguments:
      distanceM:
        value: 600.0
        unit: m
        rationale: Hypothetical reach, not measured course geometry.
```

Every override requires a rationale. The runner checks supplied names and
supported scalar types against native attribute facts, then delegates actual
argument binding and required-input checks to OpenSysML. Booleans are not
accepted as numbers and strings are not coerced into numeric inputs. Native
defaults remain model values; absent required inputs fail rather than becoming
zero. Unit labels document the supplied scalar convention. They do not add
dimensional typing or automatic conversion to the existing SI scalar model
interfaces. Use the exact convention declared by the selected model input;
unknown native units stay unknown. Record-valued and vector-valued YAML
overrides are not supported in this first schema; use model configurations.

## Results and provenance

Native results retain outputs, constraints, diagnostics and objectives. A model
output such as `reserveFits: false` remains a valid calculation result; it is
not the same as an execution error. `require_holds` defaults to true: a failed
native objective rejects the study while retaining its report on the Python
exception. Set it to false for a deliberate adverse-control group. No setting
accepts physical evidence or changes the model's constraints.

`run_study(path)` returns native reports and numerical output conveniences keyed
by group/scenario/case ID, with provenance describing the exact selectors,
resolved IDs, subjects, input facts, assumptions, configuration hash, model hash,
source hashes, driver hashes and pinned runtime. Sorted discovery and configured
scenario order determine execution order. Separate calls bind fresh inputs.
The report is orchestration output; native `AnalysisRecords` remain the model's
recording format. The existing `cli record` command saves bound model cases.
It does not capture YAML scenario overrides, so do not relabel a recording of a
default case as evidence for a separately overridden scenario.

The existing recovery demonstration now discovers all configured `RecoveryScreen`
usages from `examples/studies/recovery.yaml` and uses their native outputs in its
supervisory traces. Its module API, CLI, report fields and optional native records
remain available. `CASES` is retained only as an old import compatibility tuple;
it no longer selects execution. Existing behavior examples remain explicitly
hypothetical supplied observations.

## Extension boundaries

Add a model usage/configuration to extend an existing typed study. Add a new YAML
group when the question requires another analysis type or native subject. Add an
export in `pyproject.toml` for a reusable generated numerical calculation. Add
Python only for a numerical algorithm, geometry/data adapter or a new supported
native interface shape. YAML accepts neither expressions nor importable Python
callables; there is no `eval`, plugin registry or second relationship engine.

The search adapter discovers design/parameter indices, state record dimensions
and operating-case count where native interfaces expose them. It still implements
its numerical optimization procedure. The following boundaries remain explicit:

| Remaining assumption | Why it remains |
| --- | --- |
| Windward/leeward and both-tack search topology | The current route calculation accepts that particular ordered interface; no model contract declares arbitrary route topology. |
| Route/geometry result positions and some legacy campaign arrays | Their semantic field contracts are incomplete; guessing from labels would change model meaning. |
| Solver methods, stopping tolerances, discretization and initial-guess adjustments | Numerical algorithms require these choices; they are not vessel facts. They have not all been migrated to YAML. |
| Hypothetical supervisor events and bounded campaign conditions | They are deliberate examples rather than discovered observations or measured distributions. |
| Archived aerodynamic/geometry references and numerical warm starts | Their provenance and allowed purpose are explicit; discovery cannot establish physical applicability. |
| External scalar unit labels | Some native inputs are plain `Real`; dimensional metadata and conversions cannot be invented. |
| Scalar-only YAML overrides | Native records and vector inputs already have model/generated adapters; a second packing framework is unnecessary. |

This architecture removes repeated native-analysis orchestration and selected
array assumptions. It does not make the full voyage simulator or optimizer
entirely declarative, establish model validation against measurements, or qualify
the hardware.
