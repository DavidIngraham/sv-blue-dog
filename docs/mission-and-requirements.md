# Mission and requirements

Working baseline, October 9, 2026. The independent [challenge brief](challenge-brief.md) is defined in [challenge.sysml](../models/challenge.sysml) and imported by the vehicle requirements. Mission and architecture are in [blue-dog.sysml](../models/blue-dog.sysml); requirements and explicit derivations are in [requirements.sysml](../models/requirements.sysml). This page records decisions, rationale, and open questions; requirement definitions belong in the model.

## Mission agreed with David

The agreed threshold is completion of an autonomous sailing journey from The Dalles to Bonneville and back to The Dalles. The objective is to autonomously repeat The Dalles-Bonneville-The Dalles route for as long as practical. This replaces the earlier indefinite-operation wording: no fixed objective duration has been agreed. A qualifying round trip must be completed without operator intervention. Live operator monitoring is required. Termination conditions, monitoring coverage, and update interval remain to be agreed. Multi-day endurance with energy harvesting remains an earlier design intent to refine against this objective. Supervised local trials are proposed validation steps toward that mission, not a replacement design target.

The original Microtransat inspiration became a smaller trans-gorge idea: complete the Gorge Blowout course, with the longer round trip as an ambition. David selected the round trip as the electronics design mission on October 9, 2026.

Project objectives are to learn sailing, explore desktop manufacturing, build a complete autonomous system, and learn SysML v2 by modeling the mission and architecture. A persistent swell-monitoring mission with station keeping remains a stretch objective.

"Set and forget" now means no operator intervention during a qualifying round trip, while allowing live observation. Monitoring does not imply approval of remote mission guidance. Loss of the monitoring link shall not interrupt autonomous mission execution. The vessel shall retain telemetry onboard during the outage and transmit the retained data when contact returns. E-005 and E-007 specify outage handling, current-record priority and retention. A remote emergency override for mission abort or manual control is required when a command link is available. Using it disqualifies that attempt as an unassisted round trip; passive monitoring does not. S-003 and C-102 specify abort latching and command handling. No route coordinates, dam passages, or operating permissions are assumed by this model.

Auxiliary motor propulsion is allowed for development tests but prohibited during a qualifying challenge attempt (C-004). An auxiliary motor may remain installed and be used for vessel recovery outside a qualifying attempt. Using it during an attempt ends that attempt without qualification.

## Two top-level requirements

C-000, the independent Trans-Gorge challenge, and H-001, the Hawaii voyage goal in `blue-dog.sysml`, are the two top-level requirements. The challenge rules refine C-000. Vehicle requirements derive from those rules and H-001, with shared capabilities tracing to both missions. The Hawaii goal is confirmed intent; its detailed derivations remain proposed and its acceptance conditions are open.

## Long-term direction

The long-term ambition is to work toward a vessel capable of making a voyage to HawaiÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¹Ã…â€œi.
The Gorge is intended as a "torture test" for autonomy, endurance, and reliability.
The current baseline is the repeated Gorge route; an ocean departure point, passage
route, duration, and ocean-specific acceptance criteria have not been selected.
Gorge experience will inform that future mission, rather than establish ocean readiness by itself.

## Proposed mission decomposition

Prepare and launch; sail outbound; turn around; sail home to complete the threshold round trip; continue repeating the route for the endurance objective; eventually recover the boat and data. Energy management, health monitoring/recovery, communication, and data recording support the mission throughout. The initial SysML actions express decomposition only; sequencing, concurrency, triggers, and abort paths are the next modeling step.

## Acceptance criteria

The printer build envelope is 250 Ã— 250 Ã— 250 mm, including the entire oriented print job. Numerical handling, timing, energy and environmental values are proposed design targets. See the [verification plan](verification-plan.md) for provenance, executable predicates, physical evidence and remaining blockers. Environmental parents now derive into individually testable leaves, including explicit milfoil tolerance.

## Requirement derivation

Explore the [focused requirements views](requirements-views.md), starting with the [Trans-Gorge challenge](figures/requirements-c-000.md) and [Hawaii objective](figures/requirements-h-001.md). Each parent has its own small diagrams and links to the next level.

[Generated requirement statements and derivation rationale](requirements-register.md)

Every dashed arrow comes from an explicit `#derivation` connection in the SysML model, with `#original` and `#derive` ends. Native OpenSysML arrows read from derived to original requirement. Short IDs are listed in the register. This is a generated traceability view, not a claim of a complete standard graphical notation implementation.

The explicit derivation relationships are proposed reasoning for us to review. Node maturity is separate: a legacy requirement can have a newly proposed derivation. The challenge threshold and endurance objective remain separate inputs; the round-trip route alone does not imply a particular endurance. Low-energy recovery has two parents because it follows both the endurance objective and the energy-management policy. No link means "verified" or "satisfied."

Regenerate with `uv run python scripts/render_requirements.py`. The [modeling guide](../models/README.md) records the renderer scope and validation limits.

## Verification and remaining decisions

Use the [verification plan](verification-plan.md), [environmental hierarchy](environmental-envelope.md), [operating constraints](operating-constraints.md), and [architecture traceability](traceability.md). Remaining mission inputs include course gates, boundary margins, Hawaii route, traffic-detection scenarios, legal applicability and representative weed-test material. Model evaluation does not resolve these inputs.

The recovery architecture remains open; the [water-versus-air propeller trade study](recovery-propulsion-trade.md) compares both against the recovery energy and weed requirements.

An [independent requirements and derivation audit](requirements-audit.md) records defects, implemented corrections and remaining evidence gaps. Derivation rationales distinguish imposed stakeholder constraints from consequences of the mission.
