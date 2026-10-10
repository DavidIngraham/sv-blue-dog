# Requirement verification and executable criteria

The model distinguishes high-level mission/environment requirements from quantitative acceptance leaves. P-002's **250 × 250 × 250 mm usable printer envelope** is user-specified. Other newly selected values (15 kg separately lifted mass, 30-minute setup/service targets, 72-hour endurance campaign, timing/energy thresholds and environmental test severities) are proposed engineering targets for review, not attributed to the user or a standard. Work status remains typed SysML metadata.

## Native executable predicates

| Requirement | Inputs supplied by design/test evidence | Native predicate covers | Still requires evidence |
| --- | --- | --- | --- |
| P-002 DesktopManufacture | Occupied X/Y/Z of each oriented print job | Each dimension positive and ≤250 mm, with unit conversion | All jobs enumerated; slicer supports/brim/raft/clearance included |
| E-003 ResetRecovery | Measured restart time | 0–30 s | Correct restored state, qualification latch and motor inhibition |
| R-002 RecoveryEnergy | Separate motor and essential electrical powers; reserve energy | Reserve ≥1.2×(motor power×1800 s + essential power×7200 s) | Measurement conditions, aged/cold battery capacity, reserve enforcement |
| N-051 SelfRighting | Measured time for one release | 0–60 s | Every loading/angle/water trial, no damage or ingress |
| N-052 CapsizeControlRecovery | Measured time from release | 0–120 s | Correct restored control and retained state |

These `require constraint` expressions are in the production SysML definitions. They have no invented observation defaults. The native CLI returns exit 0 for a holding supplied case, 1 for a failing case, and 2 when missing observations prevent evaluation. Only the numeric predicate is executed; passing it is not a full physical compliance verdict.

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
| N-011–N-035 | Per-parameter functional tests plus combined-condition qualification; retain separate results for each leaf |
| N-041–N-047 | Exposure campaigns, sealing indicators, mechanical/electrical measurements, thermal logging and aged coupons |
| N-051/N-052 | Time-stamped capsize trials across the specified loading/angle/water matrix |
| N-053–N-056 | Documented milfoil-equivalent patch, snag, blocked-rudder and propulsor tests; establish surrogate equivalence before acceptance |

Next executable opportunities are trajectory gate-crossing/order, motor/qualification invariants over event logs, telemetry age/retention, and environmental sample coverage. Those need time-series evidence adapters or executable mission behavior; they are not implemented by the current five numeric predicates. The high-level environmental parents should aggregate leaf evidence, not return true merely because they contain prose.
