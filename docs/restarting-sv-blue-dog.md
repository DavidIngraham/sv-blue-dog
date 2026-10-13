# SV Blue Dog: learning through an autonomous sailboat

**Design phase:** Introduction · [Development plan](development-plan.md)

SV Blue Dog is my personal project to design and build a small autonomous sailboat that can travel from Bingen to buoy 16 near Stevenson and back without intervention, while I monitor it from shore. Longer term, I’d love to develop something capable of reaching Hawai‘i, as a separate mission with its own constraints. It brings together things I want to learn—sailing, desktop manufacturing and digital engineering—with the fun of building a complete robot that can look after itself on the water. The name comes from my blue heeler, Ozzy: another small, independent creature with plenty of energy and ideas of his own.

I started this project because I wanted to explore the limits of autonomous sailing and desktop manufacturing. I wanted to learn about sailing, build something cool, and develop a complete system. Microtransat—the challenge of sending an autonomous sailing boat across the Atlantic—gave me an idea for something closer to home: an even more micro “trans-gorge” boat.

My initial inspiration was the Gorge Blowout course. Adding a return journey made it a much more demanding challenge: the boat would have to sail both ways and make progress against the river current. For the current design, that finite round trip is the goal. A faster boat might tolerate a higher hourly failure rate and still be more likely to finish because it spends less time exposed; that [speed–reliability trade](reliability.md#can-a-faster-boat-be-more-likely-to-finish) is part of what makes the challenge interesting.

The picture in my head is the classic westerly Gorge day. With wind from the west, the outbound leg toward Stevenson is windward with the current; the return is downwind against it. I plan to choose a favorable weather window for the qualifying attempt, even though I also want to test in winter. Easterlies reverse that sailing problem and deserve much more attention in winter. The [seasonal weather study](operating-constraints.md#gorge-weather-and-launch-windows) now gives those cases an observed context, rather than treating every wind direction as equally representative. Year-round unattended operation remains a later goal.

![Map of the Columbia River Gorge challenge, from Bingen past Hood River to Stevenson, then back upstream.](figures/gorge-course-map.svg)

*The challenge follows the Columbia through the Gorge: downstream from Bingen to Stevenson, then back upstream. River geometry: [OpenStreetMap contributors](https://www.openstreetmap.org/copyright). [Explore the area](https://www.openstreetmap.org/#map=11/45.68/-121.55).*

![Bingen–Stevenson round trip, with downstream current and a westerly wind.](figures/route-context.svg)

*With a westerly, the outbound leg is windward with the current; the return is downwind against it.*

## A testbed, then a maze of decisions

I began sketching a testbed in SolidWorks to reduce risk around manufacturing techniques, wing-sail design and ArduSail control systems. The [existing CAD](../cad/) comes from that work. It was supposed to help me learn how to print and assemble the boat, explore the rig and get the control system working. It was never intended to be the final challenge vessel.

![SolidWorks rendering of the testbed: a translucent slender hull, tall crescent wing with internal ribs, mast drive, sensor mast, and deep keel with ballast bulb.](figures/testbed-solidworks.png)

*My original manufacturing, wing-sail and control testbed, rendered from [the SolidWorks assembly](../cad/SV%20Bluedog.SLDASM).*

Then I got lost in the configuration decisions. A larger wing could provide more drive, but it also changed the loads, ballast, actuator and recovery problem. More battery could help endurance while making the hull heavier. Changing the hull changed the sailing performance I needed from the wing. I could make individual choices, but I struggled to manage the consequences across the whole design.

This is a surprisingly complex, high-performance system for something I hope will be small and inexpensive to manufacture. I was trying to push the edge of what was possible, and I stalled out.

### Try the configuration decisions

This is the web of choices I was trying to hold in my head. Start with the recorded 1.2 m sizing candidate and change its wing, hull or appendages. The sketch follows the geometry inputs; the other controls expose the construction and equipment assumptions that feed the full sizing analysis.

```design-explorer
{"src":"https://davidingraham.github.io/sv-blue-dog/assets/design-explorer/design.json"}
```

The interesting part is what the sketch cannot tell me on its own. More wing area changes drive and overturning loads. More ballast changes recovery, displacement and drag. A bigger battery changes available energy and the weight the hull has to carry. Those consequences have to agree in the same candidate.

The optimizer starts from a candidate, builds its geometry, and uses native SysML calculations for mass, loads, power and requirement margins. SciPy adjusts the design and the sailing controls to balance surge, side force, yaw and roll across both tacks, upwind and downwind, at the study wind speeds. It checks structural, handling, recovery, course-progress and finite-passage energy constraints alongside that balance.

The current search sweeps overall-length caps while keeping all 29 design variables and 48 operating-state values free. It optimizes mass and conditional passage time separately and retains feasible alternatives for a design decision. The first bounded run retains a 1.2 m candidate, but its refined replay still misses the energy allocation slightly; the smaller searches remain unresolved. Finer geometry, recovery assessment and mission simulation challenge every candidate. Failure to find a solution is a reason to investigate the constraints and search, not proof that no boat of that size can work. The [sizing method](sizing.md) and [current results](results.md) carry the details.

The applet lets you explore and save a proposed configuration. It does not run that coupled optimization in your browser, and a plausible-looking sketch is not a feasible design.

## Using a model to get moving again

I realized that open-source tools and SysML v2 could give the project some structure. That also made Blue Dog a good excuse to dive into digital engineering: could I connect the mission, requirements, architecture, analysis and eventual tests closely enough to make the next decision clearer?

I am especially interested in how that model can structure an agent-driven development project. Agents can help explore alternatives and implement analyses quickly. I still need a shared description of what we are trying to achieve, why a choice was made and what would count as convincing evidence. Otherwise, producing more analysis can simply make the maze bigger.

The [development plan](development-plan.md) gives the project a path from the challenge definition to a boat on the water. At each stage, it identifies the decisions to make, the analyses or tests needed to support them, and what needs to be resolved before moving on. I use that structure to guide both my own work and the tasks I give agents, revisiting earlier decisions as simulations and experiments reveal more about the design.

## Where the project stands

I now have a challenge definition, a connected requirements and architecture model, and a coupled sizing study. The current numerical trial can satisfy the primary modeled sailing and energy screens, but handling, adverse conditions and self-righting still need work. It has not established a minimum-size design. The [results article](results.md) explains those findings and what they suggest testing next.

That feels like useful progress: I can see which assumptions are driving the design and which experiments could change the answer. The next step is to use the testbed and focused measurements to improve those assumptions, then revisit the sizing decisions with better evidence.

**Next:** [The mission and the boat’s responsibilities](architecture.md), then [the development plan](development-plan.md). The [series guide](index.md) separates the main reading path from the technical reference pages.
