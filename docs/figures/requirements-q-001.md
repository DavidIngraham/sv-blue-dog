# Q-001 CruisePerformance relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**Q-001 CruisePerformance** — The vessel shall sustain sailing performance sufficient to complete each declared unassisted mission route.

**Q-101 LegProgress** — The vessel shall achieve at least 0.5 m/s mean along-route ground progress on each planned sailing leg.

**Q-102 PassageDuration** — The vessel shall complete the declared route within the qualified unassisted operating duration.

**Q-103 CruiseEvidence** — The cruise-performance assessment shall use accepted loaded-vessel sailing evidence for its declared mission profile.

## Q-001 relationships 1

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
%% BlueDogViews::cruisePerformance1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 7 node(s) without a position, left undrawn, and 11 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**cruisePerformance : CruisePerformance**`")
  n1("`*«requirement»*
**legProgress : LegProgress**`")
  n2("`*«requirement»*
**passageDuration : PassageDuration**`")
  n3("`*«requirement»*
**cruiseEvidence : CruiseEvidence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```
