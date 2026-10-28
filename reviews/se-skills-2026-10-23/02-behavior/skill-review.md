# Behavior skill decision probes

Manual forward application, not an independent-agent review.

| Situation | Required distinction / response | Application |
| --- | --- | --- |
| Command exists but current permission was never passed to the actuator. | Command request is not authority. Expose the current permission boundary and its inhibited outcome. | Required scenario permission parameters/bindings and native sailing gate. |
| Recovery authority returns true after primary power loss. | Authority alone cannot override unknown qualification, missing durable record or an inhibit. | Recovery gate barrier tests retain R-101/R-102/E-138 conditions. |
| Abort is latched and motor recovery is needed. | Do not turn abort into a blanket motor inhibit. Qualification ends, while authorized safe recovery remains possible. | Recovery gate intentionally has no abort inhibitor; current recovery policy unchanged. |
| A restored sensor becomes healthy after disqualification. | Restored observation does not reset durable qualification state. | Existing supervisor tests and restart-fallback caller test. |
| A new MissionLogic instance begins nominally. | New-attempt initialization is distinct from restoration after watchdog reset. | Explicit restore_qualification API and native RestoreQualification, with invalid-record fallback. |
| A graph is sequential and every action has a performer. | That does not establish controller concurrency, timeouts, estimators or physical achieved response. | B-03/B-04 remain open; descriptive functions retain honest status. |
| A required input omits multiplicity and expressions happen to reject absence. | Inspect the resolved native contract; do not rely on accidental equation failure. | Explicit [1] plus native graph required-input checks. |
| Post-actuation logging reuses a command-planning record. | Distinguish pre-enable authorization durability from observed execution disposition. | Separate persistence step and actuator output record; graph endpoint/ordering assertions. |

Result: the skill led to concrete parameter, ordering, state and caller corrections without changing mission policy or inventing hardware evidence. Hardware arbitration, persistence and deadlines remain engineering work rather than claimed closure.
