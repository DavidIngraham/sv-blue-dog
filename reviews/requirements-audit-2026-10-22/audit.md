# SV Blue Dog requirements audit

Status: audit complete for the recorded baseline. Baseline: `b94b6e0`, branch `refactor/oosem-system-model`, inspected 22 October 2026. Proposed corrections have not been applied to requirements, mission policy or engineering criteria.

The main issue is relationship strength. Of 238 derivations, this review recommends retaining 67 under their stated scope, correcting 119 implications unsupported by the written premise, and resolving the intended aggregate/term meaning for 52. The model already has meaningful parent outcomes and extensive planned verification. A wholesale replacement of derivation with refinement would discard valid implications.

## Scope and evidence

The audit uses the `requirement-modeling-quality` skill and its Q01–Q12, H01–H09, R01–R08 and V01–V06 checklist. Its source guidance is [INCOSE's public requirements-writing presentation](https://www.incose.org/docs/default-source/working-groups/requirements-wg/rwg_iw2023/gtwr_introduction_and_concepts_012823.pdf?sfvrsn=634572c7_2), [NASA's requirement checklist](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/), [NASA requirements management](https://www.nasa.gov/reference/6-2-requirements-management/), the [DoD Systems Engineering Guidebook](https://www.cto.mil/wp-content/uploads/2024/05/SE-Guidebook-Feb2022.pdf), and [OMG SysML 2.0](https://www.omg.org/spec/SysML/2.0/Language/PDF). Local review rules are recommendations, not additional agency mandates.

The connected MCP server reports `develop-62b904178` and a separate Windows checkout. This audit instead uses the worktree's pinned client and `develop-23ca2e2f0` service at revision `23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2`. The native load covers 86 model documents and reports zero diagnostics.

The main authoritative requirement inventory contains 251 definitions: 27 in `GorgeChallenge`, one Hawaii goal, 208 in `BlueDogRequirements`, and 15 in `BlueDogStructure`. All have direct usages. Two additional analysis criteria are assessed separately below.

Native document queries identify 238 derivation connections in the main requirement packages, 19 refinement dependencies across the model, 422 total dependencies, 55 allocation usages, and 94 verification definitions. These counts describe model artifacts, not compliance or complete coverage.

The [native evidence snapshot](evidence/native-review.json) retains the returned tables, baseline revision and source fingerprints. [collect.py](evidence/collect.py) and [queries.sysml](evidence/queries.sysml) reproduce the collection through the pinned runtime. Allocation traversal resolves 55 targets from 49 distinct source elements. The two additional requirement definitions are `BlueDogEncounterFeasibility::TimingCriterion` and `BlueDogIntegratedCandidate::VirtualClosure`.

The review covers all 251 statements, their named conditions and additional normative comments, direct required predicates, source/basis records and relationship applicability. It also examines the 94 verification specifications and their direct objectives, supporting analysis/evidence scope, the 19 refinements, all 422 dependency endpoints and all 55 allocation targets. The ledgers distinguish reviewed modeling meaning from the outstanding engineering evidence decisions listed below.

Use the [requirement ledger](requirement-review.csv), [derivation ledger](derivation-review.csv), [dependency/refinement ledger](dependency-review.csv), [allocation ledger](allocation-review.csv), and [verification ledger](verification-review.csv) for IDs, locations, complete statements, endpoints, findings and actions. [Proposed corrections](proposed-corrections.md) give concrete replacement wording and hierarchy changes. [Checklist disposition](checklist-review.md) records all 35 quality checks.

## Findings

### F01 Selected numerical criteria are represented as logical consequences

Priority: high. Checklist: R03, R04, Q01, H03. This is a relationship defect; it does not mean the numerical criteria should be removed.

`BlueDogRequirements::EnergyAwareness` (E-001, [requirements.sysml](../../models/vehicle/requirements.sysml)) requires conservative energy and reserve estimates. Its conditions identify estimation and calibration context but do not establish a one-second update period. `decomposeEnergyEstimateCadence` nevertheless asserts derivation from `energyAwareness` to E-101, which requires estimates at least once per second. A system with accurate conservative estimates every two seconds can meet the stated E-001 obligation while violating E-101. The original-to-derived implication therefore does not follow from the original's stated meaning.

The source already recognizes E-101 as a `performanceAllocation`: `basisEnergyEstimateCadence` in [requirement-basis.sysml](../../models/vehicle/requirement-basis.sysml) explicitly says the numerical limit is not uniquely implied by mission success and requires justification. The relationship currently makes a stronger claim than that basis supports.

Proposed correction: preserve E-101 and its one-second limit as a provisional allocation; replace this derivation with a justified detailed-to-general refinement or supporting-basis dependency, depending on the intended claim. Record the actual analysis supporting the period and its review status. If the intended parent is an explicit aggregate of all those accepted criteria, model and classify that aggregate deliberately instead of using a broad sentence to imply the exact allocations.

Affected path: `energyAwareness`, `energyEstimateCadence`, `EnergyAwarenessVerification`, the logical energy responsibility and `basisEnergyEstimateCadence`. The derivation ledger gives an individual disposition for every similar edge, including cadence, accuracy, restart, handling, reporting, weed and repeating-profile allocations.

### F02 Shared derivations can expand the original's applicability

Priority: high. Checklist: R03, H09, R06.

E-003 `ResetRecovery` concerns watchdog reset under its stated preconditions. `sharedAcceptance1` derives E-136 `LogInterruptionDurability`, whose obligation covers both watchdog reset and abrupt power removal and requires every record older than five seconds to remain readable. Restoring mode-appropriate control after a watchdog reset does not establish abrupt-power-loss durability or the five-second retention bound.

Proposed correction: retain the shared E-136 obligation and its existing verification references. Use a scoped reuse/coverage relationship for the watchdog-reset aspect, and record power-loss durability and its time allocation under the recording/evidence responsibility. Do not duplicate the normative E-136 text or broaden E-003 silently. A verification case may check E-003 and E-136 together without asserting that satisfaction of the former logically entails all of the latter.

Affected path: `sharedAcceptance1`, `resetRecovery`, `logInterruptionDurability`, `ResetRecoveryVerification`, `MissionEvidenceVerification`, and the recording/supervision satisfaction claims. The ledger also identifies the global logging and motor-qualification criteria reused from narrower low-energy, ingress, control-loss and fouling contexts.

These requirements are flat sibling declarations. A derivation connection does not provide language-level inheritance of the parent's conditions or bind the child's applicability automatically. Make shared qualification context explicit by reference or a deliberately modeled context. Preserve global rules as global rules.

### F03 Outcome compliance does not entail every chosen implementation

Priority: high. Checklist: R03, R04, H09.

`challengeTrafficResponse` links C-009 to S-001 ([requirements.sysml](../../models/vehicle/requirements.sysml), line 162). C-009 specifies collision-free course completion. That outcome alone does not entail a particular traffic-assessment process or reviewed class-specific performance allocation; a collision-free passage can occur without establishing either. Retain S-001, justify its observation/response architecture and use detailed-to-general refinement or a supporting basis relationship.

`challengeNavigationSignals` links C-007's attempt-scoped compliance to S-004, whose matrix also covers powered recovery and stationary modes (line 201). The additional modes need their own basis and scope. This audit makes no independent legal applicability determination.

R-004's phrase “prevent motor propulsion from qualifying as unassisted sailing” describes qualification classification less clearly than the actual inhibition policy in R-101/E-138/R-102. Replace it with the concrete inhibition wording in the proposals. Preserve motor inhibition when qualification is unknown, durable disqualification before intervention and fresh recovery authorization. A classification-only parent does not by itself establish every implementation detail of that policy.

Affected paths: the two named challenge links, `challengeMotorInhibition`, its detailed/shared criteria, qualification persistence, safety supervision and their existing verification cases.

### F04 Aggregate membership and parent purpose need explicit decisions

Priority: medium. Checklist: H03, H05–H07, R01, R06.

The 52 unresolved relationship meanings mainly use phrases such as “applicable shared exposure requirements,” “all leaves,” “applicable criterion” or undefined integrity/function terms. Those can be intended normative aggregates, but the complete member set and scope should be explicit. They should not depend on guessing from a diagram or treating explanatory rationale as another obligation.

C-000 and C-015 retain clear outcomes and explicit numbered incorporation. T-100 expressly applies T-101–T-109. Q-001 and L-001 explicitly incorporate their assessment requirements. Keep these meaningful parents; classify their aggregate role and retain their integrated acceptance arguments. N-051/N-054 explicitly apply their leaf sets but would benefit from stable enumerated membership.

N-003 mixes capsize and vegetation responsibilities. S-003 combines emergency intervention with powered recovery. Split those concerns using the concrete hierarchy proposals. Use packages for organization rather than inventing a new requirement for every heading. No wholly empty heading-only parent was confirmed in this baseline.

Affected paths: every unresolved row in the derivation ledger, related parent verification cases, N-003/S-003 use cases, analysis bases and satisfaction claims. Conversion of a requirement to a package requires an explicit reference migration.

### F05 Independently changeable obligations are embedded in comments or combined parents

Priority: medium. Checklist: Q03, Q10, V02.

C-005's statement specifies delivery cadence, while its conditions add outage autonomy and retained-data replay. C-020 already expresses outage behavior. C-007's `governingBaseline`, `entryEvidence` and `adjudication` comments contain entrant, organizer and operator obligations alongside vessel compliance ([transgorge.sysml](../../models/missions/transgorge.sysml), lines 68–70). The comments are normative under the project conventions; their placement does not make them optional. Their present granularity makes ownership, change impact and acceptance harder to assess.

Keep C-005 focused on cadence and reference the existing outage obligations. Keep C-007 vessel compliance while giving entry, baseline-control and adjudication policy distinct identifiable process obligations. Preserve the approved content, the safety-first intervention policy and all six navigation review cases.

### F06 Several statements obscure the subject or observable result

Priority: medium. Checklist: Q02, Q04, Q08.

P-101/P-103–P-106 assign actions to “one adult” rather than state the handling capability the product must provide. E-105–E-107 say an output shall “update” without distinguishing refresh from a changed command value or achieved motion. E-103 would be clearer about absolute error magnitude. R-003 can name the vessel directly instead of relying on passive mission-start wording.

The wording proposals supply replacements for each of these IDs while retaining 100 m, 15 kg, 30 minutes, the one-second cadences, 10 percent normalization and the P-001 handling envelope. E-108/E-109's common acceptance-set rule and missing-epoch treatment are useful precision and should remain.

Affected paths: the handling, guidance/actuation, energy-estimation and launch-admission verification cases; their observation boundaries and shared conditions. Wording cleanup must not become a new mechanism, deadline or relaxed bound.

### F07 Product capability and assessment obligations are mixed

Priority: medium. Checklist: Q06, H03, R01, V05.

Q-101/Q-103, L-103/L-104, E-205 and S-005/S-122/S-123 constrain analysis, evidence or release activities. They are useful obligations, but should have explicit process roles, responsible ownership and assessable outputs. Their absence from component satisfaction mappings is often correct.

`energyDerivation6` and `energyDerivation10` derive E-205 accepted evidence from E-200 or M-002 capability. A capable energy architecture does not logically establish an accepted evidence record. Use an assurance/basis relationship, retain E-205's own acceptance objective, and distinguish the decision record from the product claim. Explicit Q-001/L-001 incorporation may remain as an aggregate acceptance contract while its product and assessment roles are classified separately.

L-101/L-102 remain explicitly provisional study objectives. Their typed requirement/satisfaction representation must not turn the 0.90/95-percent study objective into a Gorge release threshold. Likewise, the three-day/six-hour E-204 profile remains future endurance scope.

`VoyageReliabilityVerification` combines provisional study objectives with Q-101/Q-102/Q-103 and L-103 under one `reliabilitySupported` verdict ([reliability.sysml](../../models/analyses/reliability.sysml), lines 67–81). Preserve that aggregate study scope or report separate objective results; failure of the provisional reliability target must not be presented as proof that the binding passage-duration obligation failed.

The satisfaction file calls its links “allocations,” while `satisfy` makes an engineering assertion. Decide whether each link records responsibility or a whole-obligation claim. P-003 is assigned to the hull enclosure even though its conditions cover the battery, electronics modules, actuators and seals; N-045 is assigned to communications while its text covers cable assemblies ([allocations.sysml](../../models/vehicle/allocations.sysml), lines 11 and 47). Their complete subject/coverage needs justification. Preserve them as unproven candidate claims only with an explicit scope; use allocation/ownership information for responsibility alone. This review does not infer that a component assignment establishes all installed-system cases.

### F08 Generic allocation rationale does not supply the engineering basis for each value

Priority: high before design/entry release. Checklist: Q01, Q07, Q09, R04, V01.

The native basis tables contain 109 records: four owner constraints, 12 functional-acceptance records, nine selected-strategy records, 77 performance allocations, two study objectives and five assurance obligations. This classification is valuable. Many allocation records repeat that a retained limit is provisional and must be justified, without identifying the value-specific analysis or decision that would resolve it ([requirement-basis.sysml](../../models/vehicle/requirement-basis.sysml), for example line 84).

Preserve the existing limits. For each provisional value, identify why it was selected, its source or trade, applicable configuration/mode, uncertainty/margin, supporting evidence, decision owner and closure action. Owner-imposed values can have a direct owner decision; they need not be falsely derived from mission success. Missing justification is an open engineering basis, not evidence that the value is necessarily wrong.

The same review applies to test exposures introduced in verification specifications: the two-hour thermal endpoint operation and three powered 24-hour humidity cycles need a documented representativeness/coverage argument for N-030–N-032. Defining a test procedure may legitimately introduce these durations; it does not by itself establish the entire operational envelope. Preserve the test details and link their accepted basis rather than silently turning them into product requirements.

## Positive observations and limits

The native verification traversal finds direct planned verification links for 244 of the 251 main requirements. All seven without such links are explicitly deferred: C-002, H-001, N-020, N-024, N-042, E-202 and E-204. Missing links on these future obligations are not a current Gorge verification-coverage defect.

The 36 main requirements without direct satisfaction links are listed in the requirement ledger and summary: ten challenge rules C-000–C-009, eight Hawaii/ocean obligations, three repeating-energy obligations, seven process/evidence obligations and eight structural outcomes. Challenge rules may be addressed through vehicle refinements, future profiles have no current selected realization, and process obligations need accountable assessment rather than a component assertion. For T-100/T-103–T-109, record the candidate load/material/joint responsibility and eventual evidence before adding a design satisfaction claim merely to fill the graph.

C-000 states a complete-course outcome and expressly incorporates a defined set of challenge rules. C-015 expressly incorporates flotation, retention and post-capsize recovery obligations. They should not be rejected solely for being broad parents. Their representation as aggregates and their independent verification arguments still need review.

The shore-display obligations are correctly linked to the shore monitoring station rather than to onboard communications. The selected passive-righting strategy is distinguished from the challenge's architecture-neutral capsize recovery obligation. Future ocean and repeating-energy applicability is explicitly recorded.

## Open engineering decisions

These are audit outcomes requiring engineering work or owner decisions, rather than unfinished audit steps. The project owner controls acceptance; the relevant assessment and test responsibility should be recorded with each closure action.

| ID | Decision or evidence gap | Affected acceptance path and next action |
| --- | --- | --- |
| U01 | Class-specific observation/response, clearance, reliability/confidence criteria and regulatory applicability are unaccepted. | S-001/S-101, C-007/C-009, S-004/S-005 and the class-detection/navigation review cases. Freeze the configuration and admitted conditions, review the matrices and numerical allocations, then obtain corresponding evidence. No class exemption or residual-risk threshold was introduced. |
| U02 | Independent recovery capability, course-wide reachable retrieval sites, shore capture and backup observation/power/control remain unqualified. | C-013/C-016–C-018, R-001/R-002, N-051/N-052, T-111/T-112. Survey sites and demonstrate the complete casualty-to-retrieval path. Separate physical paths and allocation arrows do not establish independence. |
| U03 | Structural loads, wet/aged material bounds, joints, fatigue/buckling/impact and simultaneous environmental qualification remain incomplete. | N-001/N-002/N-010, N-041–N-047 and T-100–T-112. Define configuration-specific cases and acceptance bounds; measure and review them. Existing numerical screens are not material/site limits. |
| U04 | Installed observation validity, true-wind envelope estimation, achieved control response and interacting fault behavior need implementation evidence. | E-002/E-008/E-009, N-035, S-001/S-002 and supervisor/recovery cases. E-009 already records the local-apparent/10 m-true-wind distinction and the need to extend sensor qualification if precise survival measurements are required. Close that model/measurement interface explicitly. |
| U05 | Numerical predicate success and accepted end-product evidence need a configuration-specific integration argument. | The 26 direct required predicates in the main requirement files, energy/reliability analyses, mission replay and physical verification. Preserve interval/sample limitations, observation provenance and evidence-review records. An acceptance Boolean records a decision; it does not perform that decision's evidence review. |
| U06 | Future mission acceptance and the quantitative basis of study objectives remain open. | C-002, H-001, N-020–N-025/N-042, E-200/E-202/E-204 and L-101/L-102. Define future profiles and targets independently; do not import them into Gorge qualification through graph traversal. |

## Predicate and evidence review

The review read the 15 direct required predicates in `requirements.sysml` and 11 in `structure.sysml`, including strict reserve admission, motor qualification, restart/righting timing, valid-epoch counts, print limits, energy criteria and evidence-gated structural bounds. Their numerical interfaces are partial acceptance relations; shared conditions, subject/configuration, representative inputs and accepted evidence remain necessary. Doc-only requirements are not defects merely because they lack an executable predicate.

`BlueDogEncounterFeasibility::TimingCriterion` checks two supplied timing values in an explicitly historical comparison. `BlueDogIntegratedCandidate::VirtualClosure` conjoins seven supplied findings. Both are scoped analysis contracts. Neither supplies independent proof that its observations or findings are true. Their use as conditional checks is consistent with the recorded evidence limitations.

The existing executable-requirement and structural-acceptance regressions passed: **93 tests**, recorded in [criterion-regressions.xml](evidence/criterion-regressions.xml). They exercise valid boundaries, violating inputs and missing observations for the covered predicates. They do not test natural-language entailment or establish installed-vessel qualification. The native model and audit-query loads both report zero diagnostics.

## Remediation sequence and completion evidence

1. Resolve relationship strength and scope first: F01–F03 and F07. Preserve every legitimate obligation, its ID, applicability and direct verification objective.
2. Decide aggregate membership and split independently owned concerns: F04/F05. Migrate affected references, views and assessment queries together.
3. Apply the concrete wording corrections in F06 and give provisional allocations the specific basis records in F08. Keep approved numbers and qualification policy unchanged unless the owner separately authorizes an engineering change.
4. Close U01–U06 in the engineering sequence selected by risk. Acceptance records should identify configuration, evidence, decision owner and remaining exclusions.

The [completion record](completion.md) maps the requested audit scope to the delivered artifacts. The evidence verifier checks ledger coverage, local links, baseline/source fingerprints and the recorded test result. Its success establishes artifact integrity; the engineering judgments are the reasons and proposals in this report and its ledgers.

This audit reviews requirement modeling quality and the credibility/scope of existing acceptance claims. It does not independently rederive the vessel's physics, perform legal certification or supply missing physical trials. Those substantive limits are represented by U01–U06 and do not prevent delivery of the requested quality audit.
