# Seeing hazards early enough to act

**OOSEM:** System requirements, logical behavior, trades and virtual evidence · [Maturity assessment](development-plan.md)

The immediate architecture question is whether Blue Dog can observe a hazard early enough to maneuver, while retaining enough energy and recovery capability. I connect four investigations: detection distance, uncertain observations, sensing and energy, and casualty recovery. The [executable study](../tools/boat_analysis/mission/encounter_study.py) runs those questions together. Its sensor envelopes are hypotheses for sensitivity analysis, not vendor specifications or a selected installation.

## Challenge the detection-distance allocation

The [encounter allocation](../models/analyses/encounter-review.sysml) measures distance from the nearest physical extent of the target. A tow includes its barges; a reported antenna position is not its boundary. The native calculation is:

**required distance = closing speed × (acquisition + processing + command + maneuver + contingency time) + separation + relative-position allowance.**

The declared baseline uses 5 seconds for acquisition, 1 for processing, 2 for command, 15 for maneuvering and 15 for contingency, plus 10 m relative-position allowance and target-specific separation. Ownship contributes 3 m/s to the head-on closing-speed bound. These are engineering allocations, not observed encounter statistics or legal stand-off distances.

```sysml-report BlueDogEncounterStudyDocuments::Detection
```

The fast-powerboat case drives **724 m**, rounded to the current **750 m** acquisition allocation. Doubling its maneuver time to 30 seconds requires **994 m**. Keeping the 15-second maneuver but increasing processing to five seconds requires **796 m**. Neither variation fits 750 m. The study sweeps six target classes, three maneuver allowances and three processing delays: **54 cases**.

Slower targets require less closing distance, but a person-sized target in darkness can still be the harder sensing problem. The table does not relax the existing all-target 750 m acceptance envelope. A future class-specific allocation needs measured detection and maneuver evidence, explicit operating conditions and an owner-reviewed requirement change.

The mission controller operates every **30 seconds** with a **15-second** drift-then-sail maneuver allowance. One-second sensor sampling does not turn it into the allocated one-second risk update or two-second command implementation. Those timing obligations remain unsupported. The maneuver sweep challenges an assumption; it does not establish a real boat's turning response.

## Observations drive guidance; truth scores consequences

The [observation provider](../tools/boat_analysis/mission/perception.py) samples independent traffic and weed truth. It applies target-class range, day/night range factors, Bernoulli missed detections, delayed delivery, bounded position error, track expiry and scheduled dropouts. AIS coverage applies only to actors explicitly equipped in the scenario. A lost track does not imply clear water.

Guidance receives delivered tracks extrapolated at constant velocity. It does not receive future turns, future appearances or the target's complete scripted path. Exact instantaneous velocity and target dimensions remain hypotheses; this study does not include false positives, clutter-dependent errors, mast occlusion or correlated image/acoustic physics. Range is an all-bearing proxy: sonar beam direction and mounting are not represented. Detection distance uses a circle enclosing the target footprint, which can trigger earlier than the nearest rectangular hull; this optimistic approximation is another reason these cases cannot qualify acquisition range. Position uncertainty expands the perceived footprint.

Independent truth checks executed motion continuously for collision and required clearance. An unseen obstacle can therefore produce a recorded safety violation; truth cannot secretly veto a sailing command. Weed geometry is a separate target class, with contact scored against the swept vessel footprint. This is a coarse proxy for underwater contact, not a resolved keel, rudder or propeller snag model.

An explicit perfect-truth baseline remains available for comparison and for reproducing older experiments. Each result identifies which observation mode it used. The paired study uses the imperfect provider for every sensing hypothesis and retains observations, supervisory decisions, movement history and stopping causes.

## Compare sensing and energy together

```sysml-report BlueDogEncounterStudyDocuments::Energy
```

Every entry is an **assumed combined envelope**, not predicted hardware performance. The ranges are daylight values; the model also declares night factors, latency, misses and track age. Equipped targets use a separate 1,500 m AIS hypothesis. The radar-assisted case assumes longer craft range but still a limited low-target range. Hydrophone cueing receives **no unsupported range improvement**: it adds load while its useful cueing benefit remains unmeasured. Forward-looking sonar changes only the weed-range hypothesis, from 20 to 40 m; it is not credited with detecting every surface target.

The power entries are hypothetical **additional bus loads**, including the proposed acquisition/processing increment. They do not replace the unresolved 4.5 W electronics lump. A real shared-compute design must reconcile replacement loads once. Here the native energy screen charges each increment over the retained candidate's 48.34-hour allowance at 90% discharge efficiency, with no solar credit. All four hypotheses exceed the candidate's roughly 4 Wh headroom. They cannot be selected as drop-in installations on that budget.

The local encounter trials use the candidate's stored energy and baseline demand with the conceptual mission polar, not a correlated candidate maneuver model. Short-run remaining charge is not voyage feasibility. A redesigned energy system needs coupled resizing and full chronological replay; this experiment deliberately stops short of claiming a new feasible vessel.

## Paired encounter and casualty results

The experiment compares five local encounters—equipped oncoming tow, fast non-AIS crossing craft, low-profile drifting target, weed patch and reversing craft—by day and night, with two fixed observation seeds and a 40–60 second outage. Four stack hypotheses give **80 runs**, alongside five perfect-truth baselines. The synthetic corridor is a controlled fixture, not the charted Gorge course. A 120-second horizon is censoring, never a successful voyage or a collision-free operating-envelope claim.

The run records **38 held-command traffic-margin stops**, **two no-safe-control stops** and **40 censored encounters**. A stop is an unresolved continuation, not a demonstrated safe maneuver or station keeping. All five oracle baselines reach the short horizon without completing the voyage; they are retained beside the imperfect cases. These small, selected samples do not rank real sensors or estimate accident probability.

The four added-load hypotheses leave **−157.15, −425.68, −264.56 and −533.09 Wh** respectively. The radar-assisted daylight craft-range hypothesis can cover the baseline 724 m fast-closing allocation, but its assumed night range and the 994 m slower-maneuver case cannot. Range alone therefore cannot select that architecture.

The [archived experiment](../evidence/runs/2026-10-15-encounter-feasibility/encounter-feasibility.json) retains all 54 range cases, stack assumptions, 80 observation histories, five perfect-truth baselines and six casualty outcomes with source hashes. Reproduce it with `python -m tools.boat_analysis.mission.encounter_study`.

Casualty trials exercise declared sensing loss, steering loss, power loss, capsize, depleted energy and adverse current. Steering and power loss have no established independent propulsion/control path, so the supervisor cannot claim powered recovery. Capsize has no inverted capability in this configuration. Sensing-loss recovery is exposed to an unseen obstacle on its route. A geometrically reachable approach does not imply safe navigation or shore capture.

The [real recovery-site assessment](srr-appendix.md#course-and-recovery-decision) remains unresolved. The lateral pickup approach in this experiment is explicitly synthetic; it does not approve a refuge, beaching point, public access or casualty route. R-001, R-002 and R-005 remain open.

## Measurements that could change the choice

Before equipment selection, collect time-stamped detections and misses against independent target truth across target class, range, bearing, lighting, glare and spray. Record first acquisition, tracking gaps, position error, end-to-end latency, processor temperature and average/peak installed bus demand. Separate held-out encounters from calibration data. Use the same recorded encounters for candidate pipelines so a comparison does not confound hardware with different traffic.

Measure the boat's achieved swept maneuver and time under both tacks, low wind and adverse current. Compare the resulting detection-distance envelope with the pipeline's measured observation envelope; reject unsupported conditions rather than shortening the required distance by assumption. Repeat at finer control periods only when the implementation and maneuver model support them.

For recovery, establish surveyed water approaches and shore access, installed upright and inverted thrust/power, current authority, retention and retrieval arrangements. Inject loss of sensing, steering and power to establish which recovery functions remain independent. Until those measurements exist, the useful outcome is an explicit architecture gap and a testable experiment, not risk closure.

**Continue:** [Power budget and sensing trade](energy.md) · [Mission simulator](mission-simulation.md) · [Validation plan](validation-plan.md)
