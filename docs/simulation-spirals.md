# Developing the mission simulation in spirals

**OOSEM:** Mission, architecture, analysis and evidence · [Current assessment](current-assessment.md) · [Simulation methods](mission-simulation.md)

I want to understand how a small autonomous sailboat can complete the Gorge round trip, and what would stop it. Answering that takes more than a detailed model of any one component. The boat has to make progress, avoid traffic, manage its energy and retain a way to recover, all in the same voyage.

I develop that understanding in spirals. Each pass starts with a question the present simulation cannot answer well enough. I refine the relevant behavior or physics, exercise it in a mission, and use the result to choose the next question. The model grows alongside the simulator: requirements become more observable, architecture responsibilities become more explicit, and predictions acquire identifiable assumptions and evidence.

A working configuration lets me investigate coupled behavior while architectural choices remain open. I need to say what I assumed, what that assumption let me calculate, and what would make me revisit it. Trade studies develop alongside the simulation: they supply candidates to exercise, and the mission exposes consequences that a component comparison cannot show.

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

## Develop the trades alongside the voyage

The [sail architecture trade](sail-trade.md) compares a tail-controlled wing, a directly rotated fixed-camber wing and a soft sail. The fixed-camber wing gives the coupled sizing study a concrete geometry, force model and actuation problem. Using it for an experiment does not settle the rig choice. The comparison still needs both-tack performance, trim energy, durability and casualty behavior on comparable terms. [Initial sail trade](https://github.com/DavidIngraham/sv-blue-dog/commit/73f04bb).

Aerodynamic experiments made progress by changing what performance I was willing to credit. Mesh and heel studies exposed sensitivity in the force predictions, leading to a restricted operating domain and explicit conservative aerodynamic assumptions in sizing. This improved the basis for comparing designs without demonstrating a winning rig. A successful attached-flow case cannot settle broadside sailing, stalled flow or installed trim losses. [Conservative sizing basis](https://github.com/DavidIngraham/sv-blue-dog/commit/3eb61d8), [aerodynamic evidence](sail-trade.md#what-changed-my-sizing-assumptions).

The sizing trade also develops from searching for a small feasible boat toward retaining alternatives at overall-length caps, with mass and conditional passage time considered separately. In the bounded archived study, the two coarse-feasible outputs were effectively the same 1.2 m seed; the 1.0 and 0.8 m searches were unresolved. The study provides a method for comparing alternatives, but has not yet produced a useful spread of choices. The earlier 440 Wh, 260 mm beam reference is a local refined replay with positive nominal energy headroom, not a globally preferred architecture. [Retaining feasible alternatives](https://github.com/DavidIngraham/sv-blue-dog/commit/e97f309), [current sizing findings](results.md).

The [recovery propulsion trade](recovery-propulsion.md) remains open between water and air propulsion. Illustrative resistance, efficiency and propulsion capability let me estimate reserve and exercise casualty routes before selecting hardware. The mission then asks what a component calculation cannot: can that capability reach a usable shore approach from this position, against this current, with the remaining energy? Installed thrust, electrical demand, weeds, guarding and capsized behavior must inform the comparison. [Initial recovery analysis](https://github.com/DavidIngraham/sv-blue-dog/commit/48ff36e).

For the next comparison, I want feasible alternatives to sail the same declared scenarios with their own mass, performance, energy and recovery characteristics. Cost and construction effort also need explicit estimates. The mission should reveal the consequences of a choice; a favorable result for one provisional configuration should not silently close the alternatives.

## Let the environment act on the whole boat

Uniform wind and calm water leave out important effects for a small vessel. The environmental studies introduce wind varying with height, directional waves, current interaction and wakes. Wave-motion studies then ask how the moving wing sees the wind and how the hull and appendages move relative to the water. Those questions connect the operating environment to forces, clearance and control demands. [Wind and wave sensitivity](https://github.com/DavidIngraham/sv-blue-dog/commit/a342847), [motion and wing loads](https://github.com/DavidIngraham/sv-blue-dog/commit/86b51c0).

Paired scenarios help isolate an assumption. The archived environmental replay holds the candidate geometry fixed and uses the same weather and traffic seeds across different environmental representations. At 5 m/s reference wind, the 1.4 m candidate's modeled downwind velocity made good through the water falls from about 1.19 m/s in uniform wind to 0.66 m/s with the height-dependent profile. That identifies a consequential aerodynamic assumption. Voyage duration is less straightforward: changed motion changes when the boat encounters later weather and the rounding mark. Identical random inputs do not imply identical experiences along two different trajectories. [Environmental replay and comparison](reference/environmental-replays.md).

Calculated wave response adds another level. Heave, roll and pitch affect apparent wind, underwater inflow, loads and power; the sailing calculation seeks a balance over the wave cycle. The archived study accepted 32 operating cases for regular waves 0.04 m high with a 3 s period. Its four Gorge replays stopped at departure because their requested conditions lay outside that small-wave performance coverage. [Calculated wave response](https://github.com/DavidIngraham/sv-blue-dog/commit/8f6f098), [operating and mission evidence](../evidence/runs/2026-10-13-wave-performance/summary.json).

That is useful progress even though it does not produce a passage time. The model can identify which question it has answered and where a mission asks for more. Extending the usable range needs evidence about the sea conditions and vessel response; adding more sample points alone cannot establish that the underlying physics is applicable.

## Carry recovery through the voyage

Recovery changes the meaning of available energy. A fixed battery reserve cannot describe every position, current or casualty. The recovery model evaluates a route to a shore approach, the propulsion authority against the current, the transit energy and a declared allowance. Capsized capability is a separate input. The mission can terminate sailing before continuing would consume the recovery margin. [Recovery behavior and tests](https://github.com/DavidIngraham/sv-blue-dog/blob/9df1808/tests/test_course_recovery.py).

This makes the safety obligation observable in a scenario: where was the boat, what recovery remained reachable, why did it abort, and what happened during the transit? Tests exercise recovery without communications and retain traffic in the consequence calculation even when onboard sensing is unavailable. The present recovery fixtures use synthetic sites and capabilities. Surveyed approaches, measured propulsion and actual pickup conditions are the evidence needed to carry those conclusions into a real voyage. [Recovery assessment](site-and-environment-evidence.md#course-and-recovery-decision).

## Give decisions an executable meaning

The logical scenarios connect normal sailing, traffic encounters and abort/recovery to the boat's responsibilities. Executable supervisory behavior makes part of that architecture act within the mission simulation. A lost wind observation inhibits sailing. Communications loss alone leaves autonomy running. A safety abort remains latched, and queuing an alert does not delay recovery. [Allocated scenarios](https://github.com/DavidIngraham/sv-blue-dog/commit/8defcd1), [executable supervisor](https://github.com/DavidIngraham/sv-blue-dog/commit/d460f52).

The value is that I can follow a decision as well as a trajectory. The mission records the facts presented to the supervisor and the resulting decisions. Losing access to a weather service, for example, is different from deciding that the held forecast is no longer applicable. One preserves the attempt; the other initiates abort and recovery. That distinction can be exercised and inspected. [Forecast scenarios](https://github.com/DavidIngraham/sv-blue-dog/commit/7530eca).

The supervisor covers mission policy. The simulation still supplies conceptual heading search, traffic geometry and vessel dynamics, with perfect-truth and imperfect-observation modes explicitly distinguished. The behavioral questions concern measured observation errors, delayed decisions and maneuvers that the actual boat can execute. The [current logical execution](mission-simulation.md#executable-supervisory-logic) describes that boundary.

## Couple perception fidelity to energy

The [sensing-and-compute trade](encounter-feasibility.md#compare-sensing-and-energy-together) connects observation performance to the allocated electronics load. Its hypothesis experiment supplies target-specific range, errors, latency and dropouts, makes those observations drive avoidance and uses independent ground truth to score consequences. Measured sensing envelopes must replace those hypotheses. Pair each combination with its installed power, mass and thermal behavior, rerun sizing, and sail the same declared scenarios. The earlier sizing reference’s low electronics allowance does not establish vision feasibility. The executable hypothesis study below supplies a virtual comparison; this spiral remains open until encounter and energy measurements support a choice.

## Perception, avoidance and recovery in one experiment

The [encounter-feasibility study](encounter-feasibility.md) connects the detection-distance allocation to delayed and uncertain tracks, hypothetical sensor power, avoidance decisions and casualty consequences. The controller receives observations; separate truth scores executed collision and clearance. Weed patches provide an explicit target for the forward-sonar hypothesis. A perfect-truth baseline makes the observation assumptions visible in the comparison.

This spiral tests 54 distance cases, 80 paired encounter runs and six casualty cases. It uses a synthetic local corridor, a conceptual polar, allocated maneuver timing and candidate energy accounting. Sensor envelopes and power increments are declared hypotheses, not selected devices. The investigation can reject a drop-in energy allocation and reveal unsupported failure cases; it cannot establish measured detection, full-course recovery coverage or a qualified architecture.

## Command timing and continued casualty consequences — 15 October 2026

The question was whether the allocated detection distance survives actual scheduling and whether stopping the simulator at a rejected command hides what happens next. [Source revision 909ba57](https://github.com/DavidIngraham/sv-blue-dog/commit/909ba57) separates command delivery from maneuver completion and adds native recovery-versus-drift fallback. The [immutable continuation record](../evidence/runs/2026-10-15-encounter-continuation/encounter-continuation.json) retains the paired executions.

Working assumptions kept the experiment runnable without selecting hardware: a conceptual polar, synthetic corridor and shore approach, one- or two-second hypothetical observation delivery, two-second command delivery, a 15-second maneuver, current-only casualty drift and retained-candidate energy. Two sensing hypotheses were compared at 30-second and one-second assessment periods, by day/night, with seed 17 and an observation outage. The horizon was one hour; physical maneuver authority, windage, capsized drift and real refuge suitability remained unmeasured.

The 40 runs yielded ten complete courses, four physical terminal events and 26 unresolved horizons. Ten traffic-margin aborts continued into four contacts and six censored drifts. The casualties included a clear-path recovery approach as a positive control, common-cause steering/power loss, capsize, depleted energy and adverse current; the latter reached the shore boundary. A one-/half-second steering-loss pair checked numerical consistency. All 20 one-second cases remained censored, while the ten completions came from the 30-second group; faster scheduling did not demonstrate improved guidance. Trace inspection exposed long current-only intervals under zero-speed polar headings; the period also changed the heading-search horizon, leaving guidance tuning confounded with timing. Continuing the trajectory exposed consequences without turning a computational stop into success.

The timing trade required 760 m for the vision hypothesis and 742 m for the radar-assisted hypothesis at one-second assessment; 30-second scheduling required 1,282 m and 1,264 m. The earlier 724 m allocation calculation did not include these additional delivered-observation delays. Faster scheduling therefore did not make both stacks fit 750 m, and neither became a selected installation.

The physical trade gained a synchronized power/observation importer and native shared-compute reconciliation. Its fixed-passage capacity bound is a screening calculation. No installed measurements were available, so hypothetical loads were not relabeled as evidence and coupled resizing remained pending. The next useful evidence is an identified pipeline's installed load and detection performance, achieved maneuver timing and an independent recovery capability. Current methods and limits live in the [encounter article](encounter-feasibility.md), [energy budget](energy.md) and [validation plan](validation-plan.md).

## One allocated integration candidate — 15 October 2026

This spiral asks whether one boat can support the whole sensing–guidance–energy–recovery loop. The enabling hypothesis is IC-01: a monohull with an allocated perception load and a separately powered recovery path, including backup observations and inverted propulsion. The coupled solve supplies its mass, sailing states, dimensions and electrical demand to the mission. The sensing study therefore cannot borrow a conceptual boat's maneuvering performance while retaining a different boat's energy budget.

The trade is between installed capability, battery mass, hull support and exposure. An initial 30 Wh recovery bank lacked reserve for some inverted approaches after passage standby. A 1,400 Wh main-pack trial with 0.44 m beam balanced the eight sailing states and passed structural/righting screens, but fell outside two resistance-model geometry bounds. These were rejected integration assumptions, not accepted design alternatives. The allocated trial uses a 60 Wh recovery pack, 1,300 Wh main pack and 0.42 m beam within the 1.2 m length constraint, with a fresh coupled evaluation. This is a manually constructed candidate for integration, not a global optimum or selected hardware.

The simulation adds a fixed guidance prediction horizon, forward-progress scoring and explicit gate capture. Assessment, command delivery and persistent maneuver timing stay distinct. Recovery has a separate energy history and observation activation; a primary fault cannot receive independent recovery authority unless that capability is declared and powered. The first integrated mission runs exposed four obstructed recovery transitions that drifted to the shore boundary. The primary path therefore carries an explicit 10 m handoff allowance, and recovery evaluates routes against delivered observations, choosing another approach when necessary. It still stops and exposes drift consequences when no supported route remains. Finite-turn recovery dynamics and actual startup delay remain unmeasured.

The evidence combines nominal and uncertain-observation runs, casualty cases, end-of-exposure recovery, sampled reserve coverage, refinement and degraded controls. The [current encounter method](encounter-feasibility.md#close-the-candidate-loop) defines their scope, and the [acceptance requirement](../models/analyses/integrated-candidate.sysml) requires the loop's conditions together. Day/night ranges, 8 W incremental sensing demand, equipment mass, maneuver time and fault independence remain allocations. Actual sensor/processor selection, correlated sailing dynamics, surveyed approaches and retention remain open trades and physical evidence needs.

The [immutable sizing record](../evidence/runs/2026-10-15-integrated-candidate/integrated-sizing.json) passes the nominal static screens with a 20.061 kg candidate, 38.884-hour conditional passage and 102.062 Wh main-pack headroom. The [mission record](../evidence/runs/2026-10-15-integrated-candidate/integrated-mission.json) passes all seven virtual closure conditions: ten completed courses, eight safe aborted encounter approaches and six casualty/end-of-exposure recovery approaches, with two consistent refinement cases. The two independence/energy negative controls still reach the shore boundary. The result advances the allocated integration concept, while explicitly leaving physical qualification and full Gorge recovery coverage open.

## Make the working assumptions visible

Each spiral needs enough definition to run an experiment. These assumptions describe the scope of that experiment and the decisions it leaves open.

| Spiral | Working assumptions that enable progress | What they leave open |
| --- | --- | --- |
| Mission and coupled sizing | A parameterized monohull, a fixed-camber wing for the sizing experiment, provisional construction properties and representative operating conditions make geometry, forces, mass and power calculable together. | Rig and hull alternatives, measured material properties, detailed construction and the final equipment installation. A feasible candidate does not select the architecture. |
| Course and chronological voyage | A conceptual polar and load budget, point-mass motion, allocated maneuver timing, synthetic weather and perfectly observed scripted traffic let me exercise navigation and energy over time. | The actual controller, sensing uncertainty, local weather statistics and measured maneuver capability. Completion counts characterize those scenarios. |
| Candidate mission replay | A small set of solved sailing states supplies an averaged-tack envelope. Allocated electrical loads, storage characteristics and packaging assumptions give the candidate a voyage budget. | Full polars, explicit tack paths, installed loads and detailed fit. The 25% passage-time allowance and six-hour delay used in current sizing are provisional allowances, not measured weather statistics. |
| Environmental response | Fixed candidate geometry isolates the environmental effect. A neutral wind-height profile, effective-fetch hypotheses and prescribed motion support sensitivity studies; calculated linear wave response and declared damping support the bounded small-wave study. | Observed wind and seas, calibrated wave resistance, nonlinear motion and dynamic recovery. These studies do not reoptimize or select the whole boat. |
| Casualty recovery | Synthetic shore approaches, declared upright and capsized propulsion capability, and energy allowances make recovery reachability and reserve decisions testable. | Real site suitability, installed drive selection, pickup delay, shore retention and measured casualty capability. |
| Executable decisions | Supplied observation-validity and conflict facts, explicit events and conceptual guidance let the supervisor exercise sailing permission, abort persistence and alert behavior. | How sensors establish those facts, uncertain or delayed observations, detailed control allocation and physical maneuver execution. |

The assumptions have different purposes. A chosen wing makes one design experiment concrete; a conservative coefficient limits the performance credited; a synthetic traffic process creates repeatable encounters. None becomes a mission requirement merely because a simulation needs a value. The [design-assumption distinctions](methods/modeling.md#requirements-versus-design-assumptions) keep those roles visible.

I can therefore continue developing the mission with an unresolved architecture, provided I retain the configuration and limit each conclusion to what it exercised. When evidence challenges an assumption, the next spiral can change the parameter, compare another concept or narrow the claim. The trade remains open until the evidence supports the choice I actually need to make.

## Keep the evidence connected through every spiral

### 16 October: distinguish an upset from an ended attempt

Capsize does not necessarily require outside help. I want the qualification
policy to permit continued sailing after unassisted recovery, provided the boat
retains its required safety functions. The supervisor now assesses those facts
explicitly. During inversion the simulation permits current-driven drift but no
sailing or gate progress; a separate confirmed righting observation permits
resumption. Missing safety evidence, motor use, intervention or an already
latched abort still end qualification.

Native and simulator regression cases exercise those distinctions, including
hazards and energy use during inversion. The observations are supplied scenario
facts, not calculated righting physics. Earlier casualty records retain their
original inputs and outcomes. Physical recovery remains an experiment to design
and demonstrate.

This spiral also puts all three rig concepts on equal footing for the finite
Gorge comparison. The current wing-based sizing calculation remains one
candidate realization; it does not supply comparable physical evidence for
selecting a rig.

## Keep rig criteria within the mission being compared

The 16 October traceability review found two future-mission dependencies still attached to the finite Gorge rig trade: ocean survival waves and repeating-operation energy feasibility. I removed those links from the current comparison while retaining the future requirements in their own scope. The native assessments still give all three rigs equal development status with incomplete evidence. This corrects the basis of the comparison; it supplies no new performance or physical qualification evidence. The next useful comparison remains common measurements of performance, trim energy and recovery under Gorge conditions.

## Connect observation time, achieved turns and physical equipment

The next 16 October investigation asks what sensing must deliver before I add
detail to the hull-sizing study. The [encounter envelope](reference/encounter-envelope.md)
separates target classes and encounter geometry, then accounts for a hazard
arriving while another maneuver occupies the boat. Acquisition can overlap that
maneuver. A fast head-on case requires 742 m for a fresh response, but 940 m
when a 17-second occupied interval starts at acquisition-envelope entry. The
750 m requirement remained unchanged in that study; the calculation exposed a
condition it did not justify.

The [immutable study record](../evidence/runs/2026-10-16-response-maneuvers/manifest.json)
preserves the native response summary and synthetic trajectories against their
source revision.

The optional [maneuver model](reference/maneuver-dynamics.md) replaces an
instantaneous heading change with bounded turning, acceleration and
speed-dependent rudder authority. Synthetic turn, tack and gybe cases finish at
different times; low-speed and unavailable-rudder cases do not finish within
their horizon. Finer integration gives similar component responses. The
coefficients remain uncalibrated, guidance prediction remains kinematic and
powered recovery keeps its earlier executor. The IC-01 archive retains its
original fidelity.

The [equipment comparison](reference/sensing-configurations.md) gives the next
trade three concrete primary installations: two fixed camera rings and a
scanning head, with named compute and AIS components. Continuous coverage
challenges the added-power allowance; scanning introduces blind intervals.
None yet provides independent upright and inverted recovery observation.
Supplier specifications and project allowances are recorded separately.

This narrows the next sizing inputs to installation loads, coverage geometry
and backup packaging that can actually be tested. Configuration-specific sensing
simulation is deferred to the next experiment. It will need the selected
physical layouts, without treating catalogue resolution or range as achieved
detection performance.

## Compare acoustic observations and challenge the allocation

The acoustic follow-up asks whether the optical shortlist omitted useful ways
to observe traffic and underwater hazards. The
[comparison](reference/acoustic-sensing.md) identifies a synchronized hydrophone
array, a narrow-beam forward sonar and a multibeam imaging sonar. It separates
passive bearing cues from active range returns and records the physical
interfaces, mass and electrical assumptions needed to test each. Quiet targets,
surface reflections, flow noise and casualty orientation remain explicit gaps.
No acoustic performance is inserted into the sensing simulation.

The same investigation checks whether difficult targets can be excluded. The
[requirements review](reference/encounter-envelope.md#can-i-exclude-a-rare-or-difficult-target-class)
finds that the mission requires collision avoidance and noninterference, while
the uniform 750 m distance is an engineering allocation. L-104 permits reviewed
residual risk, but the model has no accepted probability threshold or measured
traffic evidence supporting omission of sailboats or paddlers. The next
requirement investigation is class- and condition-specific response distance
and exposure, with consequences and uncertainty assessed separately from
mission success. At that stage, targets and acceptance values remained unchanged.

## Class-specific observation and consequence — 16 October 2026

The next decision replaces the common 750 m allocation with class- and
condition-specific observation obligations. I separate the physical response
distance from reviewed consequence clearance and the reliability of both
timely observation and the complete avoidance response. Occupied kayaks, occupied stand-up paddleboards,
people in the water and unoccupied drifting craft now have distinct cases.
The other traffic classes remain; no class is excluded for being difficult to see.

The native illustrative comparison keeps the older motion inputs for continuity.
The four split low-profile cases consequently have identical illustrative
distances, not identical consequence or reliability claims. The
[native summary and source record](../evidence/runs/2026-10-16-class-specific-encounters/manifest.json)
preserve that comparison. A low-severity
glancing contact remains a conditional hypothesis requiring contact geometry
and occupancy evidence. Unknown occupancy cannot receive that presumption.

This adds the allocation structure, not accepted numerical severity or
probability thresholds. Class-specific clearance, margin, reliability/confidence
and evidence review remain open. Earlier 750 m studies and mission runs retain
their original scope. The [current encounter explanation](encounter-feasibility.md)
and [detailed allocation](reference/encounter-envelope.md) describe the criteria
needed before sensor measurements can establish an admitted operating envelope.

### Evidence through each iteration

For me, fidelity means representing the effects that matter to a decision with enough accuracy. Traceability means being able to explain which mission obligation, design, assumptions and evidence produced the conclusion. A more detailed model can strengthen one part of that chain while exposing a weakness in another.

| Question about a result | What I need to retain |
| --- | --- |
| What counted as success? | Mission conditions, course definition and observable outcome criteria |
| Which boat was evaluated? | Geometry, equipment, storage and performance configuration |
| What did it encounter? | Environmental assumptions, traffic realization, injected events and random seeds |
| Why did it act that way? | Observations, supervisory decisions, maneuver history and stopping cause |
| Where does the conclusion apply? | Model revision, source evidence, numerical checks and coverage limits |

The [archived-run provenance](https://github.com/DavidIngraham/sv-blue-dog/commit/e80e46d) preserves the identity of each experiment. Comparing spirals means comparing identifiable configurations and assumptions. A new course, different candidate or changed sea model needs an explicit comparison before a difference in outcomes can be attributed to one improvement.

The next spirals should connect measurements to the mission: wing and actuator tests to sailing and maneuver predictions; installed loads and battery tests to endurance; sensor replay and site surveys to traffic decisions and recovery. Each experiment should have a predicted observable and a decision it could change. I then replay the affected missions and update the [current assessment](current-assessment.md) according to the evidence, including results that narrow the boat's usable envelope.

The aim is a progressively better explanation of what Blue Dog can do, under which conditions, and why I believe it.

**Continue:** [Mission simulation methods](mission-simulation.md) · [Evidence and physical experiments](validation-plan.md)
