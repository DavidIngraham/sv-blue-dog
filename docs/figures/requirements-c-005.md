# C-005 LiveObservation relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**C-005 LiveObservation** — The vessel shall provide live monitoring with autonomous operation and retained telemetry across communication outages.

**E-005 Communications** — The vessel shall support live telemetry through link outages and reconnection.

## C-005 relationships 1

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
%% not represented: 125 node(s) without a position, left undrawn, and 183 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::liveObservation : LiveObservation**`")
  n1("`*«requirement»*
**BlueDogRequirements::communications : Communications**`")
  n1 -.->|"refine"| n0
```

[Continue: E-005 Communications](<requirements-e-005.md>)
