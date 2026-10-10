# R-001 recovery propulsion

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**R-001 RecoveryPropulsion** — At maximum mission load, powered recovery shall sustain at least 0.5 m/s over ground for 30 minutes against a 1.5 m/s current.

**R-002 RecoveryEnergy** — The protected reserve shall equal or exceed 1.2 × (30 minutes of worst-case recovery motor demand + 2 hours of essential recovery demand).

**N-056 RecoveryPropulsorWeeds** — The recovery propulsion system shall tolerate the specified weed encounters within its rated electrical and thermal limits.

## R-001 derivation 1

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
%% BlueDogViews::recoveryPropulsion1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 127 node(s) without a position, left undrawn, and 177 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**recoveryPropulsion : RecoveryPropulsion**`")
  n1("`*«requirement»*
**recoveryEnergy : RecoveryEnergy**`")
  n2("`*«requirement»*
**recoveryPropulsorWeeds : RecoveryPropulsorWeeds**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```

[Continue: R-002 recovery energy](<requirements-r-002.md>)

[Continue: N-056 recovery propulsor weeds](<requirements-n-056.md>)
