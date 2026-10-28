---
name: behavior-modeling-quality
description: Audit and improve operational scenarios, executable actions and state behavior, including permissions, failure responses, concurrency, persistence, resets and architectural allocation. Use for behavior coherence reviews and authorized corrections.
---

# Behavior modeling quality

Establish whether modeled behavior fulfills its operational purpose under applicable conditions. Read [the sourced checklist](references/checklist.md) and [source register](references/sources.md); use the selected language version's semantics.

## Workflow

1. Identify authoritative mission rules, configuration, operational boundary and behavior question. Inventory scenarios, functions, owned actions, state variables, events and performers through the native model. Distinguish descriptive steps, executable policy, numerical dynamics and physical implementation.
2. Follow nominal and degraded paths from observations through assessments, decisions, permissions, commands, achieved response and records. Check input provenance/applicability and positive and inhibited outcomes. A missing guard is not repaired by describing it only in prose. Inspect resolved required/optional parameter multiplicities rather than assuming that omitted multiplicity makes an input mandatory.
3. Apply relevant checklist rows. Record native identities, source/rule IDs, the counterexample, consequence and closure evidence. Read actual requirements before choosing precedence, reset or release rules. Record conflicting or undecided policy instead of inventing it.
4. Correct authorized semantics and affected action parameters, flows, allocations, configuration bindings and verification objectives together. Reuse native calculations; do not implement a second verdict or state-transition engine in a report script. Preserve stable identities and historical runs.
5. Validate through native execution or exploration where supported. Exercise boundaries, missing inputs, restoration, restart, interacting faults and event orders. Demonstrate that removing a material guard changes an expected outcome. State test invariants independently rather than copying production equations.
6. Update the operational explanation and evidence assessment, then re-audit. Separate defined, executed, integrated and physically demonstrated behavior. Identify unimplemented estimators, scheduling, durable storage and hardware interlocks.

## Decision boundaries

A function decomposition is not execution order. A flow is not automatically a control dependency. Allocation does not create an executable body or schedule. Do not serialize independent work for diagram convenience or invent concurrency without a timing/resource question.

Observation acceptance does not prove the observation. A requested command is not necessarily permitted, delivered, executed or achieved. Recovery may intentionally end qualification; do not inhibit necessary recovery by confusing qualification with safety.

Treat transient unavailability separately from durable restriction. Restored inputs cannot silently clear abort or disqualification. A new test run is not a watchdog restart. Missing persisted state must follow explicit project fallback policy. State ownership, persistence, initialization and reset need consistent meanings in model and caller.

Tailor effort to the question. This skill introduces no universal timeout, priority order, safe state or reliability claim. Native semantics and passing software tests alone do not establish safe deployed behavior.

