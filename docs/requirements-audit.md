# Independent requirements and derivation audit

Review date: October 9, 2026. An independent reviewer examined the SysML requirements, challenge, architecture allocations, trade analysis and supporting documents. The author implemented the findings, requested a second review, and applied its mode/applicability corrections. A final focused review found no additional blocking regression in that correction set. This is a model-quality audit, not physical qualification or authorization to deploy.

## Implemented findings

| Finding | Correction |
| --- | --- |
| E-002 excluded invalid samples, allowing poor navigation availability to pass | Accuracy counts all 1800 scheduled epochs. New E-008 separately records availability and stale-observation behavior, with executable count boundaries. |
| Low-energy 300-second telemetry conflicted with recovery cadence and 120-second stale indication | Emergency/powered recovery takes precedence at 60-second delivery/120-second freshness; low-energy alone uses 300/600 seconds. Stale age is not treated as proof of link failure. |
| R-002's predicate omitted the launch-admission promise | R-002 is now reserve sizing. R-003 separately requires start inhibition unless energy, age and validity conditions permit it; its predicate includes actual start-enable state. |
| Motor interlock was bundled with thrust performance and weakly traced to the challenge | New R-004 independently specifies motor inhibition, unknown-state handling and persistence, directly derived from C-003/C-004. R-001 retains recovery performance. |
| Calm endurance could begin with only a two-hour recovery reserve | N-034 requires reserve plus 24 hours of measured calm loads and no harvesting; reserve is retained throughout the test. |
| M-002 allowed unlimited harvesting within its allowed hours | Input power and accumulated harvest energy are bounded by a recorded measured installed-harvester profile; missing profile evidence invalidates qualification. |
| N-052 capsize restoration conflicted with N-035 survival exit | The 120-second deadline restores mode-appropriate control; normal sailing remains subject to the survival gate and other restrictions. |
| Second review found a possible low-energy/survival exit deadlock | Low-energy flag clears on energy recovery independently of survival state; payload enabling remains separately inhibited by other active restrictions. |
| N-054 could pass after weed shedding without functioning steering | Every snag test now requires both retained speed and full rudder travel. Weed speed comparisons explicitly use water-relative speed. |
| Current requirements referred to a nonexistent general no-progress response in S-002 | N-013/N-023 now invoke S-002 only for predicted boundary risk; no unsupported station-keeping/progress guarantee is made. |
| E-007 described loss of committed records and weak qualification persistence | Records older than five seconds persist; disqualification is committed before intervention/motor enable; unknown restored qualification is nonqualifying. |
| Printer/manufacture/serviceability chain confused correlation with derivation | P-002 is explicitly an owner-imposed constraint on M-001, not derived from handling. P-003 derives from repeated operation and ocean lifecycle support. |
| Emergency and command invariants lacked direct challenge trace | S-003 derives from C-006; C-102 additionally derives from C-003/C-006; R-004 derives from C-003/C-004. |
| Shared environmental branch obscured mission applicability | N-010 derives from M-001; N-020 from H-001. Freshwater/saltwater and Gorge weeds have direct profile links. Shared criteria explicitly select wet-exposure and capsize media; graph reachability is not unconditional applicability. |
| Ocean mission lacked boundary/deployment traces | Added H-001 derivations to S-002 and S-005. |
| Component allocations overstated whole-system outcomes | Aggregate mission/environment/traffic outcomes allocate to `boat`; shore presentation allocates to `monitoringStation`. These remain intended design allocations, not verification evidence. |
| Challenge/Hawaii descriptions called the entire environment undefined | Text now distinguishes the candidate qualification profiles from unresolved route/season suitability and mission acceptance details. |

No reversed original/derived relationships were found. The updated graph preserves the two top-level mission drivers. Explicit stakeholder constraints are identified as such; derivation does not mean that a route logically implies a 250 mm printer or any numerical design margin.

## Verification of corrections

Native validation and publication regression checks cover requirement IDs, all expected derivations, two mission roots and design/use-case traceability. Executable tests include invalid navigation counts, energy at/below/above reserve, stale/invalid admission inputs, safe inhibited starts, and every motor-enable/qualification state combination. Existing trade-analysis and numeric requirement boundary tests remain in the suite. All 18 regression tests passed. Generated register, derivation diagram, traceability and native trade results are checked for freshness.

## Remaining acceptance blockers

The reviewer explicitly recommended retaining these gaps instead of inventing values: course gates/corridors, Hawaii route and rules, traffic target/detection/clearance/maneuver criteria, regulatory applicability, milfoil-surrogate equivalence, and measured environmental/harvesting/power/drag evidence. Numeric engineering targets other than the confirmed printer bound still require review against feasibility. N-056 measures weed tolerance, not proof against every entanglement or mat.

State predicates evaluate supplied observations; they do not execute the controller or prove temporal ordering. Full verification still needs recorded trajectories, event traces, physical tests and evidence for every applicable acceptance clause. Model consistency is not a claim that the vehicle meets the requirements.

## Atomicity follow-up

The earlier independent audit corrected semantic and derivation defects but left bundled acceptance clauses. A subsequent pass decomposes 29 parent requirements into 127 leaves, preserving original IDs and test conditions. It separates estimator cadence/accuracy, reset timing/state, log properties, command rejection/application/acknowledgment, handling tasks, emergency controls, wet electrical/mechanical outcomes, capsize retention, and weed speed/steering/thermal outcomes. Shared invariants are referenced through derivations instead of copied. See the [decomposition map](requirement-decomposition.md). This follow-up is not a new independent reviewer sign-off.
