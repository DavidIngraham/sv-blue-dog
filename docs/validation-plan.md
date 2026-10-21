# From virtual evidence to water trials

**OOSEM:** Verification, validation and learning · [Current assessment](current-assessment.md)

Which measurements could change the boat I build? IC-01 gives me a specific geometry, load budget and recovery architecture to challenge. I will start with experiments that could force a different sensor, propulsion system, rig or structure, then integrate the supported choices into the first boat.

## What I need to establish

I organize verification around the [current Gorge obligations](requirements.md): mission qualification, safe autonomous operation, usable energy and recovery reserve, environmental survival, construction and handling. The model identifies 237 current requirements and two provisional reliability study objectives, each with a verification objective. The 12 future statements concern separate missions and do not set acceptance criteria for the Gorge boat. Their procedures depend on the conditions and configurations selected for those missions.

A defined objective says what must be assessed. A procedure says how to collect the evidence. An executable predicate evaluates supplied inputs; an analysis or simulation supplies evidence within its validity domain. Physical testing establishes what an identified installation actually does. I can accept a claim only when the evidence addresses its criterion and conditions. The planned cases remain inconclusive when that evidence is absent; a simulation pass does not establish physical qualification.

## Navigation-rule entry review and adjudication

The challenge's C-007 requires the [U.S. Inland Navigation Rules](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-E) and applicable local provisions. Before entry approval, the organizer reviews the identified boat, course, propulsion modes, operating conditions and current rule/notice baseline. The entrant supplies applicability decisions, justified exclusions, observation and maneuver limits, predeclared acceptance criteria and supporting demonstrations. Unsupported conditions cannot enter the admitted operating envelope.

The [model verification cases](../models/missions/verification.sysml) each verify `GorgeChallenge::navigationRules` and link to their legal sources:

| Model case | Source and review scope |
| --- | --- |
| `InlandApplicabilityVerification` | [Rules 1–3](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-E/part-83/subpart-A): jurisdiction, definitions, responsibility and exceptions |
| `InlandLookoutAndAvoidanceVerification` | [Rules 5–8](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-E/part-83/subpart-B): lookout, safe speed, risk and avoidance |
| `InlandEncounterConductVerification` | [Rules 11–18](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-E/part-83/subpart-B): sailing, overtaking, other relevant encounters and give-way/stand-on duties |
| `InlandChannelAndVisibilityVerification` | [Rules 9, 10 and 19](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-E/part-83/subpart-B): channels, applicable traffic separation and restricted visibility |
| `InlandSignalsVerification` | [Rules 20–37 and applicable annexes](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-E): lights, shapes and sound signals across operating modes |
| `NavigationRulesEntryAndAdjudicationVerification` | C-007: entry evidence and consistent qualification decisions |

All six cases remain **inconclusive**. They provide a structure for assessing compliance, not a finding that Blue Dog complies. The applicability review must account for provisions beyond these grouped cases where relevant. Physical demonstrations, simulation evidence and unresolved gaps remain distinct; passing a limited software rule subset cannot close C-007.

After an attempt, the organizer reviews retained observations, commands, motion history and independent evidence where available. A collision, established rule breach or unsafe conduct requiring intervention disqualifies the attempt. Operator intervention or motor use ends qualification even when it prevents a breach; compliant autonomous avoidance does not by itself do so. Insufficient evidence leaves qualification unconfirmed. Record the reason for each decision. Demonstrations must use controlled conditions without staging hazardous encounters with uninvolved users.

## Start with measurements that change a decision

| First experiment | What I would measure | What could change |
| --- | --- | --- |
| Run an identified sensing pipeline against recorded targets | Detections, misses and latency synchronized with bus power and temperature | Sensor/processor choice, energy budget and usable conditions |
| Disconnect primary power, steering or observations on a recovery bench | Backup startup, isolation, observation continuity and demand | Whether the independent path can be credited after each fault |
| Test recovery propulsion and battery under load | Upright/inverted thrust, speed, peak demand and usable energy | Propulsor, battery capacity and spacing of recovery approaches |
| Load construction coupons and joints after wet exposure | Strength, stiffness, bond behavior and failure mode | Laminate, seams and structural mass |
| Compare rig and actuator fixtures | Forces across both tacks, trim torque and electrical demand | Soft-sail or rigid-wing choice and sailing predictions |
| Survey and trial a shore approach | Access, hazards, capture, retention and one-person pickup | Which recovery destinations can enter the mission plan |

Before each experiment I will record the configuration, predicted result, uncertainty and result that would change the decision. Coupons and fixtures can answer these questions before a complete boat exists. My first integrated vessel will be a refined IC-01-scale build.

## Exercise decisions before physical integration

IC-01 passes a [bounded set of local integration cases](encounter-feasibility.md#close-the-candidate-loop), using its own mass, sailing performance, electrical demand and independent recovery allocation. The [acceptance requirement](../models/analyses/integrated-candidate.sysml) requires those capabilities to work together. Safe abort remains distinct from course completion, and a modeled recovery approach remains distinct from physical shore retention.

<details>
<summary>Which integration assumptions each physical test must establish</summary>

| Critical assumption | Physical evidence needed | Decision affected |
| --- | --- | --- |
| Detection range, misses, latency and night performance are available simultaneously within the allocated power and mass | Synchronized target truth, detections, power, temperature and installation mass for an identified pipeline; held-out adverse conditions | Sensing architecture and admissible operating conditions |
| Solved sailing performance and allocated maneuver time represent the boat | Measured polars, current, heading and swept tracks, including tacks and command-to-motion delay | Course feasibility, separation and detection lead time |
| The independent recovery path survives primary sensing, steering or power loss | Fault-injection tests of isolation, startup, navigation and backup observations under load | Whether recovery can be credited after each casualty |
| Upright and inverted recovery authority fits the protected energy | Thrust/speed/power tests in representative current, with usable battery capacity and load transients | Recovery battery, propulsion and refuge spacing |
| A water approach is a usable retrieval destination | Surveyed access, approach hazards, landing/capture and retention trials | Permitted course and launch conditions |
| Static mass, structure and flotation predictions transfer to the build | Weighed assemblies, material/joint coupons, watertightness and flotation/righting measurements | Geometry, handling and casualty survivability |

</details>

I will also replay recorded observations and injected faults through the mission decisions, then measure the commanded response. That connects the logical policy to actual sensor and actuator delays. Capsize testing must distinguish safety capability while inverted, unassisted righting and restored upright control; powered recovery is a separate, disqualified path.

[Runtime instructions](reference/model-runtime.md#reproducing-the-ic-01-integration) reproduce the virtual campaign. Its results help target the experiments above; they do not replace them.

## Measure sensing and shared compute as an installation

The [physical shortlist](reference/sensing-configurations.md) supplies two fixed
camera layouts and a scanning comparison. I will first check whether each camera
can support detection and metric range/motion estimation against independent
target truth. Useful image resolution alone does not establish a usable track.
I will then measure the complete sensor and compute installation at the regulated bus,
including acquisition, processing and thermal behavior. I will record the hardware and
software revision, instruments, clock basis and operating conditions so the
electrical and observation results describe the same installation.

I will pair detections and misses with independently observed targets and synchronized power and command timestamps. I will keep occupied kayaks, occupied stand-up paddleboards, people in the water and unoccupied craft separate, including uncertain occupancy. Results must distinguish range, target class, lighting and obscuration: an average can hide the conditions that determine whether the boat can operate. Held-out encounters will test the calibrated model independently.

I will measure whether a usable track arrives before the class-specific response distance is consumed, separately from how much maneuver distance is needed. I also need the complete avoidance response: reliable detection cannot compensate for unreliable steering or an obstructed escape path. Consequence studies must identify ownship mass and speed, relative motion, contact geometry and exposed people. A computed contact energy is not an injury model; neither a glancing-contact hypothesis nor a successful avoidance trial supplies an accepted severity or probability threshold.

Latency statistics cover delivered detections; missed targets must remain visible separately. An observed electrical peak is limited by instrument bandwidth and sampling. The [measurement reference](reference/sensing-measurements.md) defines the records and accounts for any base electronics load replaced by shared compute. No installed dataset has yet established these capabilities.

The [response envelope](reference/encounter-envelope.md) identifies the clock
boundaries to measure, including a target arriving during an occupied maneuver.
The [maneuver study](reference/maneuver-dynamics.md) identifies heading, speed
and swept path as separate observables. I will repeat the measurements across
tacks, gybes, low water-relative speeds and degraded steering, retaining
unfinished responses as failures to establish a bound. These measurements will replace the provisional
coefficients before they support a physical operating envelope.

## Integrate in bounded steps

I will establish individual sensors, actuators and electrical behavior on the bench, then exercise integrated state transitions and faults. Those cases include unavailable communications, loss of safety capability and the transition from a qualifying attempt to recovery. Controlled flotation and recovery trials will precede short local-water missions; I will extend the operating envelope only with supporting evidence.

Evidence transferred from a fixture must identify which geometry, hardware and conditions still apply to the assembled boat. Controlled capsize trials must measure both recovery and the safety functions needed during it.

## Compare predictions with measurements

Before each water trial, I will identify the verification objective, test article and instrumentation, and check conditions, boundaries, shore retrieval and emergency response. The trial must answer a bounded question with the available equipment and recovery arrangements.

I will compare measurements with predictions and retain failures and incomplete observations. The differences will define where the model is useful and whether I need another experiment, a different design or a wider trial.

See the [current assessment](current-assessment.md#reading-the-evidence) for the update method and the [modeling method](methods/modeling.md) for the evidence links.



## Wind-sport encounters and passage windows

The challenge's `WindSportEncounterVerification` exercises the
[wind-sport hazard cases](encounter-feasibility.md#wind-sports-change-both-motion-and-occupied-space),
including falls, separated equipment, kite lines, foils and absent rider response.
Independent observations must establish clearance and response; cooperative
passes alone cannot demonstrate the admitted capability.

`LocationTrafficAdmissionVerification` checks the
[sector and arrival-window assessment](site-and-environment-evidence.md#traffic-risk-by-location-and-arrival-window)
on both legs and recovery routes. I will test a quiet departure with a busy
delayed return, missing background coverage, wind/visibility changes and a
recovery approach that becomes occupied. Both cases remain inconclusive. Software tests
of the exposure arithmetic do not verify observed traffic or authorize launch.

**Next:** [Current assessment and next investigations](current-assessment.md) · [Series guide](index.md)
