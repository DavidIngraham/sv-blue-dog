# Comparing recovery propulsion

**OOSEM:** Candidate physical architectures · [Maturity assessment](current-assessment.md)

If a trial goes wrong, I want a practical way to bring the boat back. Should that be a water propeller or an air propeller? This [preliminary-design trade](current-assessment.md#virtual-design) starts with resistance, weed exposure and the energy reserve, and should lead to an installed comparison of the two concepts. The motor is for testing and recovery, not the qualifying sailing attempt.

I want to compare both drives against the same installed recovery task. An ideal disk calculation can help estimate the scale of the problem, but it cannot tell me which installation will work better on this boat.

Selecting a [westerly challenge window](operating-constraints.md#gorge-weather-and-launch-windows) does not remove the need to recover after a reversal or calm. Both propulsor candidates must use the same declared current, windage and reserve conditions; winter trials need a separate applicable profile. A motor-assisted recovery remains an unsuccessful qualifying attempt, never extra sailing performance hidden in a probability average.

IC-01 allocates recovery power, observations, control and thrust independently of the primary sailing path. The targets are 1.5 m/s through the water upright and 0.5 m/s inverted, with 50 W and 40 W propulsion demand respectively, plus 8 W essentials. Its separate 60 Wh pack supplies that path. Those are simultaneous design targets, not tested propulsor performance. A single installation must either support both attitudes or explain the separate hardware and mass needed to do so.

| Question | Water propeller | Air propeller |
| --- | --- | --- |
| Installed thrust and energy | Test with actual immersion, inflow and guards | Test with actual duct/guard and boat windage |
| Vegetation | Rotor, shaft and guard may foul | Upright rotor avoids submerged weeds; hull and appendages still encounter them |
| Capsized operation | Establish whether rotor, intake and steering remain usable | Establish whether immersion disables the rotor or demands another arrangement |
| Sailing penalty | Appendage drag, sealing and installation volume | Windage, elevated mass, rig clearance and guarding |
| Casualty independence | Prove power, command and steering isolation | Prove the same independence, including wet restart |

My starting point will be a hull tow measurement and the required recovery conditions. Then I can bench each complete guarded drive and compare installed thrust, electrical power, temperature and maneuvering performance. The [native analysis](../models/analyses/recovery-propulsion.sysml) currently estimates reserve demand from illustrative inputs; those estimates help plan the experiment.

Water propulsion offers compact thrust but exposes the rotor and shaft to weeds. Air propulsion avoids submerged rotor fouling while upright but adds windage, guarding, elevated mass and capsize interactions. Both still depend on the hull, keel and rudder passing vegetation. Identical weed trials, including shutdown, clearing and restart, should reveal how much that distinction matters in practice.

The comparison also needs sailing drag, rig clearance, isolation, handling, corrosion, servicing and wet restart. I keep those tradeoffs linked to the [recovery obligation](requirements/requirements-energy.md#recovery-propulsion-and-reserves), [reserve](requirements/requirements-energy.md#recovery-propulsion-and-reserves), and [weed qualification](requirements/requirements-environment.md#weed-tolerance), so it stays clear which problem each test is answering.

Actual propeller data and installed measurements will decide the selection. The [source notes](../models/vehicle/source-evidence.sysml) retain the prior research and comparison rationale; [energy accounting](energy.md) and [recovery analysis](structures-and-recovery.md) explain how that choice affects the rest of the boat.



The [mission development spirals](simulation-spirals.md#carry-recovery-through-the-voyage) connect this component trade to position-dependent recovery authority and energy reserve.

**Next:** [Seeing hazards early enough to act](encounter-feasibility.md) · [Series guide](index.md)
