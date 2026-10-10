# C-006 EmergencyIntervention relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**C-006 EmergencyIntervention** — The vessel shall permit remote emergency abort or manual control when a command link is available.

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| communications | emergencyIntervention | Vehicle communications provide emergency commands whose use ends attempt qualification. This is design motivation or an implementation choice, not a satisfaction implication. |
| safeRecovery | emergencyIntervention | Permitted emergency intervention requires explicit abort, qualification, isolation and control-loss behavior. This is design motivation or an implementation choice, not a satisfaction implication. |
| commandIntegrity | emergencyIntervention | The emergency control channel needs authenticated, fresh commands and persistent qualification changes. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: C-102 CommandIntegrity](<requirements-c-102.md>)

[Continue: S-003 SafeRecovery](<requirements-s-003.md>)

[Continue: E-005 Communications](<requirements-e-005.md>)
