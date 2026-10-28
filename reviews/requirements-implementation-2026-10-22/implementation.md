# Requirements quality implementation — 22 October 2026

Applied the [audit recommendations](../requirements-audit-2026-10-22/audit.md) to the model, verification objectives, native publication views and regression checks. All 251 original requirement IDs remain. The six added IDs identify one separate vegetation outcome and five existing navigation process/policy duties. Numerical limits and mission qualification rules are retained.

## Applied corrections

| Finding | Implemented result |
| --- | --- |
| F01 — unsupported implication | Retained 67 reviewed derivations. Converted 144 detailed specifications to child-to-parent refinements and 27 assurance/shared-context links to supporting dependencies. Each of the original 238 relationships has a recorded disposition in [relationship-decisions.json](relationship-decisions.json). |
| F02 — shared criteria and scope | Shared recording, motor and qualification rules remain single requirements with direct verification. Scoped dependencies identify the narrower event context without deriving the full global rule. Explicit qualification references were added to 125 flat acceptance leaves. |
| F03 — outcomes and chosen behavior | Traffic response refines collision-free passage with an independent navigation-duty basis. Attempt signal compliance has separate recovery/deployment bases. R-004 directly requires durable nonqualification before motor thrust. |
| F04 — parent structure | N-003 is CapsizeResilience; N-004 is VegetationResilience. S-003 is EmergencyControl; R-001 independently governs powered shore recovery. Native renames migrated incoming references. Meaningful aggregate outcomes remain; N-051 and N-054 enumerate stable members in normative conditions. |
| F05 — process duties inside comments | C-028 through C-032 identify entrant applicability review, organizer baseline control, entry evidence acceptance, operator safety intervention and adjudication. The existing entry/adjudication case verifies each directly. C-005 references the single C-020 outage rule. |
| F06 — wording | Rewrote 16 statements for observable estimates, command refresh, product handling capability, admission/inhibition behavior and assessable work products. The remaining 235 original statements are unchanged. See [change-inventory.json](evidence/change-inventory.json). |
| F07 — process/evidence roles | Thirteen process-obligation records identify responsibility, output and acceptance. The reliability verdict verifies only provisional L-101/L-102. Q-102 has an independent conditional duration verdict; Q-101/Q-103 and L-103 retain separate planned reviews. Whole-vessel serviceability and wet-wiring candidate claims now identify the whole vessel. |
| F08 — numerical justification | Added open, requirement-specific source, applicability, margin, evidence, owner and closure records for all 77 performance allocations and three environmental procedure choices. No justification or physical evidence has been fabricated or accepted. |

The [requirement model](../../models/vehicle/requirements.sysml), [challenge](../../models/missions/transgorge.sysml), [basis records](../../models/vehicle/requirement-basis.sysml) and [verification plans](../../models/vehicle/verification.sysml) are authoritative. The dated [current assessment](../../docs/current-assessment.md) and focused reference pages describe the same model. Native tables expose the closure plans under the modeling reference.

Publication also preserves requirement IDs when definitions share a display name or the native renderer elides a common namespace. Supporting dependencies remain visible in bounded views.

## Validation

- Pinned native preparation passed.
- Native inventory: 87 model documents, 257 governing requirements, 67 derivations, 98 verification definitions and zero model/query diagnostics. All 245 current requirements and study objectives have direct verification objectives; 12 future requirements retain separate scope.
- Logical-to-physical allocation pairs remain 55 across 49 sources.
- All 16 historical audit artifact hashes match their original manifest. The baseline audit remains historical; the implementation snapshot is [separate](evidence/native-review.json).
- Full regression suite: 927 passed, 0 skipped, 0 failures, 0 errors; includes all 93 executable-requirement/structural-acceptance regressions. [JUnit results](evidence/full-tests.xml).
- Publishing build passed: 36 pages and 79 native views/reports. [Validation record](evidence/validation.json).

Validation establishes model/software behavior and publication consistency, not physical compliance. The local pinned OpenSysML client/runtime was used because the connected MCP server identified a different workspace and revision. Native editor operations handled supported changes; unsupported dependency/comment authoring used native-located source spans or exact reviewed notation, followed by strict native parsing before writes. No separate SysML parser or relationship engine was introduced.

## Engineering work still open

[U01 through U06](../../models/vehicle/requirement-decisions.sysml) identify the remaining decisions: class-specific traffic/compliance acceptance, independent course-wide recovery and retrieval, structural qualification, installed observations and achieved control response, integrated evidence coverage, and future mission acceptance. Each has an owner and an evidence need; none is marked accepted.

The 77 retained numerical allocations still require their value-selection and margin evidence. The new records make that work reviewable; they do not close it. Planned cases remain inconclusive until applicable evidence is accepted. One-off authoring scripts in this directory are implementation records, not idempotent migrations.
