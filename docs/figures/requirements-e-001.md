# E-001 energy awareness

[All requirement views](<../requirements-views.md>)

**EnergyAwareness** — Aggregate requirement for EnergyAwareness. Acceptance requires all applicable derived leaf results (E-101, E-102, E-103, E-104); this parent has no independent executable pass/fail predicate. Shared verification context: Energy estimation and conservative decision inputs; accuracy uses calibrated energy integration across operating battery temperatures.

**LowEnergyRecovery** — Aggregate requirement for LowEnergyRecovery. Acceptance requires all applicable derived leaf results (E-114, E-115, E-116, E-117, E-118, E-119, E-130, E-120, E-132, R-101); this parent has no independent executable pass/fail predicate. Shared verification context: Reserve means R-002. Emergency/recovery cadence takes precedence; clearing low-energy state is independent of other modes, while payload enabling respects all restrictions.

**EnergyEstimateCadence** — The vessel shall refresh usable battery-energy estimates at least once per second. Verification uses the shared context of E-001.

**ReserveEstimateCadence** — The vessel shall refresh protected recovery-reserve estimates at least once per second. Verification uses the shared context of E-001.

**EnergyEstimateAccuracy** — Usable-energy estimation error shall not exceed 10 percent of measured usable full-charge energy relative to calibrated charge/discharge integration across operating battery temperatures. Verification uses the shared context of E-001.

**ConservativeEnergyEstimate** — The usable-energy input to admission and low-energy decisions shall equal estimated usable energy minus the EnergyEstimateAccuracy error allowance. Verification uses the shared context of E-001.

## E-001 derivation 1

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
%% BlueDogViews::energyAwareness1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 109 node(s) without a position, left undrawn, and 128 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**energyAwareness : EnergyAwareness**`")
  n1("`*«requirement»*
**lowEnergyRecovery : LowEnergyRecovery**`")
  n2("`*«requirement»*
**energyEstimateCadence : EnergyEstimateCadence**`")
  n3("`*«requirement»*
**reserveEstimateCadence : ReserveEstimateCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## E-001 derivation 2

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
%% BlueDogViews::energyAwareness2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 110 node(s) without a position, left undrawn, and 129 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**energyAwareness : EnergyAwareness**`")
  n1("`*«requirement»*
**energyEstimateAccuracy : EnergyEstimateAccuracy**`")
  n2("`*«requirement»*
**conservativeEnergyEstimate : ConservativeEnergyEstimate**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```

[Continue: E-004 low energy recovery](<requirements-e-004.md>)
