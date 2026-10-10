# E-002 navigation and control

[All requirement views](<../requirements-views.md>)

**NavigationAndControl** — Aggregate requirement for NavigationAndControl. Acceptance requires all applicable derived leaf results (E-105, E-106, E-107, E-108, E-109); this parent has no independent executable pass/fail predicate. Shared verification context: Qualification uses the selected mission profile. Accuracy trials contain 1800 scheduled one-second epochs in 30 minutes; invalid or missing epochs fail. Position and heading criteria use the same set of at least 1710 qualifying epochs, preventing separate selection of different good samples. Fault-injection runs are separate.

**TrafficSafety** — Aggregate requirement for TrafficSafety. Acceptance requires all applicable derived leaf results (S-101, S-102, S-103, S-104); this parent has no independent executable pass/fail predicate. Shared verification context: Use independently recorded head-on, crossing and overtaking AIS and non-AIS targets, day and night in the selected operational profile. Detection ranges, target signatures, closest-approach margins and maneuver feasibility remain unresolved acceptance parameters; tracking and avoidance cannot receive complete passes until these are frozen.

**NavigationAvailability** — Aggregate requirement for NavigationAvailability. Acceptance requires all applicable derived leaf results (E-140, E-141, E-142, E-143, E-132); this parent has no independent executable pass/fail predicate. Shared verification context: Campaigns use 1800 scheduled one-second epochs in 30 minutes, with missing/invalid epochs counted as failures. Fault injection is separate.

**GuidanceUpdateCadence** — During operational qualification, mission guidance shall update at least once per second. Verification uses the shared context of E-002.

**SailCommandCadence** — During operational qualification, commanded sail position shall update at least once per second. Verification uses the shared context of E-002.

**SteeringCommandCadence** — During operational qualification, commanded steering position shall update at least once per second. Verification uses the shared context of E-002.

**PositionAccuracy** — At every epoch in the common E-002 acceptance set, valid position error shall be at most 10 m against an independent reference. Verification uses the shared context of E-002.

**HeadingAccuracy** — At every epoch in the common E-002 acceptance set, valid heading error shall be at most 10 degrees against an independent reference. Verification uses the shared context of E-002.

## E-002 derivation 1

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
%% not represented: 211 node(s) without a position, left undrawn, and 390 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**navigationAndControl : NavigationAndControl**`")
  n1("`*«requirement»*
**trafficSafety : TrafficSafety**`")
  n2("`*«requirement»*
**navigationAvailability : NavigationAvailability**`")
  n3("`*«requirement»*
**guidanceUpdateCadence : GuidanceUpdateCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-002 derivation 2

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
%% not represented: 211 node(s) without a position, left undrawn, and 390 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**navigationAndControl : NavigationAndControl**`")
  n1("`*«requirement»*
**sailCommandCadence : SailCommandCadence**`")
  n2("`*«requirement»*
**steeringCommandCadence : SteeringCommandCadence**`")
  n3("`*«requirement»*
**positionAccuracy : PositionAccuracy**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-002 derivation 3

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
%% BlueDogViews::navigationAndControl3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 213 node(s) without a position, left undrawn, and 392 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**navigationAndControl : NavigationAndControl**`")
  n1("`*«requirement»*
**headingAccuracy : HeadingAccuracy**`")
  n1 -.->|"derive"| n0
```

[Continue: S-001 traffic safety](<requirements-s-001.md>)

[Continue: E-008 navigation availability](<requirements-e-008.md>)
