# L-001 MissionReliability

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**L-001 MissionReliability** — The vessel shall preserve mission-critical functions throughout each declared unassisted voyage.

**L-101 MissionSuccessProbability** — The lower 95-percent confidence bound on mission reliability shall be at least 0.90 over the declared voyage duration.

**L-102 FailureRateBudget** — The combined mission-critical failure-rate bound shall not exceed the budget derived from L-101 and the Q-102 exposure duration.

**L-103 ReliabilityEvidence** — The reliability assessment shall use accepted mission-representative evidence supporting its failure-rate bound.

**L-104 CriticalFailureDisposition** — Each identified safety-critical failure mode shall have an accepted disposition before an unassisted launch.

## L-001 derivation 1

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
%% BlueDogViews::missionReliability1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 48 node(s) without a position, left undrawn, and 58 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**missionReliability : MissionReliability**`")
  n1("`*«requirement»*
**missionSuccessProbability : MissionSuccessProbability**`")
  n2("`*«requirement»*
**failureRateBudget : FailureRateBudget**`")
  n3("`*«requirement»*
**reliabilityEvidence : ReliabilityEvidence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## L-001 derivation 2

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
%% BlueDogViews::missionReliability2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 49 node(s) without a position, left undrawn, and 52 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**missionReliability : MissionReliability**`")
  n1("`*«requirement»*
**criticalFailureDisposition : CriticalFailureDisposition**`")
  n1 -.->|"derive"| n0
```
