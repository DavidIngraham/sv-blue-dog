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
