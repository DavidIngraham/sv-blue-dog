# Safety/reliability checklist

Use source IDs from [sources.md](sources.md). Record consistency, defect, open decision, evidence gap or justified exclusion for each applicable item.

| ID | Review and closure question | Basis |
| --- | --- | --- |
| S01 | Are system, configuration, modes, lifecycle and affected people/assets/environment explicit? | SAF4.3.2,Task106.2 |
| S02 | Are hazardous conditions, initiating causes and potential mishaps distinguished? | SAF4.3.2; RM risk triplet |
| S03 | Do failure analyses include incorrect behavior, interfaces, human tasks and combinations? | SAF4.3.2; BOK3.2.4 |
| S04 | Are critical-function loss and individual component failure distinguished? | SYS8.1.8; BOK mission profile |
| S05 | Are consequence, likelihood and uncertainty characterized on a stated basis? | RM; SAF4.3.3 |
| S06 | Are unknown assessments kept distinct from low/zero risk? | RM uncertainty; local missing-evidence application |
| S07 | Are alternatives considered in design-control precedence, with secondary hazards reviewed? | SAF4.3.4; local interaction check |
| S08 | Do control intents link to actual obligations, implementations and verification? | SAF4.3.4-6,Task106 |
| S09 | Are proposed controls separate from implementation and effectiveness evidence? | SAF4.3.5-6 |
| S10 | Are residual risk and actual acceptance authority/record explicit? | SAF4.3.7,Task106; project responsibilities |
| S11 | Does coverage/readiness remain open until its scope is reviewed? | SAF4.3.1-2; local completeness check |
| S12 | Are failure definitions, exposure, censoring and data pedigree appropriate? | BOK3.2.4-5; EXP |
| S13 | Are rate terms non-overlapping and applicable to mission-critical outcomes? | SYS competing/series assumptions; local partition review |
| S14 | Are dependence and common-cause effects addressed without assuming physical independence? | SYS8.1.8; RM scenario analysis |
| S15 | Is constant hazard justified rather than applied to wear, cycles or systematic software by default? | EXP; local model-domain check |
| S16 | Are qualitative rankings kept separate from probabilities and confidence claims? | RM likelihood basis; local dimensional/statistical distinction |
| S17 | Are failure reports, corrective actions and effectiveness fed back into the model? | BOK FRACAS; SAF4.3.8 |
| S18 | Are control failures, interacting faults and rejected evidence exercised? | SAF4.3.6; local native regression practice |

For each record retain configuration/mode, cause-to-consequence scenario, control alternatives and selection basis, responsible role, requirement/verification references, evidence, risk basis/disposition and changes. An empty evidence field is an open item, not an accepted mitigation.
