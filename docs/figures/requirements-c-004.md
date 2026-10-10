# C-004 SailingPropulsion relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**C-004 SailingPropulsion** — A qualifying attempt shall use sailing propulsion without auxiliary motor propulsion.

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| roundTrip | sailingPropulsion | Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. This is design motivation or an implementation choice, not a satisfaction implication. |
| challengeMotorInhibition | sailingPropulsion | ChallengeMotorInhibition isolates a separately verifiable consequence of GorgeChallenge::sailingPropulsion. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: R-004 ChallengeMotorInhibition](<requirements-r-004.md>)

[Continue: M-001 RoundTrip](<requirements-m-001.md>)
