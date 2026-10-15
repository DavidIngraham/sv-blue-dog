# Developing the mission simulation in spirals

**OOSEM:** Mission, architecture, analysis and evidence · [Current maturity](development-plan.md) · [Simulation methods](mission-simulation.md)

I want to understand how a small autonomous sailboat can complete the Gorge round trip, and what would stop it. Answering that takes more than a detailed model of any one component. The boat has to make progress, avoid traffic, manage its energy and retain a way to recover, all in the same voyage.

I develop that understanding in spirals. Each pass starts with a question the present simulation cannot answer well enough. I refine the relevant behavior or physics, exercise it in a mission, and use the result to choose the next question. The model grows alongside the simulator: requirements become more observable, architecture responsibilities become more explicit, and predictions acquire identifiable assumptions and evidence.

The development from 9–15 October 2026 gives concrete examples of this pattern. These are overlapping investigations, with different boats and environmental assumptions in different studies. Their results belong to those configurations; they are not successive scores for one unchanged vessel.

## Establish the mission and a plausible boat

The first pass connected the challenge to a vehicle architecture and testable obligations. Course completion, autonomous operation, recovery, construction and energy gave the design a purpose. Coupled sizing then connected wing forces, underwater appendages, hull resistance, mass, structure and power. That made it possible to ask whether a candidate could balance its sailing loads and make progress under declared conditions. [Mission and architecture](https://github.com/DavidIngraham/sv-blue-dog/commit/6c5cf06), [coupled design search](https://github.com/DavidIngraham/sv-blue-dog/commit/f4e795c).

Those calculations are valuable, but a balanced operating point is only one moment in a voyage. A boat can have enough drive in a representative wind and still run out of room to tack, lose its energy margin while waiting, or encounter conditions outside its performance model. That is the question the next pass takes on: can the design's separate capabilities work together over time?

## Put the boat on a course and a clock

The mission simulation introduced chart-constrained navigation, ordered gate crossings, changing weather, traffic and chronological energy use. It began with a conceptual sailing-performance model and equipment budget so that the mission behavior could be exercised before a detailed boat was ready. A run could distinguish completion, intervention, unsafe behavior, an incomplete attempt and a computational horizon. [Initial voyage simulation](https://github.com/DavidIngraham/sv-blue-dog/commit/f178e5c).

Timing became part of the model's credibility. Steering updates and maneuver delays have their own durations; reducing the numerical integration step must not give the boat faster reactions. The timing checks preserve that distinction and apply an intervention at its actual time between samples. This lets a finer calculation test the same controller rather than silently improve it. [Guidance and maneuver timing](https://github.com/DavidIngraham/sv-blue-dog/commit/c4b1887).

The Bingen–Stevenson course added a port rounding of buoy 16, represented by ordered checkpoints. In the archived 32-voyage conceptual campaign, three runs reached the computational horizon after crossing the north and west checkpoints without completing the south crossing. That is a specific question about local guidance around a mark. It tells me more about what to investigate than an aggregate completion fraction alone. The recorded voyages also retain their chart and course configuration, so later route refinements do not change what those results mean. [Rounding geometry](https://github.com/DavidIngraham/sv-blue-dog/commit/845d701), [recorded campaign](../evidence/runs/2026-10-12-bingen-mission/mission-campaign.json).

## Make the voyage depend on the candidate

The next connection was between the boat being sized and the boat being sailed in simulation. Candidate geometry and solved sailing states supply a bounded performance envelope. Storage, electrical demand, solar area and vessel dimensions travel with that candidate. A larger battery can improve endurance while also increasing mass and changing the sailing solution; the voyage needs to reflect both effects. [Candidate mission capability](https://github.com/DavidIngraham/sv-blue-dog/commit/4480731).

This adds fidelity and traceability together. A passage prediction can be followed back to a particular candidate and its operating solutions. It also makes the limits more visible: an averaged combination of solved sailing states is not a measured polar or a resolved tack. Outside the solved wind range, the model cannot simply invent sailing performance. A coverage gap becomes a reason to extend the analysis or collect measurements, rather than an unexplained failure of the boat. [Performance coverage](https://github.com/DavidIngraham/sv-blue-dog/commit/79de537), [candidate representation](mission-simulation.md#connecting-a-sizing-candidate).

## Let the environment act on the whole boat

Uniform wind and calm water leave out important effects for a small vessel. The environmental studies introduce wind varying with height, directional waves, current interaction and wakes. Wave-motion studies then ask how the moving wing sees the wind and how the hull and appendages move relative to the water. Those questions connect the operating environment to forces, clearance and control demands. [Wind and wave sensitivity](https://github.com/DavidIngraham/sv-blue-dog/commit/a342847), [motion and wing loads](https://github.com/DavidIngraham/sv-blue-dog/commit/86b51c0).

Paired scenarios help isolate an assumption. The archived environmental replay holds the candidate geometry fixed and uses the same weather and traffic seeds across different environmental representations. At 5 m/s reference wind, the 1.4 m candidate's modeled downwind velocity made good through the water falls from about 1.19 m/s in uniform wind to 0.66 m/s with the height-dependent profile. That identifies a consequential aerodynamic assumption. Voyage duration is less straightforward: changed motion changes when the boat encounters later weather and the rounding mark. Identical random inputs do not imply identical experiences along two different trajectories. [Environmental replay and comparison](mission-simulation.md#current-sizing-candidate-replay).

Calculated wave response adds another level. Heave, roll and pitch affect apparent wind, underwater inflow, loads and power; the sailing calculation seeks a balance over the wave cycle. The archived study accepted 32 operating cases for regular waves 0.04 m high with a 3 s period. Its four Gorge replays stopped at departure because their requested conditions lay outside that small-wave performance coverage. [Calculated wave response](https://github.com/DavidIngraham/sv-blue-dog/commit/8f6f098), [operating and mission evidence](../evidence/runs/2026-10-13-wave-performance/summary.json).

That is useful progress even though it does not produce a passage time. The model can identify which question it has answered and where a mission asks for more. Extending the usable range needs evidence about the sea conditions and vessel response; adding more sample points alone cannot establish that the underlying physics is applicable.

## Carry recovery through the voyage

Recovery changes the meaning of available energy. A fixed battery reserve cannot describe every position, current or casualty. The recovery model evaluates a route to a shore approach, the propulsion authority against the current, the transit energy and a declared allowance. Capsized capability is a separate input. The mission can terminate sailing before continuing would consume the recovery margin. [Recovery behavior and tests](https://github.com/DavidIngraham/sv-blue-dog/blob/9df1808/tests/test_course_recovery.py).

This makes the safety obligation observable in a scenario: where was the boat, what recovery remained reachable, why did it abort, and what happened during the transit? Tests exercise recovery without communications and retain traffic in the consequence calculation even when onboard sensing is unavailable. The present recovery fixtures use synthetic sites and capabilities. Surveyed approaches, measured propulsion and actual pickup conditions are the evidence needed to carry those conclusions into a real voyage. [Recovery assessment](srr-appendix.md#course-and-recovery-decision).

## Give decisions an executable meaning

The logical scenarios connect normal sailing, traffic encounters and abort/recovery to the boat's responsibilities. Executable supervisory behavior makes part of that architecture act within the mission simulation. A lost wind observation inhibits sailing. Communications loss alone leaves autonomy running. A safety abort remains latched, and queuing an alert does not delay recovery. [Allocated scenarios](https://github.com/DavidIngraham/sv-blue-dog/commit/8defcd1), [executable supervisor](https://github.com/DavidIngraham/sv-blue-dog/commit/d460f52).

The value is that I can follow a decision as well as a trajectory. The mission records the facts presented to the supervisor and the resulting decisions. Losing access to a weather service, for example, is different from deciding that the held forecast is no longer applicable. One preserves the attempt; the other initiates abort and recovery. That distinction can be exercised and inspected. [Forecast scenarios](https://github.com/DavidIngraham/sv-blue-dog/commit/7530eca).

The supervisor covers mission policy. The simulation still supplies conceptual heading search, traffic geometry and vessel dynamics, and its scripted traffic is perfectly observed. The next behavioral questions concern uncertain observations, delayed decisions and maneuvers that the actual boat can execute. The [current logical execution](mission-simulation.md#executable-supervisory-logic) describes that boundary.

## Keep the evidence connected through every spiral

For me, fidelity means representing the effects that matter to a decision with enough accuracy. Traceability means being able to explain which mission obligation, design, assumptions and evidence produced the conclusion. A more detailed model can strengthen one part of that chain while exposing a weakness in another.

| Question about a result | What I need to retain |
| --- | --- |
| What counted as success? | Mission conditions, course definition and observable outcome criteria |
| Which boat was evaluated? | Geometry, equipment, storage and performance configuration |
| What did it encounter? | Environmental assumptions, traffic realization, injected events and random seeds |
| Why did it act that way? | Observations, supervisory decisions, maneuver history and stopping cause |
| Where does the conclusion apply? | Model revision, source evidence, numerical checks and coverage limits |

The [archived-run provenance](https://github.com/DavidIngraham/sv-blue-dog/commit/e80e46d) preserves the identity of each experiment. Comparing spirals means comparing identifiable configurations and assumptions. A new course, different candidate or changed sea model needs an explicit comparison before a difference in outcomes can be attributed to one improvement.

The next spirals should connect measurements to the mission: wing and actuator tests to sailing and maneuver predictions; installed loads and battery tests to endurance; sensor replay and site surveys to traffic decisions and recovery. Each experiment should have a predicted observable and a decision it could change. I then replay the affected missions and update the [maturity assessment](development-plan.md) according to the evidence, including results that narrow the boat's usable envelope.

The aim is a progressively better explanation of what Blue Dog can do, under which conditions, and why I believe it.

**Continue:** [Mission simulation methods](mission-simulation.md) · [Evidence and physical experiments](validation-plan.md)
