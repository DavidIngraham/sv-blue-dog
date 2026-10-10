# Requirement derivation register

Generated from `models/requirements.sysml`; edit the model and regenerate.

## Requirements

| ID | Requirement | Maturity | Statement |
| --- | --- | --- | --- |
| M-001 | RoundTrip | CONFIRMED INTENT | The system shall support an autonomous sailing mission from the Bonneville area to The Dalles area and back. Exact endpoints and completion criteria TBD. |
| M-002 | MultiDayEndurance | CONFIRMED INTENT | The boat shall support multi-day missions using onboard energy storage and energy harvesting. Duration, harvest conditions, and energy reserve TBD. |
| E-001 | EnergyAwareness | PROPOSED | Estimate available energy and manage electrical loads so recovery functions retain an agreed reserve. Estimation accuracy, reserve, and load priorities TBD. |
| E-002 | NavigationAndControl | PROPOSED | Acquire navigation and sailing observations, execute mission guidance, and command sail/steering actuators. Accuracy, rates, actuation interfaces, and envelope TBD. |
| E-003 | ResetRecovery | LEGACY INTENT | Recover from software reset. Proposed refinement: restore a defined operating mode and retained mission state with controlled actuator outputs. Restart time and acceptance criteria TBD. |
| E-004 | LowEnergyRecovery | LEGACY INTENT | Provide a low-energy limp mode. Trigger, remaining functions, and mission response TBD. |
| E-005 | Communications | LEGACY INTENT | Communicate with an operator. Link coverage, data products, command authority, reporting interval, and behavior during loss of contact TBD. |
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
