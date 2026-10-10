# Trans-Gorge autonomous sailing challenge

This challenge asks a sailing robot to travel from The Dalles to Bonneville and return under its own autonomous control. The Gorge is a proving ground for a longer-term ambition of sailing to Hawai'i; completing this challenge alone does not demonstrate ocean readiness.

The structure follows the [Microtransat rules](https://microtransat.org/content.php?p=rules&top=rules): course, propulsion, autonomy, safety, and judging. This is an independent project challenge. It does not adopt Microtransat's Atlantic course, boat-size limits, or reporting intervals.

The canonical rules are in [challenge.sysml](../models/challenge.sysml). They stand alone: no Blue Dog architecture is required to read or analyze them. [Vehicle requirements](../models/requirements.sysml) import the challenge and derive implementation responsibilities from it. The agreed intent below still needs measurable acceptance details before it forms a complete competition rulebook.

## Course and achievement

| Level | Agreed intent | Model reference |
| --- | --- | --- |
| Threshold | Complete The Dalles to Bonneville and back to The Dalles. | C-001 |
| Objective | Continue repeating that route autonomously for as long as practical. | C-002 |

Exact start/finish and turnaround gates, permitted corridor, crossing criteria, and any time limit remain open. No dam passage is assumed. No fixed objective endurance duration has been selected.

## Vessel and propulsion

A qualifying attempt uses sailing propulsion without auxiliary motor propulsion (C-004). Auxiliary motors are allowed in development tests; those tests do not count as qualifying challenge attempts. Motor propulsion during an attempt prevents qualification.

Whether a disabled motor may remain installed is an open decision. Electrical power for sensing, computation, communication, and sail or steering actuation is not prohibited by this propulsion rule. No challenge-wide hull dimensions, component choices, or energy-harvesting technology have been selected.

## Autonomy and observation

A qualifying round trip must be completed without operator intervention (C-003). Passive live observation is allowed and live monitoring must be available (C-005). Monitoring is not permission to guide the vessel remotely.

Loss of the monitoring link must not interrupt autonomous mission execution. The vessel retains telemetry onboard and sends the retained data when contact returns. Required coverage, update interval, data fields, retention duration, and backlog priority remain open.

## Emergency intervention and recovery

Remote emergency abort or manual control must be available when a command link is available (C-006). Using it disqualifies the attempt as unassisted. Abort behavior, recovery procedure, and conditions for starting a new attempt remain open.

Operating boundaries, traffic encounters, environmental limits, and recovery arrangements require further definition. The model does not establish operating permission or prove safe behavior.

## Evidence and judging

Qualification requires the course, autonomy, and propulsion rules above to be met. The evidence protocol has not yet been agreed.

Proposed evidence is a timestamped position track showing gate crossings, supported by command/intervention and propulsion-state records. For the endurance objective, completed round trips and elapsed autonomous operation could be reported together. These are proposals for review, not additional accepted requirements or existing test results.

The [generated requirements register](requirements-register.md) records confirmed intent separately from proposed vehicle derivations and legacy design intentions. Neither a derivation arrow nor a successful model analysis counts as verification of the vessel.

## Decisions needed to complete the rules

1. Exact course gates, corridor, and crossing criteria.
2. Whether an inactive auxiliary motor may remain aboard.
3. Attempt start, finish, disqualification, and restart procedures.
4. Environmental limits and emergency/recovery behavior.
5. Monitoring performance and acceptable outage retention.
6. Required evidence, data quality, and any completion time limit.

These decisions will refine the independent challenge first, then flow into the vehicle requirements through explicit derivations.
