# N-053 submerged weed passage

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**N-053 SubmergedWeedPassage** — The vessel shall tolerate submerged milfoil-like vegetation during the specified unassisted Gorge sailing passes.

**N-126 WeedPassageSpeed** — During each N-053 patch passage, mean water-relative sailing speed shall be at least 50 percent of the weed-free reference speed.

**N-127 WeedPassageSteering** — After each N-053 patch passage, full commanded rudder travel shall be regained within 5 minutes.

## N-053 derivation 1

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
%% BlueDogViews::submergedWeedPassage1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 66 node(s) without a position, left undrawn, and 82 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**submergedWeedPassage : SubmergedWeedPassage**`")
  n1("`*«requirement»*
**weedPassageSpeed : WeedPassageSpeed**`")
  n2("`*«requirement»*
**weedPassageSteering : WeedPassageSteering**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```
