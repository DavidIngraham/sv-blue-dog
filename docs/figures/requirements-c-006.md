# C-006 emergency intervention

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**C-006 EmergencyIntervention** — The vessel shall permit remote emergency abort or manual control when a command link is available.

**E-005 Communications** — The vessel shall support live telemetry through link outages and reconnection.

**S-003 SafeRecovery** — The vessel shall support controlled emergency intervention and powered recovery.

**C-102 CommandIntegrity** — The vessel shall accept external commands only under the specified authentication, freshness and qualification rules.

## C-006 derivation 1

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
%% BlueDogViews::emergencyIntervention1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 217 node(s) without a position, left undrawn, and 427 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::emergencyIntervention : EmergencyIntervention**`")
  n1("`*«requirement»*
**BlueDogRequirements::communications : Communications**`")
  n2("`*«requirement»*
**BlueDogRequirements::safeRecovery : SafeRecovery**`")
  n3("`*«requirement»*
**BlueDogRequirements::commandIntegrity : CommandIntegrity**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n1
  n3 -.->|"derive"| n0
```

[Continue: E-005 communications](<requirements-e-005.md>)

[Continue: S-003 safe recovery](<requirements-s-003.md>)

[Continue: C-102 command integrity](<requirements-c-102.md>)
