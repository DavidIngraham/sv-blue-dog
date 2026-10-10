# C-101 telemetry equipment

[All requirement views](<../requirements-views.md>)

**TelemetryEquipment** — Aggregate requirement for TelemetryEquipment. Acceptance requires all applicable derived leaf results (C-201, C-202, C-203, C-204); this parent has no independent executable pass/fail predicate. Shared verification context: Freshness threshold is 120 seconds for normal, emergency, powered recovery or unknown mode, and 600 seconds only for explicitly reported low energy without emergency or powered recovery. Staleness describes data age, not diagnosed link failure. Exercise a 24-hour outage and reconnection.

**TelemetryDisplayContent** — The shore endpoint shall display UTC sample time, position, mode, conservative usable energy, reserve, faults and age from each current telemetry record. Verification uses the shared context of C-101.

**TelemetryStaleIndication** — The shore endpoint shall indicate stale data when record age exceeds its C-101 mode threshold until receipt of a record within its applicable threshold. Verification uses the shared context of C-101.

**TelemetryIdentityPreservation** — The shore endpoint shall preserve received record identity and sequence numbers across the C-101 outage/reconnection test. Verification uses the shared context of C-101.

**TelemetryDuplicateSuppression** — The shore endpoint shall not present a duplicate telemetry record as a new observation. Verification uses the shared context of C-101.

## C-101 derivation 1

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
%% not represented: 113 node(s) without a position, left undrawn, and 144 edge(s) at them
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

## C-101 derivation 2

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
%% not represented: 115 node(s) without a position, left undrawn, and 146 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**telemetryEquipment : TelemetryEquipment**`")
  n1("`*«requirement»*
**telemetryDuplicateSuppression : TelemetryDuplicateSuppression**`")
  n1 -.->|"derive"| n0
```
