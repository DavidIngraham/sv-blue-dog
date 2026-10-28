# Behavior review checklist

Source IDs refer to [sources.md](sources.md). Classify each applicable row as defect, open decision, evidence gap or demonstrated consistency; justify exclusions.

| ID | Review and closure question | Source basis |
| --- | --- | --- |
| B01 | Does each scenario address a stated goal and identified configuration? | LD 4.3.1.2.1-2 |
| B02 | Are inputs, outputs, failure effects and interfaces explicit? | LD 4.3.1.2.2 |
| B03 | Can the observation-to-response path be followed? | LD; tailored end-to-end probe |
| B04 | Are request, permission, dispatch and achieved response distinguished? | LD interfaces; IM integration; tailored actuation probe |
| B05 | Do guards cover permitted and inhibited outcomes with clear precedence? | S2 7.17.3,7.17.5,7.18.3 |
| B06 | Do flow, binding, sequencing and concurrency retain their actual meanings? | S2 7.17.1,7.17.3-4 |
| B07 | Do forks/joins, decisions/merges and completion avoid unintended waits or dead paths? | S2 7.17.3; tailored reachability review |
| B08 | Are state ownership, initialization and release/reset explicit? | S2 7.17.9,7.18; tailored lifecycle review |
| B09 | Does restart preserve or conservatively restore required restrictions? | S2 state/assignment; project reset rules govern outcome |
| B10 | Do unavailable, invalid, stale and missing inputs take defined paths? | LD failure effects; IM; tailored observation probe |
| B11 | Are interrupting faults and simultaneous events addressed? | LD; S2 states/control; tailored event-order tests |
| B12 | Are repetition, re-evaluation, termination and timeout needs explicit? | S2 7.17.10-12,7.18; project timing criteria |
| B13 | Are human and automated responsibilities allocated without accidental operator dependence? | DSEG 6.2.3; project autonomy rules |
| B14 | Are resource ownership, scheduling and shared-state conflicts resolved or open? | DSEG allocation; tailored resource review |
| B15 | Do fault/restoration/restart tests exercise stated invariants? | PV 5.3.1.2; local regression practice |
| B16 | Are executable decisions, estimators, dynamics and physical evidence distinguished? | DSEG experimental validation; PV; tailored evidence boundary |

Record counterexample, native identity, rule/source, authoritative obligation, correction, affected layers, test evidence and residual limitation for each finding. Do not hide an unimplemented function behind an allocation or nominal trace.
