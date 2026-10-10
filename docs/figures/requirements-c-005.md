# C-005 live observation

[All requirement views](<../requirements-views.md>)

**LiveObservation** — Live monitoring shall be available to the operator. Monitoring-link loss shall not interrupt autonomous mission execution. Telemetry shall be retained onboard and transmitted when contact returns. Coverage, update rate, retained data, and outage retention duration are open.

**Communications** — Aggregate requirement for Communications. Acceptance requires all applicable derived leaf results (E-120, E-121, E-122, E-123, E-124, E-131, E-137); this parent has no independent executable pass/fail predicate. Shared verification context: Link availability is a delivery-test precondition, not a coverage guarantee. Normal cadence is 60 seconds; low-energy alone permits 300 seconds; emergency/powered recovery takes precedence at 60 seconds. Outage tests last 24 hours.

## C-005 derivation 1

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
%% BlueDogViews::liveObservation1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 200 node(s) without a position, left undrawn, and 365 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::liveObservation : LiveObservation**`")
  n1("`*«requirement»*
**BlueDogRequirements::communications : Communications**`")
  n1 -.->|"derive"| n0
```

[Continue: E-005 communications](<requirements-e-005.md>)
