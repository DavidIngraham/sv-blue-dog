# R-002 recovery energy

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**R-002 RecoveryEnergy** — The protected reserve shall equal or exceed 1.2 × (30 minutes of worst-case recovery motor demand + 2 hours of essential recovery demand).

**R-003 LaunchEnergyAdmission** — Mission start shall remain inhibited unless a valid usable-energy estimate no older than 1 second strictly exceeds a valid R-002 protected reserve.

**E-201 SustainedReserveProtection** — Conservative stored energy shall remain strictly above the R-002 protected reserve throughout the selected sustained-operation profile.

## R-002 derivation 1

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
%% BlueDogViews::recoveryEnergy1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 69 node(s) without a position, left undrawn, and 80 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**recoveryEnergy : RecoveryEnergy**`")
  n1("`*«requirement»*
**launchEnergyAdmission : LaunchEnergyAdmission**`")
  n2("`*«requirement»*
**sustainedReserveProtection : SustainedReserveProtection**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
