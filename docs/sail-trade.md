# Comparing sail architectures

We compare control architecture separately from section camber. A tail-controlled wing and a directly rotated fixed-camber wing solve trim differently; either needs measured aerodynamic moments, actuator losses, structural loads and failure-state behavior. A soft sail remains a useful comparator rather than an assumed failure.

The analysis separates unknown evidence, a demonstrated failure and a development preference. Apply the same durability, energy, progress, recovery, manufacturing, handling and reliability gates to each candidate. Do not turn a qualitative durability concern into a failure rate or an arbitrary weighted score.

```sysml-report BlueDogSailTradeDocuments::Conclusion
```

The candidate definitions and gate logic live in the [trade model](../models/analyses/sail-trade.sysml). The [design decisions](../models/vehicle/decisions.sysml) explain the baseline used for sizing. [Source evidence](../models/vehicle/source-evidence.sysml) preserves the prior-art findings and their limits, including the square-sail precedent, Oshen PC13, tail control and non-backdrivable gearing.

## Obtain comparable evidence

Measure both-tack lift, drag and pitching moment over the intended trim range, including stall, broadside sailing and transitions. Measure electrical energy over the same move/hold/idle duty cycle. A gearbox that holds without motor current still has movement losses, controller demand and a retained-angle failure state.

For recovery, represent each body with actual mass, center of gravity, geometry and flooding state. Pose the rig at free and locked angles and evaluate both sides of a full roll. Check pitch stability and dynamic release behavior separately from sampled static righting moments. The [structures and recovery method](structures-and-recovery.md) describes that distinction.

Use prototypes to resolve the uncertainties before committing geometry. The [sizing workflow](sizing.md) can explore a baseline while other concepts remain open; its numerical results do not complete the trade.

## What we have actually run in OpenVSP

The recorded work uses OpenVSP 3.54.0. There are two experiments: a reference-wing mesh study (three five-point alpha sweeps), and a response grid (25 eight-point sweeps, 200 operating points). The figures below are regenerated from the immutable [run records](../evidence/runs/2026-10-10-coupled/manifest.json) during every site build. No new aerodynamic solve is implied by republishing them.

### Tested geometry

The reference wing is rectangular, with area 1 m², span 2 m, chord 0.5 m and aspect ratio 4. It uses the section extracted at the 150 mm span station of `SweptCrescentWing.STEP`. The section is reflected into aerodynamic coordinates and its chord-line tilt removed. This is a section experiment, not a replica of the swept CAD planform or a complete sail-and-hull installation.

![Native OpenVSP shaded oblique screenshot of the tested reference wing](https://davidingraham.github.io/sv-blue-dog/assets/vsp/reference-perspective.png)

The oblique screenshot rotates the geometry for display only. The aerodynamic runs use the saved model orientation. [Download the tested OpenVSP model](../evidence/vsp-geometry/reference-64.vsp3); the [capture manifest](../evidence/vsp-geometry/manifest.json) records its provenance and screenshot hashes.

![Native OpenVSP planform screenshot of the reference wing](https://davidingraham.github.io/sv-blue-dog/assets/vsp/reference-planform.png)

The response grid holds area at 1 m² and changes aspect ratio through 2, 4, 6 and 8. Camber scales of 0.5, 1 and 1.5 retain the original thickness distribution. Each combination is run with forward and reversed chord coordinates; one additional zero-camber case at AR 4 provides a control. These are hypothetical section variants, not additional manufactured prototypes.

![Sections used in the camber study](https://davidingraham.github.io/sv-blue-dog/assets/vsp/sections.svg)

### Alpha sweeps and mesh sensitivity

The reference sweeps cover −4° to 12° in 4° increments, with spanwise mesh parameters 16, 32 and 64 and corresponding chordwise tessellation `2 × mesh + 1`. These labels are tessellation settings, not total panel counts. The response grid uses mesh parameter 24 and covers −12° to 16° in 4° increments.

All sweeps use 5 m/s, air density 1.225 kg/m³, zero sideslip, Mach zero, and five wake iterations. Reynolds number is supplied as `5 × chord / 1.5e-5`; the reference value is approximately 167,000. Reference area, span and chord are set explicitly. Pitching moment is reported about midchord in the solver's axes.

![Reference alpha sweeps comparing three mesh settings](https://davidingraham.github.io/sv-blue-dog/assets/vsp/reference-sweeps.svg)

Lift and pitching moment change with mesh refinement, so these curves should not be called mesh-independent. The study varies tessellation but does not establish wake-iteration convergence. The markers are actual recorded samples; connecting lines do not imply additional solved points.

### Aspect ratio, camber and chord direction

![Aspect-ratio alpha sweeps at original camber](https://davidingraham.github.io/sv-blue-dog/assets/vsp/aspect-sweeps.svg)

![Camber alpha sweeps at aspect ratio four](https://davidingraham.github.io/sv-blue-dog/assets/vsp/camber-sweeps.svg)

![Induced-drag polars by aspect ratio](https://davidingraham.github.io/sv-blue-dog/assets/vsp/induced-polars.svg)

The drag plots show **induced drag only**, not total sail drag or boat performance. The reference output also contains a profile-drag estimate, but we have not validated it for this section and Reynolds-number range. It is deliberately excluded from these comparisons.

![Forward and reversed-chord alpha sweeps](https://davidingraham.github.io/sv-blue-dog/assets/vsp/reverse-sweeps.svg)

The direction comparison shows raw solver coordinates. Reversing the chord array is a geometric sensitivity experiment, not a validated opposite-tack polar. The optimization adapter separately transforms angle, lift and moment signs when representing reverse flow; these plots do not apply that transformation.

### What these results can establish

These runs support bounded interpolation and sensitivity studies inside the sampled response grid. The plotted responses show the influence of camber and aspect ratio and the need to retain aerodynamic moments when sizing the trim actuator. They do not select a winning sail architecture.

VLM assumes attached, inviscid flow and a prescribed shedding edge. This CAD section has a rounded edge, making that shedding assumption particularly important. Increasing lift at the high-alpha endpoints does not demonstrate absence of stall. Broadside sailing, separation, real low-Re drag, both-tack transitions, gust response, mast interference and tail/elevator control are not validated here. No tail-controlled wing or soft-sail simulation is included in this dataset. The authoritative [aerodynamic decision and evidence gaps](../models/vehicle/decisions.sysml) retain those limits.

### Reproduce the figures

`uv run python -m tools.boat_analysis.evidence.aerodynamics` writes plots to `build/vsp-figures`. The standard publishing command generates the same assets for Pages without installing or running VSP. The plotter always reads the archived records, verifies their hashes, and labels them as unvalidated evidence; it does not silently substitute a newer local run.

To recapture the native geometry screenshots on Windows after installing the isolated VSP environment, run `uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.capture` from the repository root. This opens the graphics event loop, captures the archived geometry, and exits. New captures must be reviewed and their evidence manifest updated explicitly.

## Heel and incidence sweeps

The original VSP sweeps held spanwise inflow at zero and did **not** include heel. The boat force-balance model separately applies a cosine projection to upright lift. The new heel study resolves the changed flow direction in VSPAERO instead of assuming that projection is sufficient.

The [SysML analysis case](../models/analyses/wing-heel.sysml) defines coverage and assumptions. This study uses the same fixed-camber rectangular reference wing at AR 4 and area 1 m², with 5 m/s horizontal apparent wind. Apparent-wind angles are 45°, 90° and 135° from the bow; signed heels are −40°, −20°, 0°, 20° and 40°. Each combination sweeps eight nominal upright incidences from −12° to 16°: **15 sweeps and 120 newly solved operating points**. Mesh parameter 24 and five wake iterations match the earlier response-grid settings; this does not establish convergence at high spanwise inflow.

For each nominal incidence, mast trim is fixed relative to the boat while heel changes. The local angle of attack and spanwise inflow therefore change together. A nominal 8° point means the trim that produces 8° incidence upright, not a controller that maintains 8° at every heel. Across the full study the actual solver alpha spans approximately −19.5° to +23.5°, and spanwise angle reaches ±40°. These extremes extend beyond the original alpha grid and are especially vulnerable to separated-flow and stall errors; a converged algebraic solution would not establish their physical validity.

### Frames and loads

The right-handed world frame is **X aft, Y starboard, Z up**. Positive heel rotates about the aft axis and tilts the mast toward port. The wind velocity is horizontal, with direction `(cos(AWA), −sin(AWA), 0)`. Wing axes are chord X, span Y and section-normal Z. We transform wind into those axes using `R = Rx(heel) Rz(nominal incidence − AWA) Rx(90°)` and recover the solver angles from the transformed vector. At beam wind, the solver's spanwise angle is the negative of heel; at zero heel, every case recovers the original incidence and zero spanwise flow.

The direction and moment normalization follow the [VSPAERO solver conventions](https://github.com/OpenVSP/OpenVSP/blob/master/src/vsp_aero/Solver/VSP_Solver.C). Forces and moments are transformed back into world axes after solving. Forward force is `−Fx`; starboard and upward loads retain their signs. All plotted loads use **inviscid surface-integration results**, excluding the unvalidated profile-drag estimate. Moments are dimensionalized before rotation: roll/yaw coefficients use reference span, pitch uses reference chord.

The moment origin is the **wing-root midchord**, not the boat center of gravity. These are isolated-wing loads, not net vessel roll moments or a righting assessment. Positive and negative heel are both sampled; they are not a substitute for modeling the opposite sailing tack.

![Heel and incidence sweeps at 45 degrees apparent wind](https://davidingraham.github.io/sv-blue-dog/assets/vsp/heel-awa-45.svg)

![Heel and incidence sweeps at beam wind](https://davidingraham.github.io/sv-blue-dog/assets/vsp/heel-awa-90.svg)

![Heel and incidence sweeps at 135 degrees apparent wind](https://davidingraham.github.io/sv-blue-dog/assets/vsp/heel-awa-135.svg)

### Compare with the boat model's approximation

The comparison below holds nominal incidence at 8°. The dashed curve uses the upright inviscid lift and drag from this same study, multiplying lift by `cos(heel)` before resolving forward force. This isolates the projection approximation from profile-drag and discrepancy assumptions used elsewhere in the sizing model. The solid curve comes from the coupled local-alpha/spanwise-inflow solutions.

![Solved heel response versus the cosine projection approximation](https://davidingraham.github.io/sv-blue-dog/assets/vsp/heel-projection-comparison.svg)

The cosine projection overpredicts forward force for the 45° and 90° wind cases and underpredicts it for the 135° case at substantial heel in this fixed-trim comparison. Heel therefore cannot be represented by one direction-independent loss factor. These curves are sensitivity evidence, not an updated validated optimizer polar. The current optimizer is unchanged. Before replacing its projection, we need consistent heel/wind/trim coverage across the full aspect-ratio and camber grid, appropriate force/moment interfaces, and convergence and physical validation. A free-air uniform-flow study does not include the water surface, wave-induced motion, wind shear, mast/hull interference, stall or dynamic roll.

The [archived heel results](../evidence/runs/2026-10-11-heel/wing-heel-sweep.json) include actual solver alpha/beta, dimensional loads, model settings and source hashes; the [manifest](../evidence/runs/2026-10-11-heel/manifest.json) protects the record bytes. Re-run with `uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.heel_sweep`. Plotting and Pages builds use the archived evidence without launching VSP.
