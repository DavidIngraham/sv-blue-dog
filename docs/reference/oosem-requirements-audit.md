# Requirements quality and relationship audit

Assessment: 20 October 2026. Scope: the authored requirement definitions and usages in `GorgeChallenge`, `BlueDog::Goals`, `BlueDogRequirements` and `BlueDogStructure`, with their verification strategies, basis metadata and decision dependencies. This is a requirement-quality and semantic review. It does not establish physical verification or mission readiness.

## Baseline and review method

The baseline is `b12b079` on `refactor/oosem-system-model`. The review covered every requirement statement, named qualification condition and relationship family in the four packages, all mission files, vehicle verification, requirement-basis, structural requirements, decisions and source notes. Related native publishing queries, atomic requirement fixtures and requirement/relationship/acceptance tests were inspected. Architecture, execution, configurations and evidence also require the cross-domain review recorded with this refactor; this report does not substitute for it.

The matching pinned OpenSysML client loaded source snapshots and queried native `DocumentQueries` relationships. The configured MCP server pointed at a different checkout and revision, so it was not used to claim validation of this branch. No second SysML parser or relationship engine was introduced. Counts exclude anonymous satisfaction assertions and internal analysis predicates outside the four governing packages.

| Requirement-scope measure | Baseline | Refactored requirement slice |
| --- | ---: | ---: |
| Authored requirement IDs | 251 | 251 |
| Current required statements | 237 | 237 |
| Current provisional study objectives | 2 | 2 |
| Future mission/endurance statements | 12 | 12 |
| Requirements with a direct planned verification objective | 228 | 244 |
| Current-scope requirements without a direct plan | 16 | 0 |
| Future-scope requirements without a direct plan | 7 | 7 |
| Derivation connections | 242 | 238 |
| Refinement dependencies | 8 | 9 |
| Plain dependencies | 56 | 59 |

The 239 current-scope rows include two provisional reliability-study objectives; they are not 239 binding launch criteria. Native `BlueDogRequirementBasis::StudyObjective` metadata distinguishes those objectives without an ID list in the reporting code. Future applicability comes from `BlueDogMissionScope::Applicability`, including external annotations. A future row is not applicable to current Gorge acceptance; that scope disposition is not a runtime pass.

## Modeling principles and sources

The [official Requirement Derivation library](https://raw.githubusercontent.com/Systems-Modeling/SysML-v2-Release/master/sysml.library/Domain%20Libraries/Requirement%20Derivation/DerivationConnections.sysml) defines an implication from satisfaction of the original requirement to satisfaction of each derived requirement. The ends are requirement usages. It does not mean that satisfying one leaf proves its parent. This direction governed the relationship review.

The public [INCOSE Guide to Writing Requirements v4 summary](https://www.incose.org/docs/default-source/working-groups/requirements-wg/guidetowritingrequirements/incose_rwg_gtwr_v4_summary_sheet.pdf), dated June 2023, supplied the review criteria: necessity, appropriate abstraction, clarity, completeness, singularity, feasibility, verifiability, consistency and validation of the set. Its guidance supports explicit conditions, unique expressions and a justified reason for implementation constraints. It does not justify inventing numbers to fill an evidence gap. The full paid guide was not inspected; its version and relationship to the fifth-edition handbook were checked against the [official product listing](https://portal.incose.org/Web/iCore/Store/StoreLayouts/Item_Detail.aspx?Category=EBOOKS&iProductCode=GUIDEWRITEREQ).

The [INCOSE Systems Engineering Handbook page](https://www.incose.org/resources-publications/technical-publications/se-handbook/) confirms the fifth edition and its life-cycle/process scope. The full handbook was not accessed, so no clause-level claim of conformance is made. The [INCOSE MBSE methodology survey hosted by OMG](https://www.omg.org/sysml/MBSE_Methodology_Survey_RevA.pdf), section 3.2, supplies publicly accessible OOSEM context for stakeholder analysis, system requirements, logical architecture, candidate allocated architecture, trades and verification/validation. That survey is dated 2007; it is methodological background, not the SysML v2 language specification. The [current INCOSE OOSEM working group](https://www.incose.org/group/object-oriented-se-method-working-group/) describes ongoing extension to SysML v2.

## Requirement quality findings and dispositions

| Domain | Finding and disposition | Remaining engineering question |
| --- | --- | --- |
| Challenge and mission | M-001 now references the complete governing challenge context. Its previous C-003 through C-006 reference omitted independent safety, reserve and persistence obligations. Ordered crossings remain one useful mission outcome. | Course admission, installed capability and complete attempt evidence remain unaccepted. |
| Navigation and restart | E-002 now counts missing/invalid samples as failed epochs rather than ambiguously failing the whole trial while allowing 1710 of 1800 epochs. E-111 restores the persisted mission-mode record; current safety restrictions govern actual operation. | Accuracy/timing allocations and a physical restart implementation need evidence. |
| Environment and safety | N-001 distinguishes structural survival from continued required safety capability. N-035 explicitly requires upright control and preserved safety before sailing resumption; changing modes never clears disqualification. | Environmental combinations, sensing limits and recovery exposure need configuration-specific qualification. |
| Capsize and fouling | N-003 retains a useful disturbance capability. N-052 and the passive-righting campaign are identified as strategy-specific; weeds remain separate controlled exposures. Safe unassisted righting can preserve qualification. | Static roll curves do not establish dynamic righting, ingress tolerance, control restoration or safe inverted operation. |
| Traffic and boundaries | S-101 has one track-acquisition/continuity obligation; target-class conditions are separate. Class-specific evidence and conservative unknown-class envelopes remain required. | Detection, maneuver response, consequence assumptions and navigation-rule compliance remain open. No new collision-risk number was introduced. |
| Energy | E-201 now applies explicitly to the selected finite or repeating mission profile. The holding-drive decision traces to finite M-002 energy. Wind-sensing timing leaves no longer repeat an unrelated endurance condition; E-152 retains its complete mission exposure. | Installed loads, energy uncertainty and route-dependent reserve remain unmeasured. A fixed reserve passed to a predicate is an analysis approximation. |
| Battery protection | N-117 remains a universal charge-temperature protection obligation. It is no longer presented as a consequence of only the hot-sun campaign. | Manufacturer limits and installed sensing/inhibition behavior need evidence across operating conditions. |
| Reliability | L-101 and L-102 remain identified provisional study objectives. L-001 no longer inherits their probability/distribution assumptions as acceptance obligations. L-103 evidence and L-104 safety dispositions remain required. | Neither the numerical target nor the constant-hazard model has been accepted for the installed mission configuration. |
| Manufacturing and structure | P-002 and T-113 use one typed print-job predicate and one 250 mm source limit. T-113 refines its structural application and retains independent slicer-evidence acceptance. Generic structural basis wording now states the actual change dependency. | Wet properties, joints, load cases, fatigue, impact, buckling and flotation require their own evidence. |
| Owner and process constraints | Serviceability is explicitly an owner lifecycle constraint. Evidence-review obligations and selected strategies receive distinct basis metadata. Existing numerical limits are retained and identified as allocations needing justification. | The basis annotation is a review aid, not approval of a threshold or physical capability. |

Most existing atomic leaves already express independently testable outcomes. They were retained. Higher-level capabilities were also retained where they establish meaningful operating scope. No requirement was split merely to reduce word count, and no numerical threshold was invented or relaxed. Existing shared leaves avoid repeating persistence, motor-inhibition and event-recording obligations.

## Relationship decisions

| Relationship | Disposition | Engineering meaning |
| --- | --- | --- |
| L-001 to L-101 and L-102 | Replace two derivations with dependencies from the study objective to mission reliability. | Mission capability motivates the studies but does not entail an unaccepted probability target or a constant-hazard model. |
| N-003 to N-052 | Replace derivation with a dependency from control recovery to the disturbance capability. | Upright restoration belongs to the selected passive-righting strategy; the challenge also allows post-abort limp recovery. |
| N-046 to N-117 | Replace derivation with a dependency from charge protection to the thermal exposure. | The universal protection obligation has broader scope than the hot-sun campaign. |
| T-113 to P-002 | Replace plain dependency with refinement. | The structural case applies the same dimensional obligation with accepted slicer evidence. |
| Holding-drive decision to E-200 | Redirect to M-002. | A candidate motor-off holding mechanism affects the current finite mission budget; future repeatability is not a Gorge prerequisite. |
| Challenge decomposition and other scoped acceptance decompositions | Retain. | Each asserts its original-to-derived obligation under the stated conditions; no child-to-parent proof or verification closure is inferred. |
| Owner-constraint and selected-strategy dependencies | Retain with explicit rationale. | They record design basis/change impact without asserting a universal consequence of mission completion. |
| Existing formal numerical refinements | Retain. | A predicate formalizes its supplied-input criterion; representativeness and physical evidence remain separate. |
| Satisfaction assertions | Retain as unproved design claims. | The subject is intended to satisfy the requirement. A SysML `satisfy` assertion is not a logical-to-physical allocation and does not supply a verification verdict. |
| Verification objectives | Extend only where a credible grouped strategy was missing. | A direct verification relationship identifies what a case assesses; all newly defined procedures remain inconclusive. |

The review did not impose a relationship reduction quota. Generic dependencies remain appropriate for source literature, trade motivations and configuration-sensitive assumptions. Structural connections, information exchanges and functional allocations belong to their native constructs in the architecture model.

## Verification coverage and limits

Seven new grouped plans and an expanded installed-environment plan close the 16 current-scope coverage gaps. They address complete challenge qualification, observation/intervention, restricted waters, combined capsize/fouling capability, whole-mission capability, installed peak power and construction identity. The environment plan additionally covers the current Gorge profile, survival wind, complete freshwater exposure and enclosure sealing. These plans specify evidence and failure conditions; they do not fabricate measurements.

The seven future omissions are C-002, H-001, N-020, N-024, N-042, E-202 and E-204. They remain explicitly deferred from current Gorge acceptance. Other future requirements already have plans, but neither their existence nor a future numerical screen establishes ocean readiness. Future route, weather, exposure, assistance and acceptance decisions must be made before those plans can be treated as an adequate qualification program.

Native staged checks established zero requirement-slice diagnostics, agreement of the shared system/structural print predicate at zero, the 250 mm limit and an over-limit input, rejection without structural evidence acceptance, and inconclusive results from representative new plans. The full baseline regression passed 887 tests before integration. Final integrated tests and publishing results must be read in the overall validation record; isolated staging checks are not a substitute.

## ID mapping

Every one of the 251 baseline requirement IDs maps to the identical ID. No definition or usage was renamed, retired or split. The principal semantic changes are mapped below; additional basis annotations change classification only.

| Previous ID | Current ID | Change |
| --- | --- | --- |
| M-001 | M-001 | Complete challenge qualification context. |
| E-002 | E-002 | Clarified failed-epoch counting. |
| E-005 | E-005 | Explicit outage retention and subsequent delivery. |
| E-111 | E-111 | Distinguish restored record from commanded operating mode. |
| E-146 through E-152 | Same IDs | Measurement/fault conditions separated from mission endurance exposure. |
| E-201 | E-201 | Finite and repeating profile applicability clarified. |
| N-001, N-003, N-035 | Same IDs | Safety priority, strategy applicability and resumption restrictions. |
| N-052, N-117 | Same IDs | Corrected source relationship without removing the obligation. |
| S-101 | S-101 | Target-class context moved out of the single obligation. |
| L-001, L-101, L-102 | Same IDs | Required capability separated from provisional study objectives. |
| P-002, T-113 | Same IDs | Shared typed dimensional acceptance; structural refinement. |
| Every other baseline ID | Identical ID | Requirement obligation retained; plans and basis metadata may be more explicit. |

The remaining defects are engineering gaps: unaccepted allocations, unsupported installed performance, incomplete casualty and combination evidence, unresolved future mission scope and no physical qualification. A complete trace matrix cannot close them.
