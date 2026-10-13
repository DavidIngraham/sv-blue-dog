# SRR technical appendix

**Design phase:** Appendix · [SRR presentation](srr-review.md)

This appendix identifies the evidence needed to judge the current SRR baseline. Requirement statements remain in the model and its generated views. SRR approval and physical qualification are separate decisions.

## Model and implementation sources

| Subject | Authoritative source | Review focus |
| --- | --- | --- |
| Challenge | [Challenge model](../models/missions/transgorge.sysml) | Course, size, autonomy, traffic and recovery obligations |
| Verification | [Challenge cases](../models/missions/verification.sysml), [vehicle cases](../models/vehicle/verification.sysml) | Methods and missing allocations, not completed verdicts |
| Recovery | [Native physics](../models/libraries/marine/recovery.sysml), [planner](../tools/boat_analysis/mission/recovery.py), [mission engine](../tools/boat_analysis/mission/engine.py) | Current authority, route feasibility, reserve and casualty capability |
| Environmental proposal | [Review analysis](../models/analyses/environment-review.sysml) | Evidence applicability, coupled exposure and unaccepted margins |
| Design | [Sizing method](sizing.md), [results](results.md) | Scope of old results versus the new challenge limit |

## Environmental interpretation

The [NOAA-hosted gap-flow study](https://repository.library.noaa.gov/view/noaa/28157/noaa_28157_DS1.pdf) supports persistent, spatially varying winter easterlies. Its profiler jet observations must not be substituted for a 10 m surface limit on this course. The archived airport observations likewise need exposure and height interpretation.

The native fetch sensitivity evaluates coupled wind and effective-fetch hypotheses. It does not measure directional fetch, shallow-water transformation, current gradients or traffic wakes. The proposed wave margin is an engineering allocation to review. A single numerical envelope cannot replace forecast-conditioned trajectory assessment.

## Review actions

| Action | Evidence required | Decision affected |
| --- | --- | --- |
| Select accessible recovery locations | Chart-clear approach, shore access, hazards, final retention and retrieval assessment | Course baseline and reserve model |
| Resolve bridge transit | Actual span selection, vertical clearance, pool stage and uncertainty | Course feasibility |
| Accept environmental allocations | Spatial wind/current evidence, correlated wave cases and recovery duration | Design basis |
| Allocate encounter performance | Target types, detection conditions, response delays and vessel maneuver capability | Traffic verification |
| Assess impaired-sensing recovery | Failure/common-cause model, traffic exposure, transit duration and consequence severity | Residual-risk acceptance |
| Propagate the new challenge baseline | Consumer audit, generated contracts, tests and new applicable study results | SRR configuration integrity |
| Develop the eligible design frontier | Overall-envelope enforcement, multiple optimized configurations and paired scenarios | PDR concept selection |
| Correlate critical physics | Wing, actuator, structure and casualty measurements | Model credibility and physical release |

These actions are open. Their closure requires evidence and a recorded decision; the presence of a test or a model relationship does not establish that closure.

## Reproducing checks

Use the repository's uv-managed environment and pinned native SysML tool. The model validation, pytest suite and publishing workflow are described in [publishing](publishing.md). Native numerical adapters run in the Linux solver environment with GCC.

The recovery fixtures deliberately use synthetic locations and loads. They check current compensation, increasing reserve with exposure, unavailable recovery authority, explicit capsized performance, autonomous recovery without communications, persistent disqualification and independently observed collision consequences. They do not qualify a real shore location.

## Review record

**Status: open; no SRR approval recorded.** The final review record must identify the published baseline revision, evidence reviewed, accepted limitations, your disposition and follow-up actions. Updating this page cannot substitute for your approval.
