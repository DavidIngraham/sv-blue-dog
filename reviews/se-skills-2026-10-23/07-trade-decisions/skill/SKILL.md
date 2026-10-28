---
name: trade-study-decision-management
description: Audit and improve engineering trade criteria, alternative comparisons, uncertainty, recommendations and decision records. Use for trade-study reviews, decision management and authorized model corrections.
---

# Trade studies and decision management

Make the decision and its evidence explicit before choosing a scoring method.
Read the [checklist](references/checklist.md) and [primary-source register](references/sources.md).
For native SysML selection semantics, see the [synthetic example](references/native-trade-example.sysml).

1. Identify the decision question, intended outcome, mission/configuration scope,
   responsible role, constraints and cost of a wrong or delayed decision. Distinguish
   a working numerical baseline, design selection, policy and evidence-acceptance
   question. Use a proportionate method; none automatically requires a weighted matrix.
2. Inventory realistic alternatives and existing dispositions. Include continuation
   or no change when meaningful. Preserve independent architecture axes and equal
   contender status where evidence is missing. More available CAD or analysis is
   not itself superior engineering performance.
3. Separate mandatory criteria, comparative preferences and provisional study
   objectives. Trace each to its actual requirement, constraint or owner preference.
   Define applicability, direction, units/scales and evidence adequacy. Unknown is
   inconclusive, not a zero score, verified failure or permission to pass a gate.
4. Compare the complete alternatives on common mission cases and boundaries,
   including installation, safety, performance, resource demand, construction,
   lifecycle cost and schedule where material. Record missing data and shared
   assumptions. Do not invent weights, utilities, rates, measurements or a winner.
5. Assess uncertainty, dependence, numerical/model limits and preference sensitivity.
   Preserve tied or closely ranked alternatives when plausible changes reverse
   their order. Explain dominated alternatives and the value of another experiment.
   An aggregate benefit cannot compensate for a mandatory violation.
6. Report recommendation, evidence, assumptions, uncertainty and consequences.
   Record the actual decision and rationale separately, including authority/date/
   configuration and implementation evidence when actually known. Identify reopening
   triggers and affected requirements, interfaces, budgets, risks and V&V.
7. Implement authorized model/document corrections and verify unknown/failed gates,
   criterion applicability, missing inputs, ties, sensitivity and decision-record
   completeness. Preserve historical results and owner policy. This skill creates
   no new approval gate for reversible model work.

Native TradeStudies::TradeStudy selects from supplied alternatives under a scalar
objective. It does not establish admissibility, adequate evidence or an authorized
decision. Review/filter mandatory constraints before interpreting a ranking; inspect
all native evaluations and ties. The pinned implementation may return the first
of equal alternatives. Neither that ordering nor a supplied review flag selects
hardware or accepts evidence on the owner's behalf.
