# N-056 recovery propulsor weeds

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**N-056 RecoveryPropulsorWeeds** — The recovery propulsion system shall tolerate the specified weed encounters within its rated electrical and thermal limits.

**N-133 PoweredWeedSpeed** — Mean water-relative powered speed through each N-056 patch passage shall be at least 50 percent of weed-free reference speed.

**N-134 PoweredWeedCurrent** — Motor and controller currents shall remain within their respective rated limits during each N-056 patch passage.

**N-135 PoweredWeedTemperature** — Motor and controller temperatures shall remain within their respective rated limits during each N-056 patch passage.

**N-136 LockedPropulsorShutdown** — A locked propulsor shall cause motor shutdown within 2 seconds.

**R-101 MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown.

## N-056 derivation 1

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
%% BlueDogViews::recoveryPropulsorWeeds1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 107 node(s) without a position, left undrawn, and 149 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**recoveryPropulsorWeeds : RecoveryPropulsorWeeds**`")
  n1("`*«requirement»*
**poweredWeedSpeed : PoweredWeedSpeed**`")
  n2("`*«requirement»*
**poweredWeedCurrent : PoweredWeedCurrent**`")
  n3("`*«requirement»*
**poweredWeedTemperature : PoweredWeedTemperature**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-056 derivation 2

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
%% BlueDogViews::recoveryPropulsorWeeds2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 114 node(s) without a position, left undrawn, and 161 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**recoveryPropulsorWeeds : RecoveryPropulsorWeeds**`")
  n1("`*«requirement»*
**lockedPropulsorShutdown : LockedPropulsorShutdown**`")
  n2("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
