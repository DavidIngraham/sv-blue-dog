# What the evidence supports, and what I need to learn next

**Assessment: 20 October 2026** · [Candidate results](results.md) · [Simulation studies](simulation-studies.md)

I intend to refine IC-01 into the first physical boat. The project has a connected mission model and a candidate that works across bounded simulations; the next step is to replace consequential assumptions with measurements and compatible hardware choices.

## Current assessment

The rows follow the Object-Oriented Systems Engineering Method (OOSEM): mission, requirements, responsibilities, physical choices, analysis and evidence. They develop together as experiments change what I know.

| Area | Available basis | Next evidence that could change a decision |
| --- | --- | --- |
| Mission and operating context | An explicit Bingen–Stevenson round trip, independent control, traffic obligations and a distinction between qualification and recovery. | Survey the launch and recovery approaches; resolve actual access, bridge margins and operating boundaries. [Context](architecture.md), [site evidence](site-and-environment-evidence.md) |
| Requirements and scenarios | The current Gorge requirements have defined verification objectives. Scenarios cover sailing, navigation, encounters, outages, reserve protection, capsize, recovery, launch and maintenance. Reliability study objectives and future missions have separate applicability. | Develop test procedures and obtain measurements for the admitted conditions. Future ocean and sustained-operation objectives need their own mission scope and evidence. [Requirements](requirements.md), [evidence plan](validation-plan.md) |
| Logical architecture | Implementation-independent functions exchange typed observations, permissions, commands and records. The mission supervisor retains qualification loss across righting, restored navigation and communications recovery. | Exercise dynamically achieved turns with arriving hazards, backup startup and obstructed recovery routes; implement the descriptive scenario steps. [Architecture](architecture.md), [mission execution](mission-simulation.md) |
| Physical architecture | A provisional IC-01 assembly allocates the functions to separate main and recovery paths with explicit data and power interfaces. The sizing studies use its declared geometry and load assumptions. | Resolve ranging and independent recovery observation; reconcile recording/telemetry supply, installed mass, thermal behavior, electrical demand and fault isolation. [Candidate](results.md), [sensing layouts](reference/sensing-configurations.md) |
| Trades and analysis | Coupled sizing, three open rig concepts, energy accounting and bounded recovery/encounter studies. | Correlate aerodynamic, structural, maneuvering and recovery assumptions with measurements, then compare alternatives on the same cases. [Sizing](sizing.md), [rig trade](sail-trade.md) |
| Physical verification and model validation | Planned cases identify the claims to test; software checks establish behavior in supplied cases. | Obtain component and integrated measurements for an identified configuration. No completed physical qualification is claimed. [Evidence plan](validation-plan.md) |

The challenge explicitly identifies the U.S. Inland Navigation Rules, entry evidence and adjudication under C-007. Six [source-linked navigation review cases](validation-plan.md#navigation-rule-entry-review-and-adjudication) organize applicability, encounter conduct and equipment evidence. All remain inconclusive; accepted navigation compliance and physical entry qualification are still open. The next review must establish the configuration-specific applicability matrix and demonstration criteria.

The [Inland Rules model](../experiments/inland-navigation/README.md) filters
primary sailing commands in an opt-in mission replay. It retains overtaking duties
across track loss and rejects unsupported encounter assessments. The integration
is limited to an assessed clear-visibility, non-channel context; equipment,
restricted-visibility control, multi-vessel negotiation and powered recovery remain
open. The six navigation review cases remain inconclusive. The next evidence must
connect identification and response judgments to observations, and maneuver
predictions to achieved motion, before changing hardware allocations.

The [paired navigation replay](encounter-feasibility.md#navigation-assessments-in-the-ic-01-replay)
retains ten completions and eight safe aborts in the 18 nominal cases across all
three modes. Unresolved identification triggers earlier refusal, but no accepted
steering selection changes. This does not establish successful rule-directed
avoidance or support resizing IC-01. The static sizing result remains scoped to
its existing configuration and assumptions.

Blue Dog also has a [traffic courtesy preference](encounter-feasibility.md#leave-room-for-crewed-boats): avoid developing encounters that require crewed vessels to react, subject to safe navigation duties. The challenge encourages this as nonbinding guidance. It is not a qualification criterion or an implemented planner objective; comparative route studies remain to be done.

The [failure analysis and fault trees](reliability.md#how-avoidance-can-fail) connect functional and equipment failures to loss of avoidance capability. Shared power, observations and control can defeat apparently independent paths. The mitigation actions remain open: I still need evidence of installed diagnostic coverage, timely fallback and isolation from common causes. Software checks establish the behavior of the fault-tree logic; they do not establish failure probabilities or hardware independence.

## Integrated simulation evidence

I need **one candidate whose sensing, guidance, energy and recovery capabilities work together**. Its geometry, equipment mass, electrical demand and sailing performance must remain consistent across the studies.

IC-01 meets the seven conditions in the [native integration requirement](../models/analyses/integrated-candidate.sysml) for the [15 October local campaign](../evidence/runs/2026-10-15-integrated-candidate/integrated-mission.json):

- Ten courses complete.
- Eight encounter attempts end qualification and reach recovery approaches without the scored collision or clearance violations.
- Six casualty or end-of-exposure cases reach recovery approaches.
- Two finer-step cases preserve their outcome classifications; shared-fault and empty-bank controls remain adverse.

These cases support the allocated concept at their declared fidelity. They do not cover the full Gorge course or establish physical capture and retention at shore. A recovery approach reached is an intermediate outcome, not retrieval.

The native integration check combines seven supplied findings. Its passing result
checks that combination; the linked campaign records supply the underlying
evidence and its limits.

The supervisor checks distinguish observed unassisted righting from a
disqualifying casualty. They exercise the policy with supplied safety and
righting observations. Dynamic righting and safety capability during inversion
still need physical evidence. [Mission execution](mission-simulation.md#executable-supervisory-logic)
describes what happens during inversion.

The [encounter envelope](reference/encounter-envelope.md) distinguishes a fresh response from a hazard arriving during an occupied maneuver, allowing acquisition and the existing maneuver to overlap. Required distance depends on relative motion and the remaining response time. The [maneuver model](reference/maneuver-dynamics.md) represents finite turning and speed-dependent steering authority; its synthetic cases show why I need measured maneuver bounds. Its coefficients still need physical measurements. The archived integration result uses its declared motion model and does not validate this dynamic response.

The [physical sensing candidates](reference/sensing-configurations.md) identify components and installation gaps. Simultaneous camera coverage challenges the additional 8 W allocation, while independent upright and inverted observation remains unresolved. These findings constrain the next sizing study; none of the installations is selected or credited with meeting the detection requirement. Simulation of their particular coverage and failure behavior is the next separate experiment.

The [acoustic comparison](reference/acoustic-sensing.md) considers a synchronized
hydrophone array and two distinct forward-sonar installations. Passive sound
may cue powered traffic; active sonar can range a reflecting submerged target
without relying on its emitted sound. Useful near-surface detection, installed
average demand and independent inverted operation remain unmeasured.

The [class-specific allocation](reference/encounter-envelope.md) separates
response distance, consequence-informed clearance and the reliability of
observations and responses. It distinguishes occupied kayaks, occupied
stand-up paddleboards, people in the water and unoccupied drifting craft while
retaining the other traffic classes. Illustrative distances are available;
class-specific accepted margins, reliability/confidence criteria and supporting
evidence remain unresolved. No low-consequence class exemption or numerical
residual-risk threshold has been accepted. The archived campaigns use their declared acquisition assumptions; they do not
establish class-specific detection or response capability. A reviewed
design distance requires reviewed observation and whole-response reliability
criteria; accepting that distance also requires the corresponding evidence.

The [location-specific traffic assessment](site-and-environment-evidence.md#traffic-risk-by-location-and-arrival-window)
covers windsurfer, wingfoiler and kiter cases, including falls, separated equipment,
line/foil hazards and absent rider response. Eight survey sectors cover the
named access areas, constrained passage and connecting reaches. The native
visit assessment rejects unsupported timing or traffic evidence; no field
counts, traffic polygons or departure window are accepted. Reactive wind-sport
simulation and complete mission exposure aggregation remain future work.

<a id="review-gates-scaled-to-one-project"></a>
## Choosing the next work

I prioritize evidence that could change the architecture or the conditions in which I can operate the boat.

1. **Sensing and maneuvering:** complete the class-specific criteria and use the physical candidate layouts to define the next sensing simulation, then measure target detection, latency, mass, power and thermal behavior together. Replace the provisional maneuver coefficients with achieved heading, speed and swept-path measurements.
2. **Independent recovery:** test observation, control and power isolation; upright and inverted thrust; startup and usable capacity. Survey approaches and demonstrate shore retention and one-person pickup.
3. **Rig and construction:** compare soft sail, tail-controlled wing and directly rotated wing on equal terms for the finite Gorge mission. The trade links use this mission’s criteria; future ocean-wave and repeating-endurance requirements are outside its scope. Measure loads, trim energy, material properties, joints and casualty behavior that could change the IC-01 design.
4. **Integrated replay and trials:** replace provisional inputs with the measured envelopes, rerun the affected scenarios and expand physical trials within the demonstrated limits.

## Let risk select the next investigation

The [risk inventory](../models/analyses/development-risks.sysml) connects each concern to requirements, analyses and decisions. It complements the design failure modes and effects analysis (DFMEA), which examines how components and functions can fail. Traffic sensing and casualty recovery lead because they can determine the architecture; structural, wing, energy and model-coverage uncertainty also remain open.

### Technical risk cube

The explorer links each risk to its evidence and next investigation. The [native risk inventory](../models/analyses/development-risks.sysml) is also available as a reference.

```risk-explorer
{"src":"https://davidingraham.github.io/sv-blue-dog/assets/risk/risks.json"}
```

All six current entries are **technical risks**, including uncertainty in model credibility. Safety consequences inform their technical severity; they do not make these entries a separate operational-safety assessment. Cost, schedule and operational risks belong in separate inventories and cubes, with criteria appropriate to each kind. No assessments of those kinds are recorded yet.

**Risk ratings: 15 October 2026.** The cube supports concept selection and integrated-test planning. Its vertical axis expresses the prospect that an identified limitation forces redesign or a narrower operating envelope. Its horizontal axis expresses the credible consequence if the issue remains unresolved. These are qualitative engineering judgments, separate from measured probabilities of an accident during a voyage.

<details>
<summary>Rating definitions and evidence needed to resolve a risk</summary>

Likelihood classes are **Remote** (strong evidence against a material change), **Unlikely** (supported margins with limited outstanding concerns), **Possible** (a plausible challenge with insufficient evidence either way), **Likely** (specific evidence points toward a material change or restriction), and **Demonstrated** (a current limitation already restricts the conclusion). Missing evidence alone does not automatically make a risk likely.

Consequences are **Negligible** (no meaningful effect on the decision), **Minor** (local adjustment), **Moderate** (subsystem redesign or bounded loss of capability), **Major** (concept-level rework, mission noncompletion or an unsupported operating envelope), and **Critical** (credible loss of safety, flotation or recovery functions, including exposure of other river users). These classes have no numerical probability meaning and are not multiplied into a risk score. Green, yellow and red cells show low, moderate and high qualitative risk bands, increasing toward the upper-right corner. The color is an assessment aid, not a residual-risk acceptance decision.

I use these provisional judgments to choose investigations. All six risks remain open. Confidence describes the support for the development judgment, not confidence that a physical failure will occur: low for largely unmeasured assumptions, medium for specific but indirect analytical evidence, and high where the limitation is directly demonstrated.

Traffic sensing and casualty recovery lead the safety investigations. IC-01 has nominal energy headroom, but simultaneous sensing performance, installed demand and power isolation still warrant early measured-load work. Structural and wing evidence constrain the design alternatives; scenario coverage constrains every mission conclusion. The bounded simulations do not resolve these physical evidence gaps.

### Risk reduction and closure

I have no measured probabilities for these risks. An unknown probability is not a low probability, and successful software checks alone do not justify reducing a physical risk rating. I need evidence that addresses the failure mechanism and operating conditions before deciding whether the remaining risk is acceptable.

For each investigation, I will identify the configuration, predicted observable, uncertainty and decision it could change. I will use the result to reassess the risk and choose the next action. A risk remains open until evidence supports an explicit disposition; that may require a narrower operating envelope or a different architecture. I will add risks when analysis or experiments reveal omissions. The inventory complements the failure analysis; it does not authorize field trials.


</details>

<a id="engineering-record"></a>
## Reading the evidence

For each result I need to know the question, configuration, conditions, predicted observable and decision it could change. The [study guide](simulation-studies.md) explains the configuration, assumptions and limits of each simulation study.

| Evidence | What it establishes |
| --- | --- |
| Model and software checks | Consistency and implemented behavior for supplied inputs |
| Sizing and mission simulations | Conditional predictions within the model’s supported domain |
| Physical verification | Whether the tested installation meets a defined criterion |
| Model validation | How predictions compare with independent measurements and where they are useful |

A measured component result transfers to IC-01 only when its installation and conditions support that inference. I retain failures and inconclusive results because they can change the design just as much as a successful test.

<details>
<summary>Method references by engineering layer</summary>

<a id="mission-definition"></a>
### Mission and requirements

[Story](restarting-sv-blue-dog.md), [operating conditions](operating-constraints.md), [architecture](architecture.md) and [requirements](requirements.md).

<a id="virtual-design"></a>
### Architectures and analysis

[Candidate results](results.md), [sizing method](sizing.md), [rig comparison](sail-trade.md), [energy](energy.md), [recovery propulsion](recovery-propulsion.md) and [reliability](reliability.md).

<a id="detailed-design"></a>
### Physical realization

[Structure and recovery](structures-and-recovery.md) connects the candidate to construction, interfaces and measurements needed for the first build.

<a id="physical-validation"></a>
### Verification and validation

[The evidence plan](validation-plan.md) connects component and integrated experiments to their questions and operating conditions.

<a id="model-credibility"></a>
### Model credibility

[Modeling methods](methods/modeling.md) explain how requirements, assumptions, calculations and evidence stay connected. Dedicated stakeholder views and detailed physical interface definitions remain unfinished; drawing them does not substitute for the missing engineering evidence.

</details>
