# Mission and requirements

Working baseline, October 9, 2026. The SysML source is [models/blue-dog.sysml](../models/blue-dog.sysml). This page records decisions, rationale, and open questions; requirement definitions belong in the model.

## Mission agreed with David

Design for an autonomous sailing round trip from the Bonneville area to The Dalles area and back, with multi-day endurance and energy harvesting. Supervised local trials are proposed validation steps toward that mission, not a replacement design target.

The original Microtransat inspiration became a smaller trans-gorge idea: complete the Gorge Blowout course, with the longer round trip as an ambition. David selected the round trip as the electronics design mission on October 9, 2026.

Project objectives are to learn sailing, explore desktop manufacturing, build a complete autonomous system, and learn SysML v2 by modeling the mission and architecture. A persistent swell-monitoring mission with station keeping remains a stretch objective.

"Set and forget" expresses the desired autonomy. Permitted operator intervention, contact-loss behavior, recovery support, and unattended duration are still to be defined. No route coordinates, dam passages, or operating permissions are assumed by this model.

## Proposed mission decomposition

Prepare and launch; sail outbound; turn around; sail home; recover the boat and data. Energy management, health monitoring/recovery, communication, and data recording support the mission throughout. The initial SysML actions express decomposition only; sequencing, concurrency, triggers, and abort paths are the next modeling step.

## Requirements maturity

- **Confirmed intent:** M-001 round trip; M-002 multi-day endurance with energy harvesting. Quantitative acceptance criteria remain open.
- **Legacy intent:** reset recovery, limp mode, communication, and hull-breach resilience from the December 2023 brief. They need refinement and reconfirmation against this mission.
- **Proposed:** energy awareness, navigation/control responsibilities, and mission evidence recording. These are discussion candidates, not approved specifications.

Self-righting, weed resistance, printable hull geometry, and collision-avoidance/compliance goals are system-level concerns to carry into later model revisions. The old frame cost target does not establish an electronics budget. The 2023 component list is historical input, not the selected architecture.

## How we will turn intent into requirements

For each requirement, agree on an operating condition, measurable outcome, threshold, and verification method before calling it baselined. Candidate verification work includes:

| Requirement | Proposed evidence | Missing acceptance parameters |
| --- | --- | --- |
| M-001 | Mission track and recovery record | Endpoints, corridor, completion time, interventions allowed |
| M-002 / E-001 | Measured loads and mission energy balance, followed by endurance trial | Days, no-harvest autonomy, harvest scenario, reserve |
| E-002 | Bench/simulation checks followed by sailing trials | State accuracy, control rates, wind/current/wave envelope |
| E-003 | Reset injection during representative operating modes | Recovery time, retained state, permitted actuator transients |
| E-004 | Controlled low-energy test | Trigger thresholds, loads retained, recovery objective |
| E-005 | Communication and contact-loss tests | Coverage, telemetry interval, outage duration, command policy |
| E-006 | Controlled ingress-response test | Detectable/tolerable ingress, response time, pumping demand |
| E-007 | Log replay and abrupt power-loss test | Sampling rates, retention period, tolerated data loss |

These are proposed verification approaches; no passing result or satisfaction link is claimed.

## Decisions to work through next

1. How many days should the round-trip energy budget cover, and how long must the boat operate without useful harvested energy?
2. Which harvesting methods should be considered? Solar has not yet been selected.
3. What are the departure, turnaround, recovery areas, and operating envelope?
4. What must it do when it loses communications, cannot make progress, or runs short of energy?
5. What sail/steering mechanism and actuators will the electronics support?
6. What mass, space, cost, and electrical limits apply to the electronics?
7. Which SysML v2 editor/validator should we use?
