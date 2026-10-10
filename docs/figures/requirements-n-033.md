# N-033 visibility

[All requirement views](<../requirements-views.md>)

**Visibility** — Aggregate requirement for Visibility. Acceptance requires all applicable derived leaf results (N-101, N-102, N-103, N-104, N-105); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise daylight and darkness at meteorological visibility of at least 1 km, and detected visibility below 1 km. Traffic performance remains subject to unresolved S-001 scenarios.

**VisibilityNavigationCapability** — Navigation shall meet E-002 and E-008 acceptance criteria at visibility of at least 1 km in daylight and darkness. Verification uses the shared context of N-033.

**VisibilityTrafficCapability** — Traffic assessment shall meet the frozen S-001 criteria at visibility of at least 1 km in daylight and darkness. Verification uses the shared context of N-033.

**RestrictedVisibilityEntry** — On detecting visibility below 1 km, the vessel shall enter restricted-visibility state within 60 seconds. Verification uses the shared context of N-033.

**RestrictedVisibilityEvidence** — Restricted-visibility operation shall be recorded as outside the normal operational envelope. Verification uses the shared context of N-033.

**RestrictedVisibilityCollisionAssessment** — Collision assessment shall remain active during restricted-visibility operation. Verification uses the shared context of N-033.

## N-033 derivation 1

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
%% BlueDogViews::visibility1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 75 node(s) without a position, left undrawn, and 86 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**visibility : Visibility**`")
  n1("`*«requirement»*
**visibilityNavigationCapability : VisibilityNavigationCapability**`")
  n2("`*«requirement»*
**visibilityTrafficCapability : VisibilityTrafficCapability**`")
  n3("`*«requirement»*
**restrictedVisibilityEntry : RestrictedVisibilityEntry**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-033 derivation 2

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
%% BlueDogViews::visibility2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 76 node(s) without a position, left undrawn, and 87 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**visibility : Visibility**`")
  n1("`*«requirement»*
**restrictedVisibilityEvidence : RestrictedVisibilityEvidence**`")
  n2("`*«requirement»*
**restrictedVisibilityCollisionAssessment : RestrictedVisibilityCollisionAssessment**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
