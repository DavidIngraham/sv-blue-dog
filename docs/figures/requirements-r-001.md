# R-001 RecoveryPropulsion relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**R-001 RecoveryPropulsion** — At maximum mission load, powered recovery shall sustain at least 0.5 m/s over ground for 30 minutes against a 1.5 m/s current.

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| recoveryEnergy | recoveryPropulsion | RecoveryEnergy supports recoveryPropulsion. This is design motivation or an implementation choice, not a satisfaction implication. |
| recoveryPropulsorWeeds | recoveryPropulsion | The recovery propulsor must remain usable in the vegetation encountered by the sailing vessel. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: N-056 RecoveryPropulsorWeeds](<requirements-n-056.md>)

[Continue: R-002 RecoveryEnergy](<requirements-r-002.md>)
