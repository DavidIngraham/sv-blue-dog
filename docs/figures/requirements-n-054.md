# N-054 weed snag shedding

[All requirement views](<../requirements-views.md>)

**WeedSnagShedding** — Aggregate requirement for WeedSnagShedding. Acceptance requires all applicable derived leaf results (N-128, N-129); this parent has no independent executable pass/fail predicate. Shared verification context: Gorge campaign: drape one wet 1 m branched stem over one appendage leading edge at a time, five repetitions per appendage, with N-053 surrogate characteristics, 5 m/s mean wind and the unobstructed reference heading. No manual assistance or motor use. Both leaf criteria apply to every repetition; visible stem removal alone is insufficient.

**WeedSnagSpeedRecovery** — Within 5 minutes of each N-054 snag, water-relative sailing speed shall recover to at least 50 percent of unobstructed reference speed. Verification uses the shared context of N-054.

**WeedSnagSteeringRecovery** — Within 5 minutes of each N-054 snag, full commanded rudder travel shall be regained. Verification uses the shared context of N-054.

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
%% not represented: 58 node(s) without a position, left undrawn, and 68 edge(s) at them
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
