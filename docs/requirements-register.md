# Requirement derivation register

Generated natively by OpenSysML from the project models. Status describes work on the model element, not verification. Derivations record design reasoning, not proof of satisfaction.

## Requirements

| ID | Requirement | Status | Statement |
| --- | --- | --- | --- |
| C-000 | TransGorgeChallenge | open | Complete the autonomous Trans-Gorge sailing<br>challenge: The Dalles-Bonneville-The Dalles as the threshold,<br>then repeat for as long as practical, under the course, autonomy,<br>propulsion, observation, and emergency intervention rules below. |
| C-001 | CourseCompletion | open | Threshold: Complete a journey from The Dalles<br>to Bonneville and back to The Dalles. Exact start/finish and turnaround<br>gates, permitted corridor, and crossing evidence remain to be agreed. |
| C-002 | RepeatedOperation | open | Objective beyond the first completed round trip:<br>repeat The Dalles-Bonneville-The Dalles autonomously for as long as<br>practical. No fixed objective endurance duration has been selected. |
| C-003 | UnassistedAttempt | open | A qualifying attempt shall complete the round trip<br>without operator intervention. Passive live monitoring is permitted.<br>Any use of remote emergency abort or manual control disqualifies the<br>attempt as unassisted. Restart criteria remain to be agreed. |
| C-004 | SailingPropulsion | open | A qualifying challenge attempt shall use sailing<br>propulsion without auxiliary motor propulsion. Auxiliary motor use is<br>allowed during development tests, which do not count as challenge attempts.<br>Motor use during an attempt prevents it from qualifying.<br>An auxiliary motor may remain installed for vessel recovery.<br>Recovery propulsion is permitted outside the qualifying attempt; use<br>during an attempt ends that attempt without qualification.<br>The restriction concerns propulsion, not electrical power for onboard systems. |
| C-005 | LiveObservation | open | Live monitoring shall be available to the operator.<br>Monitoring-link loss shall not interrupt autonomous mission execution.<br>Telemetry shall be retained onboard and transmitted when contact returns.<br>Coverage, update rate, retained data, and outage retention duration are open. |
| C-006 | EmergencyIntervention | open | Provide remote emergency abort or manual control<br>when a command link is available. Use disqualifies the attempt as unassisted.<br>Emergency abort behavior and the subsequent recovery procedure are open. |
| H-001 | HawaiiVoyage | open | Develop SV Blue Dog toward completing an<br>autonomous sailing voyage to Hawaii. The Gorge challenge is a<br>proving ground for that end goal, not evidence of ocean readiness.<br>Departure point, destination gate, route, duration, environmental<br>envelope, assistance/propulsion rules, and acceptance evidence<br>remain to be agreed; Gorge-specific rules are not automatically<br>ocean mission rules. |
| M-001 | RoundTrip | open | SV Blue Dog shall complete the imported Gorge<br>challenge threshold and pursue its repeated-operation objective,<br>observing the imported autonomy, propulsion, monitoring, and emergency<br>intervention rules. Challenge rules are owned by challenge.sysml. |
| M-002 | MultiDayEndurance | open | The boat shall support multi-day missions<br>using onboard energy storage and energy harvesting.<br>Duration, harvest conditions, and energy reserve TBD. |
| E-001 | EnergyAwareness | open | Estimate available energy and manage electrical<br>loads so recovery functions retain an agreed reserve.<br>Estimation accuracy, reserve, and load priorities TBD. |
| E-002 | NavigationAndControl | open | Acquire navigation and sailing observations,<br>execute mission guidance, and command sail/steering actuators.<br>Accuracy, rates, actuation interfaces, and envelope TBD. |
| E-003 | ResetRecovery | open | Recover from software reset.<br>Restore a defined operating mode and<br>retained mission state with controlled actuator outputs.<br>Restart time and acceptance criteria TBD. |
| E-004 | LowEnergyRecovery | open | Provide a low-energy limp mode.<br>Trigger, remaining functions, and mission response TBD. |
| E-005 | Communications | open | Provide live operator monitoring during<br>autonomous operation. Monitoring shall not require operator<br>intervention in completing a qualifying round trip.<br>Loss of the monitoring link shall not interrupt autonomous mission<br>execution. The vessel shall retain telemetry onboard during an outage<br>and transmit the retained data when contact returns.<br>The operator shall have a remote emergency override for mission<br>abort or manual control when a command link is available.<br>Using this override ends the attempt's qualification as unassisted.<br>Link coverage, displayed data, update interval, outage retention<br>duration, and backlog transmission priority remain to be agreed. |
| E-006 | IngressResponse | open | Tolerate a small hull breach; a bilge pump<br>was proposed. Detection method, tolerable leak, response,<br>and energy allocation remain TBD. |
| E-007 | MissionEvidence | open | Record time-correlated navigation, energy,<br>commands, and faults for mission assessment and learning.<br>Rates, retention, and tolerated data loss TBD. |

## Derivations

| Original | Derived | Status | Rationale |
| --- | --- | --- | --- |
| transGorgeChallenge | courseCompletion | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | repeatedOperation | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | unassistedAttempt | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | sailingPropulsion | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | liveObservation | open | This rule refines the overall Trans-Gorge challenge. |
| transGorgeChallenge | emergencyIntervention | open | This rule refines the overall Trans-Gorge challenge. |
| courseCompletion | roundTrip | open | The vehicle mission implements the independently defined challenge course. |
| repeatedOperation | multiDayEndurance | open | Repeated autonomous journeys motivate the existing endurance and harvesting requirement; quantitative sizing remains open. |
| unassistedAttempt | navigationAndControl | open | The vessel needs onboard guidance and control to complete an unassisted attempt. |
| sailingPropulsion | roundTrip | open | Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. |
| liveObservation | communications | open | Vehicle communications implement live observation and outage data retention. |
| emergencyIntervention | communications | open | Vehicle communications provide emergency commands whose use ends attempt qualification. |
| hawaiiVoyage | multiDayEndurance | open | An ocean passage motivates sustained energy autonomy; multi-day operation is an interim capability, not an ocean endurance sizing result. |
| hawaiiVoyage | navigationAndControl | open | An autonomous Hawaii passage needs ocean guidance and sailing control; its operating envelope remains open. |
| hawaiiVoyage | communications | open | The long-term ocean mission motivates review of monitoring coverage and outage behavior without selecting a radio technology. |
| hawaiiVoyage | resetRecovery | open | Extended unattended operation motivates recovery from onboard resets. |
| hawaiiVoyage | missionEvidence | open | Ocean mission assessment requires retained voyage evidence; acceptance criteria remain open. |
| roundTrip | navigationAndControl | open | Autonomous completion of the route needs observations, guidance, and actuation. |
| roundTrip | resetRecovery | open | A reset during an autonomous journey must not leave mission behavior undefined. |
| roundTrip | communications | open | Mission supervision and recovery need an agreed operator communication policy. |
| roundTrip | ingressResponse | open | Recovering the boat after the journey motivates a defined response to small leaks. |
| roundTrip | missionEvidence | open | Assessing route completion and learning from the mission requires recorded evidence. |
| multiDayEndurance | energyAwareness | open | Multi-day operation with variable harvesting needs energy estimation and load management. |
| multiDayEndurance | lowEnergyRecovery | open | Harvest shortfalls need an explicit degraded operating mode. |
| energyAwareness | lowEnergyRecovery | open | Available-energy estimates and reserve policy must drive low-energy transitions. |
