# S-003 safe recovery

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**S-003 SafeRecovery** — The vessel shall support controlled emergency intervention and powered recovery.

**R-001 RecoveryPropulsion** — At maximum mission load, powered recovery shall sustain at least 0.5 m/s over ground for 30 minutes against a 1.5 m/s current.

**S-110 AbortLatchDeadline** — After accepting emergency abort, the vessel shall latch the attempt as disqualified within 1 second.

**S-111 RecoveryTelemetryCadence** — During active emergency or powered recovery with a functioning link, the vessel shall deliver position telemetry at least once per 60 seconds, including low-energy operation.

**S-112 MotorIsolationDeadline** — A physically accessible local isolation control shall remove motor power within 1 second of activation.

**S-113 IsolationRestartInhibition** — Motor restart shall remain inhibited after local isolation until deliberate local reset.

**S-114 ManualControlLossShutdown** — After remote control has been lost for 5 seconds during manual powered recovery, the vessel shall command zero thrust within a further 1 second.

**S-115 ControlLossLocationContinuity** — Location reporting shall continue at the active telemetry cadence after remote-control loss whenever a telemetry link is available.

**E-138 QualificationPersistence** — Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable.

**R-101 MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown.

**E-130 PeriodicLogCadence** — Periodic mission records shall be acquired at least once per second normally and once per minute in low-energy or survival operation.

## S-003 derivation 1

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
%% not represented: 130 node(s) without a position, left undrawn, and 195 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**safeRecovery : SafeRecovery**`")
  n1("`*«requirement»*
**recoveryPropulsion : RecoveryPropulsion**`")
  n2("`*«requirement»*
**abortLatchDeadline : AbortLatchDeadline**`")
  n3("`*«requirement»*
**recoveryTelemetryCadence : RecoveryTelemetryCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-003 derivation 2

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
%% not represented: 129 node(s) without a position, left undrawn, and 194 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**safeRecovery : SafeRecovery**`")
  n1("`*«requirement»*
**motorIsolationDeadline : MotorIsolationDeadline**`")
  n2("`*«requirement»*
**isolationRestartInhibition : IsolationRestartInhibition**`")
  n3("`*«requirement»*
**manualControlLossShutdown : ManualControlLossShutdown**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-003 derivation 3

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
%% not represented: 133 node(s) without a position, left undrawn, and 201 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**safeRecovery : SafeRecovery**`")
  n1("`*«requirement»*
**controlLossLocationContinuity : ControlLossLocationContinuity**`")
  n2("`*«requirement»*
**qualificationPersistence : QualificationPersistence**`")
  n3("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-003 derivation 4

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
%% BlueDogViews::safeRecovery4 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 147 node(s) without a position, left undrawn, and 236 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**safeRecovery : SafeRecovery**`")
  n1("`*«requirement»*
**periodicLogCadence : PeriodicLogCadence**`")
  n1 -.->|"derive"| n0
```

[Continue: R-001 recovery propulsion](<requirements-r-001.md>)
