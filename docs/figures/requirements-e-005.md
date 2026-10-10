# E-005 Communications relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**E-005 Communications** — The vessel shall support live telemetry through link outages and reconnection.

**E-120 TelemetryDeliveryCadence** — With a functioning link, current telemetry delivery intervals shall not exceed 60 seconds, except that low-energy operation without emergency/powered recovery permits 300 seconds.

**E-121 OutageAutonomy** — Through a 24-hour telemetry-link outage, autonomous mission control shall continue without operator intervention.

**E-122 ReconnectCurrentRecord** — After link restoration, a current telemetry record shall arrive within the active TelemetryDeliveryCadence interval.

**E-123 BacklogOrdering** — After reconnection, retained backlog records shall be transmitted in ascending acquisition sequence order.

**E-124 BacklogCurrentPriority** — During backlog transfer, current telemetry shall continue to meet TelemetryDeliveryCadence.

**E-131 LogRetention** — Acquired mission records shall remain retrievable onboard for at least 30 days.

**E-137 ReconnectLogPreservation** — Communication reconnection shall not delete retained mission records.

## E-005 relationships 1

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
%% BlueDogViews::communications1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 123 node(s) without a position, left undrawn, and 184 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**communications : Communications**`")
  n1("`*«requirement»*
**telemetryDeliveryCadence : TelemetryDeliveryCadence**`")
  n2("`*«requirement»*
**outageAutonomy : OutageAutonomy**`")
  n3("`*«requirement»*
**reconnectCurrentRecord : ReconnectCurrentRecord**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-005 relationships 2

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
%% BlueDogViews::communications2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 121 node(s) without a position, left undrawn, and 179 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**communications : Communications**`")
  n1("`*«requirement»*
**backlogOrdering : BacklogOrdering**`")
  n2("`*«requirement»*
**backlogCurrentPriority : BacklogCurrentPriority**`")
  n3("`*«requirement»*
**logRetention : LogRetention**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-005 relationships 3

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
%% BlueDogViews::communications3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 123 node(s) without a position, left undrawn, and 181 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**communications : Communications**`")
  n1("`*«requirement»*
**reconnectLogPreservation : ReconnectLogPreservation**`")
  n1 -.->|"derive"| n0
```

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| telemetryEquipment | communications | TelemetryEquipment supports communications. This is design motivation or an implementation choice, not a satisfaction implication. |
| commandIntegrity | communications | CommandIntegrity supports communications. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: C-102 CommandIntegrity](<requirements-c-102.md>)

[Continue: C-101 TelemetryEquipment](<requirements-c-101.md>)
