# C-003 UnassistedAttempt relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**C-003 UnassistedAttempt** — A qualifying attempt shall complete the round trip without operator intervention.

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| navigationAndControl | unassistedAttempt | The vessel needs onboard guidance and control to complete an unassisted attempt. This is design motivation or an implementation choice, not a satisfaction implication. |
| challengeMotorInhibition | unassistedAttempt | No-intervention qualification must survive resets and motor-mode transitions. This is design motivation or an implementation choice, not a satisfaction implication. |
| commandIntegrity | unassistedAttempt | Accepted external control changes the attempt qualification; communications alone does not supply this rule. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: C-102 CommandIntegrity](<requirements-c-102.md>)

[Continue: R-004 ChallengeMotorInhibition](<requirements-r-004.md>)

[Continue: E-002 NavigationAndControl](<requirements-e-002.md>)
