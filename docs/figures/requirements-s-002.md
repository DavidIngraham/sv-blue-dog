# S-002 operating boundary

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**S-002 OperatingBoundary** — The vessel shall enforce the configured operating boundaries.

**S-105 BoundaryEvaluationCadence** — The vessel shall evaluate its current position and predicted trajectory against the S-002 polygons at least once per second.

**S-106 BoundaryAvoidanceDeadline** — The vessel shall issue an avoidance command within 2 seconds of predicting a boundary crossing.

**S-107 BoundaryAvoidanceRecording** — Every boundary-avoidance command shall have a corresponding event record.

**S-108 BoundaryStartInhibition** — Missing or geometrically invalid boundaries shall inhibit mission start.

**S-109 BoundaryDegradedEvidence** — Navigation loss or absence of a feasible maneuver shall produce an explicit degraded-route verdict instead of a safe-route verdict.

## S-002 derivation 1

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
%% BlueDogViews::operatingBoundary1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 149 node(s) without a position, left undrawn, and 236 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**operatingBoundary : OperatingBoundary**`")
  n1("`*«requirement»*
**boundaryEvaluationCadence : BoundaryEvaluationCadence**`")
  n2("`*«requirement»*
**boundaryAvoidanceDeadline : BoundaryAvoidanceDeadline**`")
  n3("`*«requirement»*
**boundaryAvoidanceRecording : BoundaryAvoidanceRecording**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-002 derivation 2

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
%% BlueDogViews::operatingBoundary2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 150 node(s) without a position, left undrawn, and 237 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**operatingBoundary : OperatingBoundary**`")
  n1("`*«requirement»*
**boundaryStartInhibition : BoundaryStartInhibition**`")
  n2("`*«requirement»*
**boundaryDegradedEvidence : BoundaryDegradedEvidence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
