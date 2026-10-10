# Initial architecture DFMEA

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

Initial hypotheses for the logical architecture. Detection and prevention actions are proposed, not implemented controls. Risks are unassessed; no probabilities or RPNs are assigned. Scope completeness and every disposition remain open. Read cruise-reliability.md for the exposure model.

## Functions and failure modes

| ID | Model element | Function | Failure mode |
| --- | --- | --- | --- |
| FM-001 | hullLeak | Retain buoyancy | Printed seam leaks |
| FM-002 | keelLoss | Maintain righting moment | Keel attachment fractures |
| FM-003 | steeringJam | Control heading | Rudder or linkage jams |
| FM-004 | sailJam | Control sail force | Wing trim jams |
| FM-005 | batteryFault | Supply essential power | Battery disconnects or faults |
| FM-006 | harvestLoss | Replenish stored energy | Harvesting stops |
| FM-007 | powerCommonCause | Keep essential services powered | Shared bus fault disables multiple functions |
| FM-008 | navigationFault | Estimate position and heading | Plausible wrong navigation solution |
| FM-009 | controlLockup | Execute autonomous mission | Controller hangs or repeats invalid command |
| FM-010 | trafficMiss | Avoid other vessels | Traffic conflict missed |
| FM-011 | radioLoss | Provide live observation | Radio link unavailable |
| FM-012 | motorUncommanded | Provide controlled recovery thrust | Motor energizes during qualifying sailing |

[Cruise and reliability analysis guide](<cruise-reliability.md>)

## Causes and effects

| ID | Cause | Local effect | Mission effect |
| --- | --- | --- | --- |
| FM-001 | Cyclic wave load or print defect | Water enters hull | Buoyancy or electrical function lost |
| FM-002 | Fatigue or impact | Ballast detached | Persistent inversion or vessel loss |
| FM-003 | Milfoil wrap, debris or actuator fault | Commanded rudder motion unavailable | Reduced VMG; boundary excursion or collision |
| FM-004 | Bearing wear, salt or drive failure | Trim fixed in unsafe position | VMG loss or overpower/capsize |
| FM-005 | Cell degradation, BMS trip or short | Bus power lost or overheating | Mission loss; possible thermal damage |
| FM-006 | Connector corrosion or panel damage | Persistent energy deficit | Long-hold exposure exhausts reserve |
| FM-007 | Regulator short or common water ingress | Navigation, actuation and telemetry lost together | Mission and observation lost |
| FM-008 | Bias, stale data or corrupted input | Guidance uses wrong state | Boundary/traffic hazard and route failure |
| FM-009 | Systematic software fault or reset corruption | Mission logic stops or is unsafe | No progress or unsafe actuation |
| FM-010 | Sensor blind spot or prediction error | Avoidance not commanded | Collision risk |
| FM-011 | Antenna wetting, shadowing or radio fault | Live data cannot reach shore | Observation outage; autonomy must continue |
| FM-012 | Driver short or command gating fault | Unintended powered propulsion | Challenge disqualification or contact hazard |

## Detection, actions and evidence

| ID | Proposed detection | Recommended action | Owner role |
| --- | --- | --- | --- |
| FM-001 | Ingress sensing; acceptance unproven | Coupon fatigue, seam pressure test and flooded-compartment trial | Hull/structure |
| FM-002 | Attitude sensor; attachment inspection | Proof load and fatigue qualification of joint | Hull/structure |
| FM-003 | Position/current disagreement detection to be designed | Weed-jam injection and autonomous clearing trial | Actuation |
| FM-004 | Command/response monitoring to be designed | Jam test at adverse trim; passive load limiting trade | Actuation |
| FM-005 | Voltage/temperature/current sensing to be verified | Cold/aged-cell loading and BMS fault injection | Power |
| FM-006 | Harvest-current residual monitoring to be designed | No-harvest fault campaign and reserve policy validation | Power |
| FM-007 | Independent health path not yet designed | Assess isolation and independence; common-cause fault injection | Power/system |
| FM-008 | Plausibility checks; independent reference unresolved | Biased/stale-sensor injection across speed/current profiles | Navigation |
| FM-009 | Watchdog and restoration requirements; unverified | Fault injection and persisted-state consistency testing | Autonomy |
| FM-010 | Independent lookout unavailable onboard | Non-AIS traffic scenarios and safe boundary strategies | Autonomy/safety |
| FM-011 | Contact-age monitoring and retained logs | Wet/inverted antenna trials and 24-hour outage/reconnect test | Communications |
| FM-012 | Isolation and qualification latch; unverified | Stuck-driver test and independent propulsion isolation | Recovery |

## Disposition and evidence

| ID | Safety-critical | Disposition accepted | Action evidence accepted | Evidence |
| --- | --- | --- | --- | --- |
| FM-001 | true | false | false | Not yet available |
| FM-002 | true | false | false | Not yet available |
| FM-003 | true | false | false | Not yet available |
| FM-004 | true | false | false | Not yet available |
| FM-005 | true | false | false | Not yet available |
| FM-006 | false | false | false | Not yet available |
| FM-007 | true | false | false | Not yet available |
| FM-008 | true | false | false | Not yet available |
| FM-009 | true | false | false | Not yet available |
| FM-010 | true | false | false | Not yet available |
| FM-011 | false | false | false | Not yet available |
| FM-012 | true | false | false | Not yet available |

## Architecture and requirement links

| From | To |
| --- | --- |
| hullLeak | printedHull |
| hullLeak | enclosureSealing |
| keelLoss | keelAndBallast |
| keelLoss | selfRighting |
| steeringJam | actuation |
| steeringJam | weedSnagSteeringRecovery |
| sailJam | actuation |
| sailJam | sailCommandCadence |
| batteryFault | storage |
| batteryFault | sustainedReserveProtection |
| harvestLoss | harvesting |
| harvestLoss | lowEnergyEntry |
| powerCommonCause | powerManagement |
| powerCommonCause | missionReliability |
| navigationFault | positionAndAttitude |
| navigationFault | navigationAvailability |
| controlLockup | missionManager |
| controlLockup | resetRecovery |
| trafficMiss | collisionAvoidance |
| trafficMiss | trafficSafety |
| radioLoss | telemetryRadio |
| radioLoss | outageAutonomy |
| motorUncommanded | motorSystem |
| motorUncommanded | challengeMotorInhibition |
| DesignFailureReview | criticalFailureDisposition |
| DesignFailureReview | CruiseReliability |
| powerCommonCause | failureRateBudget |
