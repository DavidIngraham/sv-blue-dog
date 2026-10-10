# Polar legs feed the cruise model

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

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
%% BlueDogSemanticViews::SailingIntegration — definition rendering (view def GeneralView, filter @PartDefinition)
%% layout: n0 x=0 y=200
%% layout: n1 x=0 y=0
%% layout: n2 x=350 y=200
%% layout: n3 x=350 y=0
flowchart BT
  n0["`*«part def»*
**BlueDogSailing::PolarLeg**`"]
  n1["`*«part def»*
**BlueDogReliability::SailingLeg**`"]
  n2["`*«part def»*
**BlueDogSailing::PolarVoyageProfile**`"]
  n3["`*«part def»*
**BlueDogReliability::VoyageProfile**`"]
  n0 -->|"specialization"| n1
  n2 -->|"specialization"| n3
  n2 ---|"◆ legs"| n0
  n3 ---|"◆ legs"| n1
```
