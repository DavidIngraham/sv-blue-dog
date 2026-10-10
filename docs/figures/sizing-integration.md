# Coupled sizing configuration

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
%% BlueDogSemanticViews::SizingIntegration — definition rendering (view def GeneralView, filter @PartDefinition)
%% layout: n0 x=300 y=0
%% layout: n1 x=0 y=220
%% layout: n2 x=300 y=220
%% layout: n3 x=600 y=220
flowchart TB
  n0["`*«part def»*
**Configuration**`"]
  n1["`*«part def»*
**Sail**`"]
  n2["`*«part def»*
**Foil**`"]
  n3["`*«part def»*
**Rudder**`"]
  n0 ---|"◆ sail"| n1
  n0 ---|"◆ keel"| n2
  n0 ---|"◆ rudder"| n3
  n3 -->|"specialization"| n2
```
