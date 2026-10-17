# SV Blue Dog: learning through an autonomous sailboat

**Introduction** · [Current assessment](current-assessment.md)

SV Blue Dog is my personal project to design and build a small autonomous sailboat that can travel from Bingen to buoy 16 near Stevenson and back without intervention, while I monitor it from shore. Longer term, I’d love to develop something capable of reaching Hawai‘i, as a separate mission with its own constraints. It brings together things I want to learn—sailing, desktop manufacturing and digital engineering—with the fun of building a complete robot that can look after itself on the water. The name comes from my blue heeler, Ozzy: another small, independent creature with plenty of energy and ideas of his own.

Microtransat—the challenge of sending an autonomous sailing boat across the Atlantic—gave me an idea for something closer to home: an even more micro “trans-gorge” boat.

My initial inspiration was the Gorge Blowout course. Adding a return journey made it a much more demanding challenge: the boat would have to sail both ways and make progress against the river current. For the current design, that finite round trip is the goal. A faster boat might tolerate a higher hourly failure rate and still be more likely to finish because it spends less time exposed; that [speed–reliability trade](reliability.md#can-a-faster-boat-be-more-likely-to-finish) is part of what makes the challenge interesting.

The shorter distance does not make every part of the problem easier. I expect traffic avoidance to be more demanding here than during the open-ocean portion of a Microtransat crossing: commercial traffic, recreational boats, paddlers, windsurfers, wingfoilers and kiters share a confined river corridor. Blue Dog has less room to resolve encounters, and some of those users move quickly or are difficult to detect. Ocean crossings have shipping lanes and busy coastal approaches too, but the Gorge puts shared-water navigation at the center of this first mission. I need to establish where and when that traffic concentrates through the [location and traffic assessment](site-and-environment-evidence.md#traffic-risk-by-location-and-arrival-window).

The picture in my head is the classic westerly Gorge day. With wind from the west, the outbound leg toward Stevenson is windward with the current; the return is downwind against it. I plan to choose a favorable weather window for the qualifying attempt, even though I also want to test in winter. Easterlies reverse that sailing problem and deserve much more attention in winter. The [seasonal weather study](operating-constraints.md#gorge-weather-and-launch-windows) now gives those cases an observed context, rather than treating every wind direction as equally representative. Year-round unattended operation remains a later goal.

![Map of the Columbia River Gorge challenge, from Bingen past Hood River to Stevenson, then back upstream.](figures/gorge-course-map.svg)

*The challenge follows the Columbia through the Gorge: downstream from Bingen to Stevenson, then back upstream. Water extent and course references: NOAA electronic navigational charts. [See the start/finish and turnaround in satellite views](architecture.md#start-finish-and-turnaround-in-shore-context).*

![Bingen–Stevenson round trip, with downstream current and a westerly wind.](figures/route-context.svg)

*With a westerly, the outbound leg is windward with the current; the return is downwind against it.*

## A maze of decisions

I began sketching a testbed in SolidWorks to reduce risk around manufacturing techniques, wing-sail design and ArduSail control systems. The [existing CAD](../cad/) comes from that work. It was supposed to help me learn how to print and assemble the boat, explore the rig and get the control system working. That separate testbed is no longer my build plan. My intended first boat is a refined version of the IC-01 integration candidate described below; focused component experiments will support that build.

![SolidWorks rendering of the testbed: a translucent slender hull, tall crescent wing with internal ribs, mast drive, sensor mast, and deep keel with ballast bulb.](figures/testbed-solidworks.png)

*My original manufacturing, wing-sail and control testbed, rendered from [the SolidWorks assembly](../cad/SV%20Bluedog.SLDASM).*

Then I got lost in the configuration decisions. A larger wing could provide more drive, but it also changed the loads, ballast, actuator and recovery problem. More battery could help endurance while making the hull heavier. Changing the hull changed the sailing performance I needed from the wing. I could make individual choices, but I struggled to manage the consequences across the whole design.

This is a surprisingly complex, high-performance system for something I hope will be small and inexpensive to manufacture. I was trying to push the edge of what was possible, and I stalled out.

## Using a model to get moving again

I realized that open-source tools and SysML v2 could give the project some structure. SysML is a systems modeling language: it lets me record requirements, component responsibilities, relationships and calculations in a connected model. That also made Blue Dog a good excuse to dive into digital engineering: could I connect the mission, requirements, architecture, analysis and eventual tests closely enough to make the next decision clearer?

I am especially interested in how that model can structure an agent-driven development project. Agents can help explore alternatives and implement analyses quickly. I still need a shared description of what I am trying to achieve, why a choice was made and what would count as convincing evidence. Otherwise, producing more analysis can simply make the maze bigger.

The [current assessment](current-assessment.md) connects the mission, requirements, architecture, analyses and experiments. I use it to understand what the evidence supports, where the gaps are and which question to tackle next. Those layers develop together as I learn more about the boat.

### Try the configuration decisions

This is the web of choices I was trying to hold in my head. Start with IC-01 and change its wing, hull or appendages. The sketch follows the geometry inputs; the other controls expose the construction and equipment assumptions that feed the full sizing analysis. Its rigid wing is the geometry used in this calculation, not a selected rig.

```design-explorer
{"src":"https://davidingraham.github.io/sv-blue-dog/assets/design-explorer/design.json"}
```

The interesting part is what the sketch cannot tell me on its own. More wing area changes drive and overturning loads. More ballast changes recovery, displacement and drag. A bigger battery changes available energy and the weight the hull has to carry. Those consequences have to agree in the same candidate.

The [sizing analysis](sizing.md) connects those choices: changing battery capacity changes mass, which changes the hull and sailing performance, which changes passage duration and energy demand. I use it to compare feasible configurations, then challenge them with [mission simulations](mission-simulation.md).

The applet lets you explore and save a proposed configuration. It does not run that coupled optimization in your browser, and a plausible-looking sketch is not a feasible design.

## The boat I intend to build

**IC-01 is my current working candidate.** I intend to refine a boat at this scale into the first physical build. It gives the whole system a concrete starting point while rig, sensors, processors and recovery hardware remain open choices.

| Configuration | Purpose | Dimensions and mass | Battery capacity |
| --- | --- | --- | --- |
| Earlier sizing reference | Explore nominal sailing and energy feasibility | 1.2 m overall length, 0.26 m beam, 10.3 kg | 440 Wh |
| IC-01 | Bring sensing, sailing, energy and independent recovery into one candidate | 1.2 m overall length, 0.42 m beam, 20.1 kg | 1,300 Wh main + 60 Wh recovery |

That change in scale tells an important part of the story. The lighter reference has only about 4 Wh of calculated energy headroom. Credible sensing and a separately powered recovery system add electrical demand and equipment mass; supporting them changes the battery, hull and sailing solution together. IC-01 has about 102 Wh of main-pack headroom under its declared passage assumptions. The [candidate results](results.md) explain the calculation and the alternatives still worth investigating.

Local simulations now exercise IC-01 sailing, avoiding encounters and recovering after failures. They give me a candidate to investigate, with the full Gorge voyage and physical boat still ahead. The [current assessment](current-assessment.md#integration-milestone) records the outcomes and their limits.

The next decisions depend on measurements: which rig works best across both tacks, what the sensing installation actually consumes, how the boat maneuvers, and whether its independent recovery path works after a casualty. I will use component experiments and progressively integrated trials to turn IC-01 into a buildable design. The [current assessment](current-assessment.md) identifies which evidence would change those decisions.

**Next:** [Mission, context and architecture](architecture.md) · [Series guide](index.md)
