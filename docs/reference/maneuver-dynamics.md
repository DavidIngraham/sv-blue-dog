# How long does an avoidance turn occupy the boat?

A command reaching the controller does not instantly change the boat's course.
I added an optional low-order maneuver model to test that distinction. It limits
turn rate and acceleration, reduces speed during a turn, tack or gybe, and makes
rudder authority depend on speed through the water. Current moves the boat but
does not supply that steering authority.

The [native model](../../models/analyses/maneuver-dynamics.sysml) owns the
equations, coefficients and study cases. Its coefficients are unmeasured
hypotheses. The Python adapter integrates heading and position. It does not
resolve yaw inertia, roll, wave excitation or sail handling.

## A bounded component experiment

Each case requests a 90-degree heading change and runs for 120 seconds. The
ordinary, tack, gybe and recovery cases start at 1 m/s and request that speed
after the turn. All experience the same 0.3 m/s eastward current. The low-speed
case requests 0.1 m/s; the unavailable-rudder case has zero rudder authority.

| Case | Heading reached, 1 s integration | Heading reached, 0.25 s integration |
| --- | --- | --- |
| Ordinary turn | 20 s | 19.5 s |
| Tack | 57 s | 56.75 s |
| Gybe | 25 s | 24.75 s |
| Low water speed | Not reached within 120 s | Not reached within 120 s |
| Rudder unavailable | Not reached within 120 s | Not reached within 120 s |
| Recovery turn component | 23 s | 22.75 s |

Heading completion does not mean speed has recovered. These are synthetic
responses, not IC-01 maneuver predictions. The finer step
changes the completion times by at most half a second in these cases, but that
numerical agreement does not validate the assumed coefficients. An unfinished
turn supplies no finite maneuver-time bound.

## What changes in a mission replay

The optional `maneuverDynamics` input requires an initial heading and can supply
an initial speed and coefficient overrides. Command delivery still takes time.
The boat retains its previous motion while a command is pending, then follows
the bounded turn. A replacement heading remains blocked until both the allocated
occupied interval and the actual heading change are complete.

Existing campaigns retain their original maneuver representation unless this
option is supplied. In particular, the archived IC-01 campaign is not evidence
for the new dynamics. Guidance still forecasts kinematic candidate motion;
bounded execution does not make that forecast dynamically feasible. Full
candidate polars and tack excursions remain unresolved. Powered recovery routes
still use the existing point-mass executor; the recovery row above tests only
the standalone turn component.

## Consequence for sensing and design

The [encounter envelope](encounter-envelope.md) must include any remaining
occupied time before another avoidance command can be selected. A fixed
15-second turn cannot stand in for the achieved response across low wind,
different maneuvers and faults. I need measured heading, speed and swept path
for an identified hull, rig and actuator installation before assigning a
credible bound. Cases with insufficient authority must lead to an explicit
operating restriction or another safety response.

Reproduce the component study with
`uv run python -m tools.boat_analysis.mission.maneuver_study`. It writes
`build/analysis/maneuver-study.json`, including model inputs, trajectories and
source hashes. Configuration-specific sensing simulation is a later experiment.
