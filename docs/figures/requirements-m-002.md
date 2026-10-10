# M-002 multi day endurance

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**M-002 MultiDayEndurance** — The vessel shall operate for 72 continuous hours without servicing or external charging under the specified Gorge energy campaign.

**E-001 EnergyAwareness** — The vessel shall maintain conservative estimates of usable energy and protected recovery reserve.

**E-004 LowEnergyRecovery** — The vessel shall protect essential functions when conservative usable energy reaches the recovery reserve.

**E-201 SustainedReserveProtection** — Conservative stored energy shall remain strictly above the R-002 protected reserve throughout the selected sustained-operation profile.

**E-203 PeakSupplyCapability** — The battery supply shall support each selected mode’s coincident peak withdrawal power without harvesting.

**E-204 HarvestCampaignCoverage** — The qualification energy profile shall contain at least three consecutive 24-hour days, each with harvesting enabled for no more than 6 hours.

**E-205 EnergyEvidenceReadiness** — An energy case shall be accepted only after its installed-load coverage, resource bounds, battery derating and interval-resolution evidence have been accepted.

## M-002 derivation 1

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
%% not represented: 237 node(s) without a position, left undrawn, and 475 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**multiDayEndurance : MultiDayEndurance**`")
  n1("`*«requirement»*
**energyAwareness : EnergyAwareness**`")
  n2("`*«requirement»*
**lowEnergyRecovery : LowEnergyRecovery**`")
  n3("`*«requirement»*
**sustainedReserveProtection : SustainedReserveProtection**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n2 -.->|"derive"| n1
  n3 -.->|"derive"| n0
```

## M-002 derivation 2

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
%% not represented: 225 node(s) without a position, left undrawn, and 425 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**multiDayEndurance : MultiDayEndurance**`")
  n1("`*«requirement»*
**peakSupplyCapability : PeakSupplyCapability**`")
  n2("`*«requirement»*
**harvestCampaignCoverage : HarvestCampaignCoverage**`")
  n3("`*«requirement»*
**energyEvidenceReadiness : EnergyEvidenceReadiness**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

[Continue: E-001 energy awareness](<requirements-e-001.md>)

[Continue: E-004 low energy recovery](<requirements-e-004.md>)
