# Running the model calculations

I use a pinned revision of OpenSysML for the model engine, Python client and agent MCP server. Native analysis calls return typed values. The simulator executes the model's supervisory actions during the voyage and its outcome calculation when classifying the result. The numerical optimizer runs in SciPy, while the equations and acceptance criteria stay in SysML.

The same native engine supplies document queries and renders the scoped views in these articles. The publishing code handles narrative pages, navigation, interactive plots and the existing blog import. The numerical batch adapter remains useful for repeated compiled evaluations; it is a specialized bridge, rather than a second modeling framework.

For repeatable model analyses, I can save a standalone model snapshot with OpenSysML's native `AnalysisRecords`. Each record identifies its case, execution time, tool and outputs. The source models remain unchanged. For example:

```sh
uv run python -m tools.boat_analysis.cli record \
  --case BlueDog::Analyses::EnvironmentReview::FetchSensitivity \
  --case BlueDog::Analyses::EncounterReview::Acquisition \
  --output build/analysis/review.sysml
```

The saved model can be reopened with the same engine and queried through its Python client or MCP server. These records supplement the immutable archives for external simulations and optimizer campaigns; a recorded execution does not imply that a vessel requirement has been physically verified.

## Declarative studies

I use [validated YAML studies](declarative-studies.md) to select native analysis
cases by their model types and owners, bind named subjects and document external
scenario assumptions. The recovery demonstration discovers configured recovery
screens; the sail study discovers the current typed assessments. Engineering
equations, configured defaults and objectives remain in SysML. Reports retain
resolved identities and input/source provenance. Unit labels for plain scalar
inputs document their convention; they do not supply missing dimensional typing.

```sh
uv run python -m tools.boat_analysis.cli study examples/studies/recovery.yaml \
  --output build/analysis/recovery-study.json
uv run python -m tools.boat_analysis.cli study examples/studies/sail-trade.yaml \
  --output build/analysis/sail-trade-study.json
```

## Run the named integration candidate

[IC-01](../../models/blue-dog.sysml) owns the complete sizing design and its provisional integration assumptions, with design provenance in the immutable 15 October integration archive. The sizing adapter reads the model configuration and defaults to initial operating guesses from the 13 October SRR-readiness archive's `refinedReplay`; an explicitly supplied warm-start file can replace those guesses. Design values come from the named configuration, while warm starts supply numerical initial guesses.

```sh
uv run python -m tools.boat_analysis.mission.demonstration \
  --output build/analysis/ic01-demonstration.json \
  --records build/analysis/ic01-demonstration.sysml
uv run python -m tools.boat_analysis.model.audit \
  --output build/oosem-audit.json --archives
```

The demonstration executes native recovery analyses and feeds their feasibility outputs into the native recovery-versus-drift policy. It also records safe unassisted righting, capsize with low reserve and communications loss, and navigation degradation followed by safety loss. The JSON contains the configuration inputs, model and source hashes, revision, runtime revision, native analysis reports and timestamped behavior traces. The optional SysML snapshot contains official native analysis records. These are supplied-observation examples, not a full voyage or an installed autopilot.

The audit uses native queries for every governing requirement, derivation, dependency and impact path. Its JSON and Markdown distinguish current requirements, provisional study objectives, future applicability and defined verification objectives. Neither a link nor the audit itself executes a physical procedure or accepts evidence. Native verification verdicts are pass, fail, inconclusive or error; mission applicability separately identifies cases that do not apply. Archive checks reject altered registered records and unregistered run JSON in the supported manifest schema.

Use the locked environment and the pinned engine identified in [model conventions](../../models/README.md). An already synchronized environment can run the same commands with `.venv/bin/python` in place of `uv run python`. For MCP execution, select the same checkout and pinned revision used by the CLI and Python client.

SysML owns the equations. Python assembles geometry, chooses operating cases and coordinates the optimizer. All native calculations use the reusable library’s [execution backend](../../packages/sysml-python/sysml_python/backends/native.py). Mass, operating performance, structural margins, passage feasibility, route screening, surface/wave helpers, recovery segments, hull resistance and hydrostatics have declarative exports. Preparation reads argument order, Real types, dimensions and named output tuples from OpenSysML's API element export. Application wiring supplies friendly argument aliases and selects model-exported defaults; the generated interface supplies vector widths and output labels.

Mass, operating performance, structural margins, passage feasibility and route screening use declarative exports in [pyproject.toml](../../pyproject.toml). The [reusable SysML/Python library](../../packages/sysml-python/README.md) discovers their vector dimensions, delegates input-record generation to OpenSysML, evaluates model-owned defaults and compiles declared input checks. It still generates calculation-result wrappers for named return tuples. Surface and wave providers assemble external geometry and quadrature around generated calculations; the shared backend compiles those calculations. Named model results can be copied to arrays for NumPy operations. Geometry and interpreter reference experiments remain project-owned in the [reference preparation](../../tools/boat_analysis/model/preparation.py). Hydrostatic meshes use the same explicit batch API; the project sums the returned tetrahedron moments. Generated code and manifests remain build artifacts; fingerprints cover model and runtime sources.

OpenSysML generates frozen, slotted dataclass snapshots from `MarineDesign` for operating state, aerodynamic coefficients, hydrostatic inputs, appendage loads, mass properties and passage conditions, alongside `Design` and `Parameters`. These input records expose named fields and `to_mapping()`; NumPy conversion uses `as_array(record)` and `from_array(RecordType, values)` from `sysml_python.records`. The model declares the numerical field order; the boundary packs by field name, including for batches. Mass dictionaries are also packed by name, so insertion order cannot alter the physics. The surface-wind provider uses the same packing contract. Optimizer coordinates, mesh geometry and low-level numerical arrays remain arrays; these records describe quantities exchanged between domain calculations.

Scalar and batch calls share shape, finite-value, default and typed-record handling. Physical mass and operating preconditions are explicit SysML `InputChecks` calculations; the boundary executes them before evaluating the requested calculation. The pinned C generator omits assertions inside calculations, so these checks are compiled and called explicitly. A failed input group produces its model-defined name and, for per-case inputs, its batch index. These numerical preconditions are separate from vessel qualification requirements.

Meson builds all exported calculations and input checks together as separate shared libraries, selecting the host compiler, linker and library filenames. The runtime caches immutable build snapshots using the generated sources, wrappers, Meson recipe, compiler identity and flags. Calls sharing a loaded library use the same lock because OpenSysML's generated evaluator owns mutable execution state. Results are copied before that state can be reused. Hydrostatics uses the generated batch calculations with project-owned mesh reduction.

Independent cases can run in a native batch. Shared inputs and per-case inputs are explicit; there is no implicit broadcasting:

```python
result = operation.batch(
    shared={"design": design, "parameters": parameters,
            "aero": aero, "mass": mass, "hydro": hydro},
    cases={"state": states},  # (number of cases, 9)
    chunk_size=256,
)
# result.values columns follow the fields of generated OperationResult.
```

The C wrapper calls the same generated calculation for each row and copies its output immediately. It processes bounded chunks, preserves case order and reports the original case index on failure. With `errors="collect"`, native failures produce an error message and a NaN row; those rows must never count as feasible results. Malformed inputs and adapter precondition failures reject the batch before execution. A shared vector has shape `(width,)`; a per-case vector has shape `(cases, width)`. Scalar inputs use a scalar or a `(cases,)` array respectively.

Wing-strip load integration uses this path. Independent operating-condition sweeps can use it too. A nonlinear solver's next trial still depends on the previous result, and a mission trajectory still advances chronologically; batching does not remove those dependencies. Parallel studies can use separate worker processes, each with its own native state. The runtime itself does not create workers. Solves and mission operations use an execution session: model and generated-source fingerprints are checked before the first calculation and before the operation returns. Nested calculations share the snapshot, while numerical input checks still run on each call. Source edits invalidate the operation at exit. This avoids checking every source file for every wind strip or recovery segment.

Adding a supported calculation to the declarative library requires its SysML definition and an export declaration. It does not require a handwritten adapter or preparation function. The contract reader supports Real scalars, fixed vectors, and unbounded vectors whose size comes from a model-exported default. Unsupported schemas fail preparation. Physical preconditions are explicitly connected to their calculation; the generator does not infer engineering meaning. Hydrostatics uses the shared native batch loop, with mesh assembly and reduction in project geometry code. Resistance-domain screening is a project-owned policy over generated, named model results; it contains no compiler or ABI setup.


[Modeling method](../methods/modeling.md) · [Contributor guide](authoring.md)

## Mission actions and records

The architecture audit checks native scenario ownership, logical responsibility allocations, logical exchange coverage, mapping scopes and IC-01 configuration bindings:

```sh
uv run python -m tools.boat_analysis.model.architecture_audit --output build/architecture-audit.json
```

The [architecture article](../architecture.md#logical-responsibilities-and-the-candidate-boat) renders the same native queries as tables. Coverage includes all current scenario steps and logical exchanges; it does not establish correct controller scheduling, installed transport, authority arbitration or physical independence. Unresolved interfaces remain in the correspondence model. The audit does not reclassify historical analyses as IC-01 studies.

The [mission supervisor](../../models/blue-dog.sysml) executes through OpenSysML's native action API. `HandleEvent` determines the response to an observation or intervention. `SupervisoryCycle` determines sailing, gate-scoring and harvest permissions, operating mode, persistent abort and qualification state, and whether an abort alert is attempted or queued. `RecoveryAuthority` permits recovery after primary steering or power loss only when an explicitly independent, powered path is supplied. `FallbackPolicy` decides whether the available, permitted recovery path can be attempted or the vessel must continue drifting. Dependencies connect these actions to the logical scenarios. Supervisor and capsize decisions are allocated to logical supervision; recovery authority and fallback decisions are allocated to logical recovery management. Named candidate mappings distinguish the primary supervisor's sailing permissions from the recovery controller's qualification restrictions and fallback authority. Primary-loss startup, peer timeout and authority arbitration still need implementation and evidence.

Python supplies observations, computes chart and traffic geometry, ranks feasible headings and integrates motion and energy. It dispatches the action outputs to those mechanisms. The supervisor's traffic mode identifies a predicted encounter; avoidance geometry and maneuver selection remain conceptual Python calculations. This is a partial executable logical architecture, not a complete autopilot or a verified sensing system.

The capsize path requires explicit observations: safety functions remain available
while inverted, then unassisted righting restores upright operation. Between
those observations the simulated boat drifts with the current, consumes energy
and remains exposed to chart and traffic hazards. It cannot sail, score gate
crossings or collect solar energy. Missing safety evidence triggers abort. This
tests the qualification policy; it does not predict righting dynamics or supply
evidence that the physical boat can recover.

Each result includes `logic_trace`, with the action name, simulation time, input facts and output decisions for events and changed supervisory decisions. The abort latch and memoized pure action results are scoped to one simulation. Execution sessions check model provenance, and campaign records include the source hashes. These records support explaining a simulated decision; they do not establish physical capability.


## Reproducing mission campaigns

Run the original conceptual campaign with `uv run python -m tools.boat_analysis.mission.campaign --count 32`, or add `--candidate build/analysis/sizing-continuation.json` for a freshly checked sizing result. It records the model inputs, source hashes, seeds, generated traffic counts, gate events and chronological histories. The numerical horizon can be extended without turning incomplete observations into failures.

Forecast-service loss and forecast invalidity are separate scenario events. A service outage alone preserves the qualifying attempt; a forecast declared no longer applicable triggers autonomous recovery. A manually supplied weather update disqualifies the attempt. These cases exercise mission policy; they do not yet validate a forecast-applicability estimator or an operational weather-service integration.


## Reproducing the IC-01 integration

Prepare the pinned model/runtime inputs, then run the allocated sizing and mission phases:

```sh
uv run python -m tools.boat_analysis.cli prepare
uv run python -m tools.boat_analysis.mission.integrated --phase all
```

The sizing phase supplies a freshly evaluated candidate to the mission phase. Records retain model and driver hashes, trajectories, both energy accounts and acceptance facts. An explicitly supplied warm start can accelerate the solve; it is reevaluated before becoming acceptance evidence.

For installed sensing inputs, the [measurement format and importer](sensing-measurements.md) records the pipeline identity, synchronized observations and power, source hashes and any base electronics load replaced by shared compute. Synthetic regression fixtures remain labeled `synthetic-test`; they do not qualify hardware.

## Consumer gates and qualification restoration

`BlueDog::Behavior::Contracts` supplies partial native action contracts for observation usability, sailing actuation, recovery motor enable and qualification restoration. Observation assessment reuses the typed interface predicate. Applicability, authority, physical availability and durable-record inputs require established evidence; the actions do not infer them from connectivity. `MissionLogic.restore_qualification` executes the native restoration policy and records its inputs and result. It preserves a live disqualification and applies the nonqualifying fallback to an invalid record. This API restores qualification only, without claiming a complete watchdog/storage implementation or deadline verification.

The recovery scenario explicitly orders durable disqualification acknowledgment before actuation. The post-actuation record describes observed execution disposition, not a predicted shore arrival. Native regressions test each motor barrier, unknown state, missing acknowledgment, expired command/permission and fault restoration. The conceptual simulator still supplies scalar observations and does not implement the candidate message serialization, storage protocol or hardware interlocks.

## Verification planning audit

```sh
uv run python -m tools.boat_analysis.model.verification_audit --output build/verification-audit.json
```

This native audit inventories project verification definitions, method metadata, objective links and planned IC-01 integration configurations. It executes no case and makes no acceptance decision. The publication method register uses the same query. Empty actual-article, procedure and instrument fields identify evidence gaps. Three numerical verification definitions require supplied subjects; querying their result without inputs is an error, not a default success. The separate eligibility calculation evaluates supplied review assertions and cannot replace evidence inspection or acceptance.

Audit the initial Gorge hazard argument with
`python -m tools.boat_analysis.model.safety_audit --output /tmp/safety-audit.json`.
It groups native-resolved contributor/control/verification endpoints and executes
the native FMEA and hazard review preconditions. Six unresolved hazard records
are expected. Neither the inventory nor review flags accept risk or prove control
effectiveness; acceptance records and actual authority remain separate inputs.

## Configuration and accounting audit

`python -m tools.boat_analysis.model.configuration_audit --output /tmp/configuration-audit.json`
uses native contexts, ownership/type queries, quantity bindings and AccountingReview.
It inventories all top-level MarineDesign design/parameter parts separately from
nested references, plus historical and synthetic accounting contexts. Bound values
retain their existing owners and units. Unmeasured peaks and actual article/revision
records remain missing; a readiness assertion does not inspect evidence or accept
a configuration. The same native tables appear in architecture and energy articles.

### Analysis applicability and provenance

Run `python -m tools.boat_analysis.model.credibility_audit --output build/analysis/credibility-audit.json`
for native intended-use coverage of definitions and configured usages. This reports
scope and missing metadata, not physical validation. The model's use/limitations
register supplies the domain and next evidence for interpreting each category.

`input_record` and `input_path` require a current workspace result for generated analyses and
validate both recorded source and driver hashes. The two registered CAD/polar assets have a centrally declared reference role, preserving unchanged historical geometry consumers. An explicit current role always forbids fallback. `purpose='reference'` is limited
to the registered wing geometry/polar assets; `purpose='initial_guess'` is limited
to the historical fixed-design seed. Explicit historical `run_record` preserves
manifest byte checks and original-revision verification. Do not relabel a reference
or seed as a current design result. Regenerate stale current results with their
producer. Native `record_analyses` writes the native AnalysisRecords snapshot and
an adjacent `.provenance.json` with actual source/model, driver and executable
fingerprints. Compare its recorded-model digest before interpreting the companion.

### Decision and trade applicability

Run `python -m tools.boat_analysis.model.decision_audit --output build/analysis/decision-audit.json`
for the native inventory of 20 decision-record items, 80 allocation/procedure review
annotations and declared rig criterion basis. It checks item kinds, record states,
metadata inheritance and register coverage, including the six retained design-basis
records. It executes the three existing unknown-evidence assessments, not physical
verification or a weighted hardware downselect. The seven-entry legacy evidence
vector retains its order: entries1-6 are declared mandatory groups; entry7 is the
provisional reliability study. `qualified` is retained as a compatibility name for
`declaredMandatoryGatesMet`, not physical qualification. Inspect study disposition
separately and establish evidence adequacy and full system acceptance before use.

Native TradeStudies examples in the decision skill use synthetic numbers solely
to check scalar selection, ties and missing inputs. A native selectedAlternative
may be the first among equals; inspect every evaluation/error/tie and assess
admissibility before interpreting it as a recommendation. No production rig scores,
weights, accepted reliability rates or actual selection are supplied by those examples.
