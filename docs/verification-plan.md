# Requirement verification and executable criteria

The model distinguishes high-level mission/environment requirements from quantitative acceptance leaves. P-002's **250 Ã— 250 Ã— 250 mm usable printer envelope** is user-specified. Other newly selected values (15 kg separately lifted mass, 30-minute setup/service targets, 72-hour endurance campaign, timing/energy thresholds and environmental test severities) are proposed engineering targets for review, not attributed to the user or a standard. Work status remains typed SysML metadata.

## Native executable predicates

| Requirement | Inputs supplied by design/test evidence | Native predicate covers | Still requires evidence |
| --- | --- | --- | --- |
| P-002 DesktopManufacture | Occupied X/Y/Z of each oriented print job | Each dimension positive and â‰¤250 mm, with unit conversion | All jobs enumerated; slicer supports/brim/raft/clearance included |
| E-110 RestartDeadline (under E-003) | Measured restart time | 0â€“30 s | Correct restored state, qualification latch and motor inhibition |
| R-002 RecoveryEnergy | Separate motor and essential electrical powers; reserve energy | Reserve â‰¥1.2Ã—(motor powerÃ—1800 s + essential powerÃ—7200 s) | Measurement conditions, aged/cold battery capacity, reserve enforcement |
| N-118 RightingDeadline (under N-051) | Measured time for one release | 0â€“60 s | Every loading/angle/water trial, no damage or ingress |
| N-122 ControlRecoveryDeadline (under N-052) | Measured time from release | 0â€“120 s | Correct restored control and retained state |
| E-140 NavigationValidEpochs (under E-008) | Count of valid one-second epochs in a 30-minute run | At least 1710 and no more than 1800 | Accuracy remains E-002; timestamps, validity, and stale-data transition evidence |
| R-003 LaunchEnergyAdmission | Start-enable state, conservative start energy, reserve, age and validity flags | Start is disabled unless energy > reserve and all inputs are current/valid | Controller must actually enforce inhibition; configured reserve must satisfy R-002 |
| R-101 MotorQualificationInvariant (under R-004) | Motor-enable, qualifying and qualification-known states | Enabled motor implies known, nonqualifying status | Temporal ordering, persistence and fresh-command enforcement across resets |

These `require constraint` expressions are in the production SysML definitions. They have no invented observation defaults. The native CLI returns exit 0 for a holding supplied case, 1 for a failing case, and 2 when missing observations prevent evaluation. Only the supplied-observation predicate is executed; passing it is not a full physical compliance verdict.

Run `uv run python -m unittest discover -s tests -q`. The executable regression tests instantiate the real definitions with synthetic boundary, over-limit, negative and missing observations. They include mixed metre/millimetre inputs and a just-insufficient energy reserve. Python invokes the native engine and checks its verdict; it does not reimplement the requirement equations.

For actual evidence, create a SysML requirement usage specializing the relevant definition, bind its measured attributes, load it with the project models and invoke `-requirement Package::usage -json`. Preserve source measurements and provenance. Do not use the synthetic fixtures as vessel test results. The model's existing `satisfy` links are design allocations, not verified compliance.

## Evidence by requirement family

| Requirements | Verification method / acceptance evidence |
| --- | --- |
| C-000/C-001/M-001 | Ordered gate-crossing track and qualification event log; route coordinates still block a final acceptance test |
| C-002 | Count completed consecutive unassisted circuits and report duration; indefinite operation is an objective, never a finite-test proof |
| C-003/C-004/C-006 | Inject external control, abort and motor requests in each mode and across resets; verify qualification latch/interlocks |
| C-005/E-005/C-101 | Timestamped telemetry, 24-hour outage, reconnect and stale-display tests |
| H-001 | Passage track and arrival evidence; departure/arrival gates and ocean-specific rules remain unresolved |
| M-002/E-001/E-004/R-002 | Instrumented 72-hour harvesting/no-harvest campaign, estimator comparison and reserve-threshold injection |
| E-002/E-003 | Independent navigation reference and stale-data/reset fault injection |
| E-006/E-007 | Controlled leak, timestamped log replay and abrupt power-cut test |
| P-001/P-003 | One-person timed handling and replacement demonstrations; scale measurement and post-service leak checks |
| P-002 | Slicer envelope evidence for every job plus native dimension predicate |
| S-001 | Recorded head-on/crossing/overtaking scenarios, day/night, AIS/non-AIS; detection signatures/range, clearance and maneuver criteria still block full acceptance |
| S-002 | Boundary/trajectory injection including invalid polygons and no-feasible-maneuver cases |
| S-003/C-102 | Abort latch, isolation timing, remote-control loss, replay/expiry/authentication injections |
| S-004/S-005 | Deployment-specific compliance matrix, measured signaling performance and authorization evidence; unresolved applicability blocks deployment release |
| R-001 | Instrumented sheltered recovery speed/current/power test and challenge-mode inhibition |
| N-011â€“N-035 | Per-parameter functional tests plus combined-condition qualification; retain separate results for each leaf |
| N-041â€“N-047 | Exposure campaigns, sealing indicators, mechanical/electrical measurements, thermal logging and aged coupons |
| N-051/N-052 | Time-stamped capsize trials across the specified loading/angle/water matrix |
| N-053â€“N-056 | Documented milfoil-equivalent patch, snag, blocked-rudder and propulsor tests; establish surrogate equivalence before acceptance |

Next executable opportunities are trajectory gate-crossing/order, motor/qualification invariants over event logs, telemetry age/retention, and environmental sample coverage. Those need time-series evidence adapters or executable mission behavior; they are not implemented by the numeric/state predicates. High-level environmental acceptance should aggregate only the selected profile and its applicable shared leaf evidence, not return true merely because they contain prose.

## Audit clarifications

Accuracy counts all 1800 scheduled epochs, including missing/invalid observations. Deliberate fault-injection runs are assessed separately. Harvest replay cannot exceed a measured installed-harvester resource profile. The 24-hour calm campaign starts with both the protected recovery reserve and sufficient energy for measured calm-mode loads, with harvesting disabled.

Emergency/powered recovery takes priority over low-energy telemetry cadence and shore freshness thresholds. Clearing the low-energy flag depends on energy alone, so it cannot wait on survival exit; payload restoration still respects other active restrictions. Capsize recovery restores mode-appropriate control, while normal sailing waits for the survival exit gate. See the [independent audit and dispositions](requirements-audit.md).

## Separate acceptance verdicts

The [atomic decomposition map](requirement-decomposition.md) records the retained parent IDs and new leaves. Tests of restart timing, righting timing, control restoration timing, navigation epoch count and the motor-state invariant now target their specific leaves. A timing pass cannot stand in for retained state, sealing or motor-interlock evidence. Parent shared conditions remain mandatory for each leaf campaign; evidence must identify the same trial/epoch set where specified. Parent roll-up is not yet executable.

## Sustained energy

E-201 through E-205 add five executable acceptance predicates, with E-200 as their sustained-energy parent except that E-204 specifically refines the M-002 campaign. The native analysis uses the same criterion calculations as the requirements, and `BlueDogEnergy::SustainedEnergyVerification` explicitly verifies E-200. See the [energy framework](sustained-operations.md) for load coverage, chronological balance, repeating-cycle assumptions and the evidence acceptance checklist. E-204 also gates this initial combined demonstration analysis; future ocean campaigns need their own resource qualification profile.

Passing the numerical case is conditional on its inputs. The synthetic case deliberately keeps evidence acceptance false; its verification verdict is inconclusive. A finite energy-survival pass without nondecreasing cycle-end energy does not pass E-202. None of these results substitutes for functional mission, navigation or physical endurance evidence.
