# N-035 envelope transition

[All requirement views](<../requirements-views.md>)

**EnvelopeTransition** — Aggregate requirement for EnvelopeTransition. Acceptance requires all applicable derived leaf results (N-106, N-107, N-108, N-109, N-110, E-130, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: The trigger is a detected upper operational wind or wave limit exceedance for the selected profile; calm invokes N-034. Resumption eligibility requires 10 continuous minutes inside the selected wind/wave limits, valid navigation and no low-energy, emergency-recovery or isolation restriction.

**SurvivalEntryDeadline** — The vessel shall enter survival mode within 60 seconds of the N-035 upper-limit trigger. Verification uses the shared context of N-035.

**SurvivalTransitionRecording** — Every survival-mode entry shall have a corresponding event record. Verification uses the shared context of N-035.

**SailingResumptionDeadline** — Full autonomous sailing shall resume within 5 minutes of N-035 resumption eligibility becoming continuously true. Verification uses the shared context of N-035.

**SailingResumptionInhibition** — Full autonomous sailing shall remain inhibited while N-035 resumption eligibility is false. Verification uses the shared context of N-035.

**ResumptionBlockEvidence** — Every blocked sailing-resumption attempt shall record the blocking condition. Verification uses the shared context of N-035.

**PeriodicLogCadence** — Periodic mission records shall be acquired at least once per second normally and once per minute in low-energy or survival operation. Verification uses the shared context of E-007.

**MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown. Verification uses the shared context of R-004.

## N-035 derivation 1

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
%% BlueDogViews::envelopeTransition1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 68 node(s) without a position, left undrawn, and 75 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**envelopeTransition : EnvelopeTransition**`")
  n1("`*«requirement»*
**survivalEntryDeadline : SurvivalEntryDeadline**`")
  n2("`*«requirement»*
**survivalTransitionRecording : SurvivalTransitionRecording**`")
  n3("`*«requirement»*
**sailingResumptionDeadline : SailingResumptionDeadline**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-035 derivation 2

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
%% BlueDogViews::envelopeTransition2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 101 node(s) without a position, left undrawn, and 136 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**envelopeTransition : EnvelopeTransition**`")
  n1("`*«requirement»*
**sailingResumptionInhibition : SailingResumptionInhibition**`")
  n2("`*«requirement»*
**resumptionBlockEvidence : ResumptionBlockEvidence**`")
  n3("`*«requirement»*
**periodicLogCadence : PeriodicLogCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-035 derivation 3

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
%% BlueDogViews::envelopeTransition3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 95 node(s) without a position, left undrawn, and 115 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**envelopeTransition : EnvelopeTransition**`")
  n1("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n1 -.->|"derive"| n0
```
