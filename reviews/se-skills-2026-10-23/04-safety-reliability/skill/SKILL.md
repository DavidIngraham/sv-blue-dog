---
name: safety-reliability-analysis
description: Audit and improve system hazards, failure analyses, controls, reliability assumptions and evidence-backed risk dispositions across operating modes and lifecycle phases. Use for safety/reliability reviews and authorized model corrections.
---

# Safety and reliability analysis

Trace credible undesirable scenarios to their causes, consequences, proposed controls and actual evidence. Read [the sourced checklist](references/checklist.md) and [source register](references/sources.md). Use native failure/risk constructs where available; preserve the project's actual risk authority and criteria.

## Workflow

1. Establish system/configuration boundaries, mission/exposure, lifecycle modes, people/environment/assets affected and authoritative obligations. Inventory failure modes, hazards, causal relationships, controls, verification plans, evidence and dispositions natively.
2. Review both failure-first and consequence-first paths. Component lists alone miss unsafe interactions, human tasks, common causes and a function that operates incorrectly rather than simply stops. Include nominal, degraded, recovery, launch, handling, service and other applicable phases.
3. For each finding record native identities, checklist/source ID, scenario, consequence, uncertainty, affected configuration/modes, control responsibility and closure evidence. Distinguish an issue already observed from an uncertain future scenario. Do not invent event probabilities or classify missing information as low risk.
4. Correct authorized coverage, causal intent, configuration applicability, control/requirement and verification references. Keep proposed, implemented, effectiveness-demonstrated and risk-disposition-accepted states separate. Preserve historical records and stable failure IDs.
5. Review reliability at the critical-function/mission level. Establish the failure definition, exposure, rate pedigree, non-overlap, dependence/common-cause treatment and statistical applicability. Reuse native calculations; do not turn a qualitative ranking into a probability or count a primary failure as mission loss when an effective backup preserves the function.
6. Validate fault combinations, boundary/missing evidence, control failure and restoration. Use negative controls to expose missing critical contributors or unjustified acceptance. Update the native audit, affected architecture/configuration, verification plans and engineering assessment; run appropriate regressions.

## Decision boundaries

A populated FMEA or hazard register does not prove completeness. A warning, control requirement, separate controller or fallback command does not prove implemented risk reduction or independence. Review secondary hazards introduced by mitigations.

Safety and mission reliability concern different outcomes. An autonomous abort may protect people while ending a qualifying attempt. Component survival, system availability and successful mission completion are different measures. Apply each distribution and system model only within its assumptions; retain failures, censoring and the exposure denominator.

Use the project's defined scales and acceptance responsibilities. Agency matrices and military acceptance authorities do not automatically apply to another project. Unknown likelihood/consequence, unverified controls and absent acceptance records remain open. A native readiness predicate can organize supplied review facts; it does not accept risk on a person's behalf.

For actual physical operations, use the project's established authorization and controls. This skill does not impose blanket approval on model edits or claim that software tests qualify a vessel.
