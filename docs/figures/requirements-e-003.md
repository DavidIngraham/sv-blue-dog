# E-003 reset recovery

[All requirement views](<../requirements-views.md>)

**ResetRecovery** — Aggregate requirement for ResetRecovery. Acceptance requires all applicable derived leaf results (E-110, E-111, E-112, E-113, E-145, E-136, E-139, E-138, R-102, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: Watchdog-reset tests start above protected reserve with valid navigation observations. Normal sailing remains subject to N-035; data and qualification persistence have shared leaf criteria.

**RestartDeadline** — After a watchdog reset under E-003 preconditions, the vessel shall restore mode-appropriate autonomous control within 30 seconds. Verification uses the shared context of E-003.

**MissionStateRestoration** — Within 30 seconds after a watchdog reset under E-003 preconditions, restored mission mode shall equal the last persisted mode. Verification uses the shared context of E-003.

**GateProgressRestoration** — Within 30 seconds after a watchdog reset under E-003 preconditions, restored gate progress shall equal the last persisted gate progress. Verification uses the shared context of E-003.

**ResetRestrictionPreservation** — After watchdog reset, each active survival, low-energy, recovery and isolation restriction shall remain effective until its own release condition is met. Verification uses the shared context of E-003.

**QualificationRestoration** — Within 30 seconds after a watchdog reset under E-003 preconditions, qualification status shall equal the valid persisted status, or be nonqualifying when persisted status is absent or inconsistent. Verification uses the shared context of E-003.

**LogInterruptionDurability** — After watchdog reset or abrupt power removal, every record older than 5 seconds before interruption shall remain readable. Verification uses the shared context of E-007.

**UnknownQualificationFallback** — On restart with absent or inconsistent persisted qualification state, the vessel shall adopt nonqualifying status. Verification uses the shared context of E-007.

**QualificationPersistence** — Each disqualifying transition shall be durably stored before its associated commanded intervention or motor enable. Verification uses the shared context of E-007.

**FreshRecoveryCommand** — After restart, motor enable shall remain inhibited until a fresh authenticated recovery command is accepted. Verification uses the shared context of R-004.

**MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown. Verification uses the shared context of R-004.

## E-003 derivation 1

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
%% BlueDogViews::resetRecovery1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 194 node(s) without a position, left undrawn, and 346 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**resetRecovery : ResetRecovery**`")
  n1("`*«requirement»*
**restartDeadline : RestartDeadline**`")
  n2("`*«requirement»*
**missionStateRestoration : MissionStateRestoration**`")
  n3("`*«requirement»*
**gateProgressRestoration : GateProgressRestoration**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-003 derivation 2

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
%% BlueDogViews::resetRecovery2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 194 node(s) without a position, left undrawn, and 346 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**resetRecovery : ResetRecovery**`")
  n1("`*«requirement»*
**resetRestrictionPreservation : ResetRestrictionPreservation**`")
  n2("`*«requirement»*
**qualificationRestoration : QualificationRestoration**`")
  n3("`*«requirement»*
**logInterruptionDurability : LogInterruptionDurability**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-003 derivation 3

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
%% BlueDogViews::resetRecovery3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 194 node(s) without a position, left undrawn, and 347 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**resetRecovery : ResetRecovery**`")
  n1("`*«requirement»*
**unknownQualificationFallback : UnknownQualificationFallback**`")
  n2("`*«requirement»*
**qualificationPersistence : QualificationPersistence**`")
  n3("`*«requirement»*
**freshRecoveryCommand : FreshRecoveryCommand**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-003 derivation 4

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
%% BlueDogViews::resetRecovery4 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 196 node(s) without a position, left undrawn, and 350 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**resetRecovery : ResetRecovery**`")
  n1("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n1 -.->|"derive"| n0
```
