# Weed tolerance and design responsibility

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
%% BlueDogSemanticViews::WeedSemantics — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 64 node(s) without a position, left undrawn, and 76 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=360 y=0
%% layout: n2 x=0 y=200
%% layout: n3 x=0 y=400
%% layout: n19 x=360 y=200
flowchart BT
  n0("`*«requirement»*
**BlueDogRequirements::submergedWeedPassage : SubmergedWeedPassage**`")
  n1("`*«requirement»*
**BlueDogRequirements::weedPassageSpeed : WeedPassageSpeed**`")
  n2("`*«requirement»*
**BlueDogRequirements::weedPassageSteering : WeedPassageSteering**`")
  n3["`*«verification def»*
**BlueDogRequirementVerification::SubmergedWeedPassageVerification**`"]
  n19("`*«part»*
**BlueDog::Architecture::missionContext::boat : Boat**`")
  n3 -.->|"verify"| n0
  n3 -.->|"verify"| n1
  n3 -.->|"verify"| n2
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n19 -.->|"satisfy"| n0
  n19 -.->|"satisfy"| n1
```
