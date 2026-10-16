# Establishing operating constraints

**OOSEM:** Mission and stakeholder needs · [Current assessment](current-assessment.md)

The boat must make progress against river current, avoid traffic and remain recoverable when sailing stops. I use two environmental cases: ordinary operation during a selected weather window, and a more severe casualty exposure while the boat reaches shore and waits for pickup. These cases shape the hull, rig, sensing and recovery system before I choose hardware.

## Conditions the design must address

| Condition | Operational design basis | Casualty recovery design basis |
| --- | --- | --- |
| Mean wind / gust | 0–15 m/s / 20 m/s | Up to 25 m/s / 35 m/s |
| Significant wave height | 1.5 m | 2 m |
| Peak wave period | 1.5–5 s | 1.5–7 s |
| Separate individual-wave case | 3 m | 4 m |
| River current | Evaluate 0–1.5 m/s and local direction | Use the route's current field; reject a route if recovery cannot overcome it |
| Exposure | The actual passage, including holds and delays | The longest applicable recovery transit plus the arranged pickup delay; the study allows two hours |

Significant wave height describes the larger waves in a sea state, approximately the average height of the highest third; it is not the largest individual wave. The separate individual-wave cases therefore matter for clearance, flooding and structural loads. Wave period matters too: waves of the same height can produce very different boat motions.

These are provisional engineering allocations in the [native environmental analysis](../models/analyses/environment-review.sysml), not measured extremes or a promise that IC-01 can sail in every combination. I must test coupled wind, current and waves, including reversals and boat wakes. Calm waiting is allowed, but the boat must retain its safety and recovery functions. Ice, dam transit and surf-zone launch remain outside this scope. The [site and environmental evidence](site-and-environment-evidence.md#environmental-decision) records the basis and remaining measurements.

The practical consequence is that a favorable launch forecast does not remove the recovery problem. A boat that cannot keep sailing still needs enough flotation, observation, control and energy to reach a usable approach and remain there until pickup.

## Gorge weather and launch windows

I want the challenge to reflect the familiar west-wind Gorge, while taking winter testing seriously. I will select a favorable weather window for the qualifying attempt; year-round unattended operation comes later. In a westerly, the downstream outbound leg is windward with the current and the upstream return is leeward against it. An easterly makes the return both windward and upstream.

The seasonal distinction has a physical basis: coastal and inland pressure differences drive Gorge gap flow. Warm-season westerlies and cold-season easterlies have different frequency, persistence and spatial patterns. [Sharp and Mass (2004)](https://doi.org/10.1175/826.1) describes that climatology; the later [two-cool-season profiler study](https://journals.ametsoc.org/view/journals/mwre/147/12/mwr-d-19-0026.1.xml) further examines winter easterly flow. Neither supplies a ready-made probability of this boat completing the route.

![Stacked bars of ten years of station observations: westerlies dominate the east/west directional hours at KDLS in May–September, while easterlies become much more important in November–March, especially at Troutdale. Light winds, other directions and unknown observations remain separate.](figures/gorge-wind-seasons.svg)

The reproducible study uses **2015–2024 NOAA ISD-Lite hourly observations** from airport station KDLS and Troutdale (KTTD). At KDLS, east winds account for about **10% of east/west hours in May–September**, rising to **48% in November–March**. Troutdale gives roughly **31% and 86%**. These are station proxies, not a route-wide average: KDLS is upstream and Troutdale is downstream of the challenge reach, and airport exposure is different from a small wing over the water. The discrepancy is a reason to add observations along the route, not to average the stations together.

The next useful step is to evaluate complete, forecast-conditioned weather histories along the route, preserving wind persistence and its relationship to current, waves and daylight. Passage progress, holds and battery reserve must use the same history. Station wind frequencies alone cannot determine a launch decision or a probability of completing the mission.

<details>
<summary>How the weather statistics were calculated, and what they can support</summary>

Those percentages exclude a substantial fraction of the record. The analysis preserves light winds below 2 m/s, other directions, and unknown or absent observations. Directions are meteorological “from,” with east 45–135° and west 225–315°. The thresholds are descriptive bins, not acceptance criteria. Seasons use UTC months. The [model](../models/analyses/weather.sysml) owns these choices and the [frozen archive](../evidence/weather/2015-2024/manifest.json) records source URLs and hashes; NOAA documents the [data format](https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/isd-lite-format.pdf).

### From wind frequencies to a performance weighting

For an initial sensitivity, I would explore east-wind exposure weights around 0.10–0.31 for warm-season east/west hours, and 0.48–0.86 for winter. These span the two station estimates; they are **not confidence intervals or approved mission probabilities**. A single annual 80/20 split would obscure the season and location differences. No calibrated weight has yet been put into the size optimizer.

For passage-level decisions, the useful quantity is the probability of each complete weather trajectory **given the season, forecast and launch rule**. The native model first sweeps a simpler pair of persistent-west and persistent-east hypotheses. It computes `P(pass) = (1 − pEast) × westPass + pEast × eastPass`, then reports passage time conditional on passing. A trip that fails the progress screen contributes failure probability, never a large finite “average passage time.” The [native weather study](../models/analyses/weather.sysml) retains this calculation for its archived 2.009 m configuration. Its primary case passes the west-wind screen and fails the east-wind screen; it is not an IC-01 result. Its scope is route-screen coverage, not whole-system reliability; structural, recovery and safety failures remain visible.

Persistence matters. A hindcast probe selects hours preceded by six consecutive westerly hours and looks forward 72 hours without selecting on future direction. At KDLS, about 43% of the **complete warm-season windows** encounter at least one easterly hour. That is not a failure probability, and missing observations exclude many windows. The native report below exposes complete and incomplete counts and conservative missing-data bounds. Windows overlap, so their count is not an independent sample size. Troutdale has no complete warm-season windows under this strict rule; it cannot support that estimate.

A later probability model needs complete trajectories and a defined launch rule. Reducing the weight of easterly performance never reduces the required survival or traffic-safety capability.



```sysml-report BlueDogWeatherDocuments::Observations
```

The bounds assign every incomplete future window first to “no east encounter” and then to “east encounter.” They bound missing outcomes, not sampling uncertainty or forecast skill. Zero complete windows means the complete-case percentage is undefined; consult the status column, not the numeric placeholder. Cases with few complete windows cannot establish a useful climate estimate.

```sh
uv run python -m tools.boat_analysis.environment.climatology
uv run python -m tools.boat_analysis.environment.sensitivity
```

Both commands work from committed evidence without a network fetch. `--fetch` on the first command retrieves missing NOAA files; it is an explicit evidence-refresh operation. Native SysML owns scenario policy and probability arithmetic. Python parses observations, counts windows and plots results. Rebuilding the documents reads the model projection.

</details>

## Operating obligations

The model's [source evidence](../models/vehicle/source-evidence.sysml) preserves the research notes and limitations, including Microtransat discussions and the cited navigation rules. These are inputs to an applicability review, not an authorization to deploy.

Review the proposed mission, waters, operating modes and equipment together. Sailing, powered recovery and station keeping can raise different questions. Obtain the underlying determination behind a reported exemption and establish its scope before using it as a design constraint. Treat unresolved classification explicitly rather than choosing a convenient length limit.

The current obligations are shown in the [classification](requirements/requirements-safety.md#conspicuity-classification-and-recovery) and [conspicuity](requirements/requirements-safety.md#conspicuity-classification-and-recovery) views. Traffic also belongs in the [operating context and use cases](architecture.md). An applicability finding must identify the configuration and operating mode it covers. The [site and environment evidence](site-and-environment-evidence.md) records the route, bridge, recovery-site and exposure assumptions still requiring field confirmation.

**Next:** [Requirements: what the boat must achieve](requirements.md) · [Series guide](index.md)
