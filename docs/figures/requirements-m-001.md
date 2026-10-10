# M-001 round trip

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**M-001 RoundTrip** — The vessel shall cross the configured The Dalles departure, Bonneville turnaround and The Dalles return gates in order during one qualifying attempt.

**E-002 NavigationAndControl** — The vessel shall provide autonomous navigation and sail/steering control within the selected operational profile.

**E-003 ResetRecovery** — The vessel shall restore mode-appropriate autonomous operation after a watchdog reset.

**E-005 Communications** — The vessel shall support live telemetry through link outages and reconnection.

**E-006 IngressResponse** — The vessel shall retain recoverability during the specified hull-ingress qualification.

**E-007 MissionEvidence** — The vessel shall retain time-correlated mission evidence through communication and power interruptions.

**P-001 Transportability** — The vessel shall support transport, assembly, launch and retrieval by one adult under the specified handling conditions.

**P-002 DesktopManufacture** — Every print job shall fit within positive X, Y and Z extents no greater than 250 mm each.

**S-002 OperatingBoundary** — The vessel shall enforce the configured operating boundaries.

**S-005 RegulatoryClassification** — Deployment shall require documented compliance with applicable navigation, radio and authorization obligations.

**N-001 EnvironmentalEnvelope** — The vessel shall retain the functions required by its selected environmental profile and operating mode.

**N-010 GorgeEnvironment** — The vessel shall operate in the freshwater Columbia River reach between The Dalles and Bonneville, including opposing wind/current, short chop, traffic and submerged vegetation.

**Q-001 CruisePerformance** — The vessel shall sustain sailing performance sufficient to complete each declared unassisted mission route.

**L-001 MissionReliability** — The vessel shall preserve mission-critical functions throughout each declared unassisted voyage.

## M-001 derivation 1

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
%% BlueDogViews::roundTrip1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 240 node(s) without a position, left undrawn, and 476 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**roundTrip : RoundTrip**`")
  n1("`*«requirement»*
**navigationAndControl : NavigationAndControl**`")
  n2("`*«requirement»*
**resetRecovery : ResetRecovery**`")
  n3("`*«requirement»*
**communications : Communications**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## M-001 derivation 2

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
%% BlueDogViews::roundTrip2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 234 node(s) without a position, left undrawn, and 449 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**roundTrip : RoundTrip**`")
  n1("`*«requirement»*
**ingressResponse : IngressResponse**`")
  n2("`*«requirement»*
**missionEvidence : MissionEvidence**`")
  n3("`*«requirement»*
**transportability : Transportability**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## M-001 derivation 3

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
%% BlueDogViews::roundTrip3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 227 node(s) without a position, left undrawn, and 417 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**roundTrip : RoundTrip**`")
  n1("`*«requirement»*
**desktopManufacture : DesktopManufacture**`")
  n2("`*«requirement»*
**operatingBoundary : OperatingBoundary**`")
  n3("`*«requirement»*
**regulatoryClassification : RegulatoryClassification**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## M-001 derivation 4

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
%% BlueDogViews::roundTrip4 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 226 node(s) without a position, left undrawn, and 409 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**roundTrip : RoundTrip**`")
  n1("`*«requirement»*
**environmentalEnvelope : EnvironmentalEnvelope**`")
  n2("`*«requirement»*
**gorgeEnvironment : GorgeEnvironment**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```

[Continue: E-002 navigation and control](<requirements-e-002.md>)

[Continue: E-003 reset recovery](<requirements-e-003.md>)

[Continue: E-005 communications](<requirements-e-005.md>)

[Continue: E-006 ingress response](<requirements-e-006.md>)

[Continue: E-007 mission evidence](<requirements-e-007.md>)

[Continue: P-001 transportability](<requirements-p-001.md>)

[Continue: S-002 operating boundary](<requirements-s-002.md>)

[Continue: S-005 regulatory classification](<requirements-s-005.md>)

[Continue: N-001 environmental envelope](<requirements-n-001.md>)

[Continue: N-010 gorge environment](<requirements-n-010.md>)

## M-001 derivation 5

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
%% BlueDogViews::roundTrip5 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 225 node(s) without a position, left undrawn, and 408 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**roundTrip : RoundTrip**`")
  n1("`*«requirement»*
**cruisePerformance : CruisePerformance**`")
  n2("`*«requirement»*
**missionReliability : MissionReliability**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```

[Continue: Q-001 cruisePerformance](<requirements-q-001.md>)

[Continue: L-001 missionReliability](<requirements-l-001.md>)
