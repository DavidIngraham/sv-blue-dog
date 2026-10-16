# Blue Dog: a running OOSEM maturity assessment

**OOSEM:** All layers · [The introductory story](restarting-sv-blue-dog.md) · [Series guide](index.md)

Blue Dog brings together my interest in autonomous sailing, desktop manufacturing and learning by building a complete system. The [introduction](restarting-sv-blue-dog.md) tells that story. Here I assess what I understand well enough to use and what I should learn next.

I organize the work around OOSEM layers: mission and stakeholder needs, system requirements, logical architecture, candidate physical architectures, trades and analysis, and verification and validation. They develop together. An experiment can change an assumption, an allocation or the mission scope.

## Current maturity by layer

**Assessment updated: 15 October 2026.** Scope: the finite Gorge round trip, with the manufacturing/wing testbed treated as a separate learning configuration. Hawaii and indefinite operation remain future missions. These are authored judgments grounded in the linked model and evidence, not an automatic completeness score or a formal OOSEM certification scale.

| OOSEM layer | Current assessment | What supports it | Main gap and next useful evidence |
| --- | --- | --- | --- |
| Mission and stakeholder needs | **Defined for the Gorge; operating scope remains provisional.** The unattended round trip, live observation and distinction between challenge and recovery are explicit. | [Introduction](restarting-sv-blue-dog.md), [operating context](operating-constraints.md), [challenge model](../models/missions/transgorge.sysml) | Resolve launch/recovery sites and operational boundaries against actual conditions. A dedicated stakeholder/enterprise view is still absent. |
| System requirements and scenarios | **Connected and partly exercised in simulation.** Mission obligations, owner constraints and verification cases are modeled. | [Requirements](requirements.md), [mission simulation](mission-simulation.md), [verification model](../models/vehicle/verification.sysml) | Challenge completeness with adverse scenarios and give each important obligation an observable test and applicability statement. Synthetic scenarios do not establish field performance. |
| Logical architecture | **Scenario threads, allocations and an executable supervisor exist.** Native actions govern events, sailing permission, abort latching, independent recovery authority and recovery-versus-drift fallback. Guidance prediction, assessment, command delivery and maneuver timing are distinct. | [Architecture and scenarios](architecture.md#from-use-cases-to-allocated-behavior), [mission execution](mission-simulation.md) | Resolve hazards arriving during occupied maneuver intervals, backup startup and obstructed recovery routes; compare achieved trajectories with predictions. Physical controllers remain separate responsibilities. |
| Candidate physical architectures | **An allocated integration candidate, with a separate testbed.** IC-01 binds geometry, sensing load, equipment mass and independent recovery energy to one coupled sizing and replay configuration. | [Architecture](architecture.md), [candidate allocation](../models/analyses/integrated-candidate.sysml), [testbed CAD](../cad/) | Select compatible hardware and define interfaces; measure materials, actuation, sensing, installed demand and fault isolation. The challenge vessel is not yet a complete buildable configuration. |
| Trades, optimization and analysis | **Executable and regression-tested; physical credibility remains conditional.** Coupled sizing, energy, reliability and recovery studies inform alternatives. | [Sizing method](sizing.md), [retained results](results.md), [sail trade](sail-trade.md), [energy](energy.md), [reliability](reliability.md) | Correlate dominant aerodynamic, structural, energy and recovery assumptions with measurements, then replay the affected candidates. Numerical convergence and software tests do not validate those assumptions. |
| Verification, validation and learning | **Cases are linked; physical evidence is incomplete.** Software checks and virtual scenarios exist; the testbed offers a route to focused measurements. | [Evidence plan](validation-plan.md), [verification model](../models/vehicle/verification.sysml), [archived runs](../evidence/runs/) | Obtain configuration-specific component and integrated measurements, compare them with predictions, and establish where conclusions transfer. Integrated challenge-vessel qualification has not been demonstrated. |

The [simulation development spirals](simulation-spirals.md) show how added capability exposes the next question across these layers. The most developed numerical work does not determine the maturity of the whole boat. The immediate limitations span logical behavior, physical interfaces and model credibility. I can make useful progress with a focused testbed experiment while the larger architecture remains provisional.

The [candidate budget](energy.md#current-candidate-budget) distinguishes the retained 440 Wh sizing reference from the integrated IC-01 allocation. IC-01 includes sensing demand and independent recovery equipment in its own coupled solve and mission replay. Installed measurements remain absent; model accounting and virtual integration do not reduce R-005 by themselves.

The [energy rollup and avoidance trade](energy.md#perception-computing-and-the-avoidance-trade) expose a coupled gap across physical architecture, analysis and validation: no selected perception stack has a measured installed power or latency budget. R-001 and R-005 remain open. The integrated study uses one declared sensing envelope and the same candidate's solved sailing performance, with a fixed guidance prediction horizon, one-second assessment, two-second command delivery and persistent 15-second maneuvers. Failed recovery continues into scored drift; a bounded horizon remains unresolved. These software schedules and allocated sensing ranges do not establish installed response or physical maneuver authority.

## Integration milestone

The integration milestone is **a coherent candidate that closes the sensing–guidance–energy–recovery loop in representative simulations, with critical assumptions and physical evidence needs explicit**. The [native requirement](../models/analyses/integrated-candidate.sysml) evaluates seven linked facts: compatible sizing, nominal completion, safe encounter outcomes, casualty recovery, energy sufficiency, timing/refinement and recorded assumptions. No overall percentage substitutes for these conditions.

The candidate must use the same geometry, equipment mass, electrical load and supported sailing states throughout. Normal cases must complete. Encounter cases must complete safely or terminate qualification and reach a recovery approach without collision or clearance violation. Recovery must use available independent capabilities and its own remaining energy after passage standby. Censored runs, unsupported performance and unresolved casualties cannot count as closure. [Physical evidence needs](validation-plan.md#exercise-decisions-before-physical-integration) remain attached even if the virtual checks pass. Synthetic reaches and nominal static passage screens do not establish complete Gorge-course coverage.

**IC-01 meets this bounded virtual milestone.** The [executed record](../evidence/runs/2026-10-15-integrated-candidate/integrated-mission.json) passes all seven conditions: ten courses complete, eight encounter attempts abort and reach recovery approaches safely, and six casualty/end-of-exposure cases reach recovery approaches. Two finer-step cases preserve their outcome classifications. Shared-fault and empty-bank controls remain adverse. This supports a coherent allocated concept at the declared fidelity; sensing hardware, recovery dynamics, actual sites and physical qualification remain open.

## How the assessment stays current

I assess each layer through four questions:

- **Coverage:** what behavior, interfaces and operating conditions are described, and what is missing?
- **Traceability:** can I follow the intent through requirements, responsibilities, implementation choices and evidence?
- **Virtual evidence:** what has been calculated or simulated, for which configuration and assumptions?
- **Physical evidence:** what has actually been measured or demonstrated, and where is it applicable?

I reassess each layer as analysis, experiments and trials change the evidence. Each judgment identifies its configuration, remaining uncertainty and the next investigation that could change a decision. A failed trial can narrow the scope of a claim just as a successful experiment can strengthen it.

There is no overall percentage or automatic promotion from “modeled” to “verified.” Missing evidence stays missing. Software tests establish implementation behavior; physical measurements establish claims about the actual system. A document count or a rendered diagram establishes neither.

The model defines requirements and design facts; this assessment connects them to their present support and limitations.

## OOSEM views: what is present and what is missing

The current articles render a native system-context view and three logical-scenario views. The [mission supervisor](mission-simulation.md#executable-supervisory-logic) links executable decisions to those scenarios and records their inputs and outputs during simulation. Requirements, use cases and subsystem responsibilities also have general-purpose model views. Package roles and initial allocations connect those artifacts.

Dedicated enterprise/stakeholder, measures, logical-architecture and physical-architecture views still need development. A complete presentation from stakeholder need through allocated implementation to verification evidence is also unfinished. The [modeling method](methods/modeling.md#native-oosem-roles) explains the current library support and classification limits. These view gaps are distinct from missing engineering evidence: making a diagram does not complete its layer.

<a id="review-gates-scaled-to-one-project"></a>
## Choosing the next work

Choose the unresolved question that could most change the design or its permitted operating scope. Record what result would change the choice before collecting evidence. Focus first on traffic behavior and casualty recovery, then the material/load, wing and installed-energy assumptions that dominate the candidate. Keep practical test conditions, retrieval arrangements and data capture explicit.

1. **Requirements and logical architecture:** extend the bounded virtual closure to held-out encounters, hazards observed during occupied maneuver intervals and blocked recovery approaches. Preserve the distinction between course completion and safe abort; do not generalize the current cases to complete Gorge coverage.
2. **Physical architecture and trades:** measure identifiable sensing pipelines against simultaneous range, latency, mass, power and thermal allocations. Replace shared loads once, then rerun coupled sizing and chronological energy with the measured installation.
3. **Recovery and operating scope:** verify power/control/observation isolation, upright and inverted thrust, usable capacity and startup. Survey actual approaches and demonstrate retention before extending synthetic refuge coverage to the Gorge.
4. **Verification and validation:** compare achieved sailing and maneuver trajectories with predictions, including current and waves. Replay held-out cases with measured envelopes, retain failures and censoring, and revise the admitted scope when the evidence requires it.

The [minimal mission simulation](mission-simulation.md) exercises changing wind/current, chart-constrained navigation, communications loss, intervention and chronological energy use. Its conceptual vessel and synthetic traffic/weather support requirements discovery. Correlated component models and detailed dynamics should follow where they can change a decision.

## Let risk select the next investigation

The next investigation starts from the risks that could defeat the mission or force a different architecture. The [risk inventory](../models/analyses/development-risks.sysml) links each event to affected requirements, analyses, decisions and existing DFMEA entries. It uses a small extension of the standard [SysML RiskMetadata](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml.library/Domain%20Libraries/Metadata/RiskMetadata.sysml), with standard status and ownership metadata. The DFMEA describes failure modes; this inventory tracks the development work needed to address them and broader model uncertainty.

The first selection is safety feasibility: traffic sensing and maneuvering, together with casualty recovery. Material/load sensitivity, wing behavior and installed energy follow because they can invalidate the sizing result. Scenario and model credibility apply throughout. These are provisional work priorities, not a claim of quantified likelihood. Safety consequences take precedence over cheap, easy tasks; among competing investigations, prefer evidence that can change an imminent decision and is practical to obtain.

### Technical risk cube

Choose a risk in the cube to read its description, assessment evidence and reduction action in the detail panel below it. Filter by risk type, status or text; each risk type keeps its own cube.

```risk-explorer
{"src":"https://davidingraham.github.io/sv-blue-dog/assets/risk/risks.json"}
```

All six current entries are **technical risks**, including uncertainty in model credibility. Safety consequences inform their technical severity; they do not make these entries a separate operational-safety assessment. Cost, schedule and operational risks belong in separate inventories and cubes, with criteria appropriate to each kind. No assessments of those kinds are recorded yet.

**Assessment: 15 October 2026.** The cube assesses the next concept-selection and integrated-test planning spiral. Its vertical axis expresses the prospect that an identified limitation forces redesign or a narrower operating envelope. Its horizontal axis expresses the credible consequence if the issue remains unresolved. These are qualitative engineering judgments, separate from measured probabilities of an accident during a voyage.

Likelihood classes are **Remote** (strong evidence against a material change), **Unlikely** (supported margins with limited outstanding concerns), **Possible** (a plausible challenge with insufficient evidence either way), **Likely** (specific evidence points toward a material change or restriction), and **Demonstrated** (a current limitation already restricts the conclusion). Missing evidence alone does not automatically make a risk likely.

Consequences are **Negligible** (no meaningful effect on the decision), **Minor** (local adjustment), **Moderate** (subsystem redesign or bounded loss of capability), **Major** (concept-level rework, mission noncompletion or an unsupported operating envelope), and **Critical** (credible loss of safety, flotation or recovery functions, including exposure of other river users). These classes have no numerical probability meaning and are not multiplied into a risk score. Green, yellow and red cells show low, moderate and high qualitative risk bands, increasing toward the upper-right corner. The color is an assessment aid, not a residual-risk acceptance decision.

The judgments are recorded by the analysis agent with owner review pending. All six risks remain open. Confidence describes the support for the development judgment, not confidence that a physical failure will occur: low for largely unmeasured assumptions, medium for specific but indirect analytical evidence, and high where the limitation is directly demonstrated.

Traffic sensing and casualty recovery lead the safety investigations. The small energy margin warrants early measured-load work alongside them. Structural and wing evidence constrain the design alternatives; scenario coverage constrains every mission conclusion. A populated cell records a judgment, not a completed mitigation.

### Risk reduction and closure

The standard quantitative probability and impact fields remain unset. The qualitative classes live in explicitly named extensions of the same risk metadata. Unknown remains separate from a low assessment, and numerical regression results alone do not justify reducing a rating. The named owner coordinates the action; I review residual-risk dispositions. Planned tests and successful software checks alone do not reduce a physical risk rating.

For each investigation, record the configuration, predicted observable, uncertainty and decision it could change before running it. Link the resulting evidence back into the model, reassess the risk and select the next action. Close a risk only with supporting evidence and an explicit disposition; otherwise retain it, restrict the concept's scope, or change the architecture. The inventory starts with six risk areas and must grow when analysis or experiments reveal omissions. It does not supersede the DFMEA or authorize field trials.

<a id="engineering-record"></a>
## Traceability and the learning record

The engineering chain is mission/use case → requirement → allocated architecture → analysis or verification case → executed configuration → evidence → updated maturity assessment and next action. A second chain connects each prediction to its assumptions, measurements and validity limits. Tests should reference the model's criterion rather than maintain a separate acceptance threshold in Python.

```sysml-view Page_development_plan_0::missionEvidence direction=BT
package Page_development_plan_0 {
    private import StandardViewDefinitions::*;
    view missionEvidence : GeneralView {
        expose GorgeChallenge::courseCompletion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirementVerification::RoundTripVerification;
    }
}
```

Virtual verification asks whether the modeled design meets its criteria. Virtual validation asks whether the modeled behavior addresses mission intent. Physical verification and validation ask those questions of the built configuration. Model validation compares predictions with independent measurements and establishes where a simulation is useful. Keep these evidence streams separate when updating a layer.

Before an analysis or experiment, identify the decision, linked model elements, required accuracy and result that would change the choice. Afterwards, record what was learned and which maturity claims changed. Missing links, stale inputs and numerical failures can be checked automatically; judging physical applicability still needs explicit reasoning.

## Reading across the layers

<a id="mission-definition"></a>
### Mission and requirements

Start with the [story](restarting-sv-blue-dog.md), [operating context](operating-constraints.md), [architecture](architecture.md) and [requirements](requirements.md). Use scenarios to expose omissions and clarify observable success.

<a id="virtual-design"></a>
### Architectures and analysis

Connect logical responsibilities to candidate implementations, then use [sizing](sizing.md), [sail trades](sail-trade.md), [energy](energy.md), [recovery propulsion](recovery-propulsion.md) and [reliability](reliability.md) to compare choices. Follow the [retained results](results.md) back to their assumptions.

<a id="detailed-design"></a>
### Physical realization

Develop materials, geometry, actuators, software and electrical interfaces into identifiable configurations. [Structure and recovery](structures-and-recovery.md) connects the candidate to the measurements and manufacturing details still needed. A learning testbed and a challenge vessel can have different evidence needs.

<a id="physical-validation"></a>
### Verification and validation

The [evidence plan](validation-plan.md) connects component, subsystem and integrated experiments to their questions. Before each trial, identify its configuration, conditions, operating limits and recovery arrangements. After it, retain failures and inconclusive results alongside successful observations.

<a id="model-credibility"></a>
### Model credibility and feedback

Compare predictions with independent measurements under recorded conditions. Revise the usable domain and uncertainty, then revisit affected design conclusions. More detailed simulation does not automatically provide stronger evidence.

**Next:** [Explore the mission and architecture](architecture.md), or return to the [series guide](index.md).
