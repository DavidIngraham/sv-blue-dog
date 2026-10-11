# Establishing operating constraints

Before I size the boat around a convenient rule of thumb, I need to understand where and how it will operate. At [mission definition](development-plan.md#mission-definition), I bring together the intended waters, traffic, operating modes and source research. The result should tell me which obligations affect the design and which questions must be resolved before a [water trial](development-plan.md#physical-validation).

We distinguish rules of a voluntary challenge, jurisdiction-specific operating obligations and our own engineering allocations. A size threshold quoted in a race discussion does not by itself establish vessel classification or permission to operate.

## Gorge weather and launch windows

I want the challenge to reflect the familiar west-wind Gorge, while taking winter testing seriously. I will select a favorable weather window for the qualifying attempt; year-round unattended operation comes later. In a westerly, the downstream outbound leg is windward with the current and the upstream return is leeward against it. An easterly makes the return both windward and upstream.

The seasonal distinction has a physical basis: coastal and inland pressure differences drive Gorge gap flow. Warm-season westerlies and cold-season easterlies have different frequency, persistence and spatial patterns. [Sharp and Mass (2004)](https://doi.org/10.1175/826.1) describes that climatology; the later [two-cool-season profiler study](https://journals.ametsoc.org/view/journals/mwre/147/12/mwr-d-19-0026.1.xml) further examines winter easterly flow. Neither supplies a ready-made probability of this boat completing the route.

![Stacked bars of ten years of station observations: westerlies dominate the east/west directional hours at The Dalles in May–September, while easterlies become much more important in November–March, especially at Troutdale. Light winds, other directions and unknown observations remain separate.](figures/gorge-wind-seasons.svg)

The reproducible study uses **2015–2024 NOAA ISD-Lite hourly observations** from The Dalles airport (KDLS) and Troutdale (KTTD). At KDLS, east winds account for about **10% of east/west hours in May–September**, rising to **48% in November–March**. Troutdale gives roughly **31% and 86%**. These are station proxies, not a route-wide average: Troutdale is downstream of the challenge reach, and airport exposure is different from a small wing over the water. The discrepancy is a reason to add observations along the route, not to average the stations together.

Those percentages exclude a substantial fraction of the record. We preserve light winds below 2 m/s, other directions, and unknown or absent observations. Directions are meteorological “from,” with east 45–135° and west 225–315°. The thresholds are descriptive bins, not acceptance criteria. Seasons use UTC months. The [model](../models/analyses/weather.sysml) owns these choices and the [frozen archive](../evidence/weather/2015-2024/manifest.json) records source URLs and hashes; NOAA documents the [data format](https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/isd-lite-format.pdf).

### From wind frequencies to a performance weighting

For an initial sensitivity, I would explore east-wind exposure weights around 0.10–0.31 for warm-season east/west hours, and 0.48–0.86 for winter. These span the two station estimates; they are **not confidence intervals or approved mission probabilities**. A single annual 80/20 split would obscure the season and location differences. No calibrated weight has yet been put into the size optimizer.

For passage-level decisions, the useful quantity is the probability of each complete weather trajectory **given the season, forecast and launch rule**. The native model first sweeps a simpler pair of persistent-west and persistent-east hypotheses. It computes `P(pass) = (1 − pEast) × westPass + pEast × eastPass`, then reports passage time conditional on passing. A stalled or over-budget trip contributes failure probability, never a large finite “average passage time.” The [results](results.md) show this calculation on every archived engineering scenario. Its scope is route-screen coverage, not whole-system reliability; structural, recovery and safety failures remain visible.

Persistence matters. A hindcast probe selects hours preceded by six consecutive westerly hours and looks forward 72 hours without selecting on future direction. At KDLS, about 43% of the **complete warm-season windows** encounter at least one easterly hour. That is not a failure probability, and missing observations exclude many windows. The native report below exposes complete and incomplete counts and conservative missing-data bounds. Windows overlap, so their count is not an independent sample size. Troutdale has no complete warm-season windows under this strict rule; it cannot support that estimate.

The next fidelity step is to sample contiguous, forecast-conditioned trajectories along the route, preserving wind persistence and joint current, wave and solar conditions. Route progress and chronological battery reserve must be evaluated on the same trajectory, including holds, reversals, aborts and recovery. Winter trials need their own exposure profile. Only then can we choose a defensible weather-success allocation alongside the existing reliability target. Reducing the weight of easterly performance never reduces the required survival or traffic-safety capability.

<details>
<summary>Native observation counts, missing-data bounds and reproduction</summary>

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

The current obligations are shown in the [classification](requirements/requirements-s-005.md) and [conspicuity](requirements/requirements-s-004.md) views. Traffic also belongs in the [operating context and use cases](architecture.md). Changes in an applicability finding should update those model elements and their rationale; publication then rebuilds the affected views.


**Next:** [Look up the requirements](requirements.md).
