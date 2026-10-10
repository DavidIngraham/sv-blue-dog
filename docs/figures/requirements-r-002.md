# R-002 recovery energy

[All requirement views](<../requirements-views.md>)

**RecoveryEnergy** — The protected recovery reserve shall be at least 1.2 times the sum of 30 minutes of worst-case electrical motor power measured in the R-001 recovery test and 2 hours of essential navigation/control/recording/telemetry electrical power measured at the S-003 recovery cadence. Motor and essential powers shall be separate, non-overlapping measurements. Reserve sizing shall use the selected installed configuration; available battery energy shall be characterized at the lowest operating battery temperature and end-of-service capacity. Launch admission is R-003; in-mission reserve crossing invokes E-004.

**LaunchEnergyAdmission** — The vessel shall inhibit mission start unless the conservative usable battery-energy estimate is strictly greater than the protected reserve sized under R-002. A missing, stale or invalid energy estimate or reserve configuration shall inhibit start. The estimate shall be no older than 1 second at admission. Acceptance shall inject values below, equal to and above the reserve and missing/invalid/stale inputs.

**SustainedReserveProtection** — Conservative stored energy shall remain strictly above the R-002 protected reserve throughout the selected sustained-operation profile. For piecewise-constant net power, check the initial state and every interval endpoint; unmodeled intrainterval dips are outside this claim.

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
%% not represented: 66 node(s) without a position, left undrawn, and 77 edge(s) at them
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
