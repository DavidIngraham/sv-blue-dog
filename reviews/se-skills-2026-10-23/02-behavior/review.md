# Behavior modeling audit and implementation

Stage 2 of seven, 2026-10-23. Skill source/checklist in skill/references. Scope: nine operational scenarios, current Gorge policy, native supervisory actions, actuation consumer contracts and the qualification-restoration caller. Native revision remains 23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2; wrong-workspace MCP excluded.

## Findings

| Finding / rules | Counterexample and engineering consequence | Correction and remaining evidence |
| --- | --- | --- |
| B-F01 / B02-B05,B13 | Normal, encounter and navigation sequences did not explicitly pass supervisor permission to command selection/actuation. A command alone could be misread as authorization. | Added required permission parameters and native context bindings to guidance/actuation, plus navigation input to normal/encounter guidance. Native sailing gate separately checks applicable command/permission, current observations, safety and latches. Installed command dispatch remains B-01. |
| B-F02 / B03-B04,B08-B09 | Recovery sequence recorded a pre-actuation record as its outcome and had no durable acknowledgment before enable. | Added PersistRecoveryAuthorization, allocated to recording, before ApplyRecoveryCommand. Its required acknowledgment is passed into actuation. Actual actuation disposition supplies the later record. E-138 is the policy basis; these opaque steps do not implement storage. |
| B-F03 / B04-B05,B09-B11 | Recovery authority alone does not enforce motor qualification, durable state or interlocks. A permitted independent path could otherwise be mistaken for permission to thrust with unknown qualification. | Native RecoveryActuationGate requires known nonqualifying state, durable disqualification, established recovery authorization, applicable command, request, available path and no inhibit. R-101, R-102 and E-138 govern outcomes. Abort intentionally does not inhibit recovery. |
| B-F04 / B02,B10 | Navigation validity and consumer usability were conflated in scenario output meaning. | ValidateNavigation preserves the producer observation and separately emits required usable. Guidance consumes it explicitly. Native AssessObservationUsability reuses the stage1 typed calculation. Clock/frame/age allocations remain IF-01-03. |
| B-F05 / B08-B09,B15 | New-run initialization could be confused with watchdog restoration, and no executable qualification fallback entry existed. | Added native RestoreQualification and MissionLogic.restore_qualification. Invalid/missing record produces nonqualifying state; a live disqualification cannot be erased by an older record. E-139/E-145 are authoritative. Other persisted restrictions, atomicity and deadline implementation remain B-02. |
| B-F06 / B05,B10 | Native lowered graphs exposed unspecified gate parameter multiplicities as optional. Missing-input errors happened during expressions rather than being an explicit input contract. | Critical native actions and scenario permission/acknowledgment inputs now declare [1]. Native graph checks verify required parameters and recovery sequence/flow endpoints. This is a checked property of the pinned runtime, not an assumed universal default. |
| B-F07 / B06-B07,B12,B14 | Sequential scenario illustrations could be read as complete scheduling or fault-interrupt implementations. | Preserved representative cycle meaning; recorded B-03 scheduling/arbitration/resource/timeout decisions and B-04 unimplemented estimators/achieved response. No invented timeout, interrupt priority or hardware concurrency. Existing fault-order regressions remain relevant. |
| B-F08 / B01,B13,B16 | Allocation and passing software traces could be mistaken for implemented controllers or physical autonomy. | Retained named IC-01 mappings, operator launch/service ownership and current mission policy. Public explanation distinguishes executable decisions, scalar simulator, descriptive estimators/storage and physical evidence. |

## Scope and native audit

Reviewed NormalSailing, TrafficEncounter, AbortAndRecover, CapsizeAndResume, NavigationUpdate, CommunicationsOutage, LowEnergyResponse, PrepareAndLaunch and MaintainAndRelease. Current supervisor, capsize observation, recovery authority and fallback policy remain unchanged. Navigation/communications/restoration faults, qualification state, safety/energy abort and independent recovery retain their requirement basis. Human admission/service judgments remain descriptive and require accepted evidence.

The added persistence step brings scenario ownership coverage to 41 steps across the same nine scenarios. Four native consumer/restoration actions are allocated to their logical owners and refine actual scenario obligations or depend on their governing requirements. Those dependencies are explanatory bases, not satisfaction/verification assertions. The 28 logical transfers and candidate configuration/mapping identities remain stable.

## Open decisions

- B-01: bind real message context and current permission to consumer gates. Scalar conceptual simulation does not implement serialization/storage protocols or hardware interlocks.
- B-02: demonstrate atomic durable recording, acknowledgment ordering, all active restriction restoration and required restart deadline on an installed configuration.
- B-03: establish controller concurrency, shared resources, peer arbitration, interrupt behavior and justified timing budgets, including capsize/recovery interruption.
- B-04: implement estimators and measure achieved maneuver/recovery response. A dispatch or permission is not motion, safe arrival or human pickup.

## Validation record

Skill passed the official validator and was installed. Initial candidate flow shorthand for outer context inputs was rejected by the pinned parser before writes; native bindings correctly model shared scenario inputs. Native graph inspection then identified optional critical inputs and justified explicit multiplicities. The first focused run passed 93 checks and correctly rejected stale numerical preparation in the documentation fixture; preparation was rerun, followed by a second preparation after the required-input correction. The iterator parametrization warning was removed.

Final focused validation: 116 tests passed in 141.91 seconds. Native after audit: zero diagnostics/errors, nine scenarios, 41 owned steps, 28 logical exchanges and unchanged 85 scoped correspondences; eight native graphs retained. All four installed skill files match the validated draft. Full regression passed all 993 tests in 902.43 seconds; publication built all 36 pages. Native fingerprints matched all 90 model documents and both driver/test records. Git diff --check passed. Stage 2 is complete; B-01 through B-04 remain explicit implementation/evidence decisions.


Exact model/audit source content is retained in source-snapshot.zip and verified against the original recorded hashes. Earlier source text was reconstructed only from known reversible edits and accepted after every fingerprint matched; the snapshot manifest identifies this and its limited model/audit scope.
