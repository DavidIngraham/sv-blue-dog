# Skill decision-probe review

Manual application of the authored skill to realistic cases, 2026-10-23. This is not an independent-agent review.

| Probe | Correct decision under the skill | Application / evidence |
| --- | --- | --- |
| Clean up a navigation estimate that says valid=true but has no clock/frame context. | Preserve validity as a producer assertion; add semantic context and identify the missing consumer acceptance contract. Do not assert the packet is currently safe. | NavigationEstimate context/reference fields; IF-01/02/03; native freshness tests. |
| Set freshness to one second because the requirements say update once per second. | Decline that unsupported inference; preserve cadence, require an allocated consumer age criterion. | No maximumAge default; missing-criterion regression fails rather than succeeding. |
| The radio reports available=false and valid=true. | Interpret a valid link-down report, distinct from missing/invalid data; do not automatically end autonomous control. | LinkObservation retains separate flags; existing mission outage policy unchanged. |
| Reuse the same context type on every power connector. | Review physical quantities, mating and protection instead of treating a power transfer as a digital observation. | ElectricalSupply unchanged; IF-05 records actual physical gaps. |
| Mark recovery controller independence as established because it has a separate source ID. | Keep independence, startup, arbitration and common-cause evidence open. | CommandContext is not authentication/independence; IF-02/04 and existing candidate issue preserved. |
| Convert all flow-to-implementation mappings to generic dependency links. | Preserve native flow/allocation meaning and assess transformations and endpoints. | 28 logical exchange mappings remain; native architecture audit passes. |
| Cite ECSS Rev.1 clauses while the official file is unavailable. | Record edition/access limit; use inspected NASA/OMG/BIPM guidance for actual rules. | Source register explicitly identifies the outage and avoids uninspected clause claims. |
| Treat passing freshness unit tests as hardware qualification. | Report software predicate evidence and retain physical/interface acceptance as open. | review.md and current-assessment distinguish schema, execution, implementation and measurement. |

Manual review outcome: scope and major decision boundaries are coherent. Residual limits: completeness of consumer-specific limits, hardware integration and installed protocol design cannot be established by these probes. The skill should be revisited when actual equipment and operating procedures are chosen.
