# E-200 SustainedEnergyFeasibility relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**E-200 SustainedEnergyFeasibility** — The installed energy architecture shall support the selected bounded repeating profile without external charging, meeting the derived reserve, cycle-balance and peak-supply criteria.

**E-201 SustainedReserveProtection** — Conservative stored energy shall remain strictly above the R-002 protected reserve throughout the selected sustained-operation profile.

**E-202 RepeatableCycleBalance** — Stored energy at the end of the complete repeating profile shall be at least its initial value at the same profile phase.

**E-203 PeakSupplyCapability** — The battery supply shall support each selected mode’s coincident peak withdrawal power without harvesting.

**E-205 EnergyEvidenceReadiness** — An energy case shall be accepted only after its installed-load coverage, resource bounds, battery derating and interval-resolution evidence have been accepted.

## E-200 relationships 1

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
%% BlueDogViews::sustainedEnergyFeasibility1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 54 node(s) without a position, left undrawn, and 59 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**sustainedEnergyFeasibility : SustainedEnergyFeasibility**`")
  n1("`*«requirement»*
**sustainedReserveProtection : SustainedReserveProtection**`")
  n2("`*«requirement»*
**repeatableCycleBalance : RepeatableCycleBalance**`")
  n3("`*«requirement»*
**peakSupplyCapability : PeakSupplyCapability**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-200 relationships 2

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
%% BlueDogViews::sustainedEnergyFeasibility2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 56 node(s) without a position, left undrawn, and 61 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**sustainedEnergyFeasibility : SustainedEnergyFeasibility**`")
  n1("`*«requirement»*
**energyEvidenceReadiness : EnergyEvidenceReadiness**`")
  n1 -.->|"derive"| n0
```
