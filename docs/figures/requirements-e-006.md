# E-006 IngressResponse relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**E-006 IngressResponse** — The vessel shall retain recoverability during the specified hull-ingress qualification.

**E-125 IngressDetection** — In the E-006 injection test, ingress detection shall occur within 60 seconds of injection starting.

**E-126 IngressRecoveryRequest** — In the E-006 test, ingress detection shall set the recovery-request state.

**E-127 IngressFlotation** — In the E-006 test, the vessel shall remain afloat for the full 30 minutes.

**E-128 IngressElectronicsProtection** — After the E-006 test, enclosed-electronics water-sensitive indicators shall show no liquid ingress.

**E-129 IngressPositionContinuity** — Throughout the E-006 test with a functioning link, position reporting shall meet the active TelemetryDeliveryCadence.

**E-144 IngressEventDeadline** — In the E-006 injection test, an ingress event record shall exist within 60 seconds of injection starting.

**E-132 CriticalEventRecording** — Every external-command disposition, reset, motor-enable transition, ingress detection, recovery request, navigation-degraded transition, low-energy flag transition and qualification change shall have an event record regardless of periodic cadence.

**R-101 MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown.

## E-006 relationships 1

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
%% BlueDogViews::ingressResponse1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 121 node(s) without a position, left undrawn, and 178 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**ingressResponse : IngressResponse**`")
  n1("`*«requirement»*
**ingressDetection : IngressDetection**`")
  n2("`*«requirement»*
**ingressRecoveryRequest : IngressRecoveryRequest**`")
  n3("`*«requirement»*
**ingressFlotation : IngressFlotation**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-006 relationships 2

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
%% BlueDogViews::ingressResponse2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 121 node(s) without a position, left undrawn, and 178 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**ingressResponse : IngressResponse**`")
  n1("`*«requirement»*
**ingressElectronicsProtection : IngressElectronicsProtection**`")
  n2("`*«requirement»*
**ingressPositionContinuity : IngressPositionContinuity**`")
  n3("`*«requirement»*
**ingressEventDeadline : IngressEventDeadline**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-006 relationships 3

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
%% BlueDogViews::ingressResponse3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 124 node(s) without a position, left undrawn, and 182 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**ingressResponse : IngressResponse**`")
  n1("`*«requirement»*
**criticalEventRecording : CriticalEventRecording**`")
  n2("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
