# From an observed hazard to enough response distance

[Sensing and encounters](../encounter-feasibility.md) · [Mission simulation](../mission-simulation.md)

How far away must a hazard be when Blue Dog first has a chance to observe it? The answer depends on more than target speed. The observation has to become a usable track, reach guidance, wait for a decision opportunity and leave enough time for the boat to carry out the response. A maneuver already in progress can make that wait longer.

The [native response-envelope analysis](../../models/analyses/encounter-envelope.sysml) separates those intervals and compares encounter geometries. It leaves the existing **750 m acquisition requirement for the six traffic classes** unchanged. A lower traffic-case distance is a sensitivity result, not permission to substitute a shorter-range sensor. A higher distance identifies a combination of response time and conditions that the existing allocation does not cover. Weed cases use the same response calculation without extending that traffic requirement to vegetation.

## What the observation must establish

| Observation | Decision it supports | What is insufficient |
| --- | --- | --- |
| Presence | Recognize a hazard before it enters the remaining response distance | No AIS report, or a detection result without measured misses and false alarms |
| Bearing and its uncertainty | Locate the hazard relative to the intended course and swept boat | A cue with no usable direction, or coverage obscured by the rig |
| Range and its uncertainty | Establish metric clearance and available time | One uncalibrated image or a passive acoustic detection alone |
| Relative motion and timestamps | Bound closing speed and predict conflicts | A stale position, an assumed future course, or presence without a supported motion estimate |
| Relevant physical extent | Keep the complete boat and appendages clear | A tug's antenna position instead of the tow, or vegetation detection without its extent and depth |

Commercial tows, fast craft and towed people need their whole occupied envelope represented. Paddlers, people and low stationary objects need separate detection evidence in waves, glare and darkness. Weed sensing must resolve the region swept by the keel, rudder and recovery propulsor, including thin strands and drifting mats. A downward-looking survey return after the boat has passed is not an early forward warning.

These are observation needs, not a claim that one sensor supplies them all. The model records them in `BlueDogEncounterEnvelope::observationContract`; the [equipment comparison](sensing-configurations.md) considers possible sources of those observations.

## Count each interval once

The illustrative case reuses the existing five-second acquisition allocation, one-second assessment allowance, two-second command delivery, 15-second maneuver and 15-second contingency. It adds IC-01's separate one-second observation-delivery hypothesis. The acquisition interval must include the work needed to form the declared observation; delivery describes only the subsequent interval before guidance can use it. A measured end-to-end delay that already includes acquisition must not be added to the five seconds again.

The one-second assessment allowance is used **once** as the worst phase wait to the next eligible assessment. It is not counted again as an extra processing delay. If a real implementation needs additional processing that is outside acquisition and delivery, that work needs a separate, measured allocation before using this budget.

The occupied-controller wait also needs an explicit starting time:

- **Measured at usable observation delivery:** add the remaining old command/maneuver time, then at most one assessment period, the new command delay and the new avoidance maneuver.
- **Measured when the target enters the envelope:** acquisition and delivery overlap that occupied interval. Start the next assessment after the later of observation delivery and controller release. This version assumes that no new unrelated maneuver starts before the observation arrives.

For acquisition `A`, delivery `D`, assessment phase `P`, new command `C`, new avoidance duration `M` and contingency `R`, the response bounds are:

```text
Residual busy time B measured at delivery: A + D + B + P + C + M + R
Busy-release time E measured at entry:     max(A + D, E) + P + C + M + R
```

The old command delay is included in the residual busy time only if that command is still pending. The new command is counted separately because it has not yet been selected. The contingency is retained as an independent allowance; it is not silently spent to hide the known controller wait.

The fresh example totals **39 seconds**. A known 17-second occupied interval starting at envelope entry gives **50 seconds**, because acquisition and delivery overlap its first six seconds. A full 17 seconds still remaining when the observation arrives gives **56 seconds**. The latter is a different, more adverse timing case; the six-second difference is not a disagreement between calculations.

## Relative motion changes the distance

All velocities must use the same frame. The native calculation takes east/north velocity components and computes their relative magnitude. Adding the same current vector to both vessels leaves relative speed unchanged. A fixed obstacle does not share the boat's current; a drifting weed mat may, so its ground velocity needs its own evidence.

With ownship at 3 m/s, the fresh 39-second budget gives the following illustrative distances. Values include the existing class separation and 10 m relative-position allowance, measured from the nearest relevant physical extent.

| Target | Target speed | Head-on | Right-angle crossing | Same-course overtaking |
| --- | --- | --- | --- | --- |
| Commercial tow including barges | 3.5 m/s | 314 m | 240 m | 80 m |
| Fishing or drifting craft | 1.5 m/s | 206 m | 161 m | 89 m |
| Fast craft including towed person | 15 m/s | 742 m | 637 m | 508 m |
| Sailing craft | 4 m/s | 303 m | 225 m | 69 m |
| Passenger vessel | 4 m/s | 333 m | 255 m | 99 m |
| Person or low-profile paddle craft | 2 m/s | 225 m | 171 m | 69 m |
| Stationary person or low-profile paddle craft | 0 | 147 m | 147 m | 147 m |
| Stationary weed boundary | 0 | 127 m | 127 m | 127 m |

The stationary person or paddle-craft row retains that traffic class's 20 m separation and 750 m acquisition requirement. The weed row assumes a no-contact boundary with zero additional stand-off plus the same 10 m position allowance; it is a sensitivity, not a selected weed-clearance criterion. Real underwater geometry and uncertainties must replace that assumption. The 20–40 m weed detection hypotheses used in earlier studies do not cover this 3 m/s, 39-second case; this does not assign vegetation a 750 m requirement.

The head-on case adds speeds, crossing uses their vector difference, and overtaking uses their difference along the common course. These calculations assume the relative velocity stays constant or is bounded by the supplied magnitude throughout the response. A target turning or accelerating can invalidate the crossing/overtaking bound. If future headings are uncertain, the sum of supported speed bounds is the conservative orientation-independent alternative. A distance screen does not establish closest approach, a clear turn path or navigation-rule compliance.

## What an occupied or slower maneuver changes

For the fast-craft head-on case, the 17-second entry case needs **940 m**; the full residual-at-delivery case needs **1,048 m**. Neither fits the retained 750 m distance. These examples illustrate the old two-second command plus 15-second hold. They do not bound the newer maneuver model: an achieved turn can take longer, and insufficient steering authority can leave it unresolved.

The parameterized analysis therefore accepts separate achieved bounds for the remaining old maneuver and the new avoidance maneuver. When either motion authority or the observation bound is unavailable, it reports **unsupported**, with no finite-distance claim. The numerical `-1` fields in that result mean unavailable, not a negative or zero required range. More range cannot repair a response with no supported completion time.

Reducing ownship speed lowers head-on closing speed, but does not necessarily solve the problem. For the same assumed 39-second response against the fast craft, own speeds of 0, 0.5, 1, 2 and 3 m/s give 625, 645, 664, 703 and 742 m. Those are timing sensitivities only: reduced speed can also reduce rudder authority and lengthen the maneuver. The response duration must be reevaluated with the speed change before admitting an operating condition.

## Reproduce and use the result

The [16 October native summary](../../evidence/runs/2026-10-16-response-maneuvers/encounter-envelope.json)
preserves the table and timing results with source hashes. Its
[manifest](../../evidence/runs/2026-10-16-response-maneuvers/manifest.json)
identifies the source revision shared with the component maneuver study.

The stable native entry points are:

- `BlueDogEncounterEnvelope::Summary`: the class, geometry, timing-epoch and own-speed sensitivities above.
- `BlueDogEncounterEnvelope::Envelope`: a parameterized case; use subject `BlueDogEncounterEnvelope::study` and explicitly supply observation and motion bounds and `appliesTrafficRequirement` (true for the existing traffic classes, false for the weed sensitivity).
- `ResponseAfterDelivery` and `ResponseFromEntry`: the two timing contracts.
- `RelativeSpeed` and `RangeForResponse`: velocity and distance calculations.

```sh
.tools/develop-e002f1668/sysml models -analysis BlueDogEncounterEnvelope::Summary -json
```

The parameterized result distinguishes the scenario's `requiredRangeM` from the unchanged traffic allocation, `retainedRequirementM`. When `trafficComparisonApplicable` is true, `combinedEnvelopeM` is their maximum and `fitsRetainedDistance` reports the timing comparison. When it is false, `combinedEnvelopeM` is only the scenario distance; `fitsRetainedDistance` is false because the traffic comparison is inapplicable, and the status says so. This result establishes no new weed requirement. `physicalQualification` remains false in both cases. A smaller traffic-case budget cannot lower the existing traffic acquisition requirement.

Next I need synchronized measurements of first detection, usable track delivery, decision opportunity, command delivery and achieved motion. Those records should identify the target extent, relative motion, control state and each clock's starting point. The existing archived criteria and results remain unchanged so that improvements in the response model are compared against an identifiable baseline.
