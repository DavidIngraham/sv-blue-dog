# Design evidence and open questions

**OOSEM:** Requirements, analysis and evidence · [Maturity assessment](development-plan.md)

This appendix connects the desktop assessments to the candidate design and the evidence still needed. Requirement statements remain in the model and its generated views.

## Model and implementation sources

| Subject | Authoritative source | Assessment focus |
| --- | --- | --- |
| Challenge | [Challenge model](../models/missions/transgorge.sysml) | Course, size, autonomy, traffic and recovery obligations |
| Verification | [Challenge cases](../models/missions/verification.sysml), [vehicle cases](../models/vehicle/verification.sysml) | Methods and missing allocations, not completed verdicts |
| Recovery | [Native physics](../models/libraries/marine/recovery.sysml), [planner](../tools/boat_analysis/mission/recovery.py), [mission engine](../tools/boat_analysis/mission/engine.py) | Current authority, route feasibility, reserve and casualty capability |
| Environmental basis | [Environmental analysis](../models/analyses/environment-review.sysml) | Evidence applicability, coupled exposure and unaccepted margins |
| Design | [Sizing method](sizing.md), [results](results.md) | Eligible local alternatives, refined replay and remaining evidence gaps |

## Environmental interpretation

The [NOAA-hosted gap-flow study](https://repository.library.noaa.gov/view/noaa/28157/noaa_28157_DS1.pdf) supports persistent, spatially varying winter easterlies. Its profiler jet observations must not be substituted for a 10 m surface limit on this course. The archived airport observations likewise need exposure and height interpretation.

The native fetch sensitivity evaluates coupled wind and effective-fetch hypotheses. It does not measure directional fetch, shallow-water transformation, current gradients or traffic wakes. The proposed wave margin is an provisional engineering allocation. A single numerical envelope cannot replace forecast-conditioned trajectory assessment.

## Course and recovery decision

Both legs cross the **closed Hood River lift span**, ENC feature `0226241BDFAB1596`. The chart gives 20.4 m vertical and 74.9 m horizontal clearance. The [Port's published clearance](https://www.portofhoodriver.com/bridge-lift-request) independently identifies this span and notes that clearance changes with pool level. We do not apply its clearance to adjacent spans. The reference route excludes unassessed bridge footprints and applies a 10 m pier allowance. Bridge of the Gods is west of the buoy-16 turnaround and is not a required transit.

Before a water trial, the measured maximum air draft plus wave motion, pool rise relative to the clearance datum and the model's 2 m vertical uncertainty allowance must remain below the available clearance. No bridge opening is assumed. A commercial vessel's constrained passage has priority in our planning: wait outside its conflict region or abort rather than forcing an encounter in the span.

```sysml-report BlueDogSRRReadinessDocuments::SiteDecision
```

```sysml-report BlueDogRecoverySiteDocuments::Shortlist
```

This completes the **desktop selection**, not physical site qualification. Bingen and Stevenson are endpoint choices; Home Valley is the priority intermediate survey sector. Spring Creek and Viento are alternatives, not assumed sheltered harbors. Drano is excluded from the initial autonomous set because its entrance and fishing concentration add casualty-route hazards. No unvisited shoreline point is silently entered as an approved recovery destination.

The [site model](../models/analyses/recovery-site-review.sysml) specifies the survey record and coverage acceptance. Recovery coverage must assess both legs and each casualty state with spatial current, blocked approaches and loss of the nearest site. Every admitted mission trajectory needs reachable recovery before reserve exhaustion. Unknown authority fails that check. Field evidence must verify actual capture, retention and one-person pickup, including access hours. [Bingen prohibits overnight parking](https://www.portofklickitat.com/boat-launch-parks); the [Stevenson launch](https://portofskamania.specialdistrict.org/boat-launch-and-docks) has seasonal docks, so winter retrieval cannot depend on them. [Viento's official access description](https://stateparks.oregon.gov/index.cfm?do=park.profile&parkId=123) establishes river access, not an autonomous landing approval.

## Environmental decision

Use 0–15 m/s mean wind, 20 m/s gusts, 1.5 m significant wave height, 1.5–5 s peak periods and a separate 3 m individual-wave case as the Gorge operational design basis. Current sensitivity remains 0–1.5 m/s. These are engineering allocations supported by source research and fetch sensitivity, not measured return levels or a guarantee of progress at each combination.

Test coupled west-wind/opposing-current seas, east-wind/following-current seas, reversal with residual swell, calm drift, and separate powered-vessel wakes. Use directions that produce adverse loads and control demands; do not assign joint probabilities by multiplying unrelated extremes. Check model validity before interpreting a case—linear waves and the existing polar coverage do not establish capability at the whole envelope.

Recovery stress cases use 25 m/s mean wind, 35 m/s gusts, Hs 2 m, periods 1.5–7 s and a separate 4 m individual wave. Exposure lasts the longest applicable casualty transit plus the declared pickup delay; the design-study pickup allowance is two hours. A longer pickup plan requires a longer exposure and reserve calculation. Calm waiting likewise preserves recovery authority without imposing a fixed 24-hour waiting requirement. Hawaii allocations are unaffected and remain outside the Gorge mission.

## Traffic decision

```sysml-report BlueDogSRRReadinessDocuments::Encounters
```

The [analysis](../models/analyses/encounter-review.sysml) defines six target classes: full commercial tow, fishing/drifting craft, ski/powerboat including a towed person, sailing craft, passenger vessel, and a person or low-profile paddle craft. Exercise head-on, crossing, overtaking, anchored/drifting, changing-course, occluded emergence, bridge and casualty cases in both daylight and darkness. AIS is supplementary; it cannot substitute for the non-AIS cases.

The range budget includes closing speed, acquisition, assessment, command, maneuver, contingency, relative-position uncertainty and separation measured from the target's physical extent. The worst allocated case needs 724 m; 750 m is the proposed common envelope. Qualification observes the actual target, track continuity, one-second assessment, two-second command and 15-second maneuver. It separately checks swept-hull collision, the class-specific project separation and whether Blue Dog impedes a confined vessel. Passing a distance screen alone does not establish navigation-rule compliance.

The mission simulation's 30-second guidance loop and perfect target truth are suitable for coarse route-exposure studies. They **do not verify** these sensing and response requirements. Feasibility needs sensor replay and maneuver evidence before the allocation is considered feasible; a failed demonstration requires redesign or an explicitly changed operating envelope.

## Impaired-sensing recovery decision

Retain the agreed architecture: terminate qualification, alert when possible and begin conspicuous autonomous shore recovery without waiting for the operator. Do not assume an independent backup detector exists.

The [native sensitivity analysis](../models/analyses/recovery-risk.sysml) evaluates loss-of-sensing exposure over passage duration and conflicting-traffic exposure during recovery. A deliberately pessimistic screen treats every conflicting encounter as contact. The assumed rates are varied rather than presented as measured reliability. Shortening recovery reduces exposure, but the calculation does not justify calling the risk negligible.

Fog, waves, power faults and common-cause loss of navigation can correlate failures with traffic exposure or defeat recovery entirely. Assess these as explicit cases, not independent probability multipliers. Injury, entanglement and commercial-vessel impediment matter alongside contact probability. The resulting decision is **proceed with analysis and supervised experiments; no unattended release on this risk argument**. Unattended operation requires measured failure/traffic inputs and casualty demonstrations, with owner acceptance of the residual risk. Failure to support acceptance requires exposure restrictions or additional independent protection.

## Current baseline evidence

[Candidate desktop assessment and refined replay](../evidence/runs/2026-10-13-srr-readiness/srr-readiness.json) · [Fixed-seed mission campaign](../evidence/runs/2026-10-13-srr-readiness/srr-mission-campaign.json)

The route audit finds a 65.989 km reference circuit, chart-clear gates and both legs through the selected bridge span.

```sysml-report BlueDogSRRCurrentDocuments::Summary
```

The candidate has a 440 Wh battery, a 260 mm hull beam and a 1.2 m overall length. Total mass is 10.313 kg. Battery capacity and hull geometry are coupled through mass, reserve buoyancy and installation space.

The refined operating states balance and predict a 33.869 h conditional westerly passage. The existing 25% passage allowance plus six hours gives a 48.336 h energy basis. Available departure energy is 316.800 Wh against 312.826 Wh required, leaving **3.974 Wh positive headroom**. The nominal Gorge structural, packaging, operating and sampled static recovery screens pass at the existing numerical tolerance. These calculations do not qualify hardware or demonstrate adverse-weather robustness. The all-season easterly-progress screen still fails and remains outside the selected-window Gorge profile.

The impaired-sensing sensitivity spans approximately 0.012% to 12.6% under its explicitly assumed loss rates and recovery durations. This wide range supports collecting rate/exposure evidence; it does not support a claim that the residual risk is negligible.

The 32 fixed-seed conceptual mission scenarios produce 18 simulated completions, 13 incomplete runs and 1 censored run. Incomplete cases stop when the coarse controller finds no safe action; the censored case reaches the computational horizon. These are conditional scenario counts, not a measured completion probability.

The candidate evidence is a local refined replay, not a frontier search. Acceptance uses balanced operating cases; the coarse operating-state seed is diagnostic. Battery capacity and beam remain free in subsequent optimization. Mission logic uses a separately identified conceptual vessel and cannot qualify the optimized design.

<a id="review-actions"></a>
## Evidence and next investigations

| Topic | Current basis | Evidence still needed |
| --- | --- | --- |
| Course and bridge | Closed lifting span and chart-constrained route | Current notices, stage, measured air draft and passage margins |
| Recovery sites | Desktop endpoint selections and intermediate survey sectors | Site surveys, route/casualty coverage, physical retention and pickup |
| Environment | Operational and casualty exposure allocations | Physics coverage and measured conditions against the tested envelope |
| Traffic | Target classes, range budget, response timing and pass criteria | Sensing/maneuver feasibility and integrated encounter trials |
| Impaired sensing | Conditional exposure analysis and common-cause cases | Measured rates, casualty demonstrations and supported residual-risk assessment |
| Model consistency | Linked criteria and reproducible replay | Repeated checks as inputs and configurations change |
| Design alternatives | Bounded search and candidate replay | Feasible alternatives with comparable mission evidence |
| Critical physics | Wing, structure, actuation and casualty models | Physical correlation and established applicability |

I use these gaps to choose experiments and refine the architecture. The [maturity assessment](development-plan.md) places their evidence in the context of the whole project.

## Reproducing checks

Use the repository's uv-managed environment and pinned native SysML tool. The model validation, pytest suite and publishing workflow are described in [publishing](publishing.md). Native numerical adapters run in the Linux solver environment with GCC.

Regression checks cover implementation consistency. The candidate acceptance check separately verifies positive energy, balanced operating cases, passing refined Gorge screens and unchanged qualification status.

The recovery fixtures deliberately use synthetic locations and loads. They check current compensation, increasing reserve with exposure, unavailable recovery authority, explicit capsized performance, autonomous recovery without communications, persistent disqualification and independently observed collision consequences. They do not qualify a real shore location.

The [fixed-seed mission campaign](../evidence/runs/2026-10-13-srr-readiness/manifest.json) exercises the current course, mission policy and seeded weather/traffic workflow using the conceptual vessel. It is not a mission-performance replay of the optimized 1.2 m candidate. The independently tested casualty routes remain synthetic pending real recovery-site assessment.

```sh
uv run python -m tools.boat_analysis.evidence.srr --budget 10 --battery-wh 440 --beam-m 0.26
uv run python -m tools.boat_analysis.mission.campaign --count 32 --output build/analysis/srr-mission-campaign.json
```
