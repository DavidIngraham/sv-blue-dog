# Sizing Blue Dog for the Gorge

How small can I make the challenge vessel while keeping enough sailing performance, structural capacity and recovery capability? This is a [preliminary-design study](development-plan.md#virtual-design). Its inputs are the finite Gorge mission, chart-based course, manufacturing assumptions and provisional boat physics. Its output is a candidate to challenge with finer analysis and experiments before choosing dimensions for a build.

## What this search asks

The search first seeks feasibility, then minimizes hull length with all 29 hull, wing, appendage, ballast, structure and electrical sizing variables free. The selected weather-window profile requires progress on both legs in a westerly. Easterly performance is reported as a sensitivity. Safety, handling and structural screens remain mandatory in either wind direction.

The reference distance is 68.372 km per leg, taken from the chart-derived route between the proposed gates. Actual sailing tracks include tacks and avoidance. There is no 72-hour deadline and no daily energy-balance constraint. The static solver checks instantaneous peak power; battery capacity and harvesting still need evaluation through the [chronological mission simulation](mission-simulation.md). That simulation currently uses its own conceptual vessel, so its completion counts do not qualify this sizing candidate.

## Candidate and replay

The current run found a **2.009 m coarse-feasible candidate**. Length minimization then reached its iteration limit; the search retained the feasible geometry rather than accepting a smaller, constraint-violating trial. This establishes a candidate for further checks, not a minimum boat size or a design ready to build.

```sysml-report BlueDogEvidenceDocuments::CandidateBrief
```

The native reports read the current recorded run. The finer replay holds the candidate's geometry fixed and re-solves its operating controls across six engineering scenarios: primary, construction, aerodynamic, hydrodynamic, electrical and combined assumptions. These variations expose sensitivity; they are not measured uncertainty bounds.

<details>
<summary>Search outcome, scenario comparisons and limiting margins</summary>

```sysml-report BlueDogEvidenceDocuments::Summary
```

</details>

The sailing, structure and route screens use the selected challenge profile. The easterly passage column remains visible without becoming an extra challenge obligation. A diagnostic control solve that drops the peak-power check is identified separately. A route without positive progress has no completion time; its numerical penalty is not a predicted voyage duration.

The primary finer replay passes the selected westerly sailing, structure and route screens, with a conditional round-trip estimate of **44.5 hours**. Its easterly estimate is 85.6 hours, but upstream progress is only 0.249 m/s against the allocated 0.5 m/s target. These are persistent-wind route calculations, not chronological voyage or endurance predictions.

Primary, aerodynamic, hydrodynamic and electrical scenarios pass the selected static profile. Construction and combined sensitivity fail the operating and structural screens, with keel deflection among the limiting results. The construction assumptions therefore remain a priority for coupon and stiffness measurements.

## What a wind shift changes

![Sensitivity of the current candidate's route screens and conditional passage time to an assumed persistent easterly wind.](figures/weather-performance-sensitivity.svg)

This calculation keeps the candidate fixed and sweeps an assumed probability of a wholly easterly passage. It helps compare which engineering assumptions make wind shifts consequential. It does not estimate real mission-success probability or account for changing winds during a voyage. The [weather study](operating-constraints.md#gorge-weather-and-launch-windows) and mission simulation address those distinctions.

## What would justify a build decision

Sailing equilibrium is only one part of the decision. The [recovery assessment](structures-and-recovery.md) checks sealed, flooded and water-retaining wing states. Positive sampled roll moments cannot establish self-righting when pitch is unstable, and static equilibrium does not demonstrate a dynamic capsize recovery.

The [OpenVSP experiments](sail-trade.md#what-we-have-actually-run-in-openvsp) supply numerical wing trends for this study. Measured lift, drag, pitching moment and actuator loads remain important inputs, alongside printed/laminated construction mass and stiffness. Those measurements feed the [model-credibility loop](development-plan.md#model-credibility) before the analysis can support a build commitment.

[Current candidate and exact values](../models/evidence/current-sizing.sysml) · [Run provenance](../evidence/runs/2026-10-12-gorge/manifest.json)

**Next:** [How the sizing search works](sizing.md).
