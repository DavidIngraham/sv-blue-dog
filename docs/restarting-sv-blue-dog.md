# SV Blue Dog: learning through an autonomous sailboat

Blue Dog is named after my blue heeler, Ozzy. I like the thought of a small, independent creature puttering around the surface of a river or the ocean. Building something with a little of that character is part of the fun.

I started this project because I wanted to explore the limits of autonomous sailing and desktop manufacturing. I wanted to learn about sailing, build something cool, and develop a complete system. Microtransat—the challenge of sending an autonomous sailing boat across the Atlantic—gave me an idea for something closer to home: an even more micro “trans-gorge” boat.

My initial inspiration was the Gorge Blowout course. The challenge I eventually set myself was a journey from The Dalles to Bonneville and back, without intervention but with live monitoring. Beyond that, I would love to work toward a boat that could reach Hawai‘i. The Gorge would be a demanding proving ground along the way.

![Route schematic: start at The Dalles, sail downstream toward Bonneville, then return upstream against the current. The ocean ambition is a later development effort.](figures/route-context.svg)

*This is a route-orientation sketch, not a navigation chart. The upstream return is what makes “a little boat that sails itself” a much harder sizing problem. The model defines the challenge gates; launch locations and operational permissions need their own planning.*

## A testbed, then a maze of decisions

I began sketching a testbed in SolidWorks to reduce risk around manufacturing techniques, wing-sail design and ArduSail control systems. The [existing CAD](../cad/) comes from that work. It was supposed to help me learn how to print and assemble the boat, explore the rig and get the control system working. It was never intended to be the final challenge vessel.

Then I got lost in the configuration decisions. A larger wing could provide more drive, but it also changed the loads, ballast, actuator and recovery problem. More battery could help endurance while making the hull heavier. Changing the hull changed the sailing performance I needed from the wing. I could make individual choices, but I struggled to manage the consequences across the whole design.

This is a surprisingly complex, high-performance system for something I hope will be small and inexpensive to manufacture. I was trying to push the edge of what was possible, and I stalled out.

![Conceptual arrangement of an autonomous sailboat showing wing, hull, rudder, keel and ballast, solar collection, electronics and recovery propulsion. This is an explanatory sketch, not the SolidWorks testbed or an optimized design.](figures/boat-concept.svg)

*The parts are easy to name; choosing them together is the difficult bit. Their positions here are illustrative, including the unresolved recovery-propulsor installation.*

## Using a model to get moving again

I realized that open-source tools and SysML v2 could give the project some structure. That also made Blue Dog a good excuse to dive into digital engineering: could I connect the mission, requirements, architecture, analysis and eventual tests closely enough to make the next decision clearer?

I am especially interested in how that model can structure an agent-driven development project. Agents can help explore alternatives and implement analyses quickly. I still need a shared description of what we are trying to achieve, why a choice was made and what would count as convincing evidence. Otherwise, producing more analysis can simply make the maze bigger.

The [development plan](development-plan.md) is my way of keeping that work directed. I use “I” for my goals and design judgments; when I describe work with agents, they help develop and check the engineering record, while I make the commitment decisions. The model is the shared record, not a substitute for that judgment or for testing a real boat.

## Where the project stands

I now have a challenge definition, a connected requirements and architecture model, and a coupled sizing study. The current numerical trial can satisfy the primary modeled sailing and energy screens, but handling, adverse conditions and self-righting still need work. It has not established a minimum-size design. The [results article](results.md) explains those findings and what they suggest testing next.

That feels like useful progress: I can see which assumptions are driving the design and which experiments could change the answer. The next step is to use the testbed and focused measurements to improve those assumptions, then revisit the sizing decisions with better evidence.

**Next:** [The mission and the boat’s responsibilities](architecture.md), then [the development plan](development-plan.md). The [series guide](index.md) separates the main reading path from the technical reference pages.
