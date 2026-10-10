# N-045 WetElectricalIntegrity relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**N-045 WetElectricalIntegrity** — Cable assemblies shall retain electrical integrity after the selected wet-exposure campaign.

**N-113 WetConductorResistance** — After each N-045 exposure, end-to-end conductor resistance shall be no more than 10 percent above its pre-test value.

**N-114 WetInsulationResistance** — After each N-045 exposure, conductor-to-conductor and conductor-to-case insulation resistance shall be at least 1 megohm at 50 V DC.

## N-045 relationships 1

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
%% BlueDogViews::wetElectricalIntegrity1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 82 node(s) without a position, left undrawn, and 87 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**wetElectricalIntegrity : WetElectricalIntegrity**`")
  n1("`*«requirement»*
**wetConductorResistance : WetConductorResistance**`")
  n2("`*«requirement»*
**wetInsulationResistance : WetInsulationResistance**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
