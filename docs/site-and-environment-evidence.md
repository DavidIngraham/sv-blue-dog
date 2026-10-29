# Course, recovery sites and environmental evidence

**OOSEM:** Requirements, analysis and evidence · [Current assessment](current-assessment.md)

This reference records where the boat would sail and recover, the environmental allocations used in design, and the evidence still needed at actual sites. Candidate performance is summarized in the [results](results.md); these site and exposure assumptions must be checked for the built configuration.

## Model and implementation sources

| Subject | Authoritative source | Assessment focus |
| --- | --- | --- |
| Challenge | [Challenge model](../models/blue-dog.sysml) | Course, size, autonomy, traffic and recovery obligations |
| Verification | [Challenge cases](../models/blue-dog.sysml), [vehicle cases](../models/blue-dog.sysml) | Methods and missing allocations, not completed verdicts |
| Recovery | [Native physics](../models/libraries/analysis.sysml), [planner](../tools/boat_analysis/mission/recovery.py), [mission engine](../tools/boat_analysis/mission/engine.py) | Current authority, route feasibility, reserve and casualty capability |
| Environmental basis | [Environmental analysis](../models/blue-dog.sysml) | Evidence applicability, coupled exposure and unaccepted margins |
| Design | [Sizing method](sizing.md), [results](results.md) | Eligible local alternatives, refined replay and remaining evidence gaps |

## Environmental interpretation

The [NOAA-hosted gap-flow study](https://repository.library.noaa.gov/view/noaa/28157/noaa_28157_DS1.pdf) supports persistent, spatially varying winter easterlies. Its profiler jet observations must not be substituted for a 10 m surface limit on this course. The archived airport observations likewise need exposure and height interpretation.

The native fetch sensitivity evaluates coupled wind and effective-fetch hypotheses. It does not measure directional fetch, shallow-water transformation, current gradients or traffic wakes. The proposed wave margin is a provisional engineering allocation. A single numerical envelope cannot replace forecast-conditioned trajectory assessment.

## Course and recovery decision

Both legs cross the **closed Hood River lift span**, ENC feature `0226241BDFAB1596`. The chart gives 20.4 m vertical and 74.9 m horizontal clearance. The [Port's published clearance](https://www.portofhoodriver.com/bridge-lift-request) independently identifies this span and notes that clearance changes with pool level. I do not apply its clearance to adjacent spans. The reference route excludes unassessed bridge footprints and applies a 10 m pier allowance. Bridge of the Gods is west of the buoy-16 turnaround and is not a required transit.

Before a water trial, the measured maximum air draft plus wave motion, pool rise relative to the clearance datum and the model's 2 m vertical uncertainty allowance must remain below the available clearance. No bridge opening is assumed. A commercial vessel's constrained passage has priority in my planning: wait outside its conflict region or abort rather than forcing an encounter in the span.

```sysml-report BlueDogSRRReadinessDocuments::SiteDecision
```

```sysml-report BlueDogRecoverySiteDocuments::Shortlist
```

This completes the **desktop selection**, not physical site qualification. Bingen and Stevenson are endpoint choices; Home Valley is the priority intermediate survey sector. Spring Creek and Viento are alternatives, not assumed sheltered harbors. Drano is excluded from the initial autonomous set because its entrance and fishing concentration add casualty-route hazards. No unvisited shoreline point is silently entered as an approved recovery destination.

The [site model](../models/blue-dog.sysml) specifies the survey record and coverage acceptance. Recovery coverage must assess both legs and each casualty state with spatial current, blocked approaches and loss of the nearest site. Every admitted mission trajectory needs reachable recovery before reserve exhaustion. Unknown authority fails that check. Field evidence must verify actual capture, retention and one-person pickup, including access hours. [Bingen prohibits overnight parking](https://www.portofklickitat.com/boat-launch-parks); the [Stevenson launch](https://portofskamania.specialdistrict.org/boat-launch-and-docks) has seasonal docks, so winter retrieval cannot depend on them. [Viento's official access description](https://stateparks.oregon.gov/index.cfm?do=park.profile&parkId=123) establishes river access, not an autonomous landing approval.

## Environmental decision

Use 0–15 m/s mean wind, 20 m/s gusts, 1.5 m significant wave height, 1.5–5 s peak periods and a separate 3 m individual-wave case as the Gorge operational design basis. Current sensitivity remains 0–1.5 m/s. These are engineering allocations supported by source research and fetch sensitivity, not measured return levels or a guarantee of progress at each combination.

Test coupled west-wind/opposing-current seas, east-wind/following-current seas, reversal with residual swell, calm drift, and separate powered-vessel wakes. Use directions that produce adverse loads and control demands; do not assign joint probabilities by multiplying unrelated extremes. Check model validity before interpreting a case—linear waves and the existing polar coverage do not establish capability at the whole envelope.

Recovery stress cases use 25 m/s mean wind, 35 m/s gusts, Hs 2 m, periods 1.5–7 s and a separate 4 m individual wave. Exposure lasts the longest applicable casualty transit plus the declared pickup delay; the design-study pickup allowance is two hours. A longer pickup plan requires a longer exposure and reserve calculation. Calm waiting likewise preserves recovery authority without imposing a fixed 24-hour waiting requirement. Hawaii allocations are unaffected and remain outside the Gorge mission.

## Traffic decision

```sysml-report BlueDogSRRReadinessDocuments::Encounters
```

The historical [analysis](../models/blue-dog.sysml) used six target classes: full commercial tow, fishing/drifting craft, ski/powerboat including a towed person, sailing craft, passenger vessel, and a person or low-profile paddle craft. Exercise head-on, crossing, overtaking, anchored/drifting, changing-course, occluded emergence, bridge and casualty cases in both daylight and darkness. AIS is supplementary; it cannot substitute for the non-AIS cases.

The baseline range budget includes closing speed, acquisition, assessment, command, maneuver, contingency, relative-position uncertainty and separation measured from the target's physical extent. Its historical worst allocated case needs 724 m; that study proposed a common 750 m envelope before additional observation-delivery delays. Current allocation is class- and condition-specific, separating response distance, consequence allowance, observation reliability and whole-response reliability. The historical table is not its acceptance rule. The [encounter study](encounter-feasibility.md) shows how delayed observations change that distance and distinguishes the later IC-01 allocation. The verification plan calls for observing the actual target, track continuity, one-second assessment, two-second command, and achieved maneuver duration and swept path under the admitted conditions. The historical 15-second maneuver allowance is not a verified bound. New hazards during occupied maneuvers need a separate deadline check; the static timing screen does not establish that behavior. It separately checks swept-hull collision, the class-specific project separation and whether Blue Dog impedes a confined vessel. Passing a distance screen alone does not establish navigation-rule compliance.

Earlier experiments in the [encounter method](encounter-feasibility.md) exercise imperfect tracks, explicit command delay and 30-second/one-second schedules, alongside a perfect-truth baseline for coarse route-exposure studies. The later IC-01 campaign uses its own candidate performance and fixed guidance horizon. These conceptual simulations **do not verify** installed sensing or achieved maneuver response. Feasibility needs sensor replay and maneuver evidence before the allocation is considered feasible; a failed demonstration requires redesign or an explicitly changed operating envelope.

## Traffic risk by location and arrival window

I need to know where an encounter is likely to occur and whether Blue Dog can
respond there. A busy riding area with room to maneuver poses a different
problem from one rider appearing beside the bridge approach. I therefore assess
the course in named sectors, including the water between recreation sites.
These are survey scopes, not measured traffic boundaries or approved routes.

```sysml-report BlueDogLocationTrafficDocuments::Locations
```

The first wind-sport surveys should cover Hood River waterfront, Hatchery/Swell
City and Stevenson because the site operators document those activities.
[Viento](https://stateparks.oregon.gov/index.cfm?do=park.profile&parkId=123) adds
another documented windsurfing access point. These priorities reflect the
combination of known use and a plausible conflict with passage or recovery;
I have not assigned numerical likelihood or severity scores.

The [Hood River waterfront](https://portofhoodriver.specialdistrict.org/waterfront)
brings several activities together. [Spring Creek](https://parks.wa.gov/find-parks/state-parks/spring-creek-hatchery-state-park)
and [Swell City](https://cgw2.org/wp-content/uploads/2026/02/01-Friendly-Reminders-About-Swell-City-2026.pdf)
identify wind-sport access. At Stevenson, [Bob's Beach](https://www.portofskamania.org/bob-s-beach)
prohibits kiteboarding from that site and directs kiters to East Point. That is
a launch rule, not evidence that kiters cannot cross nearby water. Likewise,
park opening hours do not establish an empty river after closing.
The [source register](../evidence/traffic/2026-10-16-location-review/sources.json)
records what each source supports. Current works, event schedules and local
restrictions still need review for the proposed mission date.

### Choose a window for the whole passage

For each sector, I need the earliest arrival and latest departure on both legs,
including uncertain sailing progress, waiting and casualty recovery. A quiet
outbound crossing is insufficient if the return falls in an unsupported period.
The boat must also have enough energy, useful wind, observation capability and
a feasible recovery path throughout that interval. Night or calm conditions
may reduce recreation while making sensing or progress worse.

The [native window assessment](../models/blue-dog.sysml)
checks one sector, target class, operating condition and visit at a time. A
reviewed upper encounter-rate bound multiplied by exposure time gives an upper
estimate of expected encounters. It is **not collision probability**. A purely
synthetic comparison illustrates the arithmetic: half an hour at two encounters
per hour gives one expected encounter; at ten per hour it gives five. Neither
rate is a Gorge observation, and no exposure limit has been selected.

The rate must describe entries into the defined encounter envelope and cover
the whole visit's time and conditions. If those change, split the assessment
into separate intervals. Unknown rates remain unknown; they do not become zero.
Even a low estimate cannot pass without an accepted class response allocation,
navigation-rule assessment and supported recovery. I do not credit a rider
with seeing and avoiding Blue Dog.

Before selecting a departure, review every sector and plausible target class,
including connecting reaches, on outbound, return, waiting and recovery paths.
Review cumulative exposure without counting the same encounter twice. Passing
one interval does not admit the mission. No complete mission aggregation or
accepted departure window exists yet. Delay beyond a reviewed interval or
unexpected traffic requires reassessment and a supported waiting, rerouting or
recovery response; moving aside must not create a commercial-channel conflict.

### Use heatmaps to plan observations

[Strava's heatmaps](https://support.strava.com/en-us/articles/16046277-a-guide-to-strava-heatmaps)
can suggest corridors worth observing. Global aggregates the preceding year;
Weekly shows seven days; Night separates sunset-to-sunrise activity. Custom
date filtering applies to personal heatmaps. I have not sampled these maps for
this assessment. Their intensity cannot supply hourly traffic rates or prove
that an apparently quiet area is empty.

At each site, collect time-stamped counts and tracks across wind direction and
strength, daylight, season, weekdays and event days. Record the observation
area, duration, obscuration and missed coverage, including sessions with no
sightings. Use local time with its UTC offset and retain UTC timestamps for
comparison with the passage. Consenting riders' tracks can supplement shore
observations, but repeated runs and uneven recorder participation need to be
accounted for. Estimate speed, turning, falls and equipment extent separately
from how often users appear. Review confidence and sampling bias before using
an upper rate bound; zero sightings alone do not justify a zero rate.

## Impaired-sensing recovery decision

Loss of the required primary safety capability terminates qualification. The boat alerts when possible and attempts conspicuous autonomous shore recovery without waiting for the operator. IC-01 allocates an independently powered observation and control path for that recovery, but its installed performance and independence remain to be demonstrated. Older impaired-sensing studies without that allocation cannot borrow it. If the recovery path is unavailable, the simulation continues the drift and scores its consequences.

The [native sensitivity analysis](../models/blue-dog.sysml) evaluates loss-of-sensing exposure over passage duration and conflicting-traffic exposure during recovery. A deliberately pessimistic screen treats every conflicting encounter as contact. The assumed rates are varied rather than presented as measured reliability. Shortening recovery reduces exposure, but the calculation does not justify calling the risk negligible.

Fog, waves, power faults and common-cause loss of navigation can correlate failures with traffic exposure or defeat recovery entirely. Assess these as explicit cases, not independent probability multipliers. Injury, entanglement and commercial-vessel impediment matter alongside contact probability. The resulting decision is **proceed with analysis and supervised experiments; no unattended release on this risk argument**. Unattended operation requires measured failure/traffic inputs and casualty demonstrations, with owner acceptance of the residual risk. Failure to support acceptance requires exposure restrictions or additional independent protection.

## Configuration-specific desktop records

The [13 October desktop assessment](../evidence/runs/2026-10-13-srr-readiness/srr-readiness.json) records a 65.989 km reference circuit, chart-clear gates and both legs through the selected bridge span. Its boat is the earlier 1.2 m, 260 mm beam, 10.313 kg sizing reference with a 440 Wh battery. Its 3.974 Wh nominal energy headroom and failed all-season easterly-progress screen belong to that configuration.

The associated [32-run conceptual mission campaign](../evidence/runs/2026-10-13-srr-readiness/srr-mission-campaign.json) records 18 completions, 13 incomplete runs and one computational-horizon stop. It uses a separately identified conceptual vessel, not a performance replay of the 440 Wh sizing reference. Those counts differ from earlier campaigns because the course and scenario records differ; they are not estimates of measured completion probability.

The [15 October IC-01 integration record](../evidence/runs/2026-10-15-integrated-candidate/integrated-mission.json) instead uses candidate-specific performance, energy and independent recovery allocations in bounded local cases. It records ten completed courses, eight safe aborted encounter approaches and six casualty/end-of-exposure recovery approaches. These synthetic approaches do not qualify the real sites listed above. The [current assessment](current-assessment.md#integrated-simulation-evidence) explains the resulting integration claim.

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

I use these gaps to choose experiments and refine the architecture. The [current assessment](current-assessment.md) places their evidence in the context of the whole project.

<details>
<summary>Reproducing the archived desktop and conceptual campaign checks</summary>

The [publishing and validation instructions](reference/authoring.md) describe the pinned native SysML environment. The commands below reproduce the earlier 440 Wh assessment and conceptual campaign; they do not execute IC-01’s integration campaign.

```sh
uv run python -m tools.boat_analysis.evidence.srr --budget 10 --battery-wh 440 --beam-m 0.26
uv run python -m tools.boat_analysis.mission.campaign --count 32 --output build/analysis/srr-mission-campaign.json
```

Recovery fixtures use synthetic sites and loads to check current compensation, exposure-dependent reserve, unavailable authority, capsized performance and continuing consequences. Field surveys and casualty demonstrations must establish transfer to actual shore approaches.

</details>
