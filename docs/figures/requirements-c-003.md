# C-003 unassisted attempt

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**C-003 UnassistedAttempt** — A qualifying attempt shall complete the round trip without operator intervention.

**E-002 NavigationAndControl** — The vessel shall provide autonomous navigation and sail/steering control within the selected operational profile.

**R-004 ChallengeMotorInhibition** — The vessel shall prevent motor propulsion from qualifying as unassisted sailing.

**C-102 CommandIntegrity** — The vessel shall accept external commands only under the specified authentication, freshness and qualification rules.

## C-003 derivation 1

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
%% BlueDogViews::unassistedAttempt1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 230 node(s) without a position, left undrawn, and 450 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::unassistedAttempt : UnassistedAttempt**`")
  n1("`*«requirement»*
**BlueDogRequirements::navigationAndControl : NavigationAndControl**`")
  n2("`*«requirement»*
**BlueDogRequirements::challengeMotorInhibition : ChallengeMotorInhibition**`")
  n3("`*«requirement»*
**BlueDogRequirements::commandIntegrity : CommandIntegrity**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

[Continue: E-002 navigation and control](<requirements-e-002.md>)

[Continue: R-004 challenge motor inhibition](<requirements-r-004.md>)

[Continue: C-102 command integrity](<requirements-c-102.md>)
