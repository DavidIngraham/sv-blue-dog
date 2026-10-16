# From virtual evidence to water trials

**OOSEM:** Verification, validation and learning · [Current assessment](current-assessment.md)

Which measurements could change the boat I build? IC-01 gives me a specific geometry, load budget and recovery architecture to challenge. I will start with experiments that could force a different sensor, propulsion system, rig or structure, then integrate the supported choices into the first boat.

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

IC-01 already passes a [bounded set of local integration cases](encounter-feasibility.md#close-the-candidate-loop), using its own mass, sailing performance, electrical demand and independent recovery allocation. The [acceptance requirement](../models/analyses/integrated-candidate.sysml) requires those capabilities to work together. Safe abort remains distinct from course completion, and a modeled recovery approach remains distinct from physical shore retention.

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
camera layouts and a scanning comparison. Start by checking whether each camera
can support detection and metric range/motion estimation against independent
target truth. Useful image resolution alone does not establish a usable track.
Then measure the complete sensor and compute installation at the regulated bus,
including acquisition, processing and thermal behavior. Record the hardware and
software revision, instruments, clock basis and operating conditions so the
electrical and observation results describe the same installation.

Pair detections and misses with independently observed targets and synchronized power and command timestamps. Keep occupied kayaks, occupied stand-up paddleboards, people in the water and unoccupied craft separate, including uncertain occupancy. Separate range, target class, lighting and obscuration: an average can hide the conditions that determine whether the boat can operate. Keep some encounters out of calibration so they can test the resulting model independently.

Measure whether a usable track arrives before the class-specific response distance is consumed, separately from how much maneuver distance is needed. Also measure the complete avoidance response: reliable detection cannot compensate for unreliable steering or an obstructed escape path. Consequence studies must identify ownship mass and speed, relative motion, contact geometry and exposed people. A computed contact energy is not an injury model; neither a glancing-contact hypothesis nor a successful avoidance trial supplies an accepted severity or probability threshold.

Latency statistics cover delivered detections; missed targets must remain visible separately. An observed electrical peak is limited by instrument bandwidth and sampling. The [measurement reference](reference/sensing-measurements.md) defines the records and accounts for any base electronics load replaced by shared compute. No installed dataset has yet established these capabilities.

The [response envelope](reference/encounter-envelope.md) identifies the clock
boundaries to measure, including a target arriving during an occupied maneuver.
The [maneuver study](reference/maneuver-dynamics.md) identifies heading, speed
and swept path as separate observables. Repeat across tacks, gybes, low
water-relative speeds and degraded steering; retain unfinished responses as
failures to establish a bound. These measurements will replace the provisional
coefficients before they support a physical operating envelope.

## Integrate in bounded steps

First establish individual sensors, actuators and electrical behavior on the bench. Then exercise integrated state transitions and faults, including unavailable communications, loss of safety capability and the transition from a qualifying attempt to recovery. Follow with controlled flotation and recovery trials, then short local-water missions before extending the operating envelope.

Evidence transferred from a fixture must identify which geometry, hardware and conditions still apply to the assembled boat. Controlled capsize trials must measure both recovery and the safety functions needed during it.

## Update maturity from each experiment

Before each water trial, connect the objective to its verification case, identify the actual test article and instrumentation, and check conditions, boundaries, shore retrieval and emergency response. Choose a bounded scope that can answer the question with the available equipment and recovery arrangements.

Afterward, compare measurements with predictions, retain failures and censored observations, and update the model's validity limits. Use the result to choose repetition, redesign or a wider trial, and update the affected requirements, design assumptions and evidence assessment.

See the [current assessment](current-assessment.md#reading-the-evidence) for the update method and the [modeling method](methods/modeling.md) for the evidence links.

**Next:** [Current assessment and next investigations](current-assessment.md) · [Series guide](index.md)
