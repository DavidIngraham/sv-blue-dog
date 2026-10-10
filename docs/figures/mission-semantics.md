# Challenge, vehicle and verification

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

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
%% BlueDogSemanticViews::MissionSemantics — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 94 node(s) without a position, left undrawn, and 106 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=360 y=0
%% layout: n2 x=0 y=200
%% layout: n8 x=360 y=200
%% layout: n25 x=0 y=400
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::transGorgeChallenge : TransGorgeChallenge**`")
  n1("`*«requirement»*
**GorgeChallenge::courseCompletion : CourseCompletion**`")
  n2("`*«requirement»*
**BlueDogRequirements::roundTrip : RoundTrip**`")
  n8["`*«verification def»*
**BlueDogRequirementVerification::RoundTripVerification**`"]
  n25("`*«part»*
**BlueDog::Architecture::missionContext::boat : Boat**`")
  n1 -.->|"derive"| n0
  n8 -.->|"verify"| n2
  n2 -.->|"refine"| n1
  n25 -.->|"satisfy"| n2
```
