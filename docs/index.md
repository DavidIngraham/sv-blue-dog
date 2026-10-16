# SV Blue Dog: designing a small autonomous sailboat

Blue Dog is my attempt to build a small boat that can sail a Columbia River Gorge round trip on its own. It is named after my blue heeler, Ozzy. I want to understand which combination of hull, rig, sensing, energy and recovery can make that trip practical—and then build and test it.

**Start with [the story](restarting-sv-blue-dog.md).** The series assumes basic systems engineering knowledge, but no familiarity with this project or SysML. IC-01 is the working candidate for the first build; the [current assessment](current-assessment.md) summarizes its evidence and open decisions.

## Read the engineering story

| Order | Article | Question |
| --- | --- | --- |
| 1 | [Why Blue Dog?](restarting-sv-blue-dog.md) | What led me to this project and this boat? |
| 2 | [Mission and architecture](architecture.md) | What must the boat do, and which functions make it possible? |
| 3 | [Operating conditions](operating-constraints.md) | What does the Gorge demand of it? |
| 4 | [Requirements](requirements.md) | Which obligations govern the design and a qualifying attempt? |
| 5 | [Candidate results](results.md) | Why is IC-01 heavier than the earlier sizing reference? |
| 6 | [Sizing method](sizing.md) | How do geometry, performance and energy constrain each other? |
| 7 | [Rig comparison](sail-trade.md) | How should I compare soft sail and rigid-wing alternatives? |
| 8 | [Construction and recovery](structures-and-recovery.md) | Can I build it and retain its safety functions after an upset? |
| 9 | [Recovery propulsion](recovery-propulsion.md) | What can bring a disabled boat back? |
| 10 | [Sensing and encounters](encounter-feasibility.md) | Can it detect a hazard early enough to act? |
| 11 | [Power and energy](energy.md) | Can the installed functions operate for the whole voyage? |
| 12 | [Mission simulation](mission-simulation.md) | What happens when those functions operate together? |
| 13 | [Reliability](reliability.md) | How do duration and failures affect completion? |
| 14 | [Measurements and water trials](validation-plan.md) | What should I measure next, and which decision could it change? |

## Follow the evidence

- [Current assessment](current-assessment.md): evidence, open risks and next investigations.
- [Development history](simulation-spirals.md): how the analyses developed, with each result tied to its original configuration.
- [Site and environment evidence](site-and-environment-evidence.md): course, bridge, recovery approaches and environmental assumptions.
- [Reading the model](methods/modeling.md): how requirements, assumptions, decisions and evidence connect.
- [Contributor guide](reference/authoring.md): build the articles and reproduce their model views.

Detailed reproduction notes and archived studies are linked from the relevant articles. The six topic pages under [requirements](requirements.md) provide the authoritative model statements without interrupting the main reading path.
