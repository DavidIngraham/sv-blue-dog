# R-002 RecoveryEnergy relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**R-002 RecoveryEnergy** — The protected reserve shall equal or exceed 1.2 × (30 minutes of worst-case recovery motor demand + 2 hours of essential recovery demand).

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| launchEnergyAdmission | recoveryEnergy | LaunchEnergyAdmission isolates a separately verifiable consequence of recoveryEnergy. This is design motivation or an implementation choice, not a satisfaction implication. |
| sustainedReserveProtection | recoveryEnergy | Sustained operation protects the recovery reserve sized by the existing R-002 policy. This is design motivation or an implementation choice, not a satisfaction implication. |
