# Independent manufacturing constraint

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
%% BlueDogSemanticViews::ManufacturingSemantics — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 1 node(s) without a position, left undrawn, and 1 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=360 y=0
flowchart BT
  n0("`*«requirement»*
**BlueDogRequirements::desktopManufacture : DesktopManufacture**`")
  n1["`*«verification def»*
**BlueDogRequirementVerification::DesktopManufactureVerification**`"]
  n2("`*«part»*
**BlueDog::Architecture::HullAndRig::printedHull : PrintedHull**`")
  n1 -.->|"verify"| n0
  n2 -.->|"satisfy"| n0
```
