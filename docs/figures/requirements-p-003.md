# P-003 serviceability

[All requirement views](<../requirements-views.md>)

**Serviceability** — Aggregate requirement for Serviceability. Acceptance requires all applicable derived leaf results (P-107, P-108, P-109, P-110); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise individual replacement of the battery, every electronics module, every actuator and every serviceable enclosure seal by one operator using hand tools.

**ReplacementDuration** — Each P-003 replacement shall take no more than 30 minutes. Verification uses the shared context of P-003.

**NondestructiveService** — Each P-003 replacement shall leave bonded structural joints and adjacent parts intact. Verification uses the shared context of P-003.

**PostServiceSealing** — After each P-003 replacement, the assembly shall meet the N-043 immersion criterion. Verification uses the shared context of P-003.

**PostServiceActuation** — After each P-003 replacement, affected actuators shall complete their full commanded travel. Verification uses the shared context of P-003.

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
%% not represented: 56 node(s) without a position, left undrawn, and 66 edge(s) at them
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
%% not represented: 58 node(s) without a position, left undrawn, and 68 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**serviceability : Serviceability**`")
  n1("`*«requirement»*
**postServiceActuation : PostServiceActuation**`")
  n1 -.->|"derive"| n0
```
