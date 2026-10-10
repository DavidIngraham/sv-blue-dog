# P-003 serviceability

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**P-003 Serviceability** — The vessel shall support replacement of serviceable equipment without structural damage.

**P-107 ReplacementDuration** — Each P-003 replacement shall take no more than 30 minutes.

**P-108 NondestructiveService** — Each P-003 replacement shall leave bonded structural joints and adjacent parts intact.

**P-109 PostServiceSealing** — After each P-003 replacement, the assembly shall meet the N-043 immersion criterion.

**P-110 PostServiceActuation** — After each P-003 replacement, affected actuators shall complete their full commanded travel.

## P-003 derivation 1

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
%% BlueDogViews::serviceability1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 66 node(s) without a position, left undrawn, and 87 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**serviceability : Serviceability**`")
  n1("`*«requirement»*
**replacementDuration : ReplacementDuration**`")
  n2("`*«requirement»*
**nondestructiveService : NondestructiveService**`")
  n3("`*«requirement»*
**postServiceSealing : PostServiceSealing**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## P-003 derivation 2

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
%% BlueDogViews::serviceability2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 68 node(s) without a position, left undrawn, and 89 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**serviceability : Serviceability**`")
  n1("`*«requirement»*
**postServiceActuation : PostServiceActuation**`")
  n1 -.->|"derive"| n0
```
