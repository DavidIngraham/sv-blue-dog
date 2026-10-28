---
name: interface-contract-quality
description: Audit and improve systems engineering interface contracts, payload semantics, physical compatibility, timing, authority, and cross-layer mappings. Use for interface definition or integration reviews and authorized model corrections.
---

# Interface contract quality

Make each exchange sufficiently precise that its producer, consumer and integration test agree on meaning, applicability and failure handling. Preserve the project's language version and native model authority.

Read [the sourced checklist](references/checklist.md) for the engineering review and [the source register](references/sources.md) to establish the authority and limits of each recommendation. Read only applicable source sections; verify editions when the work depends on current provisions.

## Workflow

1. Establish the subject configuration, lifecycle scope, relevant scenarios and native tool revision. Enumerate internal, external, human, physical and information boundaries through native model queries. Include coallocated interactions and independent recovery paths; coallocation does not eliminate their contracts.
2. Review each boundary against applicable checklist rows. Inspect both endpoints, transformations and consumers. Record a finding with native element identity, observed defect, consequence, source/rule ID, proposed correction, evidence and closure condition. Distinguish incorrect definitions, absent engineering decisions and absent acceptance evidence.
3. Apply authorized semantic corrections with native editing or a reviewed source edit validated by the native parser. Preserve stable identities and established policy. Add fields only when their meaning and consumer obligation are clear. Use model issues for undecided limits and protocols; never infer them from a convenient update period or a diagram.
4. Check mapped logical and physical payload meaning, not just link presence. Test invalid, missing, stale, future, reordered, repeated, mismatched and conflicting inputs where relevant. Parameterized examples may test a predicate without selecting a production limit. Physical and human interfaces require their own compatibility checks.
5. Update affected interface definitions, scenarios, allocations, configuration, verification objectives and explanatory documentation. Re-run the native audit and appropriate regressions. Report what is now defined, what is executable, what is measured and what remains undecided.

## Interpretation constraints

A requirement states an obligation; a design description selects its realization. A flow describes transfer; a dependency does not implement transfer. An allocation does not establish routing, redundancy or fault independence. Use the selected SysML version's semantics rather than importing stereotype rules from another version.

A validity flag is a producer assertion, not evidence of freshness, correct frame or adequate coverage. A negative observation can itself be valid. Source identity and a sequence counter are not authentication. A shared clock identifier is not demonstrated synchronization. Field definitions alone do not implement runtime rejection or transport serialization.

Keep interface changes proportional to the engineering question. Do not apply a digital message envelope to electrical power or a mechanical joint. Do not create artificial traceability merely to make coverage complete. Treat inaccessible standards and summaries as limited evidence, not full-text compliance authority.
