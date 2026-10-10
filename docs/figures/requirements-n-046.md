# N-046 solar heating

[All requirement views](<../requirements-views.md>)

**SolarHeating** — Aggregate requirement for SolarHeating. Acceptance requires all applicable derived leaf results (N-115, N-116, N-117); this parent has no independent executable pass/fail predicate. Shared verification context: Expose the powered vessel to 40 degC ambient air and 1000 W/m2 incident solar irradiance for 8 hours; use the installed battery manufacturer temperature limits.

**HotSunElectronicsOperation** — Powered electronics shall retain operational functions throughout the N-046 exposure. Verification uses the shared context of N-046.

**HotSunBatteryTemperature** — Battery temperatures shall remain within manufacturer operating limits throughout the N-046 exposure. Verification uses the shared context of N-046.

**BatteryChargeTemperatureInhibition** — Battery charging shall remain inhibited whenever measured battery temperature is outside the manufacturer permitted charge range. Verification uses the shared context of N-046.

## N-046 derivation 1

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
%% BlueDogViews::solarHeating1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 56 node(s) without a position, left undrawn, and 58 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**solarHeating : SolarHeating**`")
  n1("`*«requirement»*
**hotSunElectronicsOperation : HotSunElectronicsOperation**`")
  n2("`*«requirement»*
**hotSunBatteryTemperature : HotSunBatteryTemperature**`")
  n3("`*«requirement»*
**batteryChargeTemperatureInhibition : BatteryChargeTemperatureInhibition**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```
