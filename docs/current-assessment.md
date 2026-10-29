# What the evidence supports, and what I need to learn next

**Assessment: 29 October 2026** · [Candidate results](results.md) · [Simulation studies](simulation-studies.md)

I intend to refine IC-01 into the first physical boat. I have defined the river mission, the boat's required functions and an IC-01 design for the simulations. The next step is to choose compatible equipment and measure the properties that matter most to sailing and recovery.

## Current assessment

The rows follow the Object-Oriented Systems Engineering Method (OOSEM): mission, requirements, responsibilities, physical choices, analysis and evidence. They develop together as experiments change what I know.

| Area | Available basis | Next evidence that could change a decision |
| --- | --- | --- |
| Mission and operating context | An explicit Bingen–Stevenson round trip, independent control, traffic obligations and a distinction between qualification and recovery. | Survey the launch and recovery approaches; resolve actual access, bridge margins and operating boundaries. [Context](architecture.md), [site evidence](site-and-environment-evidence.md) |
| Requirements and scenarios | The requirements describe the course, autonomous sailing, safety, energy, recovery and owner constraints. Each current Gorge requirement has a planned check; physical results remain open. Capsize and vegetation recovery have separate outcomes, as do emergency control and powered shore recovery. Scenarios cover sailing, navigation, encounters, outages, reserve protection, capsize, recovery, launch and maintenance. Reliability study objectives and future missions have separate applicability. | Justify the retained numerical allocations against their named measurement and margin closure plans, then obtain evidence for admitted conditions. Future ocean and sustained-operation objectives need their own mission scope and evidence. [Requirements](requirements.md), [evidence plan](validation-plan.md) |
| Logical architecture | Fourteen implementation-independent responsibilities exchange observations, permissions, commands and records. Recovery planning explicitly consumes navigation, traffic, boundary and reserve assessments; recovery actuation has its own command interface. All nine scenario descriptions have assigned step owners. The mission supervisor retains qualification loss across righting, restored navigation and communications recovery. | Exercise dynamically achieved turns with arriving hazards, backup startup and obstructed recovery routes; implement the descriptive scenario steps and establish their timing and validity contracts. [Architecture](architecture.md), [mission execution](mission-simulation.md) |
| Physical architecture | Named allocations explain each IC-01 implementation contribution and bind it to the candidate configuration. Logical exchanges map to candidate transfers or explicitly identified controller-internal interactions. The sizing studies use the candidate's declared geometry and load assumptions. | Resolve peer authority, startup after primary loss, ranging and independent recovery observation; reconcile recording/telemetry supply, installed mass, thermal behavior, electrical demand and fault isolation. Navigation signaling still needs detailed interfaces and equipment allocation. [Architecture](architecture.md), [candidate](results.md), [sensing layouts](reference/sensing-configurations.md) |
| Trades and analysis | Coupled sizing, three open rig concepts, energy accounting and bounded recovery/encounter studies. | Correlate aerodynamic, structural, maneuvering and recovery assumptions with measurements, then compare alternatives on the same cases. [Sizing](sizing.md), [rig trade](sail-trade.md) |
| Physical verification and model validation | Native method annotations cover all 100 verification definitions, including three numerical definitions. Two IC-01 integration/use plans distinguish the intended candidate from the actual test article, procedure and instruments still needed. Planned physical cases remain inconclusive; eligibility checks do not accept evidence. | Obtain component and integrated measurements for an identified configuration. No completed physical qualification is claimed. [Evidence plan](validation-plan.md) |

The challenge identifies vessel compliance under C-007 and assigns entry applicability, baseline control, evidence acceptance, operator intervention and adjudication to C-028 through C-032. Six [source-linked navigation review cases](validation-plan.md#navigation-rule-entry-review-and-adjudication) organize applicability, encounter conduct and equipment evidence. All remain inconclusive; accepted navigation compliance and physical entry qualification are still open. The next review must establish the configuration-specific applicability matrix and demonstration criteria.

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

Native recovery and sail-trade studies can select configured analyses by
model type and owner through [validated study configuration](reference/declarative-studies.md).
The execution report retains native results, resolved model identities and
explicit external assumptions. Numerical search obtains dimensions and named
fields from exported model records where available. Route topology, several
legacy vector contracts and numerical solver choices remain explicit software
limits. These capabilities improve repeatability; they add no physical
qualification evidence. The next analysis-interface work is to expose semantic
route/state contracts before generalizing the remaining campaign orchestration.

The [model's namespaces](reference/namespace-structure.md) place mission,
requirements, architecture, behavior, project analyses, configurations, decisions,
verification and evidence under one `BlueDog` project root. Reusable numerical
kernels share the independent `Analysis` root by domain. Design schemas,
battery/load types, navigation-domain types and decision records retain their
separate ownership. This supports scoped native discovery; component composition
and allocations still define how the candidate works. It adds no measurement or
physical verification evidence.

## Integrated simulation evidence

I need **one candidate whose sensing, guidance, energy and recovery capabilities work together**. Its geometry, equipment mass, electrical demand and sailing performance must remain consistent across the studies.

IC-01 meets the seven conditions in the [native integration requirement](../models/blue-dog.sysml) for the [15 October local campaign](../evidence/runs/2026-10-15-integrated-candidate/integrated-mission.json):

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

The [risk inventory](../models/blue-dog.sysml) connects each concern to requirements, analyses and decisions. It complements the design failure modes and effects analysis (DFMEA), which examines how components and functions can fail. Traffic sensing and casualty recovery lead because they can determine the architecture; structural, wing, energy and model-coverage uncertainty also remain open.

### Technical risk cube

The explorer links each risk to its evidence and next investigation. The [native risk inventory](../models/blue-dog.sysml) is also available as a reference.

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

### Interface and behavior assessment, 2026-10-23

The candidate [interface definitions](../models/blue-dog.sysml) now distinguish observation provenance from producer validity and command authority/time context. Typed native applicability calculations support synthetic boundary checks; their existence is not controller integration or physical evidence. Fourteen existing payload definitions retain their original fields and add context. Missing reserve, boundary and traffic-list timestamps are explicit; link-down, invalid and absent observations remain different conditions.

Open IF-01 through IF-05 cover justified consumer freshness/latency limits; clock uncertainty and restart/replay rules; spatial/angular references; primary/recovery command arbitration and inhibits; electrical, connector, sealing, storage/telemetry supply and transport contracts. These issues remain deployment gaps. Scenario and implementation mappings still need to preserve this meaning. The conceptual simulator currently exchanges scalar observations, not these candidate serialized messages.
The [behavior contracts](../models/blue-dog.sysml) expose current consumer gates and a qualification-restoration action. Sailing scenarios pass supervisor permission explicitly. Recovery includes a durable disqualification acknowledgment before actuation and a separate observed execution record afterward. Native tests exercise denied permissions, expired context, missing durability, unknown qualification and restoration after faults. A qualification-only restoration API preserves the nonqualifying fallback; it does not implement the watchdog, other restriction restoration or the 30-second deadline.

B-01 through B-04 keep message/storage integration, atomic durable state, controller scheduling/arbitration and achieved physical response open. The descriptive scenarios now expose these obligations but do not execute the estimators or storage hardware. Existing mission, capsize, abort and independent-recovery policy remain authoritative.

The [verification planning register](validation-plan.md#methods-configurations-and-acceptance) preserves all existing objectives and makes method choices visible. V-01 through V-04 keep released procedures, identified articles/instruments, evidence-transfer applicability and independent acceptance open. Recovery validation includes the human pickup task as well as autonomous approach. The three numerical verification definitions retain their input-dependent verdict logic; the audit does not execute them without subjects.

The initial [hazard/control argument](reliability.md#hazard-controls-and-actual-disposition)
now covers six current-Gorge scenarios and all thirteen critical whole-boat FMEA
rows. All six hazard dispositions and fifteen FMEA actions remain open. Control
effectiveness, common-cause treatment, risk criteria and actual acceptance records
are still needed; trace coverage is not a safety acceptance decision. The
reliability illustration also requires explicit review of its function partition,
dependence and common-cause coverage before evidence can support its claim.

### Configuration and accounting assessment,2026-10-23

The [configuration register](architecture.md#identify-the-study-and-the-installation)
distinguishes twelve study/input contexts, including every top-level native design
and parameter part. It preserves historical projections and identifies IC-01's
planned design/assembly without inventing actual installation records. The
[accounting scopes](energy.md#scope-the-current-accounting-before-adding-loads)
keep seven current-candidate boundaries explicit. All remain unaccepted, with two
power-peak bounds and five installation/reconciliation identities missing. The
whole-vessel mass-estimate field remains unset pending a new identified coupled
result; fixed-equipment allowance and historical totals do not substitute for it.
C-01 through C-04 cover installed identity, functional/component coverage, coupled
budget reconciliation and evidence-backed uncertainty/change/retest decisions.

Analysis-use coverage now distinguishes all110 native definitions/usages by intended
use, domain, excluded interpretations and next evidence. This is a scope inventory,
not110 physically validated analyses. Current result readers check both source and
driver provenance and reject missing current outputs; archived CAD references and
numerical seeds have explicit roles. Native recorded analyses retain execution
semantics and actual-source/runtime companions. The open work is configuration-
specific validation, uncertainty/dependence evidence and measured operating envelopes.

Decision records use a shared [SysML item definition](../models/libraries/decision-records.sysml):
eight design dispositions, six retained requirement-basis statements and six open
acceptance questions. The six mixed basis statements remain intact pending content
review; normalizing their structure does not resolve their assumptions or choose new
policies. Eight dispositions and six questions have additional scope, responsibility,
evidence basis and reopening context. The 80 allocation/procedure reviews remain
subject-attached metadata under a shared review schema. Native before/after queries
preserved record content, U-identifiers, context and 43 supporting links. Their
actual authority/date/disposition/implementation identities remain unset where no
supporting record is identified; all six acceptance flags stay false. The rig
comparison separates six declared mandatory groups from the provisional L-101
reliability study and uses current passage duration/evidence for performance.
Unknown data does not reject a contender, and a missed provisional target does not
create a new mandatory veto. No rig, gearbox, weights or hardware approval is selected.
