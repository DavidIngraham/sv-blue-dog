# Comparing recovery propulsion

**Design phase:** Concept and preliminary design · PDR · [Development plan](development-plan.md)

If a trial goes wrong, I want a practical way to bring the boat back. Should that be a water propeller or an air propeller? This [preliminary-design trade](development-plan.md#virtual-design) starts with resistance, weed exposure and the energy reserve, and should lead to an installed comparison of the two concepts. The motor is for testing and recovery, not the qualifying sailing attempt.

I want to compare both drives against the same installed recovery task. An ideal disk calculation can help estimate the scale of the problem, but it cannot tell me which installation will work better on this boat.

Selecting a [westerly challenge window](operating-constraints.md#gorge-weather-and-launch-windows) does not remove the need to recover after a reversal or calm. Both propulsor candidates must use the same declared current, windage and reserve conditions; winter trials need a separate applicable profile. A motor-assisted recovery remains an unsuccessful qualifying attempt, never extra sailing performance hidden in a probability average.

My starting point will be a hull tow measurement and the required recovery conditions. Then I can bench each complete guarded drive and compare installed thrust, electrical power, temperature and maneuvering performance. The [native analysis](../models/analyses/recovery-propulsion.sysml) currently estimates reserve demand from illustrative inputs; those estimates help plan the experiment.

Water propulsion offers compact thrust but exposes the rotor and shaft to weeds. Air propulsion avoids submerged rotor fouling while upright but adds windage, guarding, elevated mass and capsize interactions. Both still depend on the hull, keel and rudder passing vegetation. Identical weed trials, including shutdown, clearing and restart, should reveal how much that distinction matters in practice.

The comparison also needs sailing drag, rig clearance, isolation, handling, corrosion, servicing and wet restart. I keep those tradeoffs linked to the [recovery obligation](requirements/requirements-energy.md#recovery-propulsion-and-reserves), [reserve](requirements/requirements-energy.md#recovery-propulsion-and-reserves), and [weed qualification](requirements/requirements-environment.md#weed-tolerance), so it stays clear which problem each test is answering.

Actual propeller data and installed measurements will decide the selection. The [source notes](../models/vehicle/source-evidence.sysml) retain the prior research and comparison rationale; [energy accounting](energy.md) and [recovery analysis](structures-and-recovery.md) explain how that choice affects the rest of the boat.


**Next:** [Construction and self-righting](structures-and-recovery.md).
