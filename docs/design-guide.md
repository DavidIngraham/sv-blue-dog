# Design process and current model

SV Blue Dog explores autonomous sailing and desktop manufacture, with the Trans-Gorge challenge as a proving ground for the longer-term Hawaii objective. The checked-in SysML is the design source of truth. Published views are generated from it; prose explains how to read and develop the design.

## Follow the design

| Step | Authoritative model | Generated view |
| --- | --- | --- |
| Define the challenge independently of the boat | [challenge.sysml](../models/challenge.sysml) | [Challenge brief](challenge-brief.md) |
| Derive vehicle requirements from the challenge and Hawaii goal | [requirements.sysml](../models/requirements.sysml), [blue-dog.sysml](../models/blue-dog.sysml) | [Focused derivations](requirements-views.md), [register](requirements-register.md) |
| Define system context, traffic and logical responsibilities | [blue-dog.sysml](../models/blue-dog.sysml) | [Context](figures/context.md), [composition](figures/architecture.md), [detail](figures/architecture-detail.md) |
| Connect operational use cases and design allocations | [use-cases.sysml](../models/use-cases.sysml), [satisfaction.sysml](../models/satisfaction.sysml) | [Use cases](figures/use-cases.md), [traceability](traceability.md) |
| Assess performance and failure modes | Analysis models linked below | Native reports linked below |
| Define acceptance and collect evidence | Requirement predicates and verification cases | [Conditions, rationale, issues and verification specifications](requirements-context.md) |

Requirements state obligations concisely. Qualification conditions remain normative and separate; rationale explains decisions; issue metadata records unresolved questions. Follow a parent to its individual acceptance outcomes rather than treating a derivation arrow as a combined pass/fail rule.

The architecture describes logical responsibilities, not selected boards or a completed physical design. Satisfaction relationships record intended allocations. Mission actions are decomposed, but do not yet form an executable controller. The CAD in this repository is a manufacturing and wing-sail prototype, not the qualified challenge vessel.

## Use analysis to refine the design

| Question | Method and limitations | Generated evidence |
| --- | --- | --- |
| Can loads and harvesting sustain operation? | [Energy model guide](sustained-operations.md) | [Load budget](energy-budget.md), [native results](analysis/sustained-energy.json) |
| Which recovery propulsion medium is practical? | [Water/air propeller trade](recovery-propulsion-trade.md) | [Native candidate results](analysis/recovery-trade.json) |
| How does cruise speed change reliability exposure? | [Cruise/reliability guide](cruise-reliability.md) | [Results](cruise-reliability-results.md), [native analysis](analysis/cruise-reliability.json) |
| Which failures need design action? | [DFMEA model](../models/dfmea.sysml) | [DFMEA](dfmea.md), [review results](analysis/dfmea.json) |

Example inputs support sensitivity studies, not hardware qualification. Numerical feasibility, accepted evidence and verification verdicts are separate. The current examples use unaccepted evidence; planned verification cases remain inconclusive. Physical trials must identify the configuration, applicable conditions, measurements and review disposition.

Unresolved acceptance decisions belong in model metadata, exposed in the context report. External applicability references are retained in the [source register](operating-constraints.md). Do not infer operating authorization from model consistency.

## Maintain one source of truth

Edit requirements, thresholds, relationships, architecture and analysis logic in SysML. Regenerate the reports and diagrams with the same change. Keep authored pages focused on purpose, method, evidence interpretation and navigation; link to generated statements and results instead of copying tables, counts or verdicts.

Review conversations, audit transcripts, temporary checklists and superseded snapshots belong in Git history or working notes outside tracked documentation. The [project article](restarting-sv-blue-dog.md) gives a short account of the design approach and links to the current model rather than acting as a second requirements register.

See [modeling and publishing](../models/README.md) for commands and checks.
