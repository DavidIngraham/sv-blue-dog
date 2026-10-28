# Decision-record structure normalization — 2026-10-23

The authorized change is structural normalization without further engineering
decisions. Existing dispositions, open questions, assumptions, constraints, owner
policy and acceptance status remain authoritative and unchanged.

## Structure and scope

- Twenty existing records use `EngineeringDecisions::DecisionRecord`, a shared
  project-defined item definition: eight design dispositions, six requirement-basis
  statements and six open questions. The former `Decision` and `OpenDecision` part
  definitions are removed. Existing qualified names and U01–U06 short names remain.
- Fourteen retained records describe working dispositions; six describe open
  questions. These states describe existing content, not formal approval. Mixed
  assumptions/constraints remain intact for a future content review. They have not
  been split into newly approved decisions.
- Fourteen original context annotations retain their scope, kind, responsibility,
  comparison/evidence basis and reopening triggers. Actual authority/date/record/
  implementation identities remain absent where originally absent.
- Eighty allocation/procedure review annotations retain their identities, subjects
  and values. Their existing `AllocationDecision` metadata definition specializes
  a shared `AllocationReview` metadata definition. They are attached review
  information, not automatically eighty additional standalone decision records.
- Native publication queries and the decision audit include all twenty records,
  including the six previously absent from the decision register. Allocation and
  procedure reviews retain their existing dedicated register.

## Sources and interpretation

[OMG SysML 2.0 Part 1, formal/2026-03-02, §7.10](https://www.omg.org/spec/SysML/2.0/Language/PDF)
defines items as identifiable objects acted on over time; §7.11 distinguishes parts
that can perform actions. Information records use items, subject annotations use
metadata, and runtime control branching remains behavior. This schema is project
tailoring, not a claim of a normative SysML decision-record type.

[NASA SE Handbook §6.8.1.2–6.8.1.3](https://www.nasa.gov/reference/6-8-decision-analysis/)
distinguishes evaluation, recommendation and the actual disposition with supporting
assumptions, limitations and rationale. Normalizing a record does not make an
engineering selection or accept evidence.

## Native preservation and validation

The pinned native runtime is `23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2`, operated
through the matching local Python client. The differently configured connected
MCP workspace is not used for this checkout.

`preservation.py` compares native document-query projections before/after. It
requires identical record text, questions, owners, acceptance values, short IDs,
rationale, issues, fourteen context projections, eighty allocation/procedure review
rows and forty-three supporting dependency identities/endpoints. Only the intended
PartUsage-to-ItemUsage endpoint kind change is normalized in the comparison.

The native editor does not expose a declaration-kind conversion. Guarded literal
syntax edits were validated by native strict parsing and semantic projections;
no alternate parser or relationship engine was introduced.

Native parsing, semantic preservation, the expanded decision audit, model
preparation and patch whitespace checks pass.

- Full regression: **1,097 passed**, zero failures/errors/skips, 1,227.38 seconds
  ([JUnit](full.xml), [log](full.log)).
- Local publication: **36 pages built** ([log](publication.log)). The generated
  decision register includes all twenty information items.
- Final native preservation check passes. The exact model and audit source
  fingerprints match the audited content, and all three rig assessments match the
  pre-migration assessments ([validation summary](validation-summary.json)).
- The focused run had 27 passing checks and one publication assertion expecting
  an unformatted SysML identifier. The renderer correctly uses readable names;
  the assertion now checks the preserved engineering statement. Its targeted rerun
  and the complete final suite both pass.

Final native model hash:
`2db64b0fc2097a37aa7a251e11ba513ef6b4c4efe36d2ffcc6e47b5cee9749ef`.

No new engineering selection, evidence acceptance, decision authority/date or
approval was introduced. Splitting mixed assumptions/constraints and resolving
the open engineering questions remain future content work, as requested.
