# Blue Dog system requirements review

**Design phase:** Mission and requirements · SRR · [Development plan](development-plan.md)

This review asks whether the mission and requirements are clear enough to develop the boat. The proposed baseline and supporting desktop assessments are prepared for review; **SRR approval is open**. The [technical appendix](srr-appendix.md) separates evidence, limitations and proposed actions. Your review determines the disposition.

## 1 · A small boat with a definite job

Build an autonomous sailboat that completes the Gorge round trip and can recover to shore when continuing is unsafe. I want to learn digital engineering while building something I can transport, manufacture and test myself.

Hawaii remains a future mission. This review concerns the finite Gorge challenge.

![The existing manufacturing and wing testbed in SolidWorks.](figures/testbed-solidworks.png)

The testbed informs construction and control experiments; it is not the challenge-vessel design.

## 2 · The course is the mission backbone

![Bingen to Stevenson and back, with marker-referenced gates.](figures/gorge-course-map.svg)

Launch and retrieval at Bingen Point are outside the scored passage. Both scored legs use the charted Hood River lift span with the bridge closed. Adjacent spans without clearance evidence are excluded from the reference route. The complete reference circuit is approximately 66 km. Current notices belong in launch readiness.

[Course definition](../models/missions/course.sysml) · [Mission simulation](mission-simulation.md)

## 3 · Qualification has a clear boundary

```sysml-view SRR_Qualification::scope direction=BT statements=true
package SRR_Qualification {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view scope : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::overallLength;
        expose GorgeChallenge::unassistedAttempt;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unattachedPassage;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::overallLength { x = 640; y = 0; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::unattachedPassage { x = 640; y = 400; }
    }
}
```

Safe waiting is allowed. Refuge, grounding, anchoring, intervention or recovery propulsion ends the attempt; a later attempt starts again at the departure gate.

## 4 · Safety takes priority over finishing

```sysml-view SRR_Safety::scope direction=BT statements=true
package SRR_Safety {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view scope : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::navigationRules;
        expose GorgeChallenge::trafficCoexistence;
        expose GorgeChallenge::trafficNonInterference;
        expose GorgeChallenge::safetyCapabilityAbort;
        expose GorgeChallenge::autonomousShoreRecovery;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::navigationRules { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::trafficCoexistence { x = 640; y = 0; }
        metadata Layout about GorgeChallenge::trafficNonInterference { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::safetyCapabilityAbort { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::autonomousShoreRecovery { x = 640; y = 400; }
    }
}
```

A failed component need not end the attempt if a demonstrated backup preserves the required function. Loss of the function requires an onboard decision; contact with the operator is not a prerequisite.

## 5 · No littering drives casualty recovery

```sysml-view SRR_Recovery::scope direction=BT statements=true
package SRR_Recovery {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view scope : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::noLittering;
        expose GorgeChallenge::casualtyFlotation;
        expose GorgeChallenge::majorComponentRetention;
        expose GorgeChallenge::capsizeRecovery;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::noLittering { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::casualtyFlotation { x = 640; y = 0; }
        metadata Layout about GorgeChallenge::majorComponentRetention { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::capsizeRecovery { x = 320; y = 400; }
    }
}
```

The requirement is recovery after capsize. Self-righting is one possible solution; inverted powered recovery is another. Neither has been physically demonstrated for the eventual boat. The present monohull sizing study screens self-righting as a vehicle design allocation; the challenge itself permits another demonstrated recovery solution.

## 6 · Recovery follows the course

```mermaid
flowchart TD
    state["Position, current and remaining capabilities"] --> routes["Assess routes to accessible shore locations"]
    routes --> reserve["Transit energy + essential loads + uncertainty"]
    reserve --> decision{"Can continuing preserve recovery?"}
    decision -->|Yes| sailing["Continue or wait safely"]
    decision -->|No| abort["End qualification and alert operator"]
    abort --> recover["Conspicuous autonomous recovery"]
    recover --> retrieval["Shore retrieval or suitable deliberate grounding"]
```

The implementation models route-dependent reserve and powered approach. The desktop assessment selects Bingen and Stevenson as endpoint retrieval candidates, prioritizes Home Valley for intermediate north-bank coverage, and rejects Drano as a default autonomous destination. Spring Creek and Viento remain conditional alternatives. Endpoint-only recovery is not an accepted coverage solution.

The [site assessment and survey acceptance criteria](srr-appendix.md#course-and-recovery-decision) define the physical evidence required before operational routing. Recovery exposure includes transit and arranged pickup delay, rather than a fixed 24-hour survival requirement.

## 7 · Monitoring does not steer the boat

The boat makes mission and weather decisions onboard. The operator watches position, mode and health, and can intervene to end qualification.

Autonomous weather polling is allowed; manual data pushes are not. Communications loss alone does not end a safe attempt. Critical alerts are queued during outages.

[Observation and outage requirements](../models/missions/transgorge.sysml) · [Communications implementation requirements](requirements/requirements-safety.md)

## 8 · Define exposure before claiming capability

```sysml-report BlueDogSRRDocuments::EnvironmentProposal
```

These are **review proposals**, not measured extremes or accepted launch limits. The fetch sensitivity exposed a mismatch in the old wave allocation. The model now uses this same wave allocation, includes calm, and separates operational exposure from casualty recovery. The appendix specifies correlated cases, wake tests and the evidence needed before expanding the on-water envelope.

Darkness is included. Fog matters when it compromises a required safety capability. Calm is a possible waiting state, not an automatic mission failure.

[Environmental basis and limitations](../models/analyses/environment-review.sysml)

## 9 · Reproducible scenarios challenge the requirements

```mermaid
flowchart LR
    inputs["Versioned boat, course and scenario model"] --> ensemble["Fixed seeds + explicit edge cases"]
    ensemble --> execution["Chronological passage and recovery"]
    execution --> outcomes["Completion / abort / unsafe / censored / coverage stop"]
    outcomes --> review["Requirement gaps and design comparisons"]
```

Keep the same realizations across candidates. Record the scenario generator and inputs as well as seeds. Synthetic completion fractions do not establish real-world reliability.

[Simulation methods](mission-simulation.md)

## 10 · Choose a boat from a frontier

Sweep overall-length caps while leaving hull length and the remaining parameters free. Retain alternatives showing the trade between mission outcomes, passage time, mass, recovery margin, cost and construction effort.

There is no handicap score and no fixed sailing-speed floor. The reliability target is provisional. The design team chooses the preferred balance and records its rationale.

The 1.2 m concept, corrected to a 440 Wh battery and 260 mm hull beam, passes nominal refined Gorge static screens against the corrected course in the [current SRR evidence](srr-appendix.md#current-baseline-evidence). It is not an accepted vessel design. The earlier frontier is retained as historical exploration; current feasibility comes from the new replay. Local searches do not establish a minimum feasible size or a calibrated mission probability.

[Alternatives, scope and unresolved searches](results.md)

## 11 · Keep construction practical

Individual printed parts fit a 250 × 250 × 250 mm build volume; joined assemblies may be larger and bought components need not be printed. One person handles transport, assembly, launch and retrieval, using simple aids and removable components.

```sysml-view SRR_Construction::thread direction=BT statements=true
package SRR_Construction {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        expose BlueDog::DesignIntent;
        expose BlueDogRequirements::desktopManufacture;
        expose BlueDogStructure::hybridConstruction;
        expose BlueDogStructure::printTileEnvelope;
        metadata Layout about BlueDog::DesignIntent { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::desktopManufacture { x = 400; y = 0; }
        metadata Layout about BlueDogStructure::hybridConstruction { x = 800; y = 0; }
        metadata Layout about BlueDogStructure::printTileEnvelope { x = 0; y = 400; }
    }
}
```

The selected construction is an FDM substrate with wet-layup glass/epoxy reinforcement. Evidence-backed laminate properties, functional deformation limits and glass-to-print bond proof are separate [construction qualification requirements](requirements/requirements-practicality.md#construction-qualification).

The 10 GPa/50 MPa inputs and other [preliminary structural screens](methods/modeling.md#requirements-versus-design-assumptions) are not challenge-derived material minima.

The next experiments should inform structural mass, seams, wing behavior, actuator loads and casualty recovery. Their results feed the model before detailed design release.

[Construction requirements](requirements/requirements-practicality.md#construction) · [Structure and recovery methods](structures-and-recovery.md)

## 12 · Three kinds of evidence

| Evidence | What it can establish now | What it cannot establish |
| --- | --- | --- |
| Native model and regression checks | Consistent criteria and implemented behavior in supplied cases | Physical vessel performance |
| Mission and sizing studies | Conditional predictions and sensitivity | Calibrated mission probability outside their validity |
| Physical tests | Measured behavior for the tested configuration | Automatic transfer to a different boat or environment |

[Verification plans](../models/missions/verification.sysml) remain inconclusive until supported by the required evidence.

## 13 · What is resolved, and what comes next

The SRR preparation defines the course and bridge passage, recovery-site selection, environmental design basis, traffic-performance allocations and impaired-sensing risk method. The model, reference routing, verification plans and fresh evidence use the same proposed baseline. These are concrete proposals for your review, not analyses you need to perform.

```sysml-report BlueDogSRRReadinessDocuments::Encounters
```

The largest allocated closing-speed case needs 724 m of acquisition distance; the proposed design envelope rounds this to 750 m. This is an engineering allocation, not a navigation-rule stand-off. Demonstrating detection from a small, moving boat—especially in darkness—is a major PDR feasibility question.

| Next gate | Deliverable | Who does the work |
| --- | --- | --- |
| PDR | Demonstrate a credible sensing/maneuver architecture and route/casualty recovery coverage; select a feasible design from the frontier | Analysis agent, using owner-supplied field observations and priorities |
| CDR | Correlate critical loads, construction, propulsion and capsize behavior; release a defined build | Analysis agent integrates experiments conducted with the owner |
| Each TRR | Confirm actual sites, access, notices, stage, forecast and the tested configuration; accept the scoped residual risk | Agent prepares the evidence; owner reviews and authorizes the trial |

[Completed desktop assessments and explicit gate criteria](srr-appendix.md#review-actions)

## 14 · Your SRR disposition

The available decisions are **proceed**, **proceed with limitations**, or **iterate**. No decision is recorded yet.

**Recommendation: proceed with limitations** to concept development and supervised component experiments. No unattended on-water operation is included. A limited release can authorize this work. It does not authorize an unattended challenge trial or certify the current numerical design.

Review the baseline and proposed allocations, add actions, and identify the limits of any approval. I will implement the resulting actions and return the changed evidence for review.

[Technical appendix](srr-appendix.md) · [Development plan](development-plan.md)
