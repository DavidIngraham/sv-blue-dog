# N-003 StabilityAndFouling relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**N-003 StabilityAndFouling** — The vessel shall autonomously tolerate capsize and submerged aquatic vegetation, including milfoil-like stems.

**N-051 SelfRighting** — The vessel shall recover from the specified capsize releases without external assistance or motor thrust.

**N-052 CapsizeControlRecovery** — The vessel shall restore mode-appropriate control after each specified capsize release.

**N-053 SubmergedWeedPassage** — The vessel shall tolerate submerged milfoil-like vegetation during the specified unassisted Gorge sailing passes.

**N-054 WeedSnagShedding** — The vessel shall recover sailing performance after the specified appendage weed snags without assistance or motor use.

**N-055 WeedBlockageResponse** — The vessel shall enter autonomous fouling contingency when the defined weed-blockage trigger occurs.

**N-056 RecoveryPropulsorWeeds** — The recovery propulsion system shall tolerate the specified weed encounters within its rated electrical and thermal limits.

## N-003 relationships 1

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
%% BlueDogViews::stabilityAndFouling1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 79 node(s) without a position, left undrawn, and 108 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**stabilityAndFouling : StabilityAndFouling**`")
  n1("`*«requirement»*
**selfRighting : SelfRighting**`")
  n2("`*«requirement»*
**capsizeControlRecovery : CapsizeControlRecovery**`")
  n3("`*«requirement»*
**submergedWeedPassage : SubmergedWeedPassage**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-003 relationships 2

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
%% BlueDogViews::stabilityAndFouling2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 125 node(s) without a position, left undrawn, and 188 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**stabilityAndFouling : StabilityAndFouling**`")
  n1("`*«requirement»*
**weedSnagShedding : WeedSnagShedding**`")
  n2("`*«requirement»*
**weedBlockageResponse : WeedBlockageResponse**`")
  n3("`*«requirement»*
**recoveryPropulsorWeeds : RecoveryPropulsorWeeds**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

[Continue: N-051 SelfRighting](<requirements-n-051.md>)

[Continue: N-052 CapsizeControlRecovery](<requirements-n-052.md>)

[Continue: N-053 SubmergedWeedPassage](<requirements-n-053.md>)

[Continue: N-054 WeedSnagShedding](<requirements-n-054.md>)

[Continue: N-055 WeedBlockageResponse](<requirements-n-055.md>)

[Continue: N-056 RecoveryPropulsorWeeds](<requirements-n-056.md>)
