# N-035 EnvelopeTransition relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**N-035 EnvelopeTransition** — The vessel shall select survival or sailing operation according to the defined environmental transition conditions.

**N-106 SurvivalEntryDeadline** — The vessel shall enter survival mode within 60 seconds of the N-035 upper-limit trigger.

**N-107 SurvivalTransitionRecording** — Every survival-mode entry shall have a corresponding event record.

**N-108 SailingResumptionDeadline** — Full autonomous sailing shall resume within 5 minutes of N-035 resumption eligibility becoming continuously true.

**N-109 SailingResumptionInhibition** — Full autonomous sailing shall remain inhibited while N-035 resumption eligibility is false.

**N-110 ResumptionBlockEvidence** — Every blocked sailing-resumption attempt shall record the blocking condition.

**E-130 PeriodicLogCadence** — Periodic mission records shall be acquired at least once per second normally and once per minute in low-energy or survival operation.

**R-101 MotorQualificationInvariant** — Motor thrust shall remain disabled whenever an attempt is qualifying or qualification status is unknown.

## N-035 relationships 1

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
%% BlueDogViews::envelopeTransition1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 111 node(s) without a position, left undrawn, and 158 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**envelopeTransition : EnvelopeTransition**`")
  n1("`*«requirement»*
**survivalEntryDeadline : SurvivalEntryDeadline**`")
  n2("`*«requirement»*
**survivalTransitionRecording : SurvivalTransitionRecording**`")
  n3("`*«requirement»*
**sailingResumptionDeadline : SailingResumptionDeadline**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-035 relationships 2

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
%% BlueDogViews::envelopeTransition2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 122 node(s) without a position, left undrawn, and 196 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**envelopeTransition : EnvelopeTransition**`")
  n1("`*«requirement»*
**sailingResumptionInhibition : SailingResumptionInhibition**`")
  n2("`*«requirement»*
**resumptionBlockEvidence : ResumptionBlockEvidence**`")
  n3("`*«requirement»*
**periodicLogCadence : PeriodicLogCadence**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-035 relationships 3

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
%% BlueDogViews::envelopeTransition3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 117 node(s) without a position, left undrawn, and 165 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**envelopeTransition : EnvelopeTransition**`")
  n1("`*«requirement»*
**motorQualificationInvariant : MotorQualificationInvariant**`")
  n1 -.->|"derive"| n0
```
