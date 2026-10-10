# C-102 command integrity

[All requirement views](<../requirements-views.md>)

**CommandIntegrity** — Aggregate requirement for CommandIntegrity. Acceptance requires all applicable derived leaf results (C-205, C-206, C-207, C-208, C-209, C-210, C-211, E-132, E-138); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise complete command receipt, authentication failure, replayed sequence numbers, age greater than 30 seconds, and external control during a qualifying attempt.

**UnauthenticatedCommandRejection** — Commands failing authentication shall cause zero accepted actuator or mission-state changes. Verification uses the shared context of C-102.

**ReplayCommandRejection** — Commands with previously used sequence numbers shall cause zero accepted actuator or mission-state changes. Verification uses the shared context of C-102.

**ExpiredCommandRejection** — Commands older than 30 seconds shall cause zero accepted actuator or mission-state changes. Verification uses the shared context of C-102.

**AcceptedCommandDeadline** — An accepted abort or mode-change command shall be applied within 1 second of complete receipt. Verification uses the shared context of C-102.

**OnboardAcknowledgmentDeadline** — An accepted abort or mode-change command shall be acknowledged onboard within 1 second of complete receipt. Verification uses the shared context of C-102.

**AcknowledgmentQueueing** — An accepted command acknowledgment shall enter the transmit queue in the same command-processing cycle when a link is available. Verification uses the shared context of C-102.

**ExternalControlDisqualification** — Acceptance of external mission or steering control during a qualifying attempt shall permanently disqualify that attempt. Verification uses the shared context of C-102.

**CriticalEventRecording** — Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence. Verification uses the shared context of E-007.

**QualificationPersistence** — Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable. Verification uses the shared context of E-007.

## C-102 derivation 1

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
%% BlueDogViews::commandIntegrity1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 107 node(s) without a position, left undrawn, and 134 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**commandIntegrity : CommandIntegrity**`")
  n1("`*«requirement»*
**unauthenticatedCommandRejection : UnauthenticatedCommandRejection**`")
  n2("`*«requirement»*
**replayCommandRejection : ReplayCommandRejection**`")
  n3("`*«requirement»*
**expiredCommandRejection : ExpiredCommandRejection**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## C-102 derivation 2

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
%% BlueDogViews::commandIntegrity2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 107 node(s) without a position, left undrawn, and 134 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**commandIntegrity : CommandIntegrity**`")
  n1("`*«requirement»*
**acceptedCommandDeadline : AcceptedCommandDeadline**`")
  n2("`*«requirement»*
**onboardAcknowledgmentDeadline : OnboardAcknowledgmentDeadline**`")
  n3("`*«requirement»*
**acknowledgmentQueueing : AcknowledgmentQueueing**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## C-102 derivation 3

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
%% BlueDogViews::commandIntegrity3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 107 node(s) without a position, left undrawn, and 147 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**commandIntegrity : CommandIntegrity**`")
  n1("`*«requirement»*
**externalControlDisqualification : ExternalControlDisqualification**`")
  n2("`*«requirement»*
**criticalEventRecording : CriticalEventRecording**`")
  n3("`*«requirement»*
**qualificationPersistence : QualificationPersistence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```
