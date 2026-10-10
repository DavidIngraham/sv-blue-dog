# N-020 ocean environment

[All requirement views](<../requirements-views.md>)

**OceanEnvironment** — The vessel shall operate on a northeast Pacific passage toward Hawaii in saltwater, ocean swell, wind seas and prolonged unattended exposure. Ocean-derived parameter requirements and the shared exposure requirements apply together. The baseline is not a hurricane-survival claim or a completed route/season qualification.

**OceanWind** — The vessel shall retain the N-001 operational functions in true wind from 3 to 15 m/s (10-minute mean referenced to 10 m above water), including 3-second gusts up to 20 m/s. Qualification shall include upwind, crosswind and downwind headings; this is a functional wind limit, not a guarantee of upstream progress.

**OceanWaves** — The vessel shall retain N-001 operational functions in significant wave heights up to 3 m with peak periods 5-20 s, including individual waves up to 6 m. Wave statistics shall use 20-minute records. Qualification shall include head, beam and following seas and physically realizable wind-wave-current combinations within the profile.

**OceanCurrent** — The vessel shall retain navigation and control in currents from 0 to 1.0 m/s from any direction relative to wind and waves. Qualification shall include opposing current. Predicted boundary risk shall invoke S-002; current tolerance alone does not ensure progress or station keeping. Positive upstream speed is not required at every wind speed or heading.

**OceanSurvivalWind** — For 24 continuous hours, the vessel shall meet the N-001 survival acceptance outcomes in mean wind up to 25 m/s and 3-second gusts up to 35 m/s, using the operational wind reference convention. The respective wave, current, temperature and humidity limits apply concurrently.

**OceanSurvivalWaves** — For 24 continuous hours, the vessel shall meet the N-001 survival acceptance outcomes in significant wave heights up to 6 m, peak periods 6-20 s and individual waves up to 12 m. Qualification shall include adverse relative directions and physically realizable combinations with profile survival wind and current.

**SaltwaterExposure** — For ocean qualification, following 30 days continuous 35 g/kg saltwater exposure, with submerged parts continuously wet and complete topside spray wetting at least once per hour, the vessel shall pass its ocean functional checks without repair or servicing. This campaign is an exposure qualification, not proof of the eventual passage duration.

## N-020 derivation 1

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
%% not represented: 72 node(s) without a position, left undrawn, and 92 edge(s) at them
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

## N-020 derivation 2

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
%% not represented: 111 node(s) without a position, left undrawn, and 139 edge(s) at them
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
