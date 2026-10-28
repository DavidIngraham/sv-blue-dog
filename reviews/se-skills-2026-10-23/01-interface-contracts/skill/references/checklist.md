# Interface review checklist

Use source IDs from [sources.md](sources.md). Record pass, defect, open decision, evidence gap or justified not-applicable for every applicable row. A structurally populated model is not necessarily an accepted design.

| ID | Review question and closure evidence | Basis |
| --- | --- | --- |
| I01 | Are boundary, origin, destination, stimulus and responsible parties identified, including human interfaces? | NIM 6.3.1.2.1-2; DSEG 6.1.8 |
| I02 | Are logical meaning and physical realization distinguished, with transformations explained? | S2 7.12-7.16; local mapping review |
| I03 | Do data identifiers, types, structure, ranges and encodings agree at both ends? | IDD section 3, individual elements/assemblies |
| I04 | Are quantity kinds, units and conversions explicit? Are sign and reference-frame conventions resolved where needed? | SI chapters 2,5; IDD individual elements; frame check is tailored application |
| I05 | Are accuracy and numerical precision distinguished? | IDD individual elements |
| I06 | Are rate, latency, ordering, buffering, loss and priority behavior defined? | IDD communication methods/protocols |
| I07 | Can consumers distinguish missing, invalid and negative observations? | IDD legality/error handling; tailored validity check |
| I08 | Is age assessed against an established time basis and justified freshness criterion? Avoid treating cadence as proof of freshness. | IDD timing/synchronization; tailored temporal check |
| I09 | Can duplicate, reordered and pre-restart messages be recognized when hazardous? | IDD sequencing/synchronization; tailored restart check |
| I10 | Are command authorization, arbitration, expiry and inhibition responsibilities settled? | IDD safety-related interfaces; tailored authority review |
| I11 | Are configuration and protocol versions mutually applicable? | NIM 6.3.1.2.2-4; DSEG 6.1.8; tailored compatibility check |
| I12 | Do initialization, disconnect, reconnect and recovery preserve required behavior? | IDD establishment/termination/error recovery |
| I13 | Are physical mating, tolerances, loads and electrical compatibility established? | IDD physical compatibility; S2 7.14 |
| I14 | Are relevant safety/security consequences addressed without equating identification with authentication? | IDD safety/security; tailored trust check |
| I15 | Do interface requirements, selected designs and integration checks trace in both directions? | IDD traceability; NIM 6.3.1.2.3 |
| I16 | Are changes jointly reviewed, configuration-controlled and reflected in verification? | NIM 6.3.1.2.1,3-4; DSEG 6.1.8 |

## Decision probes

- A healthy-looking navigation packet has an unknown heading reference: define/identify the reference or reject its applicability; do not assume true north.
- A valid reserve assessment is old: retain its producer validity assertion, but do not call it currently usable without the age criterion.
- An empty traffic list without coverage confirmation cannot establish absence of traffic.
- A radio reports unavailable: that may be a valid link-down observation; missing telemetry is a different condition.
- Both controllers can send a recovery command: distinct parts and source IDs do not resolve authority, safe inhibit or common-cause power loss.
- Two ports connect with the same type: still examine units, timing, startup and physical compatibility. A typed connection alone does not establish integration readiness.

## Review record

For each finding record: native element and named configuration; rule/source; observed condition; engineering consequence; corrected definition or explicit decision owner; verification objective and evidence needed; regression result; remaining limitation. Keep the record outside the model as audit evidence while the model owns the actual contract and open issue.

