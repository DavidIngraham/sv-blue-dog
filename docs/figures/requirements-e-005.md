# E-005 communications

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**E-005 Communications** — The vessel shall support live telemetry through link outages and reconnection.

**C-101 TelemetryEquipment** — The shore endpoint shall present current vessel telemetry with explicit data age and identity.

**C-102 CommandIntegrity** — The vessel shall accept external commands only under the specified authentication, freshness and qualification rules.

**E-120 TelemetryDeliveryCadence** — With a functioning link, current telemetry delivery intervals shall not exceed 60 seconds, except that low-energy operation without emergency/powered recovery permits 300 seconds.

**E-121 OutageAutonomy** — Through a 24-hour telemetry-link outage, autonomous mission control shall continue without operator intervention.

**E-122 ReconnectCurrentRecord** — After link restoration, a current telemetry record shall arrive within the active TelemetryDeliveryCadence interval.

**E-123 BacklogOrdering** — After reconnection, retained backlog records shall be transmitted in ascending acquisition sequence order.

**E-124 BacklogCurrentPriority** — During backlog transfer, current telemetry shall continue to meet TelemetryDeliveryCadence.

**E-131 LogRetention** — Acquired mission records shall remain retrievable onboard for at least 30 days.

**E-137 ReconnectLogPreservation** — Communication reconnection shall not delete retained mission records.

## E-005 derivation 1

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
%% not represented: 219 node(s) without a position, left undrawn, and 430 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**communications : Communications**`")
  n1("`*«requirement»*
**telemetryEquipment : TelemetryEquipment**`")
  n2("`*«requirement»*
**commandIntegrity : CommandIntegrity**`")
  n3("`*«requirement»*
**telemetryDeliveryCadence : TelemetryDeliveryCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-005 derivation 2

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
%% not represented: 216 node(s) without a position, left undrawn, and 412 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**communications : Communications**`")
  n1("`*«requirement»*
**outageAutonomy : OutageAutonomy**`")
  n2("`*«requirement»*
**reconnectCurrentRecord : ReconnectCurrentRecord**`")
  n3("`*«requirement»*
**backlogOrdering : BacklogOrdering**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-005 derivation 3

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
%% not represented: 216 node(s) without a position, left undrawn, and 412 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**communications : Communications**`")
  n1("`*«requirement»*
**backlogCurrentPriority : BacklogCurrentPriority**`")
  n2("`*«requirement»*
**logRetention : LogRetention**`")
  n3("`*«requirement»*
**reconnectLogPreservation : ReconnectLogPreservation**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

[Continue: C-101 telemetry equipment](<requirements-c-101.md>)

[Continue: C-102 command integrity](<requirements-c-102.md>)
