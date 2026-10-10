# N-002 MarineDurability relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**N-002 MarineDurability** — The vessel shall retain required function and structural integrity through its selected wet-exposure campaign.

**N-041 FreshwaterExposure** — For Gorge qualification, following 72 hours continuous freshwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its Gorge functional checks without repair or servicing.

**N-042 SaltwaterExposure** — For ocean qualification, following 30 days continuous 35 g/kg saltwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its ocean functional checks without repair or servicing.

**N-043 EnclosureSealing** — Before and after each wet-exposure campaign, installed electronics enclosures, connectors and penetrations shall show no detectable liquid ingress on dry internal water-sensitive indicators after 30 minutes immersion with their highest point 1 m below the water surface.

**N-044 WetMechanicalIntegrity** — External mechanisms and structural joints shall retain integrity after the selected wet-exposure campaign.

**N-045 WetElectricalIntegrity** — Cable assemblies shall retain electrical integrity after the selected wet-exposure campaign.

**N-046 SolarHeating** — The vessel shall retain safe powered operation during the specified solar-heating exposure.

**N-047 PrintedMaterialAging** — Printed structural material shall retain at least 80 percent of unaged failure load after the specified UV and wet-exposure sequence.

## N-002 relationships 1

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
%% BlueDogViews::marineDurability1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 96 node(s) without a position, left undrawn, and 110 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**marineDurability : MarineDurability**`")
  n1("`*«requirement»*
**freshwaterExposure : FreshwaterExposure**`")
  n2("`*«requirement»*
**saltwaterExposure : SaltwaterExposure**`")
  n3("`*«requirement»*
**enclosureSealing : EnclosureSealing**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-002 relationships 2

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
%% BlueDogViews::marineDurability2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 99 node(s) without a position, left undrawn, and 120 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**marineDurability : MarineDurability**`")
  n1("`*«requirement»*
**wetMechanicalIntegrity : WetMechanicalIntegrity**`")
  n2("`*«requirement»*
**wetElectricalIntegrity : WetElectricalIntegrity**`")
  n3("`*«requirement»*
**solarHeating : SolarHeating**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-002 relationships 3

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
%% BlueDogViews::marineDurability3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 99 node(s) without a position, left undrawn, and 113 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**marineDurability : MarineDurability**`")
  n1("`*«requirement»*
**printedMaterialAging : PrintedMaterialAging**`")
  n1 -.->|"derive"| n0
```

[Continue: N-044 WetMechanicalIntegrity](<requirements-n-044.md>)

[Continue: N-045 WetElectricalIntegrity](<requirements-n-045.md>)

[Continue: N-046 SolarHeating](<requirements-n-046.md>)
