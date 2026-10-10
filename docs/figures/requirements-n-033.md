# N-033 visibility

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**N-033 Visibility** — The vessel shall provide mode-appropriate navigation and traffic response across the specified visibility conditions.

**N-101 VisibilityNavigationCapability** — Navigation shall meet E-002 and E-008 acceptance criteria at visibility of at least 1 km in daylight and darkness.

**N-102 VisibilityTrafficCapability** — Traffic assessment shall meet the frozen S-001 criteria at visibility of at least 1 km in daylight and darkness.

**N-103 RestrictedVisibilityEntry** — On detecting visibility below 1 km, the vessel shall enter restricted-visibility state within 60 seconds.

**N-104 RestrictedVisibilityEvidence** — Restricted-visibility operation shall be recorded as outside the normal operational envelope.

**N-105 RestrictedVisibilityCollisionAssessment** — Collision assessment shall remain active during restricted-visibility operation.

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
%% not represented: 82 node(s) without a position, left undrawn, and 98 edge(s) at them
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
%% not represented: 83 node(s) without a position, left undrawn, and 99 edge(s) at them
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
