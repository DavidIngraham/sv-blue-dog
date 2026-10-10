# N-044 wet mechanical integrity

[All requirement views](<../requirements-views.md>)

**WetMechanicalIntegrity** — Aggregate requirement for WetMechanicalIntegrity. Acceptance requires all applicable derived leaf results (N-111, N-112); this parent has no independent executable pass/fail predicate. Shared verification context: Evaluate after each selected profile wet-exposure campaign under N-002.

**WetMechanismTravel** — After each N-044 exposure, external mechanisms shall complete their full commanded travel without seizure. Verification uses the shared context of N-044.

**WetJointIntegrity** — After each N-044 exposure, structural joints shall show no separation or through-cracks on visual inspection at 5 times magnification. Verification uses the shared context of N-044.

## N-044 derivation 1

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
%% BlueDogViews::wetMechanicalIntegrity1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 82 node(s) without a position, left undrawn, and 87 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**wetMechanicalIntegrity : WetMechanicalIntegrity**`")
  n1("`*«requirement»*
**wetMechanismTravel : WetMechanismTravel**`")
  n2("`*«requirement»*
**wetJointIntegrity : WetJointIntegrity**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
