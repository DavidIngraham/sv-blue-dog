# S-002 operating boundary

[All requirement views](<../requirements-views.md>)

**OperatingBoundary** — Aggregate requirement for OperatingBoundary. Acceptance requires all applicable derived leaf results (S-105, S-106, S-107, S-108, S-109); this parent has no independent executable pass/fail predicate. Shared verification context: Use uploaded permitted-water and exclusion polygons, with a 60-second prediction horizon. Inject approaches to every boundary, navigation loss and no-feasible-maneuver cases. Coordinates and uncertainty/clearance margins are controlled mission inputs with no default values.

**BoundaryEvaluationCadence** — The vessel shall evaluate its current position and predicted trajectory against the S-002 polygons at least once per second. Verification uses the shared context of S-002.

**BoundaryAvoidanceDeadline** — The vessel shall issue an avoidance command within 2 seconds of predicting a boundary crossing. Verification uses the shared context of S-002.

**BoundaryAvoidanceRecording** — Every boundary-avoidance command shall have a corresponding event record. Verification uses the shared context of S-002.

**BoundaryStartInhibition** — Missing or geometrically invalid boundaries shall inhibit mission start. Verification uses the shared context of S-002.

**BoundaryDegradedEvidence** — Navigation loss or absence of a feasible maneuver shall produce an explicit degraded-route verdict instead of a safe-route verdict. Verification uses the shared context of S-002.

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
%% not represented: 148 node(s) without a position, left undrawn, and 230 edge(s) at them
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
%% not represented: 149 node(s) without a position, left undrawn, and 231 edge(s) at them
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
