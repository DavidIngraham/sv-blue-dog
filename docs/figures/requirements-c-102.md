# C-102 command integrity

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**C-102 CommandIntegrity** — The vessel shall accept external commands only under the specified authentication, freshness and qualification rules.

**C-205 UnauthenticatedCommandRejection** — Commands failing authentication shall cause zero accepted actuator or mission-state changes.

**C-206 ReplayCommandRejection** — Commands with previously used sequence numbers shall cause zero accepted actuator or mission-state changes.

**C-207 ExpiredCommandRejection** — Commands older than 30 seconds shall cause zero accepted actuator or mission-state changes.

**C-208 AcceptedCommandDeadline** — An accepted abort or mode-change command shall be applied within 1 second of complete receipt.

**C-209 OnboardAcknowledgmentDeadline** — An accepted abort or mode-change command shall be acknowledged onboard within 1 second of complete receipt.

**C-210 AcknowledgmentQueueing** — An accepted command acknowledgment shall enter the transmit queue in the same command-processing cycle when a link is available.

**C-211 ExternalControlDisqualification** — Acceptance of external mission or steering control during a qualifying attempt shall permanently disqualify that attempt.

**E-132 CriticalEventRecording** — Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence.

**E-138 QualificationPersistence** — Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable.

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
%% not represented: 116 node(s) without a position, left undrawn, and 166 edge(s) at them
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
%% not represented: 116 node(s) without a position, left undrawn, and 166 edge(s) at them
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
%% not represented: 124 node(s) without a position, left undrawn, and 194 edge(s) at them
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
