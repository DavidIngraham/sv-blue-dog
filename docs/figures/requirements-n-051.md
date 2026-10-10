# N-051 self righting

[All requirement views](<../requirements-views.md>)

**SelfRighting** — Aggregate requirement for SelfRighting. Acceptance requires all applicable derived leaf results (N-118, N-119, N-120, N-121); this parent has no independent executable pass/fail predicate. Shared verification context: Use minimum and maximum mission loading, five releases at each angle of 90 and 180 degrees toward each side, without external action or motor thrust. Use freshwater for Gorge or 35 g/kg saltwater for ocean; dual qualification requires both media. All leaves apply to every release.

**RightingDeadline** — The vessel shall self-right within 60 seconds of each N-051 release. Verification uses the shared context of N-051.

**CapsizeRigRetention** — The vessel shall retain its rig through every N-051 release. Verification uses the shared context of N-051.

**CapsizeBallastRetention** — The vessel shall retain its ballast through every N-051 release. Verification uses the shared context of N-051.

**CapsizeElectronicsSealing** — No water shall reach electronics during any N-051 release. Verification uses the shared context of N-051.

## N-051 derivation 1

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
%% BlueDogViews::selfRighting1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 70 node(s) without a position, left undrawn, and 90 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**selfRighting : SelfRighting**`")
  n1("`*«requirement»*
**rightingDeadline : RightingDeadline**`")
  n2("`*«requirement»*
**capsizeRigRetention : CapsizeRigRetention**`")
  n3("`*«requirement»*
**capsizeBallastRetention : CapsizeBallastRetention**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-051 derivation 2

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
%% BlueDogViews::selfRighting2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 72 node(s) without a position, left undrawn, and 92 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**selfRighting : SelfRighting**`")
  n1("`*«requirement»*
**capsizeElectronicsSealing : CapsizeElectronicsSealing**`")
  n1 -.->|"derive"| n0
```
