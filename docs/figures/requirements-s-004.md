# S-004 navigation conspicuity

[All requirement views](<../requirements-views.md>)

**NavigationConspicuity** — Aggregate requirement for NavigationConspicuity. Acceptance requires all applicable derived leaf results (S-116, S-117, S-118, S-119, S-120, S-121); this parent has no independent executable pass/fail predicate. Shared verification context: Use the deployment-specific compliance matrix for sailing, powered-recovery and stationary modes, including its visibility, arcs, colors and sound criteria. The matrix remains a deployment hold point under S-005.

**NavigationLightPresentation** — The vessel shall present the lights prescribed for its current mode by the S-004 compliance matrix without a person aboard. Verification uses the shared context of S-004.

**NavigationShapePresentation** — The vessel shall present the shapes prescribed for its current mode by the S-004 compliance matrix without a person aboard. Verification uses the shared context of S-004.

**NavigationSoundPresentation** — The vessel shall present the sound signals prescribed for its current mode by the S-004 compliance matrix without a person aboard. Verification uses the shared context of S-004.

**SignalingModeDeadline** — A commanded mode change shall select the corresponding signaling configuration within 1 second. Verification uses the shared context of S-004.

**SignalingFaultRecording** — Each detectable signaling failure shall be logged within 5 seconds of detection. Verification uses the shared context of S-004.

**SignalingFaultReporting** — With a functioning link, each detected signaling failure shall be reported to shore within 5 seconds. Verification uses the shared context of S-004.

## S-004 derivation 1

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
%% BlueDogViews::navigationConspicuity1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 67 node(s) without a position, left undrawn, and 73 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**navigationConspicuity : NavigationConspicuity**`")
  n1("`*«requirement»*
**navigationLightPresentation : NavigationLightPresentation**`")
  n2("`*«requirement»*
**navigationShapePresentation : NavigationShapePresentation**`")
  n3("`*«requirement»*
**navigationSoundPresentation : NavigationSoundPresentation**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-004 derivation 2

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
%% BlueDogViews::navigationConspicuity2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 67 node(s) without a position, left undrawn, and 73 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**navigationConspicuity : NavigationConspicuity**`")
  n1("`*«requirement»*
**signalingModeDeadline : SignalingModeDeadline**`")
  n2("`*«requirement»*
**signalingFaultRecording : SignalingFaultRecording**`")
  n3("`*«requirement»*
**signalingFaultReporting : SignalingFaultReporting**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```
