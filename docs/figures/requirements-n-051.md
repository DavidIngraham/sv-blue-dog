# N-051 self righting

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**N-051 SelfRighting** — The vessel shall recover from the specified capsize releases without external assistance or motor thrust.

**N-118 RightingDeadline** — The vessel shall self-right within 60 seconds of each N-051 release.

**N-119 CapsizeRigRetention** — The vessel shall retain its rig through every N-051 release.

**N-120 CapsizeBallastRetention** — The vessel shall retain its ballast through every N-051 release.

**N-121 CapsizeElectronicsSealing** — No water shall reach electronics during any N-051 release.

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
%% not represented: 77 node(s) without a position, left undrawn, and 101 edge(s) at them
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
%% not represented: 79 node(s) without a position, left undrawn, and 103 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**selfRighting : SelfRighting**`")
  n1("`*«requirement»*
**capsizeElectronicsSealing : CapsizeElectronicsSealing**`")
  n1 -.->|"derive"| n0
```
