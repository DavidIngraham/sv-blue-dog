# E-002 NavigationAndControl relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**E-002 NavigationAndControl** — The vessel shall provide autonomous navigation and sail/steering control within the selected operational profile.

**E-008 NavigationAvailability** — The vessel shall maintain valid navigation inputs and reject stale observations.

**E-105 GuidanceUpdateCadence** — During operational qualification, mission guidance shall update at least once per second.

**E-106 SailCommandCadence** — During operational qualification, commanded sail position shall update at least once per second.

**E-107 SteeringCommandCadence** — During operational qualification, commanded steering position shall update at least once per second.

**E-108 PositionAccuracy** — At every epoch in the common E-002 acceptance set, valid position error shall be at most 10 m against an independent reference.

**E-109 HeadingAccuracy** — At every epoch in the common E-002 acceptance set, valid heading error shall be at most 10 degrees against an independent reference.

## E-002 relationships 1

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
%% BlueDogViews::navigationAndControl1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 128 node(s) without a position, left undrawn, and 172 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**navigationAndControl : NavigationAndControl**`")
  n1("`*«requirement»*
**navigationAvailability : NavigationAvailability**`")
  n2("`*«requirement»*
**guidanceUpdateCadence : GuidanceUpdateCadence**`")
  n3("`*«requirement»*
**sailCommandCadence : SailCommandCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-002 relationships 2

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
%% BlueDogViews::navigationAndControl2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 85 node(s) without a position, left undrawn, and 96 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**navigationAndControl : NavigationAndControl**`")
  n1("`*«requirement»*
**steeringCommandCadence : SteeringCommandCadence**`")
  n2("`*«requirement»*
**positionAccuracy : PositionAccuracy**`")
  n3("`*«requirement»*
**headingAccuracy : HeadingAccuracy**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| trafficSafety | navigationAndControl | TrafficSafety supports navigationAndControl. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: E-008 NavigationAvailability](<requirements-e-008.md>)

[Continue: S-001 TrafficSafety](<requirements-s-001.md>)
