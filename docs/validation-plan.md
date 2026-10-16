# From virtual evidence to water trials

**OOSEM:** Verification, validation and learning · [Maturity assessment](current-assessment.md)

What must I learn before building and sailing a refined IC-01? The current calculations identify a possible combination of hull, loads and recovery capability. Physical experiments must establish whether those assumptions hold, starting with measurements that can change the design. The [development plan](current-assessment.md#physical-validation) tracks that evidence; these are planned activities.

## Start with measurements that change a decision

Before building the challenge vessel, I want experiments that separate plausible concepts. Construction coupons inform structural mass and joint assumptions. Wing and actuator measurements inform force and energy predictions. Flotation and capsize experiments inform whether recovery remains possible after an upset. The [structure and recovery methods](structures-and-recovery.md), [sail trade](sail-trade.md) and [energy study](energy.md) describe those questions.

Each experiment needs a declared configuration, predicted result, measurement uncertainty and a decision it will inform. A useful experiment can disprove a prediction. Passing a numerical check is not physical validation.

## Exercise decisions before physical integration

Virtual integration requires **one coherent candidate closing the sensing–guidance–energy–recovery loop in representative simulations**. Its [native acceptance requirement](../models/analyses/integrated-candidate.sysml) requires compatible sizing, normal completion, safe encounter outcomes, casualty recovery, energy sufficiency, executable timing and recorded assumptions together. A safe abort counts as recovery evidence, never as challenge completion. A collision, unresolved horizon, unsupported sailing state or exhausted recovery bank prevents closure of the applicable case. IC-01 passes the declared [bounded case set](encounter-feasibility.md#close-the-candidate-loop); the following physical evidence remains necessary.

The candidate's equipment mass and bus load enter the coupled sizing calculation. Its solved sailing states, swept dimensions and electrical demand then enter the mission simulation. A separate recovery bank and explicitly independent observation, control and thrust path must survive the injected primary fault. Recovery evidence ends at a modeled water approach; it does not establish physical capture or retention. Synthetic local reaches exercise the loop; they cannot establish coverage of every location on the charted Gorge course.

| Critical assumption | Physical evidence needed | Decision affected |
| --- | --- | --- |
| Detection range, misses, latency and night performance are available simultaneously within the allocated power and mass | Synchronized target truth, detections, power, temperature and installation mass for an identified pipeline; held-out adverse conditions | Sensing architecture and admissible operating conditions |
| Solved sailing performance and allocated maneuver time represent the boat | Measured polars, current, heading and swept tracks, including tacks and command-to-motion delay | Course feasibility, separation and detection lead time |
| The independent recovery path survives primary sensing, steering or power loss | Fault-injection tests of isolation, startup, navigation and backup observations under load | Whether recovery can be credited after each casualty |
| Upright and inverted recovery authority fits the protected energy | Thrust/speed/power tests in representative current, with usable battery capacity and load transients | Recovery battery, propulsion and refuge spacing |
| A water approach is a usable retrieval destination | Surveyed access, approach hazards, landing/capture and retention trials | Permitted course and launch conditions |
| Static mass, structure and flotation predictions transfer to the build | Weighed assemblies, material/joint coupons, watertightness and flotation/righting measurements | Geometry, handling and casualty survivability |

These are evidence needs, not measurements already obtained. Passing the virtual milestone permits a more focused physical experiment; it does not qualify the challenge vessel or close its technical risks.

Reproduce the candidate with `python -m tools.boat_analysis.cli prepare`, then `python -m tools.boat_analysis.mission.integrated --phase all`. The sizing phase solves the allocated geometry and loads before supplying performance to the mission phase. The resulting JSON records retain their model and driver hashes, trajectories, energy accounts and acceptance facts. An explicitly supplied warm start may accelerate a fresh sizing solve; it is never reused as acceptance evidence without reevaluation.

The [executable mission logic](mission-simulation.md#executable-supervisory-logic) is exercised with observation outages, interventions and casualty events. The regression cases check sailing inhibition and restoration, a persistent abort latch, and alert queuing without a monitoring link. An isolated change to the modeled event policy changes the simulated response, checking that the logical model actually governs the behavior.

The next evidence is timed sensor and controller replay: feed recorded observations and faults into the decision loop, compare the resulting commands with the modeled intent, then measure the boat’s response. Preserve observation uncertainty and actuator delay when carrying those results into the [mission development spirals](simulation-spirals.md). Passing a supervisory test does not demonstrate detection range, maneuver authority or physical recovery.

## Measure sensing and shared compute as an installation

The [measurement importer](../tools/boat_analysis/mission/measurements.py) accepts synchronized records for one identified sensor/compute stack. Measure the complete declared load at the regulated bus, including acquisition, processing and thermal behavior. State the hardware, pipeline revision, instruments, clock basis, operating conditions, operator and measurement date. Keep raw records and their hashes. No installed measurement is currently available; synthetic regression inputs are labeled `synthetic-test` and cannot qualify hardware.

Record detections and misses against independently observed targets, with synchronized power and command timestamps. Separate target classes, range, lighting and obscuration so an average does not hide an unsupported condition. Retain held-out encounters for comparison. Delivered-detection latency excludes misses, and an observed electrical peak is limited by instrument bandwidth and sampling. The [measurement format and importer](reference/sensing-measurements.md) preserve those distinctions and identify any base electronics load replaced by shared compute.

The continuation regression suite checks command timing, maneuver persistence, energy exhaustion and physical consequences at finer integration steps. The archived paired experiment exposes completed courses, contacts and unresolved horizons separately. Neither software checks nor a synthetic log substitutes for installed measurements.

## Integrate in bounded steps

First establish individual sensors, actuators and electrical behavior on the bench. Then exercise integrated state transitions and faults, including unavailable communications, loss of safety capability and the transition from a qualifying attempt to recovery. Follow with controlled flotation and recovery trials, then short local-water missions before extending the operating envelope.

My first complete boat will be a refined IC-01-scale design. I will use coupons, rig fixtures, actuator benches and flotation experiments to resolve individual questions before integrating that boat. The original CAD testbed is project history, not a separate build ahead of it. Evidence transferred from any fixture must identify the geometry, hardware and conditions that remain applicable.

## Update maturity from each experiment

Before each water trial, connect the objective to its verification case, identify the actual test article and instrumentation, and check conditions, boundaries, shore retrieval and emergency response. Choose a bounded scope that can answer the question with the available equipment and recovery arrangements.

Afterward, compare measurements with predictions, retain failures and censored observations, and update the model's validity limits. Update the affected OOSEM layers with what the evidence supports, what failed or remains uncertain, and whether the next useful step is repetition, redesign or a wider trial. A successful simulated voyage alone does not establish readiness for the physical challenge.

See the [running maturity assessment](current-assessment.md#reading-the-evidence) for the update method and the [modeling method](methods/modeling.md) for the evidence links.

**Next:** [Current assessment and next investigations](current-assessment.md) · [Series guide](index.md)
