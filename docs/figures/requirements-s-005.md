# S-005 regulatory classification

[All requirement views](<../requirements-views.md>)

**RegulatoryClassification** — Aggregate requirement for RegulatoryClassification. Acceptance requires all applicable derived leaf results (S-122, S-123); this parent has no independent executable pass/fail predicate. Shared verification context: Acceptance is deployment document review, not onboard behavior or an assertion of buoy status.

**DeploymentComplianceRecord** — Each deployment shall have a dated compliance record identifying the craft, dimensions, waters, operating modes, applicable navigation and radio obligations, and permission evidence. Verification uses the shared context of S-005.

**DeploymentReleaseGate** — Deployment release shall be withheld while any mandatory authorization is absent, expired or unresolved. Verification uses the shared context of S-005.

## S-005 derivation 1

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
%% BlueDogViews::regulatoryClassification1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 149 node(s) without a position, left undrawn, and 230 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**regulatoryClassification : RegulatoryClassification**`")
  n1("`*«requirement»*
**deploymentComplianceRecord : DeploymentComplianceRecord**`")
  n2("`*«requirement»*
**deploymentReleaseGate : DeploymentReleaseGate**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
