# M-002 MultiDayEndurance relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**M-002 MultiDayEndurance** — The vessel shall operate for 72 continuous hours without servicing or external charging under the specified Gorge energy campaign.

**E-201 SustainedReserveProtection** — Conservative stored energy shall remain strictly above the R-002 protected reserve throughout the selected sustained-operation profile.

**E-203 PeakSupplyCapability** — The battery supply shall support each selected mode’s coincident peak withdrawal power without harvesting.

**E-204 HarvestCampaignCoverage** — The qualification energy profile shall contain at least three consecutive 24-hour days, each with harvesting enabled for no more than 6 hours.

**E-205 EnergyEvidenceReadiness** — An energy case shall be accepted only after its installed-load coverage, resource bounds, battery derating and interval-resolution evidence have been accepted.

## M-002 relationships 1

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
%% BlueDogViews::multiDayEndurance1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 54 node(s) without a position, left undrawn, and 59 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**multiDayEndurance : MultiDayEndurance**`")
  n1("`*«requirement»*
**sustainedReserveProtection : SustainedReserveProtection**`")
  n2("`*«requirement»*
**peakSupplyCapability : PeakSupplyCapability**`")
  n3("`*«requirement»*
**harvestCampaignCoverage : HarvestCampaignCoverage**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## M-002 relationships 2

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
%% BlueDogViews::multiDayEndurance2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 55 node(s) without a position, left undrawn, and 57 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**multiDayEndurance : MultiDayEndurance**`")
  n1("`*«requirement»*
**energyEvidenceReadiness : EnergyEvidenceReadiness**`")
  n1 -.->|"derive"| n0
```

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| energyAwareness | multiDayEndurance | Multi-day operation with variable harvesting needs energy estimation and load management. This is design motivation or an implementation choice, not a satisfaction implication. |
| lowEnergyRecovery | multiDayEndurance | Harvest shortfalls need an explicit degraded operating mode. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: E-004 LowEnergyRecovery](<requirements-e-004.md>)

[Continue: E-001 EnergyAwareness](<requirements-e-001.md>)
