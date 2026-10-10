# M-001 RoundTrip relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**M-001 RoundTrip** — The vessel shall cross the configured The Dalles departure, Bonneville turnaround and The Dalles return gates in order during one qualifying attempt.

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| navigationAndControl | roundTrip | Autonomous completion of the route needs observations, guidance, and actuation. This is design motivation or an implementation choice, not a satisfaction implication. |
| resetRecovery | roundTrip | A reset during an autonomous journey must not leave mission behavior undefined. This is design motivation or an implementation choice, not a satisfaction implication. |
| communications | roundTrip | Mission supervision and recovery need an agreed operator communication policy. This is design motivation or an implementation choice, not a satisfaction implication. |
| ingressResponse | roundTrip | Recovering the boat after the journey motivates a defined response to small leaks. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionEvidence | roundTrip | Assessing route completion and learning from the mission requires recorded evidence. This is design motivation or an implementation choice, not a satisfaction implication. |
| operatingBoundary | roundTrip | OperatingBoundary supports roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| regulatoryClassification | roundTrip | RegulatoryClassification supports roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| environmentalEnvelope | roundTrip | EnvironmentalEnvelope supports roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| gorgeEnvironment | roundTrip | The Gorge mission sets the river environment; it does not impose the ocean profile. This is design motivation or an implementation choice, not a satisfaction implication. |
| cruisePerformance | roundTrip | cruisePerformance is a selected engineering objective supporting roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionReliability | roundTrip | missionReliability is a selected engineering objective supporting roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: L-001 MissionReliability](<requirements-l-001.md>)

[Continue: Q-001 CruisePerformance](<requirements-q-001.md>)

[Continue: N-010 GorgeEnvironment](<requirements-n-010.md>)

[Continue: N-001 EnvironmentalEnvelope](<requirements-n-001.md>)

[Continue: S-005 RegulatoryClassification](<requirements-s-005.md>)

[Continue: S-002 OperatingBoundary](<requirements-s-002.md>)

[Continue: E-007 MissionEvidence](<requirements-e-007.md>)

[Continue: E-006 IngressResponse](<requirements-e-006.md>)

[Continue: E-005 Communications](<requirements-e-005.md>)

[Continue: E-003 ResetRecovery](<requirements-e-003.md>)

[Continue: E-002 NavigationAndControl](<requirements-e-002.md>)
