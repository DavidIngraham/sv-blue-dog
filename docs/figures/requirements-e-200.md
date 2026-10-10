# E-200 sustained energy feasibility

[All requirement views](<../requirements-views.md>)

**SustainedEnergyFeasibility** — The installed energy architecture shall support the selected bounded repeating mission profile without external charging, while meeting the derived reserve, cycle-balance and peak-supply criteria. The 72-hour campaign is an initial energy demonstration, not proof of indefinite weather availability, functional performance or ocean readiness.

**SustainedReserveProtection** — Conservative stored energy shall remain strictly above the R-002 protected reserve throughout the selected sustained-operation profile. For piecewise-constant net power, check the initial state and every interval endpoint; unmodeled intrainterval dips are outside this claim.

**RepeatableCycleBalance** — Stored energy at the end of the complete repeating profile shall be at least its initial value at the same profile phase. This is a conditional repeatability criterion with fixed capacity, loads and resource bounds; it is not an indefinite endurance verdict.

**PeakSupplyCapability** — The battery supply shall support each selected mode's coincident peak withdrawal power without relying on harvesting. Load power shall include conversion losses and the declared uncertainty allowance.

**EnergyEvidenceReadiness** — An energy case shall be accepted as evidence-backed only after the installed-configuration load coverage, resource bounds, battery derating and interval-resolution evidence have been reviewed and accepted under the sustained-operations evidence checklist.

## E-200 derivation 1

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
%% not represented: 47 node(s) without a position, left undrawn, and 53 edge(s) at them
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

## E-200 derivation 2

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
%% not represented: 49 node(s) without a position, left undrawn, and 55 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**sustainedEnergyFeasibility : SustainedEnergyFeasibility**`")
  n1("`*«requirement»*
**energyEvidenceReadiness : EnergyEvidenceReadiness**`")
  n1 -.->|"derive"| n0
```
