# Simulation studies and their limits

**OOSEM:** Analysis and evidence · [Current assessment](current-assessment.md) · [Simulation methods](mission-simulation.md)

I use simulation to ask whether the boat's functions can work together over a voyage. Sailing performance affects exposure time; sensing consumes energy and determines when guidance can respond; a casualty changes both the available control and the route to safety. A useful result identifies the boat, conditions and assumptions behind that chain.

IC-01 is the working integration candidate. Its local simulations connect its mass, sailing states, allocated observation capability, electrical loads and independent recovery reserve. Other studies use different boats or deliberately simplified fixtures to isolate a question. Their results help identify sensitivities and missing evidence, but cannot be combined into a claim that IC-01 has completed the full Gorge mission.

## Which study answers which question?

| Engineering question | Configuration and method | What the evidence supports | Main limitation |
| --- | --- | --- | --- |
| Can one candidate support sailing, observation and recovery? | [IC-01 integration](encounter-feasibility.md#close-the-candidate-loop) uses candidate-specific sailing performance and separate main/recovery energy accounts. | Bounded local encounters, casualty approaches and end-of-exposure reserve checks. | Hypothetical observation and propulsion capability; no installed sensing stack, full-course safety demonstration or measured recovery envelope. |
| Can a candidate balance its loads and make progress? | [Coupled sizing](sizing.md) solves geometry, mass, structure, operating states and power together. | Conditional operating solutions and constraint margins under named assumptions. | Local search, bounded aerodynamic and hydrodynamic validity, provisional material and equipment inputs. |
| How does the environment change performance? | [Environmental replays](reference/environmental-replays.md) hold identified candidate geometries fixed while varying wind profiles, waves and vessel response. | Sensitivity of forces, progress, loads and energy to environmental assumptions. | Prescribed or linear motion, provisional damping and limited operating coverage. |
| How early must a usable observation arrive? | [Encounter envelopes](reference/encounter-envelope.md) combine target motion, acquisition, decision, command and achieved-response timing. | Required response distance for supplied bounds and control states. | Accepted class margins and observation/whole-response reliability criteria still need evidence. |
| What happens after a command is unsafe or a capability is lost? | [Conceptual encounter continuation](reference/encounter-continuation.md) follows avoidance, powered recovery and drift in synthetic local corridors. | Conditional consequences and energy sensitivity for that fixture. | Conceptual polar, current-only drift and assumed maneuver/propulsion performance. |
| Can navigation-rule assessments guide an encounter? | [Mission rule assessment](mission-simulation.md#navigation-duties-in-the-local-replay) evaluates delivered tracks and supplied vessel/context facts. | Conditional permission and encounter behavior in bounded cases. | Vessel status, intent, channel context and achieved maneuvers are not demonstrated by supplied labels. |
| What can prevent the safety functions from working? | [Failure analysis](reliability.md#how-avoidance-can-fail) connects functional and concept-specific causes to qualitative fault trees. | A basis for choosing measurements and fault-injection trials. | No accepted failure rates, common-cause isolation or complete diagnostic coverage. |

## Read IC-01's results as one configuration

The [candidate results](results.md) identify IC-01's geometry, mass, equipment allowances and energy account. A solved sailing state is an operating point, not an observed voyage. The mission replay uses a bounded performance envelope from those states; behavior outside that envelope needs additional analysis or measurement.

The local integration includes ten completed courses, eight safely aborted encounter approaches and six casualty/end-of-exposure approaches. These outcomes belong to the [15 October integration record](../evidence/runs/2026-10-15-integrated-candidate/manifest.json), its synthetic reach and its declared capabilities. They do not establish full-course completion or safe recovery from every point on the river. The [current assessment](current-assessment.md) identifies which installation and environmental evidence is still missing.

The retained 440 Wh sizing reference has a different beam, mass and electronics allocation. Its small positive nominal energy margin cannot be transferred to IC-01 or used to credit an unmeasured sensing installation. The [energy account](energy.md) explains the separate configurations and the coupling between load, battery mass and passage duration.

## Compare observations, maneuvers and energy together

A sensing hypothesis must identify the targets it can observe, the conditions, latency, error, dropouts and electrical demand. The controller receives those observations; independent simulated truth scores clearance and contact. Missing a target and passing it safely by chance are distinct outcomes.

The [conceptual perception experiment](../evidence/runs/2026-10-15-encounter-feasibility/manifest.json) includes 54 distance cases, 80 paired encounters and six casualty cases. It uses a synthetic corridor, conceptual sailing performance and allocated maneuver timing. The [continuation comparison](reference/encounter-continuation.md) follows casualties through powered recovery or drift. These studies expose unsupported capabilities and energy demands without selecting a sensor.

Scheduling, command delivery and maneuver completion have separate clocks. An observation arriving during an occupied maneuver can require more distance than one arriving when the boat is free to act. The [maneuver study](reference/maneuver-dynamics.md) also distinguishes elapsed time from achieved heading, speed and swept path. A finer numerical integration step must represent the same response assumptions.

The [physical sensing candidates](reference/sensing-configurations.md) and [acoustic comparison](reference/acoustic-sensing.md) identify installations to investigate. Their next inputs are synchronized measurements of usable tracks, missed targets, power, mass and thermal behavior. Those measurements can change the equipment choice, energy budget or admitted operating conditions.

## Carry recovery through the voyage

Recovery depends on position, current, casualty state and remaining usable energy. The [recovery propulsion trade](recovery-propulsion.md) supplies candidate capabilities; the mission assesses whether those capabilities can reach a suitable approach while preserving the required safety functions. Reaching a modeled water approach does not demonstrate shore retention or pickup.

IC-01's recovery path has its own allocated energy and backup functions, but separate model parts do not establish physical independence. Common water ingress, shared power or unavailable observations may defeat both sailing and recovery. Inverted observation, thrust, righting and restored control need configuration-specific tests.

The native [IC-01 demonstration](reference/model-runtime.md#run-the-named-integration-candidate) makes the reserve decision inspectable. In its four-hour, 600 m illustration, the bank has 43 Wh remaining. Upright recovery against 0.4 m/s current needs about 12.55 Wh; the assumed inverted case needs 98 Wh; current equal to the allocated through-water speed leaves no upstream authority. These are conditional arithmetic cases, not measured propulsion performance or approved shore approaches.

## Compare the open trades on common terms

Soft sail, tail-controlled rigid wing and directly rotated fixed-camber wing remain equal development contenders for the Gorge mission. The wing geometry in a sizing case makes that calculation concrete; it does not supply comparative evidence for selecting the rig. The [rig trade](sail-trade.md) needs both-tack performance, trim energy, construction effort, durability and casualty behavior under comparable conditions.

Water and air recovery propulsion likewise need comparable installed thrust, demand, guarding, weed tolerance and inverted-operation evidence. A component advantage matters only if the resulting boat can carry it and use it through the voyage. I want each feasible alternative to face the same declared mission cases with its own mass, performance, energy and recovery capability.

## Establish what an analysis can support

An analysis definition and a configured run have different roles. The model's use
register identifies input exports, historical reviews, conditional physics screens,
rule assessments and evidence-readiness checks. Each declares its domain, excluded
interpretations and the evidence needed for further use. These declarations help
choose an investigation; they do not establish completed validation.

<details>
<summary>Analysis purposes, domains and limitations</summary>

```sysml-report BlueDogAnalysisDocuments::UseRegister
```

</details>

Before using a result, I need its actual configuration and inputs, suitable numerical
checks, relevant measurements, uncertainty and consequential sensitivities. Evidence
appropriate to a simple arithmetic check may be inadequate for a recovery safety
claim. A useful analysis can show that a candidate fails a criterion.

Archived CAD and aerodynamic data remain identified reference inputs. An old
solution can seed a new numerical solve, whose configuration and calculations must
still be current. Missing current results must be regenerated rather than silently
replaced with an archived design. Native execution records carry source, driver and
runtime fingerprints; their existence does not accept the resulting engineering claim.

## Keep assumptions visible when interpreting a result

The [environmental replays](reference/environmental-replays.md) illustrate why configuration identity matters. On the studied 1.4 m boat at 5 m/s reference wind, modeled downwind progress through the water is about 1.19 m/s with uniform wind and 0.66 m/s with the height-dependent profile. This is a sensitivity for that geometry, not IC-01's sailing prediction.

The bounded wave-performance study supplies 32 operating cases for regular waves 0.04 m high with a 3 s period. Its four Gorge replays stop at departure because their requested conditions lie outside that coverage. The [recorded summary](../evidence/runs/2026-10-13-wave-performance/summary.json) therefore supports a limited operating calculation, not a passage estimate.

For every result I need the named configuration, model inputs, environmental conditions, observed or predicted quantities and validity limits. Archive dates and source fingerprints identify those inputs. A completed calculation, a simulated outcome and a physical measurement answer different questions. The [measurement plan](validation-plan.md) turns the consequential uncertainties into the next experiments.
