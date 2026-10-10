# C-000 trans gorge challenge

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**C-000 TransGorgeChallenge** — The vessel shall complete the Trans-Gorge challenge under C-001 through C-006.

**C-001 CourseCompletion** — The vessel shall complete a journey from The Dalles to Bonneville and back to The Dalles.

**C-002 RepeatedOperation** — After its first circuit, the vessel should repeat The Dalles–Bonneville–The Dalles autonomously for as long as practical.

**C-003 UnassistedAttempt** — A qualifying attempt shall complete the round trip without operator intervention.

**C-004 SailingPropulsion** — A qualifying attempt shall use sailing propulsion without auxiliary motor propulsion.

**C-005 LiveObservation** — The vessel shall provide live monitoring with autonomous operation and retained telemetry across communication outages.

**C-006 EmergencyIntervention** — The vessel shall permit remote emergency abort or manual control when a command link is available.

## C-000 derivation 1

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
%% BlueDogViews::transGorgeChallenge1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 229 node(s) without a position, left undrawn, and 450 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**transGorgeChallenge : TransGorgeChallenge**`")
  n1("`*«requirement»*
**courseCompletion : CourseCompletion**`")
  n2("`*«requirement»*
**repeatedOperation : RepeatedOperation**`")
  n3("`*«requirement»*
**unassistedAttempt : UnassistedAttempt**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## C-000 derivation 2

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
%% BlueDogViews::transGorgeChallenge2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 229 node(s) without a position, left undrawn, and 450 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**transGorgeChallenge : TransGorgeChallenge**`")
  n1("`*«requirement»*
**sailingPropulsion : SailingPropulsion**`")
  n2("`*«requirement»*
**liveObservation : LiveObservation**`")
  n3("`*«requirement»*
**emergencyIntervention : EmergencyIntervention**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

[Continue: C-001 course completion](<requirements-c-001.md>)

[Continue: C-002 repeated operation](<requirements-c-002.md>)

[Continue: C-003 unassisted attempt](<requirements-c-003.md>)

[Continue: C-004 sailing propulsion](<requirements-c-004.md>)

[Continue: C-005 live observation](<requirements-c-005.md>)

[Continue: C-006 emergency intervention](<requirements-c-006.md>)
