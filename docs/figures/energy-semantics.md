# Energy acceptance, formalization and verification

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
%% BlueDogSemanticViews::EnergySemantics — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 53 node(s) without a position, left undrawn, and 57 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=360 y=0
%% layout: n2 x=360 y=200
%% layout: n9 x=0 y=200
%% layout: n51 x=0 y=400
flowchart BT
  n0("`*«requirement»*
**BlueDogRequirements::sustainedEnergyFeasibility : SustainedEnergyFeasibility**`")
  n1("`*«requirement»*
**BlueDogRequirements::sustainedReserveProtection : SustainedReserveProtection**`")
  n2["`*«verification def»*
**BlueDogEnergy::SustainedEnergyVerification**`"]
  n9["`*«calc def»*
**BlueDogRequirements::SustainedReserveProtectionCriterion**`"]
  n51("`*«part»*
**BlueDog::Architecture::Boat::energy : EnergySubsystem**`")
  n2 -.->|"verify"| n0
  n1 -.->|"derive"| n0
  n9 -.->|"refine"| n1
  n51 -.->|"satisfy"| n0
  n51 -.->|"satisfy"| n1
```
