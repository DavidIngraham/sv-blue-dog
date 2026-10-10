# N-054 weed snag shedding

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**N-054 WeedSnagShedding** — The vessel shall recover sailing performance after the specified appendage weed snags without assistance or motor use.

**N-128 WeedSnagSpeedRecovery** — Within 5 minutes of each N-054 snag, water-relative sailing speed shall recover to at least 50 percent of unobstructed reference speed.

**N-129 WeedSnagSteeringRecovery** — Within 5 minutes of each N-054 snag, full commanded rudder travel shall be regained.

## N-054 derivation 1

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
%% BlueDogViews::weedSnagShedding1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 65 node(s) without a position, left undrawn, and 77 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**weedSnagShedding : WeedSnagShedding**`")
  n1("`*«requirement»*
**weedSnagSpeedRecovery : WeedSnagSpeedRecovery**`")
  n2("`*«requirement»*
**weedSnagSteeringRecovery : WeedSnagSteeringRecovery**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
