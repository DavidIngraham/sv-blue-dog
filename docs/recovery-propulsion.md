# Comparing recovery propulsion

**OOSEM:** Candidate physical architectures · [Current assessment](current-assessment.md)

If a trial goes wrong, I want a practical way to bring the boat back. Should that be a water propeller or an air propeller? This [preliminary-design trade](current-assessment.md#virtual-design) starts with resistance, weed exposure and the energy reserve, and should lead to an installed comparison of the two concepts. The motor is for testing and recovery, not the qualifying sailing attempt.

I will compare both installations against the same recovery task: the same current, windage, distance and usable battery energy, including a reversal or calm after launch. A motor-assisted recovery ends qualification for the sailing attempt.

IC-01 allocates recovery power, observations, control and thrust independently of the primary sailing path. The targets are 1.5 m/s through the water upright and 0.5 m/s inverted, with 50 W and 40 W propulsion demand respectively, plus 8 W essentials. Its separate 60 Wh pack supplies that path. Those are simultaneous design targets, not tested propulsor performance. A single installation must either support both attitudes or explain the separate hardware and mass needed to do so.

| Question | Water propeller | Air propeller |
| --- | --- | --- |
| Installed thrust and energy | Test with actual immersion, inflow and guards | Test with actual duct/guard and boat windage |
| Vegetation | Rotor, shaft and guard may foul | Upright rotor avoids submerged weeds; hull and appendages still encounter them |
| Capsized operation | Establish whether rotor, intake and steering remain usable | Establish whether immersion disables the rotor or demands another arrangement |
| Sailing penalty | Appendage drag, sealing and installation volume | Windage, elevated mass, rig clearance and guarding |
| Casualty independence | Prove power, command and steering isolation | Prove the same independence, including wet restart |

## Measure the complete installation

I will start by towing the hull to measure the force needed at the recovery speeds. Each complete guarded drive then needs thrust, electrical power and temperature measurements, followed by maneuvering tests upright and inverted. The [native analysis](../models/analyses/recovery-propulsion.sysml) estimates reserve demand from illustrative inputs to help plan those tests.

The same weed trials must include contact, shutdown, clearing and restart. An air rotor may avoid submerged vegetation while upright, but it does not protect the hull, keel or rudder from fouling. Fault tests must also establish that recovery still starts, observes and steers after the primary path loses power or control.

Finally I will include the installation's sailing drag or windage, rig clearance, mass, guarding, corrosion, servicing and handling. Those results connect the [recovery and reserve requirements](requirements/requirements-energy.md#recovery-propulsion-and-reserves) and [weed requirement](requirements/requirements-environment.md#weed-tolerance) to an actual equipment choice.

Actual propeller data and installed measurements will decide the selection. The [source notes](../models/vehicle/source-evidence.sysml) retain the prior research and comparison rationale; [energy accounting](energy.md) and [recovery analysis](structures-and-recovery.md) explain how that choice affects the rest of the boat.

The [mission development spirals](simulation-spirals.md#carry-recovery-through-the-voyage) connect this component trade to position-dependent recovery authority and energy reserve.

**Next:** [Seeing hazards early enough to act](encounter-feasibility.md) · [Series guide](index.md)
