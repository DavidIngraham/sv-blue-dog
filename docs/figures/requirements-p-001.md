# P-001 transportability

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**P-001 Transportability** — The vessel shall support transport, assembly, launch and retrieval by one adult under the specified handling conditions.

**P-101 SoloTransport** — One adult shall move all mission equipment 100 m without assistance.

**P-102 LiftMass** — Each separately lifted assembly shall have a mass no greater than 15 kg.

**P-103 SetupDuration** — One adult shall assemble the vessel from its transport configuration within 30 minutes.

**P-104 PackDuration** — One adult shall pack the vessel into its transport configuration within 30 minutes.

**P-105 SoloLaunch** — One adult shall launch the assembled vessel without assistance.

**P-106 SoloRetrieval** — One adult shall retrieve the vessel from the water without assistance.

## P-001 derivation 1

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
%% BlueDogViews::transportability1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 158 node(s) without a position, left undrawn, and 253 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**transportability : Transportability**`")
  n1("`*«requirement»*
**soloTransport : SoloTransport**`")
  n2("`*«requirement»*
**liftMass : LiftMass**`")
  n3("`*«requirement»*
**setupDuration : SetupDuration**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## P-001 derivation 2

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
%% BlueDogViews::transportability2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 158 node(s) without a position, left undrawn, and 253 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**transportability : Transportability**`")
  n1("`*«requirement»*
**packDuration : PackDuration**`")
  n2("`*«requirement»*
**soloLaunch : SoloLaunch**`")
  n3("`*«requirement»*
**soloRetrieval : SoloRetrieval**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```
