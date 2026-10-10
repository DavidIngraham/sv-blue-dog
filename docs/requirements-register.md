# Requirement derivation register

Generated from `models/requirements.sysml`; edit the model and regenerate.

## Requirements

| ID | Requirement | Maturity | Statement |
| --- | --- | --- | --- |
| M-001 | RoundTrip | CONFIRMED INTENT | Threshold: The vessel shall complete an autonomous sailing journey from The Dalles to Bonneville and back to The Dalles. Objective: After the first round trip, the vessel shall autonomously repeat The Dalles-Bonneville-The Dalles route for as long as practical. No fixed objective endurance duration is specified. A qualifying round trip shall be completed without operator intervention. Live operator monitoring shall be available without directing the vessel. Use of a remote emergency override shall disqualify that attempt as an unassisted round trip. Exact endpoints, completion criteria, termination conditions, and monitoring coverage and update interval remain to be agreed. |
| M-002 | MultiDayEndurance | CONFIRMED INTENT | The boat shall support multi-day missions using onboard energy storage and energy harvesting. Duration, harvest conditions, and energy reserve TBD. |
| E-001 | EnergyAwareness | PROPOSED | Estimate available energy and manage electrical loads so recovery functions retain an agreed reserve. Estimation accuracy, reserve, and load priorities TBD. |
| E-002 | NavigationAndControl | PROPOSED | Acquire navigation and sailing observations, execute mission guidance, and command sail/steering actuators. Accuracy, rates, actuation interfaces, and envelope TBD. |
| E-003 | ResetRecovery | LEGACY INTENT | Recover from software reset. Proposed refinement: restore a defined operating mode and retained mission state with controlled actuator outputs. Restart time and acceptance criteria TBD. |
| E-004 | LowEnergyRecovery | LEGACY INTENT | Provide a low-energy limp mode. Trigger, remaining functions, and mission response TBD. |
| E-005 | Communications | CONFIRMED INTENT | Provide live operator monitoring during autonomous operation. Monitoring shall not require operator intervention in completing a qualifying round trip. Loss of the monitoring link shall not interrupt autonomous mission execution. The vessel shall retain telemetry onboard during an outage and transmit the retained data when contact returns. The operator shall have a remote emergency override for mission abort or manual control when a command link is available. Using this override ends the attempt's qualification as unassisted. Link coverage, displayed data, update interval, outage retention duration, and backlog transmission priority remain to be agreed. |
| E-006 | IngressResponse | LEGACY INTENT | Tolerate a small hull breach; a bilge pump was proposed. Detection method, tolerable leak, response, and energy allocation remain TBD. |
| E-007 | MissionEvidence | PROPOSED | Record time-correlated navigation, energy, commands, and faults for mission assessment and learning. Rates, retention, and tolerated data loss TBD. |

## Proposed derivations

Direction: original requirement to derived requirement. These relationships record design reasoning, not proof of satisfaction.

| Original | Derived | Rationale |
| --- | --- | --- |
| M-001 | E-002 | PROPOSED: Autonomous completion of the route needs observations, guidance, and actuation. |
| M-001 | E-003 | PROPOSED: A reset during an autonomous journey must not leave mission behavior undefined. |
| M-001 | E-005 | PROPOSED: Mission supervision and recovery need an agreed operator communication policy. |
| M-001 | E-006 | PROPOSED: Recovering the boat after the journey motivates a defined response to small leaks. |
| M-001 | E-007 | PROPOSED: Assessing route completion and learning from the mission requires recorded evidence. |
| M-002 | E-001 | PROPOSED: Multi-day operation with variable harvesting needs energy estimation and load management. |
| M-002 | E-004 | PROPOSED: Harvest shortfalls need an explicit degraded operating mode. |
| E-001 | E-004 | PROPOSED: Available-energy estimates and reserve policy must drive low-energy transitions. |
