# N-055 weed blockage response

[All requirement views](<../requirements-views.md>)

**WeedBlockageResponse** — Aggregate requirement for WeedBlockageResponse. Acceptance requires all applicable derived leaf results (N-130, N-131, N-132, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: Gorge trigger: vegetation prevents completion of commanded rudder motion for 5 seconds, or keeps water-relative speed below 25 percent of the preceding weed-free 60-second mean for 60 seconds with mean wind at least 3 m/s. Dense mats are a blockage/avoidance case, not a pass-through claim.

**WeedBlockageFault** — A suspected-fouling fault shall be logged within 10 seconds after the N-055 trigger. Verification uses the shared context of N-055.

**WeedBlockageContingency** — The vessel shall enter fouling-contingency state within 10 seconds after the N-055 trigger. Verification uses the shared context of N-055.

**WeedBlockageLocation** — Location reporting shall continue at the active telemetry cadence during fouling contingency whenever a link is available. Verification uses the shared context of N-055.

**MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown. Verification uses the shared context of R-004.

## N-055 derivation 1

```mermaid
---
config:
  fontFamily: "Helvetica, Arial, sans-serif"
  theme: base
  themeCSS: ".edgeLabel rect { opacity: 1 !important; } .cluster-label .nodeLabel { text-align: center; }"
  themeVariables:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "14px"
    primaryColor: "#FFFFFF"
    secondaryColor: "#FFFFFF"
    tertiaryColor: "#FFFFFF"
    background: "#FFFFFF"
    primaryBorderColor: "#181818"
    primaryTextColor: "#000000"
    lineColor: "#181818"
    textColor: "#000000"
    noteBkgColor: "#FEFFDD"
    noteBorderColor: "#181818"
    noteTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#181818"
    edgeLabelBackground: "#FFFFFF"
---
%% BlueDogViews::weedBlockageResponse1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 55 node(s) without a position, left undrawn, and 62 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**weedBlockageResponse : WeedBlockageResponse**`")
  n1("`*«requirement»*
**weedBlockageFault : WeedBlockageFault**`")
  n2("`*«requirement»*
**weedBlockageContingency : WeedBlockageContingency**`")
  n3("`*«requirement»*
**weedBlockageLocation : WeedBlockageLocation**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-055 derivation 2

```mermaid
---
config:
  fontFamily: "Helvetica, Arial, sans-serif"
  theme: base
  themeCSS: ".edgeLabel rect { opacity: 1 !important; } .cluster-label .nodeLabel { text-align: center; }"
  themeVariables:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "14px"
    primaryColor: "#FFFFFF"
    secondaryColor: "#FFFFFF"
    tertiaryColor: "#FFFFFF"
    background: "#FFFFFF"
    primaryBorderColor: "#181818"
    primaryTextColor: "#000000"
    lineColor: "#181818"
    textColor: "#000000"
    noteBkgColor: "#FEFFDD"
    noteBorderColor: "#181818"
    noteTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#181818"
    edgeLabelBackground: "#FFFFFF"
---
%% BlueDogViews::weedBlockageResponse2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 95 node(s) without a position, left undrawn, and 118 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**weedBlockageResponse : WeedBlockageResponse**`")
  n1("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n1 -.->|"derive"| n0
```
