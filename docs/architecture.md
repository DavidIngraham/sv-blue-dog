# SV Blue Dog logical architecture

The Mermaid diagrams are generated natively by OpenSysML through
`scripts/render_requirements.py`. The same model views also produce standalone
HTML documents in `figures/`; GitHub renders the Mermaid blocks below.

## Mission context

<!-- diagram:context -->
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
%% BlueDogArchitectureViews::context — interconnection rendering (render Views::asInterconnectionDiagram)
flowchart TB
  subgraph n0 ["`*«part»* **missionContext**`"]
    direction TB
    n1("`*«part»*
**boat : Boat**`")
    n2("`*«part»*
**operator : Operator**`")
    n3("`*«part»*
**shoreSupport : ShoreSupport**`")
    n4("`*«part»*
**environment : Environment**`")
    n5("`*«part»*
**traffic : OtherVessel**`")
  end
```
<!-- /diagram -->

## Boat definition and composition

<!-- diagram:architecture -->
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
%% BlueDogArchitectureViews::architecture — definition rendering (view def GeneralView, filter @PartDefinition)
flowchart TB
  n0["`*«part def»*
**Boat**`"]
  n1["`*«part def»*
**NavigationSignaling**`"]
  n2["`*«part def»*
**HullAndRig**`"]
  n3["`*«part def»*
**EnergySubsystem**`"]
  n4["`*«part def»*
**NavigationAndSensing**`"]
  n5["`*«part def»*
**GuidanceAndControl**`"]
  n6["`*«part def»*
**SailAndSteeringActuation**`"]
  n7["`*«part def»*
**Communications**`"]
  n8["`*«part def»*
**HealthAndRecovery**`"]
  n9["`*«part def»*
**DataRecording**`"]
  n10["`*«part def»*
**ObservationPayload**`"]
  n0 ---|"◆ hullAndRig"| n2
  n0 ---|"◆ energy"| n3
  n0 ---|"◆ navigation"| n4
  n0 ---|"◆ control"| n5
  n0 ---|"◆ actuation"| n6
  n0 ---|"◆ communications"| n7
  n0 ---|"◆ recovery"| n8
  n0 ---|"◆ recording"| n9
  n0 ---|"◆ signaling"| n1
  n0 ---|"◆ observationPayload"| n10
```
<!-- /diagram -->

The boat view uses native definition-diagram rendering: composition links have
filled diamonds at Boat and labels naming its parts. This is the SysML v2
equivalent of the requested BDD-style presentation. The context view retains
its nested parts. Both views show the model already declared in
[blue-dog.sysml](../models/blue-dog.sysml). They describe logical responsibilities
shared by the Gorge and Hawaii missions, not selected circuit boards.
The observation payload is optional (`[0..1]` in the model); the native diagram
currently omits that multiplicity label.

## Detailed composition

<!-- diagram:architecture-detail -->
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
%% BlueDogArchitectureViews::detail — definition rendering (view def GeneralView, filter @PartDefinition)
flowchart TB
  n0["`*«part def»*
**Operator**`"]
  n1["`*«part def»*
**MonitoringStation**`"]
  n2["`*«part def»*
**ShoreSupport**`"]
  n3["`*«part def»*
**Environment**`"]
  n4["`*«part def»*
**OtherVessel**`"]
  n5["`*«part def»*
**PrintedHull**`"]
  n6["`*«part def»*
**SealedEnclosure**`"]
  n7["`*«part def»*
**KeelAndBallast**`"]
  n8["`*«part def»*
**HandlingInterfaces**`"]
  n9["`*«part def»*
**HullAndRig**`"]
  n10["`*«part def»*
**EnergyStorage**`"]
  n11["`*«part def»*
**HarvestingInterface**`"]
  n12["`*«part def»*
**PowerManagement**`"]
  n13["`*«part def»*
**EnergySubsystem**`"]
  n14["`*«part def»*
**PositionAndAttitude**`"]
  n15["`*«part def»*
**WindSensing**`"]
  n16["`*«part def»*
**TrafficSensing**`"]
  n17["`*«part def»*
**NavigationAndSensing**`"]
  n18["`*«part def»*
**MissionManager**`"]
  n19["`*«part def»*
**CollisionAvoidance**`"]
  n20["`*«part def»*
**BoundarySupervisor**`"]
  n21["`*«part def»*
**GuidanceAndControl**`"]
  n22["`*«part def»*
**SailAndSteeringActuation**`"]
  n23["`*«part def»*
**TelemetryRadio**`"]
  n24["`*«part def»*
**AntennaSystem**`"]
  n25["`*«part def»*
**CommandGateway**`"]
  n26["`*«part def»*
**Communications**`"]
  n27["`*«part def»*
**RecoveryPropulsion**`"]
  n28["`*«part def»*
**RecoveryController**`"]
  n29["`*«part def»*
**IngressMonitor**`"]
  n30["`*«part def»*
**HealthAndRecovery**`"]
  n31["`*«part def»*
**NavigationSignaling**`"]
  n32["`*«part def»*
**DataRecording**`"]
  n33["`*«part def»*
**ObservationPayload**`"]
  n34["`*«part def»*
**Boat**`"]
  n2 ---|"◆ monitoringStation"| n1
  n9 ---|"◆ printedHull"| n5
  n9 ---|"◆ enclosure"| n6
  n9 ---|"◆ keelAndBallast"| n7
  n9 ---|"◆ handling"| n8
  n13 ---|"◆ storage"| n10
  n13 ---|"◆ harvesting"| n11
  n13 ---|"◆ powerManagement"| n12
  n17 ---|"◆ positionAndAttitude"| n14
  n17 ---|"◆ wind"| n15
  n17 ---|"◆ traffic"| n16
  n21 ---|"◆ missionManager"| n18
  n21 ---|"◆ collisionAvoidance"| n19
  n21 ---|"◆ boundarySupervisor"| n20
  n26 ---|"◆ telemetryRadio"| n23
  n26 ---|"◆ antenna"| n24
  n26 ---|"◆ commandGateway"| n25
  n30 ---|"◆ motorSystem"| n27
  n30 ---|"◆ recoveryController"| n28
  n30 ---|"◆ ingressMonitor"| n29
  n34 ---|"◆ hullAndRig"| n9
  n34 ---|"◆ energy"| n13
  n34 ---|"◆ navigation"| n17
  n34 ---|"◆ control"| n21
  n34 ---|"◆ actuation"| n22
  n34 ---|"◆ communications"| n26
  n34 ---|"◆ recovery"| n30
  n34 ---|"◆ recording"| n32
  n34 ---|"◆ signaling"| n31
  n34 ---|"◆ observationPayload"| n33
```
<!-- /diagram -->

The model now separates printed hull and seals, handling interfaces, energy
storage and management, position/wind/traffic sensing, mission and collision
control, telemetry/command equipment, and powered recovery. Navigation signaling
is a separate logical responsibility. Equipment makes, dimensions, and budgets
remain open.

## Use cases and requirements

<!-- diagram:use-cases -->
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
%% BlueDogUseCaseViews::operations — case rendering (view def GeneralView, filter @UseCaseUsage)
flowchart TB
  n0(["`*«use case»*
**BlueDogUseCases::prepare**`"])
  n1["`*«subject»*
**boat : Boat**`"]
  n2["`*«actor»*
**operator : Operator**`"]
  n3@{ shape: notch-rect, label: "«objective»<br>'P-001 Transportability'" }
  n4(["`*«use case»*
**BlueDogUseCases::sailGorge**`"])
  n5["`*«subject»*
**boat : Boat**`"]
  n6["`*«actor»*
**operator : Operator**`"]
  n7["`*«actor»*
**traffic : OtherVessel**`"]
  n8@{ shape: notch-rect, label: "«objective»<br>'M-001 Gorge mission'" }
  n9(["`*«use case»*
**BlueDogUseCases::sailOcean**`"])
  n10["`*«subject»*
**boat : Boat**`"]
  n11["`*«actor»*
**operator : Operator**`"]
  n12["`*«actor»*
**traffic : OtherVessel**`"]
  n13@{ shape: notch-rect, label: "«objective»<br>'H-001 Hawaii voyage'" }
  n14(["`*«use case»*
**BlueDogUseCases::monitor**`"])
  n15["`*«subject»*
**boat : Boat**`"]
  n16["`*«actor»*
**operator : Operator**`"]
  n17@{ shape: notch-rect, label: "«objective»<br>'C-101 Telemetry'" }
  n18(["`*«use case»*
**BlueDogUseCases::recover**`"])
  n19["`*«subject»*
**boat : Boat**`"]
  n20["`*«actor»*
**operator : Operator**`"]
  n21["`*«actor»*
**traffic : OtherVessel**`"]
  n22@{ shape: notch-rect, label: "«objective»<br>'S-003 Safe recovery'" }
  n23(["`*«use case»*
**BlueDogUseCases::maintain**`"])
  n24["`*«subject»*
**boat : Boat**`"]
  n25["`*«actor»*
**operator : Operator**`"]
  n26@{ shape: notch-rect, label: "«objective»<br>'P-003 Serviceability'" }
  n27(["`*«use case»*
**BlueDogUseCases::avoidTraffic**`"])
  n28["`*«subject»*
**boat : Boat**`"]
  n29["`*«actor»*
**operator : Operator**`"]
  n30["`*«actor»*
**traffic : OtherVessel**`"]
  n31@{ shape: notch-rect, label: "«objective»<br>'S-001 Traffic safety'" }
  n32(["`*«use case»*
**BlueDogUseCases::presentNavigationSignals**`"])
  n33["`*«subject»*
**boat : Boat**`"]
  n34["`*«actor»*
**traffic : OtherVessel**`"]
  n35@{ shape: notch-rect, label: "«objective»<br>'S-004 Navigation conspicuity'" }
  n0 ---|"«subject»"| n1
  n2 --- n0
  n0 -.- n3
  n4 ---|"«subject»"| n5
  n6 --- n4
  n7 --- n4
  n4 -.- n8
  n9 ---|"«subject»"| n10
  n11 --- n9
  n12 --- n9
  n9 -.- n13
  n14 ---|"«subject»"| n15
  n16 --- n14
  n14 -.- n17
  n18 ---|"«subject»"| n19
  n20 --- n18
  n21 --- n18
  n18 -.- n22
  n23 ---|"«subject»"| n24
  n25 --- n23
  n23 -.- n26
  n27 ---|"«subject»"| n28
  n29 --- n27
  n30 --- n27
  n27 -.- n31
  n32 ---|"«subject»"| n33
  n34 --- n32
  n32 -.- n35
```
<!-- /diagram -->

The use cases cover preparation, Gorge and Hawaii sailing, live monitoring,
collision avoidance, manufacturing/service, and abort/recovery. Each objective
subsets an existing requirement usage; its ID is shown in the diagram.
Actor participation represents stakeholder involvement, not permission to guide
a qualifying voyage remotely.

[Native traceability tables](traceability.md) connect use-case objectives to
requirements and requirements to candidate design elements through SysML
`satisfy` relationships. These are design assertions awaiting evidence, not
verification results. Unallocated regulatory classification is deliberately
visible as a gap: it requires a project-level review.

[Operating constraints and regulatory sources](operating-constraints.md) explain
why no unattended-buoy size exemption has been assumed.

Ports and power/data connections have not yet been modeled; composition links
are not interfaces.
The context boat is typed by the Boat definition shown in the subsystem view.

The views are defined in [architecture-view.sysml](../models/architecture-view.sysml).
Regenerate both diagrams, the requirement diagram, and the register with
`uv run python scripts/render_requirements.py`. Native DOT, SVG, and PNG are
committed in `docs/figures/`; `--check` checks the DOT and register for freshness.

## External traffic

The context includes zero or more `OtherVessel` instances: commercial ships, barges and recreational/fishing craft, including non-AIS traffic. These are external participants, not onboard components or controllable resources. Voyage and recovery use cases include traffic; collision avoidance links to S-001 and presentation of navigation signals links to S-004. The operator actor does not imply intervention is required during a qualifying attempt. Encounter geometry and sensor performance remain to be decomposed.

Environmental qualification targets are decomposed beneath N-001 through N-003; see [envelope and acceptance criteria](environmental-envelope.md).

Recovery propulsion medium remains unselected; see the [water/air propeller trade study](recovery-propulsion-trade.md).

The independent requirements audit moved aggregate mission and environmental outcomes to the whole `boat` design allocation, and shore-display behavior to `monitoringStation`. Component responsibilities remain visible in the architecture, but a subsystem is not claimed to independently satisfy a whole-vessel outcome. The launch-energy gate and challenge motor invariant are separately identified requirements.

## Reliability and failure modes

The [initial DFMEA](dfmea.md) links 12 failure modes to logical parts and affected requirements. [Cruise/reliability analysis](cruise-reliability.md) relates sailing performance and holds to failure exposure. Architecture allocations are design intentions; these analyses are not proof of hardware reliability.
