# Requirement derivation register

Generated from `models/challenge.sysml` and `models/requirements.sysml`; edit the models and regenerate. C-IDs identify challenge rules; M/E-IDs identify vehicle requirements.

## Requirements

| ID | Requirement | Maturity | Statement |
| --- | --- | --- | --- |
| C-001 | CourseCompletion | CONFIRMED INTENT | Threshold: Complete a journey from The Dalles to Bonneville and back to The Dalles. Exact start/finish and turnaround gates, permitted corridor, and crossing evidence remain to be agreed. |
| C-002 | RepeatedOperation | CONFIRMED INTENT | Objective beyond the first completed round trip: repeat The Dalles-Bonneville-The Dalles autonomously for as long as practical. No fixed objective endurance duration has been selected. |
| C-003 | UnassistedAttempt | CONFIRMED INTENT | A qualifying attempt shall complete the round trip without operator intervention. Passive live monitoring is permitted. Any use of remote emergency abort or manual control disqualifies the attempt as unassisted. Restart criteria remain to be agreed. |
| C-004 | SailingPropulsion | CONFIRMED INTENT | A qualifying challenge attempt shall use sailing propulsion without auxiliary motor propulsion. Auxiliary motor use is allowed during development tests, which do not count as challenge attempts. Motor use during an attempt prevents it from qualifying. Whether a disabled motor may remain installed remains to be agreed. The restriction concerns propulsion, not electrical power for onboard systems. |
| C-005 | LiveObservation | CONFIRMED INTENT | Live monitoring shall be available to the operator. Monitoring-link loss shall not interrupt autonomous mission execution. Telemetry shall be retained onboard and transmitted when contact returns. Coverage, update rate, retained data, and outage retention duration are open. |
| C-006 | EmergencyIntervention | CONFIRMED INTENT | Provide remote emergency abort or manual control when a command link is available. Use disqualifies the attempt as unassisted. Emergency abort behavior and the subsequent recovery procedure are open. |
| M-001 | RoundTrip | CONFIRMED INTENT | SV Blue Dog shall complete the imported Gorge challenge threshold and pursue its repeated-operation objective, observing the imported autonomy, propulsion, monitoring, and emergency intervention rules. Challenge rules are owned by challenge.sysml. |
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
| C-001 | M-001 | PROPOSED: The vehicle mission implements the independently defined challenge course. |
| C-002 | M-002 | PROPOSED: Repeated autonomous journeys motivate the existing endurance and harvesting requirement; quantitative sizing remains open. |
| C-003 | E-002 | PROPOSED: The vessel needs onboard guidance and control to complete an unassisted attempt. |
| C-004 | M-001 | PROPOSED: Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. |
| C-005 | E-005 | PROPOSED: Vehicle communications implement live observation and outage data retention. |
| C-006 | E-005 | PROPOSED: Vehicle communications provide emergency commands whose use ends attempt qualification. |
| M-001 | E-002 | PROPOSED: Autonomous completion of the route needs observations, guidance, and actuation. |
| M-001 | E-003 | PROPOSED: A reset during an autonomous journey must not leave mission behavior undefined. |
| M-001 | E-005 | PROPOSED: Mission supervision and recovery need an agreed operator communication policy. |
| M-001 | E-006 | PROPOSED: Recovering the boat after the journey motivates a defined response to small leaks. |
| M-001 | E-007 | PROPOSED: Assessing route completion and learning from the mission requires recorded evidence. |
| M-002 | E-001 | PROPOSED: Multi-day operation with variable harvesting needs energy estimation and load management. |
| M-002 | E-004 | PROPOSED: Harvest shortfalls need an explicit degraded operating mode. |
| E-001 | E-004 | PROPOSED: Available-energy estimates and reserve policy must drive low-energy transitions. |
