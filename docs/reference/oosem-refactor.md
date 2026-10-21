# OOSEM model integration and validation record

Assessment: 20 October 2026. Baseline: `b12b079`; work branch: `refactor/oosem-system-model`. The [system concept](../architecture.md), [current assessment](../current-assessment.md) and [model conventions](../../models/README.md) describe the resulting engineering model. This record accounts for the refactor, its evidence and its limits. It is not a vessel qualification record.

The [saved run manifest](../../evidence/runs/2026-10-20-oosem-refactor/manifest.json) identifies source commit `9ab77ad` and protects the [coverage, relationship and impact register](../../evidence/runs/2026-10-20-oosem-refactor/oosem-audit.json), [IC-01 execution](../../evidence/runs/2026-10-20-oosem-refactor/ic01-demonstration.json), [exact numerical comparison](../../evidence/runs/2026-10-20-oosem-refactor/oosem-numerical-comparison.json), baseline values and [validation record with test logs](../../evidence/runs/2026-10-20-oosem-refactor/validation-summary.json). The audit ran before the source commit and retains its honest modified-tree execution identity; the manifest verifies its actual source fingerprints against the committed refactor. The demonstration and numerical comparison were repeated after that commit.

## Engineering result

The model connects the finite Gorge mission to typed operational scenarios, implementation-independent responsibilities, a provisional physical assembly, native supervisory decisions, a complete named candidate and verification objectives. The original subsystem/context tree remains useful and retains its identity. Separate logical and physical packages now express the distinctions that the mixed tree could not carry by itself.

The review covered missions, all vehicle models, 35 analysis documents, 19 reusable libraries, the existing nine configuration documents and seven evidence projections, together with execution, numerical adapters, evidence handling, tests and publishing. The named IC-01 configuration adds one model document. The reusable libraries retain no project-specific reverse dependencies. Established numerical formulations and useful historical structures were retained where the review found no engineering reason to replace them.

| Layer | Implemented change | Meaning and remaining limit |
| --- | --- | --- |
| Mission and requirement basis | Preserve all 251 IDs; separate 237 current requirements, two study objectives and 12 future statements; correct four false derivations and print-envelope refinement. | No new acceptance number or mission rule. See the complete [requirements audit](oosem-requirements-audit.md). |
| Operational behavior | Nine typed scenarios cover sailing, navigation, traffic, outage, reserve protection, capsize, abort/recovery, launch and maintenance. | Inputs, results and responsibility allocations are explicit. Descriptive action steps are not automatically executable controllers. |
| Logical architecture | Separate navigation, wind, safety, traffic observation, collision assessment, boundary assessment, energy, supervision, guidance, actuation, recovery, recording and communications. | Typed observations carry validity and time; permissions and commands cross native flows. Physical assignment is separate. |
| Physical architecture | A provisional IC-01 assembly identifies main/recovery banks, navigation, observation, controllers, sailing actuation, recovery propulsion, storage, telemetry and the wind installation. | Power/data exchanges are explicit. Bus protocols, ratings, common-cause isolation and storage/telemetry supply remain unresolved. |
| Executable supervision | Native actions own sailing, gate-scoring and harvest permissions, safety abort and persistent qualification loss. | Safe unassisted righting can preserve qualification; safety loss, motor use and intervention cannot be cleared by a later observation. |
| Configuration and analysis | `BlueDogIC01::design` owns all 29 sizing properties; `integration` owns capability assumptions. Named native recovery cases connect arithmetic to fallback policy. | Archived results supply numerical initial guesses only. The recovery screen explicitly rejects a different subject rather than mixing its design with IC-01 assumptions. |
| Verification and evidence | Add credible grouped objectives for all 16 current coverage gaps; native audit reports scope, relationships, impact paths and provenance. | Defined objectives are distinct from executed procedures, accepted evidence and physical validation. All physical gaps remain open. |

IC-01 remains the first intended integration candidate and scale for a refined physical build. Soft sail, tail-controlled rigid wing and directly rotated fixed-camber wing retain equal development standing. The old CAD testbed remains historical. The refactor supplies no new comparison that could justify selecting a rig.

## Relationship review across the model

The full native register contains 238 governing derivations, 19 refinements and 403 other dependencies at the integrated checkpoint. The requirement-only register uses a narrower scope: 238 derivations, nine refinements and 59 dependencies. Counts are inventories, not quality scores. Generated JSON retains every queried endpoint and declared rationale, including empty rationale for inspection.

| Relationship family | Disposition and engineering claim |
| --- | --- |
| Governing derivations | Retain justified original-to-derived obligations; replace reliability targets, selected upright-restoration strategy and universal battery protection links where implication was false. Parent satisfaction implies the child under its conditions; the reverse is not established. |
| Formal refinements | Retain explicit acceptance-predicate refinements; add the structural application of the shared print bound. Scenario refinements connect more detailed interactions to their use cases. |
| Satisfaction | Update 86 targets from coarse mixed-subsystem subjects to the relevant logical responsibilities. Retain system-level claims at the boat boundary where they require integrated evidence. These assertions remain unproved design claims. |
| Allocation | Allocate descriptive actions and executable supervisory policy to logical responsibilities, then map those responsibilities to provisional physical elements. Remove misleading logical-role annotations from the legacy mixed tree instead of inventing allocations to silence warnings. |
| Interactions | Add native typed ports and flows for observations, permissions, commands, records and power. A supporting dependency is not used to represent message transport. |
| Analysis, trade and evidence dependencies | Retain general change-impact relationships where they identify an assumption, scenario, requirement, decision or evidence basis. They do not claim satisfaction or carry values; named subjects, expressions and typed bindings carry analysis inputs. |
| Future mission basis | Preserve future repeating operation's use of the course geometry as a dependency, with explicit rationale. It does not impose indefinite endurance on the finite Gorge attempt. |

The [requirements report](oosem-requirements-audit.md) contains the changed-ID accounting and full quality dispositions. No IDs were removed, split or reassigned. The [conventions](../../models/README.md) identify the OMG and INCOSE sources used and their access limits. Neither parsing success nor this review certifies all engineering judgments as correct.

The non-requirement review retained these relationship families deliberately:

| Domain and representative endpoints | Basis for retaining the relationship |
| --- | --- |
| Sizing: `MassProperties` → `liftMass`; `DesignMargins` → `structuralIntegrity`; `Route` → `legProgress` | Analysis purpose and sensitivity to the referenced obligation; expressions and subjects supply the actual calculation. |
| Energy/reliability: `SustainedOperation` → `sustainedReserveProtection`; `CruiseReliability` → `passageDuration` | Conditional study context, alongside separate executable criteria and verification objectives. |
| Environment/recovery sites: proposed profiles → Gorge wind/waves; Bingen approach → course recovery reserve | Unaccepted environmental applicability and candidate-site investigation. |
| Mission/navigation: `MissionOutcome` → course completion/unassisted attempt; encounter policy → navigation duties | Outcome-policy traceability; dependencies do not establish rule compliance. |
| Sensing/encounters: class-detection policy → traffic safety; acoustic budget → integration hypothesis | Study purpose and configuration-sensitive budgets; historical hypotheses remain distinct from current acceptance policy. |
| Equipment: existing `controllerAllocation` and `logicalAllocation` dependencies | Budget attribution and candidate correspondence. Despite their legacy names, they are general dependencies, not SysML allocations. The new architecture uses actual `allocate` statements. |
| Rig/propulsion: trade assessments → self-righting; recovery sizing → recovery energy | Open trade criteria, without selecting a winner or asserting physical feasibility. |
| Failure/risk models: DFMEA → design/criteria; development risks → analyses/decisions | Scope and investigation links. Native causal connections carry failure causation; neither family supplies measured failure probability. |
| Historical evidence → source studies and current method references | Provenance and interpretive context. Original source revisions govern each result; a later link does not rerun an archive. |

Reusable domain calculations such as `MarineRecovery::Segment` and `MarineActuation::DrivePower` retain no Blue Dog dependencies. Their project wrappers carry mission-specific purpose and configuration bindings.

## Reproducible execution and impact analysis

The [runtime instructions](model-runtime.md#run-the-named-integration-candidate) generate the demonstration, coverage JSON/Markdown and optional native analysis-record snapshot. The outputs identify the named configuration, model hash, source hashes, source revision, modified-tree status and pinned runtime. A modified working tree is reported rather than mislabeled as the baseline commit.

The supplied four-hour, 600 m recovery illustration leaves 43 Wh in the independent bank. Upright recovery against 0.4 m/s current requires 12.545454545454543 Wh and fits that reserve. Inverted recovery at the assumed 0.5 m/s through-water speed requires 98 Wh and does not fit. Opposing current equal to the allocated 1.5 m/s recovery speed produces no upstream authority. All three native calculations can complete successfully; their `routeFeasible` and `reserveFits` results distinguish engineering feasibility from calculation completion. No case establishes a safe physical approach or shore retention.

Native behavior traces exercise safe unassisted righting, capsize plus reserve threat and lost communications, navigation degradation followed by safety loss, and recovery versus drift from those numerical outputs. The simulator also tests interacting faults and both orders of simultaneous navigation observations. A later safe observation cannot erase earlier loss. Reserve exhaustion now always invokes the native safety-abort latch, including default runs without a recovery planner; previously those runs ended as incomplete. Continuation settings control subsequent modeled motion, not qualification.

Useful native impact paths include:

- `capsizeQualificationRetention` → incoming verification → `CapsizeControlRecoveryVerification`.
- The same requirement → incoming satisfaction → `LogicalVessel::supervision` → outgoing allocation → `IC01Candidate::primaryController`.
- `GorgeChallenge::capsizeRecovery` → incoming derivation → `noLittering` and the challenge. This is upstream obligation context, not proof that a particular righting design is sufficient.
- The native dependency register identifies `BlueDogIC01::design` as supplier to its recovery analysis basis. The pinned `RelatedElements` query does not traverse generic dependencies, so this example uses the register's explicit client/supplier columns. A configuration-mutation test additionally proves that changing battery inputs changes native outputs; a graph alone cannot establish numerical coupling.

The coverage report contains 239 current rows with objectives and 12 future rows; five future rows already have plans and seven do not. It separately marks studies and never assigns executed or accepted evidence based on a relationship. A mutation test deletes a current `verify` objective and requires an error. Another changes a future applicability annotation to Gorge and requires the uncovered current obligation to reappear. Native applicability values, including external annotations, govern scope.

## Validation record

The prescribed commands were run in the existing locked Linux environment using `.venv/bin/python`, equivalent to `uv run python` after synchronization. The pinned engine/client revision is `23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2`. The desktop MCP server was available but indexed the older Windows checkout at `develop-62b904178`; its successful responses were not treated as validation of this branch.

| Check | Baseline or completed result |
| --- | --- |
| Native model | Baseline: 85 documents, zero diagnostics. Integrated architecture checkpoint: 86 documents, zero errors or warnings. |
| Preparation | Baseline, pilot and final integrated model completed all five steps. |
| Baseline regression | 887 tests passed in 638.49 seconds. |
| Capsize pilot | 78 focused tests passed. |
| Initial integrated regression | 97 passed; three failures and one error exposed stale diagram expectations and the inherited-name audit query. Corrections preserve the intended model semantics. |
| Full integrated regression | `python -m pytest -q --durations=30 --junitxml=...`: 916 passed in 774.27 seconds. No skipped tests, failures or errors. |
| Final audit follow-up | Five tests passed in 21.04 seconds after the dependency-digest convention correction, including current/future scope mutation, missing objectives and changed/orphaned evidence. |
| Numerical preservation | Exact equality for all 29 IC-01 properties, original integration inputs, retained-candidate energy reconciliation, weather outputs and recovery bank at the recorded exposure. The design interface expands from nine overrides to 29 complete properties. |
| Historical run integrity | Final audit passed for all 22 supported run manifests: 96 records, 2,066 record-level source fingerprints, 80 additional manifest model-source fingerprints and 16 cross-run input artifacts. |
| Publishing | Baseline: 36 pages. Integrated build: 38 pages, including the two review reports. Local browser inspection confirmed native diagrams, working zoom controls and no architecture-page rendering errors. |
| Editorial follow-up | The corrected reading sequence rebuilt successfully; all three documentation checks passed in 36.27 seconds. |

The numerical comparison is `build/analysis/oosem-numerical-comparison.json`. It retains before/after outputs and source fingerprints. The earlier 440 Wh candidate still has 3.9736604490556715 Wh nominal headroom at 48.33604399677567 hours; this is a separate historical configuration, not IC-01's battery. IC-01's recovery bank remains 40.46977165885351 Wh after 54.604566822929904 hours under the original standby assumption. No archived evidence file was rewritten.

The generic archive audit covers the existing run-manifest schema, registered record hashes, record-level source/driver hashes, manifest model-source hashes and cross-run input artifacts. Existing specialized regressions cover heel records, VSP geometry/driver provenance and frozen weather inputs. These formats are preserved; the refactor does not invent a replacement evidence ontology.

The class-specific encounter manifest retains its original `develop-e002f1668` toolchain and 80 model-source hashes; it is not relabeled as an execution by the new pin. The surface-environment manifest has 16 cross-run input artifacts. Unused incidental environment files are explicitly segregated in their original archive rather than treated as scientific inputs. The original IC-01 warm-start file is unavailable, but its exact initial states are embedded in the immutable run record and remain usable.

Registered output bytes use raw SHA-256. Source and input-dependency fingerprints use the repository's existing LF-normalized digest. An initial raw comparison of dependency hashes incorrectly flagged six preserved CRLF files; all 16 inputs match their original revision and the baseline byte for byte, and all normalized dependency fingerprints match. The validator now uses the correct contract, with a newline-format regression check. No archive was rewritten to make a check pass.

## Independent review and remaining work

A non-author reviewer exercised the navigation-event ordering defect, checked default reserve handling and identified missing wind/link inputs in the logical architecture. The fixes were independently reprobed. Review also found the invalid inherited query name, the future-applicability filter defect and missing audit implementation fingerprints; these were corrected with regression coverage. A separate analysis review found and corrected an overly broad recovery-screen subject contract.

The full integrated regression and final archive audit passed with the results above. The non-author reviewer then read the generated concept, mission simulation, validation plan, current assessment, modeling/runtime guidance and audit reports in sequence. That pass corrected the default sizing-seed archive reference and stale architecture wording. The coordinator separately inspected the rendered logical, physical and capsize diagrams, including zoom and scrolling, and checked browser errors. The reviewer did not rerun the shared build or full suite; those were run serially by the coordinator.

Outstanding engineering work remains substantial: measured sensing and maneuver envelopes; inverted safety, righting and propulsion evidence; independent-path fault isolation; installed power, thermal and mass reconciliation; recovery-site suitability and capture; justified reliability criteria; future mission definition; and accepted physical procedures. Launch and maintenance interactions are descriptive. The physical interfaces are conceptual, and several numerical adapters retain documented SI scalar conventions rather than universal dimensional type checking. These are explicit capability and evidence limits of the resulting model, not newly closed qualification claims.
