# Requirement derivation register

Generated from `models/challenge.sysml` , `models/blue-dog.sysml`, and `models/requirements.sysml`; edit the models and regenerate. C-IDs identify challenge rules; H-IDs identify the Hawaii goal; M/E-IDs identify vehicle requirements.

## Requirements

| ID | Requirement | Status | Statement |
| --- | --- | --- | --- |
| C-000 | TransGorgeChallenge | open | Complete the autonomous Trans-Gorge sailing challenge: The Dalles-Bonneville-The Dalles as the threshold, then repeat for as long as practical, under the course, autonomy, propulsion, observation, and emergency intervention rules below. |
| C-001 | CourseCompletion | open | Threshold: Complete a journey from The Dalles to Bonneville and back to The Dalles. Exact start/finish and turnaround gates, permitted corridor, and crossing evidence remain to be agreed. |
| C-002 | RepeatedOperation | open | Objective beyond the first completed round trip: repeat The Dalles-Bonneville-The Dalles autonomously for as long as practical. No fixed objective endurance duration has been selected. |
| C-003 | UnassistedAttempt | open | A qualifying attempt shall complete the round trip without operator intervention. Passive live monitoring is permitted. Any use of remote emergency abort or manual control disqualifies the attempt as unassisted. Restart criteria remain to be agreed. |
| C-004 | SailingPropulsion | open | A qualifying challenge attempt shall use sailing propulsion without auxiliary motor propulsion. Auxiliary motor use is allowed during development tests, which do not count as challenge attempts. Motor use during an attempt prevents it from qualifying. An auxiliary motor may remain installed for vessel recovery. Recovery propulsion is permitted outside the qualifying attempt; use during an attempt ends that attempt without qualification. The restriction concerns propulsion, not electrical power for onboard systems. |
| C-005 | LiveObservation | open | Live monitoring shall be available to the operator. Monitoring-link loss shall not interrupt autonomous mission execution. Telemetry shall be retained onboard and transmitted when contact returns. Coverage, update rate, retained data, and outage retention duration are open. |
| C-006 | EmergencyIntervention | open | Provide remote emergency abort or manual control when a command link is available. Use disqualifies the attempt as unassisted. Emergency abort behavior and the subsequent recovery procedure are open. |
| H-001 | HawaiiVoyage | open | Develop SV Blue Dog toward completing an autonomous sailing voyage to Hawaii. The Gorge challenge is a proving ground for that end goal, not evidence of ocean readiness. Departure point, destination gate, route, duration, environmental envelope, assistance/propulsion rules, and acceptance evidence remain to be agreed; Gorge-specific rules are not automatically ocean mission rules. |
| M-001 | RoundTrip | open | SV Blue Dog shall complete the imported Gorge challenge threshold and pursue its repeated-operation objective, observing the imported autonomy, propulsion, monitoring, and emergency intervention rules. Challenge rules are owned by challenge.sysml. |
| M-002 | MultiDayEndurance | open | The boat shall support multi-day missions using onboard energy storage and energy harvesting. Duration, harvest conditions, and energy reserve TBD. |
| E-001 | EnergyAwareness | open | Estimate available energy and manage electrical loads so recovery functions retain an agreed reserve. Estimation accuracy, reserve, and load priorities TBD. |
| E-002 | NavigationAndControl | open | Acquire navigation and sailing observations, execute mission guidance, and command sail/steering actuators. Accuracy, rates, actuation interfaces, and envelope TBD. |
| E-003 | ResetRecovery | open | Recover from software reset. Restore a defined operating mode and retained mission state with controlled actuator outputs. Restart time and acceptance criteria TBD. |
| E-004 | LowEnergyRecovery | open | Provide a low-energy limp mode. Trigger, remaining functions, and mission response TBD. |
| E-005 | Communications | open | Provide live operator monitoring during autonomous operation. Monitoring shall not require operator intervention in completing a qualifying round trip. Loss of the monitoring link shall not interrupt autonomous mission execution. The vessel shall retain telemetry onboard during an outage and transmit the retained data when contact returns. The operator shall have a remote emergency override for mission abort or manual control when a command link is available. Using this override ends the attempt's qualification as unassisted. Link coverage, displayed data, update interval, outage retention duration, and backlog transmission priority remain to be agreed. |
| E-006 | IngressResponse | open | Tolerate a small hull breach; a bilge pump was proposed. Detection method, tolerable leak, response, and energy allocation remain TBD. |
| E-007 | MissionEvidence | open | Record time-correlated navigation, energy, commands, and faults for mission assessment and learning. Rates, retention, and tolerated data loss TBD. |

## Derivations

Direction: original requirement to derived requirement. These relationships record design reasoning, not proof of satisfaction.

| Original | Derived | Status | Rationale |
| --- | --- | --- | --- |
| C-000 | C-001 | open | This rule refines the overall Trans-Gorge challenge. |
| C-000 | C-002 | open | This rule refines the overall Trans-Gorge challenge. |
| C-000 | C-003 | open | This rule refines the overall Trans-Gorge challenge. |
| C-000 | C-004 | open | This rule refines the overall Trans-Gorge challenge. |
| C-000 | C-005 | open | This rule refines the overall Trans-Gorge challenge. |
| C-000 | C-006 | open | This rule refines the overall Trans-Gorge challenge. |
| C-001 | M-001 | open | The vehicle mission implements the independently defined challenge course. |
| C-002 | M-002 | open | Repeated autonomous journeys motivate the existing endurance and harvesting requirement; quantitative sizing remains open. |
| C-003 | E-002 | open | The vessel needs onboard guidance and control to complete an unassisted attempt. |
| C-004 | M-001 | open | Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. |
| C-005 | E-005 | open | Vehicle communications implement live observation and outage data retention. |
| C-006 | E-005 | open | Vehicle communications provide emergency commands whose use ends attempt qualification. |
| H-001 | M-002 | open | An ocean passage motivates sustained energy autonomy; multi-day operation is an interim capability, not an ocean endurance sizing result. |
| H-001 | E-002 | open | An autonomous Hawaii passage needs ocean guidance and sailing control; its operating envelope remains open. |
| H-001 | E-005 | open | The long-term ocean mission motivates review of monitoring coverage and outage behavior without selecting a radio technology. |
| H-001 | E-003 | open | Extended unattended operation motivates recovery from onboard resets. |
| H-001 | E-007 | open | Ocean mission assessment requires retained voyage evidence; acceptance criteria remain open. |
| M-001 | E-002 | open | Autonomous completion of the route needs observations, guidance, and actuation. |
| M-001 | E-003 | open | A reset during an autonomous journey must not leave mission behavior undefined. |
| M-001 | E-005 | open | Mission supervision and recovery need an agreed operator communication policy. |
| M-001 | E-006 | open | Recovering the boat after the journey motivates a defined response to small leaks. |
| M-001 | E-007 | open | Assessing route completion and learning from the mission requires recorded evidence. |
| M-002 | E-001 | open | Multi-day operation with variable harvesting needs energy estimation and load management. |
| M-002 | E-004 | open | Harvest shortfalls need an explicit degraded operating mode. |
| E-001 | E-004 | open | Available-energy estimates and reserve policy must drive low-energy transitions. |
