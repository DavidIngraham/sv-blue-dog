# S-004 navigation conspicuity

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**S-004 NavigationConspicuity** — The vessel shall present the navigation signals required for its operating mode.

**S-116 NavigationLightPresentation** — The vessel shall present the lights prescribed for its current mode by the S-004 compliance matrix without a person aboard.

**S-117 NavigationShapePresentation** — The vessel shall present the shapes prescribed for its current mode by the S-004 compliance matrix without a person aboard.

**S-118 NavigationSoundPresentation** — The vessel shall present the sound signals prescribed for its current mode by the S-004 compliance matrix without a person aboard.

**S-119 SignalingModeDeadline** — A commanded mode change shall select the corresponding signaling configuration within 1 second.

**S-120 SignalingFaultRecording** — Each detectable signaling failure shall be logged within 5 seconds of detection.

**S-121 SignalingFaultReporting** — With a functioning link, each detected signaling failure shall be reported to shore within 5 seconds.

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
%% not represented: 74 node(s) without a position, left undrawn, and 86 edge(s) at them
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
%% not represented: 74 node(s) without a position, left undrawn, and 86 edge(s) at them
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
