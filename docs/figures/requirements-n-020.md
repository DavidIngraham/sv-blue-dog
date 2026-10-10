# N-020 OceanEnvironment relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**N-020 OceanEnvironment** — The vessel shall operate on a northeast Pacific passage toward Hawaii amid saltwater, ocean swell, wind seas and prolonged unattended exposure.

**N-021 OceanWind** — The vessel shall retain operational functions in 3–15 m/s mean true wind with 3-second gusts up to 20 m/s.

**N-022 OceanWaves** — The vessel shall retain operational functions in significant wave heights up to 3 m, peak periods 5–20 s and individual waves up to 6 m.

**N-023 OceanCurrent** — The vessel shall retain navigation and control in currents from 0 to 1.0 m/s from any direction relative to wind and waves.

**N-024 OceanSurvivalWind** — The vessel shall retain survival functions for 24 continuous hours in mean wind up to 25 m/s and 3-second gusts up to 35 m/s.

**N-025 OceanSurvivalWaves** — The vessel shall retain survival functions for 24 continuous hours in significant wave heights up to 6 m, peak periods 6–20 s and individual waves up to 12 m.

**N-042 SaltwaterExposure** — For ocean qualification, following 30 days continuous 35 g/kg saltwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its ocean functional checks without repair or servicing.

## N-020 relationships 1

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
%% BlueDogViews::oceanEnvironment1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 36 node(s) without a position, left undrawn, and 42 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**oceanEnvironment : OceanEnvironment**`")
  n1("`*«requirement»*
**oceanWind : OceanWind**`")
  n2("`*«requirement»*
**oceanWaves : OceanWaves**`")
  n3("`*«requirement»*
**oceanCurrent : OceanCurrent**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-020 relationships 2

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
%% BlueDogViews::oceanEnvironment2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 93 node(s) without a position, left undrawn, and 105 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**oceanEnvironment : OceanEnvironment**`")
  n1("`*«requirement»*
**oceanSurvivalWind : OceanSurvivalWind**`")
  n2("`*«requirement»*
**oceanSurvivalWaves : OceanSurvivalWaves**`")
  n3("`*«requirement»*
**saltwaterExposure : SaltwaterExposure**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```
