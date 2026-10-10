# S-003 SafeRecovery relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**S-003 SafeRecovery** — The vessel shall support controlled emergency intervention and powered recovery.

**S-110 AbortLatchDeadline** — After accepting emergency abort, the vessel shall latch the attempt as disqualified within 1 second.

**S-111 RecoveryTelemetryCadence** — During active emergency or powered recovery with a functioning link, the vessel shall deliver position telemetry at least once per 60 seconds, including low-energy operation.

**S-112 MotorIsolationDeadline** — A physically accessible local isolation control shall remove motor power within 1 second of activation.

**S-113 IsolationRestartInhibition** — Motor restart shall remain inhibited after local isolation until deliberate local reset.

**S-114 ManualControlLossShutdown** — After remote control has been lost for 5 seconds during manual powered recovery, the vessel shall command zero thrust within a further 1 second.

**S-115 ControlLossLocationContinuity** — Location reporting shall continue at the active telemetry cadence after remote-control loss whenever a telemetry link is available.

**E-138 QualificationPersistence** — Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable.

**R-101 MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown.

**E-130 PeriodicLogCadence** — Periodic mission records shall be acquired at least once per second normally and once per minute in low-energy or survival operation.

## S-003 relationships 1

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
%% BlueDogViews::safeRecovery1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 113 node(s) without a position, left undrawn, and 163 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**safeRecovery : SafeRecovery**`")
  n1("`*«requirement»*
**abortLatchDeadline : AbortLatchDeadline**`")
  n2("`*«requirement»*
**recoveryTelemetryCadence : RecoveryTelemetryCadence**`")
  n3("`*«requirement»*
**motorIsolationDeadline : MotorIsolationDeadline**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-003 relationships 2

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
%% BlueDogViews::safeRecovery2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 113 node(s) without a position, left undrawn, and 163 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**safeRecovery : SafeRecovery**`")
  n1("`*«requirement»*
**isolationRestartInhibition : IsolationRestartInhibition**`")
  n2("`*«requirement»*
**manualControlLossShutdown : ManualControlLossShutdown**`")
  n3("`*«requirement»*
**controlLossLocationContinuity : ControlLossLocationContinuity**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-003 relationships 3

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
%% BlueDogViews::safeRecovery3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 130 node(s) without a position, left undrawn, and 206 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**safeRecovery : SafeRecovery**`")
  n1("`*«requirement»*
**qualificationPersistence : QualificationPersistence**`")
  n2("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n3("`*«requirement»*
**periodicLogCadence : PeriodicLogCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| recoveryPropulsion | safeRecovery | RecoveryPropulsion supports safeRecovery. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: R-001 RecoveryPropulsion](<requirements-r-001.md>)
