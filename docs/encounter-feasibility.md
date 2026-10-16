# Seeing hazards early enough to act

**OOSEM:** System requirements, logical behavior, trades and virtual evidence · [Maturity assessment](development-plan.md)

The immediate architecture question is whether Blue Dog can observe a hazard early enough to maneuver, while retaining enough energy and recovery capability. I connect detection distance, uncertain observations, sensing demand and casualty recovery in the [integrated candidate study](../tools/boat_analysis/mission/integrated.py). Its sailing performance and energy come from the same coupled candidate. Sensing ranges and recovery authority remain explicit allocations, not vendor specifications or a selected installation. The [paired sensing comparison](../tools/boat_analysis/mission/continuation_study.py) remains the evidence for comparing four earlier sensing hypotheses on its declared conceptual vessel.

## Close the candidate loop

IC-01 links an allocated sensing envelope to one-second guidance assessments, explicit command and maneuver clocks, candidate-specific sailing performance and separately accounted recovery energy. Day/night runs pair clear water, a non-AIS crossing, a stationary low target and a weed patch across fixed seeds. Additional cases exercise the solved wind endpoints, primary sensing/steering/power loss, capsize, recovery after passage standby, finer integration and degraded capabilities. The synthetic reach is 600 m between gates in a 700 m wide water domain, with two hypothetical shore approaches. It is a representative integration exercise, not the complete charted Gorge mission.

Normal sailing must complete; an encounter may complete or deliberately abort and reach a recovery approach safely. These outcomes remain separate. A collision, clearance violation, unsupported sailing state, exhausted recovery bank or censored trajectory prevents the applicable acceptance condition from passing. The [native closure requirement](../models/analyses/integrated-candidate.sysml) also requires compatible sizing and explicit assumptions. The [physical evidence plan](validation-plan.md#exercise-decisions-before-physical-integration) identifies what must replace those assumptions.

The allocated day/night range is deliberately a capability target. It does not identify hardware able to deliver that range within the power and mass budget. This local case set also does not cover every high-speed encounter, occupied-maneuver arrival, false positive, correlated obscuration or recovery-route blockage. Broader admission and held-out cases remain necessary before extending a conditional result to the challenge.

The [executed IC-01 record](../evidence/runs/2026-10-15-integrated-candidate/integrated-mission.json) passes the seven native closure conditions. Of 18 nominal/encounter runs, **10 complete** and **eight safely abort to recovery approaches**. All six casualty/end-of-exposure runs reach an approach; these remain disqualified challenge attempts. The clear-water and weed cases preserve their classifications at half-second integration. Eighteen upright/inverted reserve samples fit the independent bank after full energy-exposure standby. Shared primary/recovery power failure and an empty recovery bank produce shore contact, while the short-range weed sensitivity safely aborts. That one short-range result does not establish a reduced sensing requirement. No successful admitted case records collision, clearance violation or unsupported sailing performance.

## Challenge the detection-distance allocation

The [encounter allocation](../models/analyses/encounter-review.sysml) measures distance from the nearest physical extent of the target. A tow includes its barges; a reported antenna position is not its boundary. The native calculation is:

**required distance = closing speed × (acquisition + processing + command + maneuver + contingency time) + separation + relative-position allowance.**

The declared baseline uses 5 seconds for acquisition, 1 for processing, 2 for command, 15 for maneuvering and 15 for contingency, plus 10 m relative-position allowance and target-specific separation. Ownship contributes 3 m/s to the head-on closing-speed bound. These are engineering allocations, not observed encounter statistics or legal stand-off distances.

```sysml-report BlueDogEncounterStudyDocuments::Detection
```

The fast-powerboat case drives **724 m**, rounded to the current **750 m** acquisition allocation. Doubling its maneuver time to 30 seconds requires **994 m**. Keeping the 15-second maneuver but increasing processing to five seconds requires **796 m**. Neither variation fits 750 m. The study sweeps six target classes, three maneuver allowances and three processing delays: **54 cases**.

Slower targets require less closing distance, but a person-sized target in darkness can still be the harder sensing problem. The table does not relax the existing all-target 750 m acceptance envelope. A future class-specific allocation needs measured detection and maneuver evidence, explicit operating conditions and an owner-reviewed requirement change.

The executed timing comparison uses **30-second and one-second assessment schedules**, **two-second command delivery** and a persistent **15-second maneuver**. Pending commands hold the previous heading until delivery; frequent updates cannot restart or shorten a maneuver. The native timing criterion distinguishes the declared schedules, but a passing simulated schedule is not a measurement of installed response.

The table's one-second processing allowance is an allocation. In the replay hypotheses, sensor delivery adds another one or two seconds before the next assessment opportunity. Including both gives **742 m** for the radar-assisted stack and **760 m** for the vision stack at one-second assessment. At 30-second assessment the same bounds are **1,264 m** and **1,282 m**. The vision hypothesis therefore exceeds 750 m even with the faster schedule. The radar-assisted daylight craft hypothesis only narrowly fits; its night and low-target hypotheses still do not. These timing sums are serial allowances for a fresh response opportunity, not measured latency distributions. A pending command or active maneuver blocks selection of another heading; one-second margin checks can request abort but cannot pre-empt that maneuver. Encounters beginning during that occupied interval require additional response-time analysis. Passing the declared schedule criterion does not verify the complete avoidance deadline.

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

The four-stack screening trials use the reference candidate's stored energy and baseline demand with the conceptual mission polar, not a correlated candidate maneuver model. Short-run remaining charge is not voyage feasibility. IC-01 has its own coupled resizing and local chronological replay; its static full-passage energy screen remains separate from complete charted-course execution.

## Continue encounters and casualties to their consequences

The [paired continuation experiment](../evidence/runs/2026-10-15-encounter-continuation/encounter-continuation.json) compares five local encounters: equipped oncoming tow, fast non-AIS crossing craft, low-profile drifting target, weed patch and reversing craft. Two hypothetical stacks, day/night conditions and 30/1-second assessment schedules give **40 runs**, using seed 17 and a 40–60 second observation outage. The synthetic corridor, conceptual polar and candidate energy are a controlled fixture, not the charted Gorge or a correlated candidate maneuver model. The declared one-hour horizon remains a computational bound.

The 40 archived runs produce **10 complete courses, four physical terminal events and 26 unresolved horizons**. Ten attempts trigger a traffic-margin abort; continuation exposes four contacts and leaves six drifting at the horizon. Twenty other attempts remain sailing at the computational limit. A completed course is separate from its safety classification: retained clearance violations still determine the verdict. All 20 one-second cases in that configuration remain censored; the ten completions occur in the 30-second group. Its assessment period also changes the heading-search horizon, and its traces include zero-speed sailing headings, so it does not isolate update frequency. IC-01's fixed prediction horizon and explicit gate-capture policy have their own acceptance cases. Non-preemptive maneuver response remains a timing limit. These selected synthetic cases do not rank real sensors or estimate accident probability.

When no safe command remains, the native supervisor latches abort and chooses available recovery or continued drift. A failed powered attempt also continues into drift. Energy can reach zero without stopping the moving vessel. Independent truth retains clearance violations and scores physical collision; it does not feed an unseen obstacle to guidance. Shore contact is an adverse terminal event, not demonstrated capture. Current-only drift omits windage, wave forcing and capsize dynamics. The point-mass maneuver and heading-search forecast still need correlation against achieved swept motion.

Casualty cases include sensing loss, common-cause steering and power loss, capsize, inadequate recovery energy and adverse current. A synthetic clear-path sensing-loss case exercises reaching the water approach as a positive control. It does not establish an independent backup detector; the preceding [spiral record](simulation-spirals.md#perception-avoidance-and-recovery-in-one-experiment) retains the obstructed recovery case and its collision. The refinement pair repeats a steering-loss continuation at one- and half-second integration steps; it checks numerical consistency for that trajectory, not all encounter geometries.

The four added-load hypotheses retain their **−157.15, −425.68, −264.56 and −533.09 Wh** voyage headrooms. No installed measurements have replaced them. The [measurement procedure](validation-plan.md#measure-sensing-and-shared-compute-as-an-installation) records synchronized load and latency, reconciles shared compute and screens a fixed-passage capacity lower bound. Coupled resizing remains dependent on an identified measured installation.

The archive retains source hashes, assumptions, observation and command traces, complete saved trajectories, casualty outcomes and numerical refinement. `python -m tools.boat_analysis.mission.continuation_study` runs the paired comparison; `python -m tools.boat_analysis.mission.integrated --phase all` runs candidate integration. Historical configurations and their original conclusions remain in the [spiral log](simulation-spirals.md).

The [real recovery-site assessment](srr-appendix.md#course-and-recovery-decision) remains unresolved. The lateral approach is explicitly synthetic; it does not approve a refuge, beaching point, public access or casualty route. R-001, R-002 and R-005 remain open.

## Measurements that could change the choice

Before equipment selection, collect time-stamped detections and misses against independent target truth across target class, range, bearing, lighting, glare and spray. Record first acquisition, tracking gaps, position error, end-to-end latency, processor temperature and average/peak installed bus demand. Separate held-out encounters from calibration data. Use the same recorded encounters for candidate pipelines so a comparison does not confound hardware with different traffic.

Measure the boat's achieved swept maneuver and time under both tacks, low wind and adverse current. Compare the resulting detection-distance envelope with the pipeline's measured observation envelope; reject unsupported conditions rather than shortening the required distance by assumption. Repeat at finer control periods only when the implementation and maneuver model support them.

For recovery, establish surveyed water approaches and shore access, installed upright and inverted thrust/power, current authority, retention and retrieval arrangements. Inject loss of sensing, steering and power to establish which recovery functions remain independent. Until those measurements exist, the useful outcome is an explicit architecture gap and a testable experiment, not risk closure.

**Continue:** [Power budget and sensing trade](energy.md) · [Mission simulator](mission-simulation.md) · [Validation plan](validation-plan.md)
