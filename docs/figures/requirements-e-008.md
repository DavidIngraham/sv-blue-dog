# E-008 navigation availability

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**E-008 NavigationAvailability** — The vessel shall maintain valid navigation inputs and reject stale observations.

**E-140 NavigationValidEpochs** — In each E-008 campaign, at least 1710 of 1800 scheduled epochs shall contain valid position and heading observations.

**E-141 StaleNavigationInvalidation** — Navigation observations older than 5 seconds shall be marked invalid.

**E-142 NavigationDegradedTransition** — When position or heading becomes invalid due to age, the vessel shall enter navigation-degraded state within 1 second.

**E-143 StaleNavigationUseInhibition** — The controller shall not use observations marked invalid as current navigation inputs.

**E-132 CriticalEventRecording** — Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence.

## E-008 derivation 1

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
%% BlueDogViews::navigationAvailability1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 121 node(s) without a position, left undrawn, and 160 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**navigationAvailability : NavigationAvailability**`")
  n1("`*«requirement»*
**navigationValidEpochs : NavigationValidEpochs**`")
  n2("`*«requirement»*
**staleNavigationInvalidation : StaleNavigationInvalidation**`")
  n3("`*«requirement»*
**navigationDegradedTransition : NavigationDegradedTransition**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-008 derivation 2

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
%% BlueDogViews::navigationAvailability2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 130 node(s) without a position, left undrawn, and 190 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**navigationAvailability : NavigationAvailability**`")
  n1("`*«requirement»*
**staleNavigationUseInhibition : StaleNavigationUseInhibition**`")
  n2("`*«requirement»*
**criticalEventRecording : CriticalEventRecording**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
