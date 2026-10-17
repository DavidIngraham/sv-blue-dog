# From an observed hazard to enough response distance

[Sensing and encounters](../encounter-feasibility.md) · [Mission simulation](../mission-simulation.md)

How far away must a hazard be when Blue Dog first has a chance to observe it? The answer depends on more than target speed. The observation has to become a usable track, reach guidance, wait for a decision opportunity and leave enough time for the boat to carry out the response. A maneuver already in progress can make that wait longer.

The current [class-specific allocation](../../models/analyses/class-specific-detection.sysml)
separates the distance needed to respond from the reliability needed to support
the safety argument. No common 750 m floor remains in that current policy.
The earlier [response-envelope analysis](../../models/analyses/encounter-envelope.sysml)
and numerical table below preserve the old allocation for comparison; their
750 m fields are historical, not current acceptance criteria.

## The current allocation has three parts

1. **Kinematics:** relative motion, acquisition and delivery, controller occupancy,
   command delay, achieved maneuver and position uncertainty determine the
   minimum response distance.
2. **Consequence allowance:** a reviewed clearance and additional margin reflect
   the target's occupied extent, contact modes and uncertainty. Those choices
   can increase the required distance; they cannot erase the maneuver distance.
3. **Reliability and evidence:** timely acquisition, usable tracks and the
   complete avoidance response each need applicable evidence. Confidence,
   exposure and an explicit review determine whether the installation is
   supported for that class and condition.

Reliability here means timely acquisition **and enough track continuity for the encounter**, not per-frame detector accuracy. The confidence bound must come from applicable independent evidence; a supplied success flag is insufficient.

A numerical distance alone cannot satisfy all three. Current class-specific
clearances, margins and reliability criteria still need evidence and review;
unknown criteria remain unsupported rather than becoming zero or inheriting
approval from the old 750 m number.

| Current target class | Distinction the evidence must preserve |
| --- | --- |
| Commercial tow | Tug, barges and occupied water, including restrictions on its maneuvering |
| Fishing craft | Variable motion, possible drifting and noncooperative observation |
| Fast craft | High closure and any towed person or equipment |
| Sailing craft | Quiet operation, heading changes and rig/occupied extent |
| Windsurfer | High closure and turning; rider, mast and sail, including falls |
| Wingfoiler | Rider, wing, leash and submerged foil; fall and separation transitions |
| Kiter | Rider, board/foil, kite and line sweep through jumps, crashes and relaunch |
| Passenger vessel | Occupied extent and consequences affecting multiple people |
| Occupied kayak | Low profile; possible occupant injury, upset or entrapment |
| Occupied stand-up paddleboard | Standing or fallen occupant; low board profile and loss of balance |
| Person in the water | Direct human exposure, wave occlusion and no protective hull |
| Unoccupied drifting craft | Occupancy must be established; drift, entanglement and secondary hazards remain |

I would investigate a low-energy glancing contact with an intact hull as a
potentially low-severity contact mode. That hypothesis does not apply to every
kayak or paddleboard encounter, nor to direct contact with a person. Relative
speed, angle, appendages, occupancy and possible secondary immersion matter.
Ownship mass and speed also matter, but contact energy alone does not predict injury. An unidentified target or uncertain occupancy must not be assigned a presumed low-consequence class. Before reliable classification, I need a reviewed conservative envelope covering the plausible classes and changes in occupancy; an apparently empty craft may have a person beside it. Without that envelope, admission is unsupported. There is no accepted numerical severity or probability limit yet.

The historical nine-row illustrative class summary retains the older speeds and separations
for comparability. In particular, all four split low-profile classes use the
same inherited 2 m/s and 20 m separation in that sensitivity. Identical calculated
distances therefore do not mean identical consequences or approved allocations.

Wind-sport speed and consequence allocations remain open. The
[location and window assessment](../site-and-environment-evidence.md#traffic-risk-by-location-and-arrival-window)
connects their hazard cases to passage and recovery exposure.

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

The historical illustrative case reuses the five-second acquisition allocation, one-second assessment allowance, two-second command delivery, 15-second maneuver and 15-second contingency. It adds IC-01's separate one-second observation-delivery hypothesis. The acquisition interval must include the work needed to form the declared observation; delivery describes only the subsequent interval before guidance can use it. A measured end-to-end delay that already includes acquisition must not be added to the five seconds again.

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

The combined stationary person/paddle-craft row retains the historical 20 m separation for that old class. It does not replace the four distinct current cases. The weed row assumes a no-contact boundary with zero additional stand-off plus the same 10 m position allowance; it is a sensitivity, not a selected weed-clearance criterion. Real underwater geometry and uncertainties must replace that assumption. The 20–40 m weed detection hypotheses used in earlier studies do not cover this 3 m/s, 39-second case; this does not assign vegetation a 750 m requirement.

The head-on case adds speeds, crossing uses their vector difference, and overtaking uses their difference along the common course. These calculations assume the relative velocity stays constant or is bounded by the supplied magnitude throughout the response. A target turning or accelerating can invalidate the crossing/overtaking bound. If future headings are uncertain, the sum of supported speed bounds is the conservative orientation-independent alternative. A distance screen does not establish closest approach, a clear turn path or navigation-rule compliance.

## What an occupied or slower maneuver changes

For the fast-craft head-on case, the 17-second entry case needs **940 m**; the full residual-at-delivery case needs **1,048 m**. Neither fits the historical 750 m comparison distance. These examples illustrate the old two-second command plus 15-second hold. They do not bound the newer maneuver model: an achieved turn can take longer, and insufficient steering authority can leave it unresolved.

The parameterized analysis therefore accepts separate achieved bounds for the remaining old maneuver and the new avoidance maneuver. When either motion authority or the observation bound is unavailable, it reports **unsupported**, with no finite-distance claim. The numerical `-1` fields in that result mean unavailable, not a negative or zero required range. More range cannot repair a response with no supported completion time.

Reducing ownship speed lowers head-on closing speed, but does not necessarily solve the problem. For the same assumed 39-second response against the fast craft, own speeds of 0, 0.5, 1, 2 and 3 m/s give 625, 645, 664, 703 and 742 m. Those are timing sensitivities only: reduced speed can also reduce rudder authority and lengthen the maneuver. The response duration must be reevaluated with the speed change before admitting an operating condition.

## Can I exclude a rare or difficult target class?

The current scope includes all twelve classes above. The
[challenge](../../models/missions/transgorge.sysml) retains collision avoidance,
applicable nonimpediment duties and other navigation obligations. Class-specific allocation
changes how I substantiate the response, not which river users count.

The old six-class review's 750 m distance is now a historical comparison.
Numerical assessment and command timing also need a response-time basis.
Shorter distances are possible where supported motion, observation and reviewed
clearance allow them; neither an attractive sensor specification nor a presumed
minor contact completes that argument.

### Probability can inform a disposition

L-104 permits an explicitly reviewed residual risk for an identified
safety-critical failure mode. This is not a demand to prove that every imaginable
collision is impossible. It is also not permission to omit a class because the
available sensor cannot see it. The requirement explicitly keeps harm to other
users separate from an attractive aggregate reliability score. L-101's proposed
90% mission-reliability objective is nonbinding and is not a collision-risk budget.

A useful probabilistic argument would distinguish the chance of encountering
the class over the admitted voyage from the chance of collision or other harm
given that encounter and the installed response. It would also assess severity,
uncertainty and shared causes such as glare or weather. The local exposure
evidence must include non-AIS users, the return leg, waiting and recovery near
shore. An AIS-only traffic count cannot establish that paddlers or unpowered
sailboats are rare.

The [existing recovery-risk sensitivity](../../models/analyses/recovery-risk.sysml)
shows how exposure can be studied, but uses hypothetical rates and a conditional
independence assumption for sensing-loss recovery. It establishes neither a
target-class exclusion nor an accepted probability threshold. A simulated
completion fraction or an absence of encounters in a short trial cannot fill
that gap.

Route, time and weather restrictions may reduce exposure if they can be
established and enforced. They still need a disposition for unexpected users;
the sensor's failure to report a quiet target cannot establish that the area is
clear. Daylight-only development trials are possible, but changing the qualifying
mission to daylight only would also revisit C-025, which currently requires night
operation.

USCG guidance treats lookout and collision appraisal as ongoing responsibilities
and cautions against assumptions based on scanty information. A project risk
acceptance does not itself settle compliance with those obligations.
[USCG navigation-rule guidance](https://navcen.uscg.gov/navigation-rules-faqs).

The current decision is to use class-specific allocations and develop their
missing criteria and evidence, while retaining all current traffic classes. The [acoustic comparison](acoustic-sensing.md) evaluates
what sound can contribute without treating acoustic quietness as absence.

## Reproduce and use the result

The [class-specific summary](../../evidence/runs/2026-10-16-class-specific-encounters/summary.json)
records the nine-class illustrative comparison. Its
[manifest](../../evidence/runs/2026-10-16-class-specific-encounters/manifest.json)
identifies the model revision and source hashes. No row supplies an accepted
consequence or reliability allocation.

`BlueDogClassDetection::Summary` reproduces that comparison.
`BlueDogClassDetection::Assessment` checks supplied class-specific bounds and
review declarations. It does not inspect the contents of the referenced records
or establish physical qualification.

The [16 October native summary](../../evidence/runs/2026-10-16-response-maneuvers/encounter-envelope.json)
preserves the table and timing results with source hashes. Its
[manifest](../../evidence/runs/2026-10-16-response-maneuvers/manifest.json)
identifies the source revision shared with the component maneuver study.

The historical response-envelope entry points are:

- `BlueDogEncounterEnvelope::Summary`: the class, geometry, timing-epoch and own-speed sensitivities above.
- `BlueDogEncounterEnvelope::Envelope`: a parameterized case; use subject `BlueDogEncounterEnvelope::study` and explicitly supply observation and motion bounds and `appliesTrafficRequirement` (true for the existing traffic classes, false for the weed sensitivity).
- `ResponseAfterDelivery` and `ResponseFromEntry`: the two timing contracts.
- `RelativeSpeed` and `RangeForResponse`: velocity and distance calculations.

```sh
.tools/develop-23ca2e2f0/sysml models -analysis BlueDogEncounterEnvelope::Summary -json
```

The older parameterized result retains `retainedRequirementM`,
`combinedEnvelopeM` and `fitsRetainedDistance` to reproduce its original
comparison. Those fields are not the current class-specific policy and must not
be used to restore a hidden 750 m minimum. `physicalQualification` remains false.
The new class allocation keeps acceptance and evidence readiness separate from
the illustrative distance calculation.

Next I need synchronized measurements of first detection, usable track delivery, decision opportunity, command delivery and achieved motion. Those records should identify the target extent, relative motion, control state and each clock's starting point. The existing archived criteria and results remain unchanged so that improvements in the response model are compared against an identifiable baseline.
