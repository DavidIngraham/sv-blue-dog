# R-004 challenge motor inhibition

[All requirement views](<../requirements-views.md>)

**ChallengeMotorInhibition** — Aggregate requirement for ChallengeMotorInhibition. Acceptance requires all applicable derived leaf results (R-101, R-102, E-138, E-132); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise qualifying, nonqualifying and unknown qualification states, restart, link loss, power loss during transitions and conflicting/stale commands. Shared qualification persistence applies before enabling intervention.

**MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown. Verification uses the shared context of R-004.

**FreshRecoveryCommand** — After restart, motor enable shall remain inhibited until a fresh authenticated recovery command is accepted. Verification uses the shared context of R-004.

**QualificationPersistence** — Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable. Verification uses the shared context of E-007.

**CriticalEventRecording** — Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence. Verification uses the shared context of E-007.

## R-004 derivation 1

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
%% BlueDogViews::challengeMotorInhibition1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 97 node(s) without a position, left undrawn, and 126 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**challengeMotorInhibition : ChallengeMotorInhibition**`")
  n1("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n2("`*«requirement»*
**freshRecoveryCommand : FreshRecoveryCommand**`")
  n3("`*«requirement»*
**qualificationPersistence : QualificationPersistence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## R-004 derivation 2

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
%% BlueDogViews::challengeMotorInhibition2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 99 node(s) without a position, left undrawn, and 136 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**challengeMotorInhibition : ChallengeMotorInhibition**`")
  n1("`*«requirement»*
**criticalEventRecording : CriticalEventRecording**`")
  n1 -.->|"derive"| n0
```
