# Conservative sizing: reading the results

The current trial answers part of the question: under the primary assumptions it can balance the modeled sailing states and energy demand and meet the route screen in both directions. The representative westerly passage takes about 48 hours in that calculation, compared with about 67 hours in an easterly. It does **not** yet give me a design to build. Handling is still outside its allocation, added aerodynamic degradation loses easterly upstream progress, and self-righting remains unproven.

For [preliminary design](development-plan.md#virtual-design), I use the archived search, replay and recovery runs to decide what to investigate next. The most useful next evidence is wing force and moment measurements, construction mass/stiffness measurements, and controlled recovery experiments. Those feed the [model-credibility loop](development-plan.md#model-credibility) before another sizing decision.

The search stopped just outside its coarse feasibility tolerance, before minimizing length. The dimensions below describe a near-feasible trial, not a proven minimum. Refined replay keeps its geometry fixed and re-solves the controls; that is why a primary sailing pass can coexist with an unsuccessful coarse search.

## Read the candidate and scenario record

```sysml-report BlueDogEvidenceDocuments::CandidateBrief
```

Displayed numbers are rounded for reading; the model and archived runs retain their original precision. The concept sketch in the [mission article](architecture.md) explains the parts, but is not a rendering of this trial geometry.

The native tables below are generated from the model. “No” in the combined or accepted-evidence columns matters even when an individual screen passes. In the energy stress case, all eight states needed energy-unconstrained diagnostics; those durations cannot predict sustained operation. The combined case’s duration penalty is not a voyage time. Positive sampled roll moments also do not establish recovery when pitch is unstable.

The archived search required both wind directions to pass. Our new weather-window profile prioritizes westerly challenge performance, but it does not retroactively turn that run into a successful optimization. The following native assessment holds the archived geometry and sailing results fixed and sweeps an assumed probability of a wholly easterly passage. It is a sensitivity study, not a forecast or a new size optimum.

![Probability sensitivity for the fixed candidate: the primary case passes both direction screens; construction, aerodynamic and hydrodynamic cases pass only the west-wind route. Energy and combined cases have no eligible passing route. Conditional passage times omit failed cases.](figures/weather-performance-sensitivity.svg)

*The six curves represent separate engineering assumptions, not six equally probable weather states. Passing a route screen does not resolve handling or self-righting. The [weather article](operating-constraints.md#gorge-weather-and-launch-windows) explains why hourly east-wind frequency cannot be inserted as a whole-passage probability.*

<details>
<summary>Candidate dimensions, scenario comparisons and limiting margins</summary>

```sysml-report BlueDogEvidenceDocuments::Summary
```

</details>

[Inspect the candidate definition and exact values](../models/evidence/conservative-2026-10-11.sysml). The report is a readable projection; archived evidence retains full precision.

The [ingress assessment](structures-and-recovery.md) finds negative restoring moments with a flooded or water-retaining wing. Even the positive sealed-wing roll samples include pitch-unstable equilibria. Self-righting therefore remains unproven.

The [OpenVSP experiment gallery](sail-trade.md#what-we-have-actually-run-in-openvsp) includes tested geometry, alpha and heel sweeps, mesh/wake sensitivity, induced-drag polars and a direct interpolation check at the trial's aspect ratio and camber. Those experiments support exploratory trends; measured low-Reynolds-number polars, stall, real drag and moment data are still missing. None of these numerical outcomes qualifies the vessel for the challenge.


[Run provenance](../evidence/runs/2026-10-11-conservative/manifest.json) · **Next:** [How the sizing search works](sizing.md).
