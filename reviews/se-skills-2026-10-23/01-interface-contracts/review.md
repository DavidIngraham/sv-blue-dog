# Interface contract audit and implementation

Stage 1 of seven, 2026-10-23. Scope: the current Gorge candidate, descriptive operational scenarios, fourteen logical responsibilities and the IC-01 primary/recovery realization. Existing architecture and requirements fixes are preserved. Native revision: 23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2. MCP workspace/revision mismatch excluded. Source register and checklist are in `skill/references/`; recommendations are tailored guidance, not a full standards certification.

## Findings and action

| Finding | Native subjects / consequence | Correction or outstanding decision | Source/check |
| --- | --- | --- | --- |
| F01 | ReserveAssessment, BoundaryAssessment and TrafficObservation lacked assessment time. Consumers could not distinguish a recent assertion from an old one. | Added typed observedAt; no numerical freshness default. | I06-I08 / IDD timing, NIM integration |
| F02 | SafetyObservation and TrafficObservation lacked an explicit producer validity assertion; LinkObservation could represent availability but not distinguish an invalid report. | Added valid; link-down remains distinct from invalid/missing data, and traffic coverage remains independent of track count. | I07 / tailored error-handling application |
| F03 | Eleven observation/record payloads lacked producer, configuration, clock and restart context. | Added ObservationContext to navigation, safety, reserve, traffic assessment, boundary, track/list, mission record, bank state, wind and link. Existing field identities retained. Clock establishment and restart rules remain IF-02. | I08-I09,I11 / IDD synchronization, NIM configuration |
| F04 | Navigation, contact and sailing-command angular values had incomplete reference semantics. | Explicit coordinate/heading/bearing/range/trim reference identities; wind retains vessel-frame intent with frame identity. Choosing datum, axes, true/magnetic headings and transforms remains IF-03; strings do not enforce these choices. | I04 / IDD data meaning, SI quantity conventions; tailored frame check |
| F05 | OperationPermission, RecoveryCommand and SailingCommand lacked issuance/expiry and authority context. | Added CommandContext without defaults. Arbitration, inhibit, replay/restart and independent recovery remain IF-02/04. Source identity is not authentication. | I09-I10,I14 / tailored IDD safety/protocol review |
| F06 | Producer validity could be mistaken for current usability; an age bound alone admits future observations. | Native typed ObservationUsable predicate requires applicable context, established clock, producer validity, nonnegative supplied age bound, no future timestamp and age within bound. | I07-I08 / tailored timing/legality application |
| F07 | A command validity interval could be inverted, future-issued, expired, from an unaccepted authority or out of order. | Native CommandApplicable checks these preconditions. It does not grant operational permission. Binding and implementation remain open. | I09-I10 / tailored sequencing/safety application |
| F08 | Physical supply is represented only by available power/availability; connector, voltage, current, protection and sealing remain unspecified. Storage and telemetry supply are unresolved. | Retained physical supply semantics; IF-05 explicitly records needed compatibility decisions. Did not attach digital envelopes to physical power or invent voltages/equipment. | I13 / IDD physical compatibility, S2 7.14 |
| F09 | Human deployment/service assessments and recovery plans describe evidence judgments and feasibility, not installed messages. | Retained these distinct types and existing configuration identity. Actual approval validity, operator procedures, safe capture and hardware compatibility require defined evidence; not closed by this digital schema pass. | I01,I15 / NIM human boundaries and integration |
| F10 | 28 logical flows have candidate mappings, but link coverage does not prove preservation of timing, units or authority. | Native mapping audit retained; physical ports reuse corrected payload types. Internal scheduling, serialization, bandwidth and acceptance checks remain open. | I02,I03,I06 / S2, IDD |

All information exchanges were inspected through the logical and candidate port/flow definitions; the after inventory records resolved native items, ports and flows. Nine scenarios, forty steps, fourteen logical responsibilities and 85 correspondences remain present. No mission rule, requirement value, battery size, equipment selection, acceptance verdict or historical record was changed.

## Outstanding engineering work

IF-01: allocate consumer freshness, latency and uncertainty from control and safety needs. Existing one-second refresh requirements do not supply a safe age limit.

IF-02: establish clocks, uncertainty, source/authority epochs, duplicate/reordered message handling, restart and replay protection.

IF-03: agree spatial/angular references and transformations at both ends.

IF-04: establish primary/recovery authority, inhibit precedence, expiry response and primary-loss startup. These interface predicates are not yet consumed by the scalar conceptual simulator; the next behavior stage must preserve that distinction.

IF-05: define physical mating, electrical compatibility, protection, storage/telemetry supply, transport encoding, bandwidth and failure behavior. Verify against selected hardware and identified installation.

The model owns these issues in BlueDogInterfaceContracts. A hardware, timing or safety decision requires supporting analysis and measurements; no arbitrary threshold was selected to make this audit look closed.

## Validation

- Skill passed the official quick validator and was installed in the personal skills directory. Manual decision probes distinguish stale validity, empty traffic coverage, link-down, conflicting controllers and typed-but-incompatible ports.
- Native parser accepted candidate source before existing payload files were written; zero diagnostics.
- 22 focused native tests pass: schema, unset authority/times, freshness boundaries, equivalent time units, future/stale/invalid/context/clock cases, command interval and authority/ordering cases, missing criterion, and a future-guard mutation control. Synthetic cases are software evidence only.
- First focused run exposed test assumptions about CalcResult wrappers, canonical duration aliases and a unit shorthand; assertions were corrected to use native values/types and supported units. No production equation was changed in response.
- Preparation completed; full regression passed all 957 cases in 937.82 seconds. A final narrowed missing-input assertion also passed the 22 focused tests. Publication built all 36 pages successfully. Final native source hashes match all 89 model documents, using the native loader's text/newline convention. Git diff --check passes. See validation-summary.json and the JUnit records. Stage 1 is complete; the documented engineering decisions remain open.

Exact model/audit source content is retained in source-snapshot.zip and verified against the original recorded hashes. Earlier source text was reconstructed only from known reversible edits and accepted after every fingerprint matched; the snapshot manifest identifies this and its limited model/audit scope.
