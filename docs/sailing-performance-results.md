# Required polars and hull-speed screening

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[Method, assumptions and hull-regime interpretation](<sailing-performance.md>)

Synthetic design probes, not measured polars, selected hull dimensions or new mission requirements. The named inputs below are evaluated from the scenario model. The offshore case is a sizing probe, not an approved Hawaii route or operating window.

## Declared scenario inputs

| Case | Leg distance | Along-current | Moving-time allocation |
| --- | --- | --- | --- |
| Upstream / headwind | 100000 \[m\] | -1.5 \[m/s\] | 201600 \[s\] |
| Upstream / tailwind | 100000 \[m\] | -1.5 \[m/s\] | 201600 \[s\] |
| Downstream / headwind | 100000 \[m\] | 1.5 \[m/s\] | 36000 \[s\] |
| Downstream / tailwind | 100000 \[m\] | 1.5 \[m/s\] | 36000 \[s\] |
| Offshore sizing probe | 4000000 \[m\] | 0 \[m/s\] | 2419200 \[s\] |

| Case | True wind speed | TWA (radians) | Candidate clean boat speed | Waterline length |
| --- | --- | --- | --- | --- |
| Upstream / headwind | 5 \[m/s\] | 0.7853981633974483 \[rad\] | 4 \[m/s\] | 1 \[m\] |
| Upstream / tailwind | 5 \[m/s\] | 2.443460952792061 \[rad\] | 3.6 \[m/s\] | 1 \[m\] |
| Downstream / headwind | 5 \[m/s\] | 0.7853981633974483 \[rad\] | 3 \[m/s\] | 1 \[m\] |
| Downstream / tailwind | 5 \[m/s\] | 2.443460952792061 \[rad\] | 3 \[m/s\] | 1 \[m\] |
| Offshore sizing probe | 5 \[m/s\] | 2.443460952792061 \[rad\] | 3 \[m/s\] | 1 \[m\] |

## Inverse polar demand

| Case | Required ground VMG | Required clean polar speed | Knots |
| --- | --- | --- | --- |
| upstreamBeat | 0.5 \[SI::'m/s'\] | 3.721614637823934 \[SI::'m/s'\] | 7.23424011672039 |
| upstreamRun | 0.5 \[SI::'m/s'\] | 3.4352823403481025 \[SI::'m/s'\] | 6.67765465726413 |
| downstreamBeat | 25/9 \[SI::'m/s'\] | 2.3776982408319576 \[SI::'m/s'\] | 4.621875630126915 |
| downstreamRun | 25/9 \[SI::'m/s'\] | 2.1947637174446206 \[SI::'m/s'\] | 4.266279364363193 |
| oceanDemand | 625/378 \[SI::'m/s'\] | 2.84001516232482 \[SI::'m/s'\] | 5.520547831732911 |

## Hull screening

Wave-reference length inverts c = sqrt(g L / (2 pi)). It is neither a minimum allowable hull length nor a planing criterion. Froude numbers use water speed, not ground speed or VMG.

| Case | Froude at clean demand | Froude at degraded operating speed | Wave-reference waterline at clean demand |
| --- | --- | --- | --- |
| upstreamBeat | 1.1884230414520724 | 0.9507384331616578 | 8.874052530298792 \[m\] |
| upstreamRun | 1.096988561274094 | 0.8775908490192751 | 7.561084061783603 \[m\] |
| downstreamBeat | 0.7592702764832684 | 0.6074162211866148 | 3.622201997321034 \[m\] |
| downstreamRun | 0.7008538030362265 | 0.5606830424289813 | 3.0862758246014854 \[m\] |
| oceanDemand | 0.9069019190427362 | 0.7255215352341889 | 5.167738273064548 \[m\] |

## Demand across wind strength

The mission imposes the same required speed at each sampled wind strength; a measured or validated polar must establish whether that speed is available. No wind-to-speed prediction is made.

| True wind speed | Required clean speed / true wind speed | Evidence ready |
| --- | --- | --- |
| 3 \[SI::'m/s'\] | 1.240538212607978 | false |
| 5 \[SI::'m/s'\] | 0.7443229275647868 | false |
| 10 \[SI::'m/s'\] | 0.3721614637823934 | false |
| 15 \[SI::'m/s'\] | 0.2481076425215956 | false |

## Candidate polars through cruise and reliability

The candidate speeds listed above are synthetic feasibility probes, not predicted polars. Westerly and easterly scenarios use different points of sail; rate assumptions are inherited from the existing cruise illustration.

| Case | Allocated hours including holds | Candidate passage hours | Critical-rate budget per hour |
| --- | --- | --- | --- |
| westerlyPassage | 72 | 57.31706223726946 | 0.001838205091909218 |
| easterlyPassage | 72 | 57.31706223726946 | 0.001838205091909218 |

| Case | Time allocation valid | Candidate numerically feasible | Voyage supported by evidence |
| --- | --- | --- | --- |
| westerlyPassage | true | true | false |
| easterlyPassage | true | true | false |

## Analysis dependencies

| Dependent model | Basis |
| --- | --- |
| PolarDemandAndHullScreen | legProgress |
| PolarDemandAndHullScreen | passageDuration |
| PolarDemandAndHullScreen | cruiseEvidence |
| PolarDemandAndHullScreen | gorgeCurrent |
| PolarDemandAndHullScreen | submergedWeedPassage |
| PolarDemandAndHullScreen | HullAndRig |
| CruiseReliability | PolarDemandAndHullScreen |
