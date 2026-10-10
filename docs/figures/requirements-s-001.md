# S-001 TrafficSafety relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**S-001 TrafficSafety** — The vessel shall assess and respond to collision risks within the deployment-specific traffic envelope.

**S-101 TrafficTracking** — The vessel shall maintain a track for every encounter target within the frozen S-001 detection envelope.

**S-102 CollisionAssessmentCadence** — The vessel shall update collision-risk estimates at least once per second.

**S-103 AvoidanceCommandDeadline** — The vessel shall issue the prescribed avoiding-action command within 2 seconds of each S-001 collision-risk trigger.

**S-104 TrafficAwarenessFault** — After traffic assessment has been invalid for more than 5 seconds, the vessel shall log a traffic-awareness fault within 1 second.

## S-001 relationships 1

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
%% BlueDogViews::trafficSafety1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 58 node(s) without a position, left undrawn, and 64 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**trafficSafety : TrafficSafety**`")
  n1("`*«requirement»*
**trafficTracking : TrafficTracking**`")
  n2("`*«requirement»*
**collisionAssessmentCadence : CollisionAssessmentCadence**`")
  n3("`*«requirement»*
**avoidanceCommandDeadline : AvoidanceCommandDeadline**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## S-001 relationships 2

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
%% BlueDogViews::trafficSafety2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 60 node(s) without a position, left undrawn, and 66 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
flowchart BT
  n0("`*«requirement»*
**trafficSafety : TrafficSafety**`")
  n1("`*«requirement»*
**trafficAwarenessFault : TrafficAwarenessFault**`")
  n1 -.->|"derive"| n0
```

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| navigationConspicuity | trafficSafety | NavigationConspicuity supports trafficSafety. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: S-004 NavigationConspicuity](<requirements-s-004.md>)
