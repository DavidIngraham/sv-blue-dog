# Proposed wording and hierarchy corrections

These proposals preserve the existing numerical limits, mission rules and applicability. They have not been applied to the model. Locations, current statements, verification links and affected relationship IDs are in [requirement-review.csv](requirement-review.csv) and [derivation-review.csv](derivation-review.csv).

## Relationship corrections

For E-101, replace `decomposeEnergyEstimateCadence`'s original-to-derived implication with a detailed-to-general refinement, retaining the requirement and its one-second allocation:

```sysml
#refinement dependency decomposeEnergyEstimateCadence
    from energyEstimateCadence to energyAwareness {
    metadata rationale : ModelingMetadata::Rationale {
        text = "E-101 specifies the selected update-period allocation for E-001. The one-second value remains provisional pending its engineering justification; this refinement does not assert that E-001 logically entails that value.";
    }
}
```

This is proposed notation, not an applied or compilation-tested edit. Preserve incoming references when changing the element from connection to dependency. Reconcile document queries, diagrams and checks that select connections by type. Use a plain dependency instead when the child records a selected mechanism or supporting assurance obligation rather than a more precise representation of the parent.

For `challengeTrafficResponse`, use refinement from `BlueDogRequirements::trafficSafety` to `GorgeChallenge::trafficCoexistence`, with rationale identifying its observation/response allocation. Add or retain a separate basis reference to C-007 for navigation duties. An accident-free result alone does not establish S-001's assessment process or reviewed performance envelopes.

For `challengeNavigationSignals`, scope the clarification of C-007 to attempt operation and separately justify the S-004 powered-recovery/stationary-mode coverage. The original C-007 statement governs the attempt; its derivation cannot silently establish all later modes.

For `sharedAcceptance1`, retain E-136 once. Record that `ResetRecoveryVerification` assesses its watchdog-reset aspect, while the recording/evidence responsibility also covers abrupt power loss. Replace the broad implication with a scoped supporting dependency. Keep both verification objectives; do not create a second E-136 with slightly different wording.

Apply the same decision to each row in the derivation ledger. Where an explicit aggregate is intended, enumerating its members can justify retaining the derivation. Do not use explanatory rationale as a substitute for a normative membership decision.

## Wording proposals

The following examples are intended replacements for the cited statements. Existing qualification conditions continue to apply unless a separate structural proposal below relocates them.

| ID | Proposed statement | Reason |
| --- | --- | --- |
| E-001 | The vessel shall maintain conservative estimates of usable battery energy and the energy required for protected recovery. | Names the two estimated quantities and preserves a useful outcome above their allocated criteria. |
| E-103 | Across the operating battery-temperature range, the absolute difference between estimated usable energy and calibrated charge/discharge integration shall not exceed 10 percent of measured usable full-charge energy. | Makes error magnitude and its normalization explicit. Preserve the calibration procedure and temperature qualification. |
| E-105 | During operational qualification, mission guidance shall refresh its guidance output at intervals no greater than 1 second. | Replaces an ambiguous “update” with an observable refresh; this does not require a different value every second. |
| E-106 | During operational qualification, sail control shall refresh the commanded sail position at intervals no greater than 1 second. | Distinguishes command refresh from physical movement. |
| E-107 | During operational qualification, steering control shall refresh the commanded steering position at intervals no greater than 1 second. | Same distinction as E-106. |
| P-101 | The vessel and its mission equipment shall be transportable for 100 m by one adult without assistance under the P-001 handling conditions. | Places the obligation on the product and equipment. |
| P-103 | The vessel shall be capable of assembly from its transport configuration by one adult within 30 minutes under the P-001 handling conditions. | Makes assembly a product capability rather than a task assigned to an unspecified adult. |
| P-104 | The vessel shall be capable of packing into its transport configuration by one adult within 30 minutes under the P-001 handling conditions. | Same distinction as P-103. |
| P-105 | The assembled vessel shall be launchable by one adult without assistance under the P-001 handling conditions. | Preserves the single-person capability and its existing exposure limits. |
| P-106 | The vessel shall be retrievable from the water by one adult without assistance under the P-001 handling conditions. | Keeps retrieval distinct from merely reaching a shore approach. |
| R-003 | The vessel shall inhibit mission start unless a valid usable-energy estimate no older than 1 second strictly exceeds a valid R-002 protected reserve. | Names the responsible subject and preserves the strict comparison and freshness bound. |
| R-004 | The vessel shall inhibit motor thrust until it has durably recorded a known nonqualifying status for the attempt. | States the intended inhibition behavior directly. R-102 authorization and E-138 persistence remain independently applicable. |
| Q-101 | The mission-performance assessment shall evaluate complete-route progress over the declared reproducible scenario ensemble, including sailing legs, holds and maneuvers. | Identifies an assessment obligation. It does not reintroduce the retired minimum-speed screen. |
| E-205 | The energy-case acceptance record shall identify accepted evidence for installed-load coverage, resource bounds, battery derating and interval resolution before the case is accepted. | Gives the assurance obligation an assessable work product. A Boolean alone cannot audit those records. |

Review the wording proposals against actual interfaces before implementing them. For example, if “guidance output” has no identified observation boundary, define that boundary without prescribing an unnecessary bus or protocol. No proposed number is a new allocation.

## Hierarchy proposals

| Current element | Proposed treatment | References and acceptance that must follow the change |
| --- | --- | --- |
| C-000 | Keep the complete-course outcome and its explicitly incorporated challenge rules. Identify it as an aggregate acceptance contract. | `PassageQualificationVerification`, course/qualification evidence and the 22 direct challenge derivations. Its own outcome is meaningful. |
| C-015 | Keep the recovery-without-abandonment outcome and explicit C-016–C-018 incorporation. | Flotation, retention and capsize-recovery cases remain separate tests supporting the integrated outcome. |
| E-001, E-002, E-003 and E-005 | Keep meaningful outcomes. Group their detailed allocations in packages/collections; use refinement or basis dependencies where logical implication is unsupported. | Existing verification cases already enumerate detailed objectives. Preserve those direct links instead of relying on a parent verdict to prove every leaf. |
| N-003 | Split the capsize and vegetation responsibilities, with a package/collection organizing them. Proposed capsize outcome: “After the declared capsize disturbances, the vessel shall provide the recovery behavior defined for the selected righting or post-abort recovery strategy.” Proposed vegetation outcome: “The vessel shall preserve or autonomously recover the sailing and recovery functions specified for the declared submerged-vegetation encounters.” | Migrate `stabilityAndFouling` references in requirements, analysis, satisfaction claims, use cases and verification deliberately. N-051/N-052 remain selected-strategy criteria; N-053–N-056 retain their separate sailing/recovery tests. Do not retire N-003 before its references are reconciled. |
| S-003 | Separate emergency-control acceptance from powered-recovery capability; organize them together without another vague requirement. Existing C-006 and R-001 already provide useful source obligations. | Preserve S-110–S-115, isolation/reset behavior, shared qualification constraints and `SafeRecoveryVerification`. Confirm the source for local isolation and control-loss allocations. |
| C-005 | Keep the 30-second delivery obligation. Reference the existing C-020 outage rule for continuation/retention/replay instead of keeping additional independently changeable shalls inside C-005's conditions. | `ObservationAndInterventionVerification`, vehicle E-005/E-120–E-124, logging and reconnect cases. |
| C-007 | Keep vessel rule compliance. Give entry review, organizer baseline control, operator intervention and adjudication their own identifiable process/policy obligations. | Preserve the current approved policy text and six source-linked navigation review cases. This is a traceability restructuring, not a legal reinterpretation. |
| Q-101/Q-103, L-103/L-104, E-205 and S-005/S-122/S-123 | Classify as analysis, evidence or release-process obligations, with explicit responsibility and outputs. | Keep their verification/assessment objectives. Do not manufacture component satisfaction claims to fill a graph. |
| T-100 | Keep the load-carrying outcome and explicit T-101–T-109 aggregate. | Preserve the independent material, load and deformation evidence; those nine members are not a complete impact/fatigue/buckling qualification. |
| Future profiles and study objectives | Keep their future/nonbinding status visible in sets, queries and reports. | C-002, H-001, ocean requirements and E-200/E-202/E-204 do not become Gorge gates. L-101/L-102 remain study objectives. |

If a future parent really serves only as a heading, use a package. This review did not confirm a current parent with no outcome of its own. The recurring problems are implicit membership, combined independent concerns and unsupported implication, rather than an empty heading alone.
