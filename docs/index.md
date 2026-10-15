# SV Blue Dog: the development series

**Start here:** [Why Blue Dog?](restarting-sv-blue-dog.md) · [Running maturity assessment](development-plan.md)

Blue Dog is named after my blue heeler, Ozzy. I hope the vessel will share a little of that character: small, something like a dog, independently puttering around the surface of a river or the ocean.

The [introductory story](restarting-sv-blue-dog.md) remains the beginning: sailing, desktop manufacturing, an early testbed and the maze of decisions that led me to a connected model. From there, follow the engineering through OOSEM layers. The [running maturity assessment](development-plan.md) explains what is established, what is provisional and what evidence would change the next decision.

| Read through the layers | Articles | Question |
| --- | --- | --- |
| The story and current position | [Why Blue Dog?](restarting-sv-blue-dog.md), [maturity assessment](development-plan.md) | Why build this, and what have I learned so far? |
| Mission and stakeholder needs | [Mission and context](architecture.md), [operating conditions](operating-constraints.md) | What should the boat accomplish, for whom and in what environment? |
| System requirements and scenarios | [Requirements](requirements.md), [mission simulation](mission-simulation.md) | What behavior counts as success, and what could we have missed? |
| Logical architecture | [Use cases and allocated behavior](architecture.md#from-use-cases-to-allocated-behavior) | What responsibilities, information and fault responses make that behavior possible? |
| Candidate physical architectures | [Structure and recovery](structures-and-recovery.md), [sail concepts](sail-trade.md), [recovery propulsion](recovery-propulsion.md) | How could those responsibilities be realized in a buildable boat? |
| Trades, optimization and analysis | [Sizing results](results.md), [sizing method](sizing.md), [energy](energy.md), [reliability](reliability.md) | Which choices work under the stated assumptions, and which assumptions dominate? |
| Verification, validation and learning | [From virtual evidence to water trials](validation-plan.md) | What evidence supports each claim, and what measurement should come next? |
| Methods and historical assessments | [Modeling](methods/modeling.md), [publishing](publishing.md), [earlier SRR assessment](srr-review.md), [its appendix](srr-appendix.md) | How is the engineering record maintained, and what did earlier assessments conclude? |

These layers are connected activities, not sequential gates or a completion checklist. An article can support several layers. A focused testbed experiment can improve a physical model while the integrated architecture remains provisional.

The SysML model owns engineering facts and rationale. The articles explain the choices and their evidence, with scoped views rendered from that model. Virtual findings, planned experiments and accepted measurements remain distinct. Earlier review pages retain their URLs and evidence, but formal SETR approval is no longer the organizing process.
