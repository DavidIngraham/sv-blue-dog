# Architecture correspondence review — 23 October 2026

Implemented architecture structure and cross-layer relationship corrections for the current finite-Gorge model. The reusable `architecture-modeling-quality` skill is installed in the personal Codex skill directory, with a sourced checklist and automatic discovery enabled.

## Scope and evidence

Reviewed the context/responsibility description, all nine current logical scenario usages and their steps, the complete `LogicalVessel` responsibility/flow structure, IC-01 candidate allocations and interfaces, executable supervisory/recovery action correspondences, and the affected configuration and verification context. Analysis configuration applicability and immutable evidence conventions were retained. This is not a full review of future ocean architecture, every numerical library, installed software or physical interface design.

Used the pinned OpenSysML runtime at `23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2`. The MCP server still reports `develop-62b904178` against the OneDrive checkout, rather than this WSL checkout. Its model results were not used. Native before/after snapshots record source hashes; pre-existing uncommitted requirement work was preserved.

- [Before: native relationships and source fingerprints](before.json)
- [After: native architecture audit](after.json)
- [Model structure and interfaces](../../models/vehicle/architecture.sysml)
- [Scoped correspondences](../../models/vehicle/architecture-contracts.sysml)
- [Scenario steps, allocations and verification context](../../models/vehicle/method.sysml)
- [Executable action allocations](../../models/vehicle/mission-logic.sysml)

## Findings and applied corrections

| Finding | Checklist | Correction and consequence |
| --- | --- | --- |
| Context and logical descriptions overlapped without explicit correspondence. | A01–A02, L02 | Documented their distinct purposes and added 14 scoped context-to-logical mappings. Preserved existing names and hardware concepts. |
| Anonymous logical-to-equipment allocations did not state partial responsibility, configuration or implementation path. | L02–L03, C01 | Replaced them with 27 named, scoped IC-01 contributions, each bound to the named design. Primary/recovery/shared labels identify paths without inventing mode selection or qualification. |
| Navigation validation, record scheduling and queued telemetry were represented mainly by sensor, storage and radio allocations. | A03, L02 | Added controller-side contributions while retaining the equipment contributions. These describe implementation responsibilities, not installed software. |
| Recovery management had no explicit navigation, traffic or boundary input interfaces. | A04, I01 | Added these inputs and their logical transfers. Expanded the recovery scenario to supply navigation, traffic, boundary and reserve assessments to shore planning. |
| Recovery commands had no logical thrust-execution recipient, although the candidate controller-to-propulsor interface existed. | A03, L01–L02, I01 | Added `RecoveryActuation`, allocated it to the candidate propulsor, and connected recovery commands through both descriptions. Recovery planning/control remains distinct from thrust and shore retrieval. |
| Recovery outcome records and stored-record readback lacked explicit paths. | A04, I01 | Connected recovery records to recording/communications, added a scenario record step, and supplied logical and candidate storage-readback interfaces. Supply and arbitration remain unresolved. |
| Logical transfers did not identify their candidate implementation paths. | I01, L03 | Named all 28 logical flows and candidate flows. Added 30 transfer mappings plus 14 controller-internal interaction mappings. Internal mappings expose implementation obligations rather than claiming completed software calls. |
| Recovery authority and fallback actions lacked explicit logical owners. | A05, L01 | Allocated their representative action usages to recovery management and connected their scenario context. Executable bodies and policy were preserved. |
| Several affected scenarios had sparse verification context. | V01, C03 | Added contextual dependencies for recovery propulsion/reserve, capsize, navigation, communications outage, low reserve and service verification. These links do not execute or accept a verification procedure. |

## Review outcomes and remaining decisions

| Criteria | Disposition |
| --- | --- |
| A01–A02, L01–L03 | Structural corrections implemented for the stated current scope; native ownership, target coverage, mapping scope and configuration checks are automated. |
| A03–A05, V01 | Recovery path and related responsibilities reviewed and clarified. Other current scenario owners are checked; complete implementation and achieved dynamics remain unresolved. |
| I01 | All 28 current logical exchanges have native mappings. Mapping presence alone does not demonstrate correct encoding, timing, software scheduling or physical transport. |
| L05, I02–I04 | Unresolved: freshness/validity propagation, peer timeout, authority arbitration, backup startup, inverted safety observation, installed protocols, recording/telemetry supply, retention and arbitration. Separate components do not establish fault independence. |
| C01–C03 | Candidate assembly and mappings explicitly identify IC-01 and its integration assumptions. Existing analysis subjects and archived evidence retain their identity and provenance. Every historical analysis was not revalidated as part of this change. |
| V02 | Regression checks include removed ownership, allocation and exchange links, an invalid candidate target, blank scope and accidental substitution of the archived design. Structural regression and physical qualification remain distinct. |
| Detailed navigation signaling | Open: current requirements/context exist, but detailed logical interfaces and IC-01 equipment allocation need design work. No arbitrary signaling hardware was selected. |
| Optional payload, future harvesting/ocean architecture | Outside the current candidate implementation scope; retained without fabricated allocations. |
| Hull/rig and human launch/pickup | Retained in physical and human descriptions. Controller allocations do not claim shore capture, retention or operator retrieval. |

The 1,300 Wh IC-01 design, independent 60 Wh recovery-bank hypothesis, archived 440 Wh study, sensing/maneuver assumptions, numerical equations and mission acceptance policy were preserved. The model still requires compatible equipment choices and measured evidence; added relationships do not resolve those engineering uncertainties.

## Reproduction

```sh
.venv/bin/python -m tools.boat_analysis.cli prepare
.venv/bin/python -m tools.boat_analysis.model.architecture_audit --output reviews/architecture-quality-2026-10-23/after.json
.venv/bin/python -m pytest -q --junitxml=reviews/architecture-quality-2026-10-23/test-results.xml
.venv/bin/python -m pytest -q tests/test_architecture_quality.py tests/test_requirements.py tests/test_relationship_semantics.py --junitxml=reviews/architecture-quality-2026-10-23/follow-up-tests.xml
.venv/bin/python -m pytest -q tests/test_architecture_quality.py --junitxml=reviews/architecture-quality-2026-10-23/final-architecture-tests.xml
```

The architecture article renders the same native responsibility and exchange queries used by the audit. Its tables and diagrams are generated from the model, not separately maintained relationship lists.

## Validation results

- Personal skill format/frontmatter validation passed. Its references distinguish primary guidance from project conventions and historical INCOSE material.
- Native preparation passed. The final audit parsed 88 model documents with no diagnostics and reported no structural errors: nine scenarios, 40 scenario steps, 14 logical responsibilities and 28 logical exchanges. Its 85 scoped correspondences comprise 14 context mappings, 27 candidate contributions, 30 candidate transfers and 14 internal interactions.
- The [initial full regression](test-results.xml) completed with 933 passed and one failure: the recovery rendering test still expected four actions. Its expectation was updated to the ten explicitly modeled actions without weakening the sequence check.
- The [affected requirements, architecture and publication run](follow-up-tests.xml) passed 38 cases. Its one failure was the newly added table assertion comparing an unspaced identifier to the native renderer's word-spaced label. The check now compares both cells together while normalizing whitespace and case.
- The [final architecture run](final-architecture-tests.xml) passed all eight cases, including the six negative audit controls and the source/target table check. The fresh publishing build ran through the existing `rendered_site` fixture; generated responsibility/exchange tables and the revised recovery diagram were checked.
- The [validation summary](validation-summary.json) reconciles the runs by test identity: 935 distinct cases have passing latest results and no failure remains unresolved. The initial failure records are retained. This is a full run plus targeted follow-up, not a second full-suite run after the expectation corrections.
- Final source fingerprints match the after snapshot, and `git diff --check` passed. No numerical configuration, mission policy, historical evidence or physical acceptance state was changed.
