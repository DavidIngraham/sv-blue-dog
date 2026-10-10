# N-052 capsize control recovery

[All requirement views](<../requirements-views.md>)

**CapsizeControlRecovery** — Aggregate requirement for CapsizeControlRecovery. Acceptance requires all applicable derived leaf results (N-122, N-123, N-124, N-125); this parent has no independent executable pass/fail predicate. Shared verification context: Apply to every N-051 release without operator input. Mode-appropriate control does not mean normal sailing before the N-035 resumption gate permits it.

**ControlRecoveryDeadline** — The vessel shall restore mode-appropriate autonomous sail/steering control within 120 seconds from each N-051 release. Verification uses the shared context of N-052.

**CapsizeGateProgressRetention** — Gate progress shall be preserved through every N-051 release. Verification uses the shared context of N-052.

**CapsizeQualificationRetention** — Qualification status shall be preserved through every N-051 release absent an independently disqualifying event. Verification uses the shared context of N-052.

**CapsizeRestrictionRetention** — Control restoration after each N-051 release shall preserve every active survival, low-energy, recovery and motor-inhibition restriction. Verification uses the shared context of N-052.

## N-052 derivation 1

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
%% BlueDogViews::capsizeControlRecovery1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 63 node(s) without a position, left undrawn, and 81 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**capsizeControlRecovery : CapsizeControlRecovery**`")
  n1("`*«requirement»*
**controlRecoveryDeadline : ControlRecoveryDeadline**`")
  n2("`*«requirement»*
**capsizeGateProgressRetention : CapsizeGateProgressRetention**`")
  n3("`*«requirement»*
**capsizeQualificationRetention : CapsizeQualificationRetention**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-052 derivation 2

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
%% BlueDogViews::capsizeControlRecovery2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 65 node(s) without a position, left undrawn, and 83 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**capsizeControlRecovery : CapsizeControlRecovery**`")
  n1("`*«requirement»*
**capsizeRestrictionRetention : CapsizeRestrictionRetention**`")
  n1 -.->|"derive"| n0
```
