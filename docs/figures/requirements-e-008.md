# E-008 navigation availability

[All requirement views](<../requirements-views.md>)

**NavigationAvailability** — Aggregate requirement for NavigationAvailability. Acceptance requires all applicable derived leaf results (E-140, E-141, E-142, E-143, E-132); this parent has no independent executable pass/fail predicate. Shared verification context: Campaigns use 1800 scheduled one-second epochs in 30 minutes, with missing/invalid epochs counted as failures. Fault injection is separate.

**NavigationValidEpochs** — In each E-008 campaign, at least 1710 of 1800 scheduled epochs shall contain valid position and heading observations. Verification uses the shared context of E-008.

**StaleNavigationInvalidation** — Navigation observations older than 5 seconds shall be marked invalid. Verification uses the shared context of E-008.

**NavigationDegradedTransition** — When position or heading becomes invalid due to age, the vessel shall enter navigation-degraded state within 1 second. Verification uses the shared context of E-008.

**StaleNavigationUseInhibition** — The controller shall not use observations marked invalid as current navigation inputs. Verification uses the shared context of E-008.

**CriticalEventRecording** — Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence. Verification uses the shared context of E-007.

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
%% not represented: 78 node(s) without a position, left undrawn, and 84 edge(s) at them
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
%% not represented: 120 node(s) without a position, left undrawn, and 154 edge(s) at them
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
