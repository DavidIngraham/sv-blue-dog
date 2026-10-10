# C-006 emergency intervention

[All requirement views](<../requirements-views.md>)

**EmergencyIntervention** — Provide remote emergency abort or manual control when a command link is available. Use disqualifies the attempt as unassisted. Emergency abort behavior and the subsequent recovery procedure are open.

**Communications** — Aggregate requirement for Communications. Acceptance requires all applicable derived leaf results (E-120, E-121, E-122, E-123, E-124, E-131, E-137); this parent has no independent executable pass/fail predicate. Shared verification context: Link availability is a delivery-test precondition, not a coverage guarantee. Normal cadence is 60 seconds; low-energy alone permits 300 seconds; emergency/powered recovery takes precedence at 60 seconds. Outage tests last 24 hours.

**SafeRecovery** — Aggregate requirement for SafeRecovery. Acceptance requires all applicable derived leaf results (S-110, S-111, S-112, S-113, S-114, S-115, E-138, R-101, E-130); this parent has no independent executable pass/fail predicate. Shared verification context: Emergency intervention ends attempt qualification. Exercise active emergency, powered recovery, local isolation and remote-control loss, including coexisting low-energy flags.

**CommandIntegrity** — Aggregate requirement for CommandIntegrity. Acceptance requires all applicable derived leaf results (C-205, C-206, C-207, C-208, C-209, C-210, C-211, E-132, E-138); this parent has no independent executable pass/fail predicate. Shared verification context: Exercise complete command receipt, authentication failure, replayed sequence numbers, age greater than 30 seconds, and external control during a qualifying attempt.

## C-006 derivation 1

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
%% BlueDogViews::emergencyIntervention1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 198 node(s) without a position, left undrawn, and 361 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**GorgeChallenge::emergencyIntervention : EmergencyIntervention**`")
  n1("`*«requirement»*
**BlueDogRequirements::communications : Communications**`")
  n2("`*«requirement»*
**BlueDogRequirements::safeRecovery : SafeRecovery**`")
  n3("`*«requirement»*
**BlueDogRequirements::commandIntegrity : CommandIntegrity**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n1
  n3 -.->|"derive"| n0
```

[Continue: E-005 communications](<requirements-e-005.md>)

[Continue: S-003 safe recovery](<requirements-s-003.md>)

[Continue: C-102 command integrity](<requirements-c-102.md>)
