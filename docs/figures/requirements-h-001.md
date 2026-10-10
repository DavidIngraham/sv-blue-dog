# H-001 hawaii voyage

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**H-001 HawaiiVoyage** — The vessel shall complete an autonomous sailing voyage to Hawaii.

**M-002 MultiDayEndurance** — The vessel shall operate for 72 continuous hours without servicing or external charging under the specified Gorge energy campaign.

**E-002 NavigationAndControl** — The vessel shall provide autonomous navigation and sail/steering control within the selected operational profile.

**E-005 Communications** — The vessel shall support live telemetry through link outages and reconnection.

**E-003 ResetRecovery** — The vessel shall restore mode-appropriate autonomous operation after a watchdog reset.

**E-007 MissionEvidence** — The vessel shall retain time-correlated mission evidence through communication and power interruptions.

**N-001 EnvironmentalEnvelope** — The vessel shall retain the functions required by its selected environmental profile and operating mode.

**N-020 OceanEnvironment** — The vessel shall operate on a northeast Pacific passage toward Hawaii amid saltwater, ocean swell, wind seas and prolonged unattended exposure.

**S-002 OperatingBoundary** — The vessel shall enforce the configured operating boundaries.

**S-005 RegulatoryClassification** — Deployment shall require documented compliance with applicable navigation, radio and authorization obligations.

**P-003 Serviceability** — The vessel shall support replacement of serviceable equipment without structural damage.

**E-200 SustainedEnergyFeasibility** — The installed energy architecture shall support the selected bounded repeating profile without external charging, meeting the derived reserve, cycle-balance and peak-supply criteria.

## H-001 derivation 1

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
%% BlueDogViews::hawaiiVoyage1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 228 node(s) without a position, left undrawn, and 461 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**BlueDog::Goals::hawaiiVoyage : HawaiiVoyage**`")
  n1("`*«requirement»*
**BlueDogRequirements::multiDayEndurance : MultiDayEndurance**`")
  n2("`*«requirement»*
**BlueDogRequirements::navigationAndControl : NavigationAndControl**`")
  n3("`*«requirement»*
**BlueDogRequirements::communications : Communications**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## H-001 derivation 2

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
%% BlueDogViews::hawaiiVoyage2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 225 node(s) without a position, left undrawn, and 443 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**BlueDog::Goals::hawaiiVoyage : HawaiiVoyage**`")
  n1("`*«requirement»*
**BlueDogRequirements::resetRecovery : ResetRecovery**`")
  n2("`*«requirement»*
**BlueDogRequirements::missionEvidence : MissionEvidence**`")
  n3("`*«requirement»*
**BlueDogRequirements::environmentalEnvelope : EnvironmentalEnvelope**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## H-001 derivation 3

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
%% BlueDogViews::hawaiiVoyage3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 215 node(s) without a position, left undrawn, and 411 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**BlueDog::Goals::hawaiiVoyage : HawaiiVoyage**`")
  n1("`*«requirement»*
**BlueDogRequirements::oceanEnvironment : OceanEnvironment**`")
  n2("`*«requirement»*
**BlueDogRequirements::operatingBoundary : OperatingBoundary**`")
  n3("`*«requirement»*
**BlueDogRequirements::regulatoryClassification : RegulatoryClassification**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## H-001 derivation 4

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
%% BlueDogViews::hawaiiVoyage4 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 217 node(s) without a position, left undrawn, and 411 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**BlueDog::Goals::hawaiiVoyage : HawaiiVoyage**`")
  n1("`*«requirement»*
**BlueDogRequirements::serviceability : Serviceability**`")
  n2("`*«requirement»*
**BlueDogRequirements::sustainedEnergyFeasibility : SustainedEnergyFeasibility**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```

[Continue: M-002 multi day endurance](<requirements-m-002.md>)

[Continue: E-002 navigation and control](<requirements-e-002.md>)

[Continue: E-005 communications](<requirements-e-005.md>)

[Continue: E-003 reset recovery](<requirements-e-003.md>)

[Continue: E-007 mission evidence](<requirements-e-007.md>)

[Continue: N-001 environmental envelope](<requirements-n-001.md>)

[Continue: N-020 ocean environment](<requirements-n-020.md>)

[Continue: S-002 operating boundary](<requirements-s-002.md>)

[Continue: S-005 regulatory classification](<requirements-s-005.md>)

[Continue: P-003 serviceability](<requirements-p-003.md>)

[Continue: E-200 sustained energy feasibility](<requirements-e-200.md>)
