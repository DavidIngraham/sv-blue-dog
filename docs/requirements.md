# Requirements: what the boat must achieve

The requirements turn the Gorge challenge and my practical constraints into observable obligations. They define the job before I choose hardware. The six references below retain the detailed model statements; the governing decisions are enough to continue the main story.

- **Complete one independent, sail-only round trip.** Start at the Bingen gate, round Buoy 16 near Stevenson and return. Safe waiting is allowed; motor use, intervention, anchoring, grounding or refuge ends qualification.
- **Make decisions onboard.** Shore communications support observation. Their loss must not remove navigation or safety capability.
- **Preserve safety and recoverability.** The boat must avoid collisions, meet applicable navigation duties and act autonomously when a required capability is lost. Capsize alone need not end qualification if unassisted recovery preserves the required safety functions without motor use.
- **Carry enough usable energy.** Support the finite passage and its delays while preserving recovery reserve. This mission imposes neither a fixed 72-hour deadline nor daily energy neutrality.
- **Survive the declared conditions.** Environmental, structural and casualty tests must identify their configuration and exposure. A calculated margin is evidence for a prediction, not a physical demonstration.
- **Remain practical for me to build and handle.** Printed jobs must fit a 250 × 250 × 250 mm envelope; assembled structures can be larger. One person must be able to transport, launch and retrieve the boat with appropriate aids.

Hawai‘i and sustained repeated operation are separate future missions. Their labeled ocean and repeating-energy requirements remain in the reference model, but they do not set acceptance criteria for the first Gorge boat.

The challenge also encourages routes and operating windows that reduce traffic encounters. That is guidance, not a pass/fail test of whether another skipper changes course. My stronger [courtesy preference for Blue Dog](encounter-feasibility.md#leave-room-for-crewed-boats) accepts delay to reduce the need for crewed boats to maneuver, while preserving safe, rule-consistent behavior.

## Which requirements can the sensing study challenge?

Avoiding collision and meeting applicable navigation duties remain mission obligations. Observation
distance depends on target class, encounter geometry, uncertainty and
achievable response.

I keep two questions separate: **how much distance does the response need**, and
**how reliably must the installation provide a usable observation**? Consequences inform reviewed clearance and extra distance margins as well as
observation reliability; exposure also informs reliability and admissible
conditions. None can reduce the physical response time or maneuver distance.
Accepted numerical class allocations remain unresolved.
Occupied kayaks, occupied stand-up paddleboards, people in the water and
unoccupied craft are distinct cases. A potentially minor glancing contact is a
specific hypothesis, not a zero-consequence classification.

L-104 permits explicitly reviewed residual risk. No numerical severity or
probability threshold has been accepted, and the provisional mission-reliability
objective is not a collision-risk budget. The
[encounter reference](reference/encounter-envelope.md#can-i-exclude-a-rare-or-difficult-target-class)
explains the evidence needed to complete these allocations. All traffic classes
remain in scope; acoustic and optical choices must expose their unsupported cases.

## Reference by engineering question

| Topic | What to look up |
| --- | --- |
| [Mission and endurance](requirements/requirements-mission.md) | Course completion, qualification, launch admission and reliability |
| [Autonomy and observation](requirements/requirements-autonomy.md) | Navigation, wind data, faults, restarts and trustworthy records |
| [Energy and recovery propulsion](requirements/requirements-energy.md) | Available-energy estimates, low-energy priorities, motor permission and reserve |
| [Environment and casualty recovery](requirements/requirements-environment.md) | Operating exposure, wet integrity, capsize, weeds and component retention |
| [Traffic safety and monitoring](requirements/requirements-safety.md) | Traffic response, navigation signals, telemetry, commands and autonomous abort |
| [Manufacturing and handling](requirements/requirements-practicality.md) | Printed construction, material qualification, one-person handling and service |

Each reference starts with the design consequence, then offers expandable model views and authoritative statements. Repeated upstream requirements remain visible in the diagrams; their statements appear only at their first occurrence on each page. In a view, arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision and **dependency** records a design basis. These relationships explain why a requirement exists; evidence must separately establish whether a configuration meets it. The [modeling reference](methods/modeling.md) explains the notation and the distinction between requirements and provisional design assumptions.

These obligations have to fit in one boat. The next article examines the mass and energy needed for sensing, sailing and independent recovery in IC-01.

**Next:** [IC-01 candidate results](results.md) · [Series guide](index.md)
