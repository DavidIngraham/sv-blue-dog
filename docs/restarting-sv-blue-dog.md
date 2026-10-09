# SV Blue Dog: picking up a small sailing robot again

Draft for review. Based on the OneNote design brief dated December 26, 2023, revisited October 9, 2026.

SV Blue Dog started with a balancing act: efficiency, reliability, and ease of manufacture. My original notes describe a one-metre sailing robot with a printable hull, a ballasted fin keel, and a strong emphasis on low power consumption. I am picking the project up again, beginning with those requirements and the CAD work already collected.

## Start with the boat

The design brief calls for a monohull that can right itself from a fully inverted position and resist catching weeds. It specifies a sealed hull, a fin keel with a ballast bulb, and a printable hull cross-section of 250 by 250. The notes do not give units for that cross-section; that needs checking against the CAD before it becomes a manufacturing requirement.

The manufacturing target was deliberately ambitious: a frame bill of materials below $100 and less than four hours of labour. That is the target written in the notes, not a measured cost or a budget for the complete boat and its electronics.

The existing CAD folder includes the main boat and mast assemblies, hull sections, a keel shell, and several sail or wing design files. Those files give me something concrete to return to. Their presence alone does not establish which design was selected, printed, assembled, or tested.

## Design around things going wrong

The most useful part of the old brief is its list of expected failures. A small hull breach should have a recovery path, with a bilge pump listed as the proposed response. Battery exhaustion should lead to a low-energy "limp mode." A software reset should also be something the system can recover from.

Those are requirements to make specific and test. What remains powered in limp mode? What state does the controller recover after a reset? How much water can the boat tolerate, and how is it detected? The old notes identify the problems without yet documenting the answers.

Communication and COLREGs compliance also appear as goals. The brief does not document an implemented collision-avoidance system or evidence of compliance.

## The electronics sketch

The proposed architecture separates the autopilot, communications, AIS, and air-data functions. The autopilot list includes an STM32 H7, a CAN transceiver, an inertial sensor, an RM3100 magnetometer, an SD card, battery monitoring, an LT3652 energy harvester, an 18650 holder, a u-blox M10Q, an ExpressLRS/LoRa receiver with ESP32, and a light controller.

The communications notes name a possible RockBLOCK 9603N and a u-blox cellular modem. Separate lists cover an AIS board and an air-data board, the latter with an STM32 L4, CAN, an AS5048B, and a hot-wire anemometer.

This is a record of candidate hardware from 2023. It is useful context for restarting the design, but it is not a final bill of materials. The next revision needs a power budget and a clearer account of what each subsystem must do before those choices become commitments.

## Picking it up again

The first step is to establish the actual baseline: which CAD assembly is current, what physical hardware exists, and what testing has already happened. From there, I want to turn the brief into a small set of measurable checks: hull mass and buoyancy, recovery from inversion, sealing and water ingress, and energy use in normal operation and recovery modes.

The project notes and this write-up will live as Markdown in the source repository. My website can read that material through its existing publication manifest, keeping the article close to the design work as it develops.

For now, the recovered brief gives the project a clear direction. The next update should connect those intentions to the hardware and measurements that actually exist.

---

Source: personal OneNote page "SV Blue Dog," dated December 26, 2023, supplied as a two-page PDF. The export contains a reference photograph labeled "Sailbotix silicon sailor"; it is not presented here as a photograph of SV Blue Dog. Proposed restart steps above are new editorial suggestions, not recorded test results.
