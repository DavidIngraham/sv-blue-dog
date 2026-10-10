# C-001 course completion

[All requirement views](<../requirements-views.md>)

**CourseCompletion** — Threshold: Complete a journey from The Dalles to Bonneville and back to The Dalles. Exact start/finish and turnaround gates, permitted corridor, and crossing evidence remain to be agreed.

**RoundTrip** — The vessel shall cross the configured The Dalles departure gate, Bonneville turnaround gate and The Dalles return gate in that order during one attempt, satisfying C-003 through C-006. Acceptance shall use the timestamped trajectory and intervention/propulsion event log; a missing gate crossing or disqualifying event shall prevent a completion verdict.

## C-001 derivation 1

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
%% BlueDogViews::courseCompletion1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 222 node(s) without a position, left undrawn, and 434 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::courseCompletion : CourseCompletion**`")
  n1("`*«requirement»*
**BlueDogRequirements::roundTrip : RoundTrip**`")
  n1 -.->|"derive"| n0
```

[Continue: M-001 round trip](<requirements-m-001.md>)
