# C-101 TelemetryEquipment relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**C-101 TelemetryEquipment** — The shore endpoint shall present current vessel telemetry with explicit data age and identity.

**C-201 TelemetryDisplayContent** — The shore endpoint shall display UTC sample time, position, mode, conservative usable energy, reserve, faults and age from each current telemetry record.

**C-202 TelemetryStaleIndication** — The shore endpoint shall indicate stale data when record age exceeds its C-101 mode threshold until receipt of a record within its applicable threshold.

**C-203 TelemetryIdentityPreservation** — The shore endpoint shall preserve received record identity and sequence numbers across the C-101 outage/reconnection test.

**C-204 TelemetryDuplicateSuppression** — The shore endpoint shall not present a duplicate telemetry record as a new observation.

## C-101 relationships 1

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
%% BlueDogViews::telemetryEquipment1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 3 node(s) without a position, left undrawn, and 11 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**telemetryEquipment : TelemetryEquipment**`")
  n1("`*«requirement»*
**telemetryDisplayContent : TelemetryDisplayContent**`")
  n2("`*«requirement»*
**telemetryStaleIndication : TelemetryStaleIndication**`")
  n3("`*«requirement»*
**telemetryIdentityPreservation : TelemetryIdentityPreservation**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## C-101 relationships 2

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
%% BlueDogViews::telemetryEquipment2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 5 node(s) without a position, left undrawn, and 13 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**telemetryEquipment : TelemetryEquipment**`")
  n1("`*«requirement»*
**telemetryDuplicateSuppression : TelemetryDuplicateSuppression**`")
  n1 -.->|"derive"| n0
```
