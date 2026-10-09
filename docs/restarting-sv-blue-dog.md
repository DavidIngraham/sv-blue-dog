# SV Blue Dog: picking up a small sailing robot again

I wanted to explore how far I could get with autonomous sailing and desktop manufacturing. I wanted to learn about sailing, build something cool, and develop a complete system: the boat, the electronics, the controls, and the decisions that would let it look after itself.

The original inspiration was Microtransat. My version was an even more micro "trans-gorge" sailboat. Could I build a small robot that would complete the Gorge Blowout course? Could it go further, sailing from Bonneville to The Dalles and back?

That was the ambition behind SV Blue Dog. I am picking it up again with the original design notes and CAD, and returning to the questions that made me want to build it.

## What would a trans-gorge boat need to do?

I envisioned a robot I could "set and forget." I wanted to give it a mission and have it handle the sailing, manage its energy, and recover from the kinds of problems that would otherwise end the trip.

The round-trip idea gave me a concrete mission to think about. Getting somewhere was only part of it; I wanted the boat to bring itself back. How small could I make a system capable of that? What would I need to understand about sailing to make good decisions about the hull, rig, and controller?

Those questions were part of the appeal. This was a way to learn about sailing by trying to build something that could do it for itself.

## How much of the boat could I make on a desktop?

Desktop manufacturing was central to the idea. My December 2023 notes describe a one-metre monohull with a printable hull, a fin keel, and a ballast bulb. I wanted to balance efficiency and reliability with something I could actually manufacture.

I set an ambitious target for the frame: a bill of materials below $100 and less than four hours of labour. That was a design target for the frame, not a measured cost for a finished boat. The notes also call for a printable hull cross-section of 250 by 250, although I still need to confirm the units against the CAD.

The [CAD files](../cad/) include hull sections, boat and mast assemblies, a keel shell, and several sail or wing variants. That is the design work I am returning to. The next step is to sort through those alternatives and establish which configuration to carry forward.

## What does "set and forget" ask of the design?

That ambition shows up clearly in the failure cases I wrote down. The boat should right itself from a fully inverted position, resist catching weeds, and recover from a software reset. A small hull breach had a proposed response: a bilge pump. Battery exhaustion had another: a low-energy "limp mode."

Each of those ideas opens up a more specific question. What should the boat keep doing when energy runs low? What does it need to remember after a reset? How would it detect water ingress, and what could it recover from? Self-righting also needs to become a demonstrated property of the boat and rig together.

My notes include communication and COLREGs compliance as goals, too. These are still design questions to work through; the brief records what I wanted the system to handle, rather than results showing that it can.

## Bringing the whole system together

The electronics sketch separates the autopilot, communications, AIS, and air-data functions. It includes an STM32 H7-based autopilot concept, inertial and magnetic sensing, GNSS, logging, battery monitoring, and energy harvesting. CAN appears in both the autopilot and air-data board notes. I also considered cellular communication and a possible RockBLOCK satellite modem.

The detailed candidate parts are in the [project notes](project-status.md). What interests me now is how those pieces fit together: what information the boat needs to sail, how it uses that information, and how much energy it takes to keep the whole system running. The hardware list was a starting point for that work.

## Could it do something useful while it was out there?

I also liked the possibility of collecting interesting data. One idea was a persistent swell monitor: could the boat keep station in an area and measure conditions over time?

That adds another question to the journey. Completing a course gives the robot a destination; monitoring asks it to stay somewhere useful. I would need to work out what station keeping means for this boat, what measurements would be useful, and how to interpret them from a moving platform. For now, it is a possibility I want to explore.

## Picking up the thread

The original motivation still holds: learn about sailing, see what I can make with desktop tools, and bring a complete autonomous system together. The trans-gorge mission gives that work a direction, and the swell-monitor idea gives me another reason to keep thinking about endurance and station keeping.

I am starting by revisiting the CAD and the old requirements, documenting the current build status, and choosing the next questions to test. This is where I will keep the journey: the designs I try, the things I learn, and how those results change the boat.
