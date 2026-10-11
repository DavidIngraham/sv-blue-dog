# SV Blue Dog: learning through an autonomous sailboat

I started Blue Dog to explore how far autonomous sailing and desktop manufacturing could go together. I wanted to learn about sailing, build something interesting, and develop a complete system rather than an isolated mechanism.

Microtransat was the inspiration. My smaller version was a “trans-gorge” boat: first the Gorge Blowout idea, then a journey from The Dalles to Bonneville and back. The longer-term ambition is Hawaii. The Gorge is a demanding place to learn about the system; completing a river challenge would not by itself establish ocean readiness.

## Build the process around the mission

I keep the [challenge brief](architecture.md) independent of the vehicle design. That prevents a convenient hardware choice from quietly changing what success means. The [design guide](index.md) follows the current chain from mission to requirements, architecture, analysis and verification.

The existing [CAD](../cad/) is a separate manufacturing and wing-sail testbed. It helps explore what I can print and assemble, but is not a claim that the challenge boat has been designed or qualified. One of the project goals is learning SysML v2 by making these distinctions explicit.

## Ask what “set and forget” requires

Live observation, autonomy, energy, weeds, traffic and recovery all interact. I use [small requirement views](requirements.md) to follow individual derivations, and [architecture traceability](architecture.md) to show intended responsibilities. Requirement statements stay concise; [conditions, rationale, issues and verification plans](methods/modeling.md) remain distinct fields in the authoritative model.

The [energy model](energy.md) asks whether loads, storage and harvesting support a declared profile. The [recovery propulsion trade](recovery-propulsion.md) compares water and air propellers without pretending an energy calculation alone selects the design. The [cruise/reliability analysis](reliability.md) makes the cost of a slow passage explicit: every extra hour asks the boat to keep working longer.

I am also [working backward from the mission to the required sailing polar](sizing.md), checking what that demand means for a small displacement hull or a higher-speed concept.

The [architecture DFMEA](reliability.md) identifies ways those functions can fail and the evidence needed to address them. A persistent swell-monitoring role is a possible future use, not a replacement for the sailing mission.

## Let evidence change the design

I am using the CAD-derived fixed-camber wing to explore the [coupled sizing problem](sizing.md), with hull dimensions, ballast, appendages, structure and energy changing together. OpenVSP/VSPAERO helps reveal finite-wing and heel sensitivities, but it cannot supply validated low-Reynolds-number performance for this rounded-edge section. The heel sweeps also show that a simple cosine correction is incomplete.

That changes how I use the optimizer: the primary case now credits less lift, assumes more drag, treats actuator moment independently, and restricts incidence and heel. The assumptions are explicit in SysML. The rerun reached a near-feasible trial but missed the coarse solver tolerance, so it did not establish a minimum length. I then test that geometry under further adverse scenarios and free-pitch recovery. The [generated results](results.md) distinguish a numerical candidate from a design supported by evidence; a solver failure is not proof that the boat is impossible.

The finer primary replay can balance sailing and energy and meet the modeled route target, but the handling allocation is still exceeded, additional aerodynamic degradation loses upstream performance, and the recovery studies do not establish self-righting. That makes the next evidence needs concrete. Generated results show what the current inputs imply; they are not physical test results. I want measured sailing performance, manufacturing trials and fault tests to refine those assumptions. The current model and its open issues are linked above, so this article can explain the journey without becoming another requirements document.
