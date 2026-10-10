# SV Blue Dog: learning through an autonomous sailboat

I started Blue Dog to explore how far autonomous sailing and desktop manufacturing could go together. I wanted to learn about sailing, build something interesting, and develop a complete system rather than an isolated mechanism.

Microtransat was the inspiration. My smaller version was a “trans-gorge” boat: first the Gorge Blowout idea, then a journey from The Dalles to Bonneville and back. The longer-term ambition is Hawaii. The Gorge is a demanding place to learn about the system; completing a river challenge would not by itself establish ocean readiness.

## Build the process around the mission

I keep the [challenge brief](challenge-brief.md) independent of the vehicle design. That prevents a convenient hardware choice from quietly changing what success means. The [design guide](design-guide.md) follows the current chain from mission to requirements, architecture, analysis and verification.

The existing [CAD](../cad/) is a separate manufacturing and wing-sail testbed. It helps explore what I can print and assemble, but is not a claim that the challenge boat has been designed or qualified. One of the project goals is learning SysML v2 by making these distinctions explicit.

## Ask what “set and forget” requires

Live observation, autonomy, energy, weeds, traffic and recovery all interact. I use [small requirement views](requirements-views.md) to follow individual derivations, and [architecture traceability](traceability.md) to show intended responsibilities. Requirement statements stay concise; [conditions, rationale, issues and verification plans](requirements-context.md) are published separately from the same model.

The [energy model](sustained-operations.md) asks whether loads, storage and harvesting support a declared profile. The [recovery propulsion trade](recovery-propulsion-trade.md) compares water and air propellers without pretending an energy calculation alone selects the design. The [cruise/reliability analysis](cruise-reliability.md) makes the cost of a slow passage explicit: every extra hour asks the boat to keep working longer.

I am also [working backward from the mission to the required sailing polar](sailing-performance.md), checking what that demand means for a small displacement hull or a higher-speed concept.

The [architecture DFMEA](dfmea.md) identifies ways those functions can fail and the evidence needed to address them. A persistent swell-monitoring role is a possible future use, not a replacement for the sailing mission.

## Let evidence change the design

The model is a way to make assumptions inspectable. Generated results show what the current inputs imply; they are not physical test results. I want measured sailing performance, manufacturing trials and fault tests to refine those assumptions. The current model and its open issues are linked above, so this article can explain the journey without becoming another requirements document.
