# SV Blue Dog: the development series

Blue Dog is named after my blue heeler, Ozzy. I hope the vessel will share a little of that character: small, something like a dog, independently puttering around the surface of a river or the ocean.

If you are new here, follow the engineering story first:

1. [Why I started—and why I stalled](restarting-sv-blue-dog.md).
2. [The route and the boat’s responsibilities](architecture.md).
3. [A development plan with room to learn](development-plan.md).
4. [What the current sizing study tells me](results.md).
5. [How the coupled sizing works](sizing.md), then the rig, energy and recovery studies below.

The matrix is a reference for returning readers. The [focused requirement views](requirements.md) are a lookup library, rather than additional chapters to read in order.

| Part of the plan | Read | Decisions informed |
| --- | --- | --- |
| [Mission definition and SRR](development-plan.md#mission-definition) | [Mission and architecture](architecture.md), [operating constraints](operating-constraints.md), [mission simulation](mission-simulation.md), [focused requirements](requirements.md) | Mission scope, operating scenarios, design obligations and intended responsibilities |
| [Virtual design and PDR](development-plan.md#virtual-design) | [Coupled sizing](sizing.md), [current results](results.md), [sail trade](sail-trade.md), [energy](energy.md), [recovery propulsion](recovery-propulsion.md), [reliability](reliability.md) | Which concepts and assumptions warrant further development, and what early simulated behavior must be assessed |
| [Detailed design and build readiness](development-plan.md#detailed-design) | [Manufacturing, structure and recovery](structures-and-recovery.md), equipment and interface views in [requirements](requirements.md) | Construction, component selection, integration details and the scope of a build release |
| [Physical V&V and progression](development-plan.md#physical-validation) | Test methods and evidence needs in [energy](energy.md), [recovery propulsion](recovery-propulsion.md), [structures and recovery](structures-and-recovery.md), and [reliability](reliability.md) | What to measure, readiness for a bounded test, and what evidence could support progression |
| [Model validation and feedback](development-plan.md#model-credibility) | [Wing analysis and experiments](sail-trade.md), [structural and recovery methods](structures-and-recovery.md), [energy characterization](energy.md) | Where predictions can be trusted and which assumptions need revision |
| [Engineering record throughout](development-plan.md#engineering-record) | [Modeling method](methods/modeling.md), [authoring and publishing](publishing.md) | How requirements, rationale, configurations and evidence remain connected |

These are recurring activities, not a completion checklist. An article can serve more than one stage, and a testbed can answer a focused question before the challenge vessel is ready for detailed design. Each article explains the question it addresses and the design decision it supports.

The SysML model owns engineering facts and rationale. The articles explain our methods and thought process, with scoped views and statements rendered from that model. Current numerical results remain conditional; the series distinguishes virtual findings, planned physical evidence and accepted measurements rather than treating them as interchangeable.
