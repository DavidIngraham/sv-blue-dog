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
