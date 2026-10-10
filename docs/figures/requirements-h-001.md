# H-001 HawaiiVoyage relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**H-001 HawaiiVoyage** — The vessel shall complete an autonomous sailing voyage to Hawaii.

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| multiDayEndurance | hawaiiVoyage | An ocean passage motivates sustained energy autonomy; multi-day operation is an interim capability, not an ocean endurance sizing result. This is design motivation or an implementation choice, not a satisfaction implication. |
| navigationAndControl | hawaiiVoyage | An autonomous Hawaii passage needs ocean guidance and sailing control; N-001 specifies its environmental design envelope. This is design motivation or an implementation choice, not a satisfaction implication. |
| communications | hawaiiVoyage | The long-term ocean mission motivates review of monitoring coverage and outage behavior without selecting a radio technology. This is design motivation or an implementation choice, not a satisfaction implication. |
| resetRecovery | hawaiiVoyage | Extended unattended operation motivates recovery from onboard resets. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionEvidence | hawaiiVoyage | Ocean mission assessment requires retained voyage evidence; E-007 specifies recording and retention acceptance criteria. This is design motivation or an implementation choice, not a satisfaction implication. |
| environmentalEnvelope | hawaiiVoyage | Ocean operation requires its own environmental envelope; Gorge success does not establish it. This is design motivation or an implementation choice, not a satisfaction implication. |
| oceanEnvironment | hawaiiVoyage | The Hawaii mission sets the ocean environment; this profile is not a Gorge acceptance prerequisite. This is design motivation or an implementation choice, not a satisfaction implication. |
| operatingBoundary | hawaiiVoyage | An ocean route also needs configured boundaries and no-feasible-route behavior; its boundaries differ from the Gorge course. This is design motivation or an implementation choice, not a satisfaction implication. |
| regulatoryClassification | hawaiiVoyage | Deployment permissions and applicable rules depend on the ocean route as well as the Gorge mission. This is design motivation or an implementation choice, not a satisfaction implication. |
| serviceability | hawaiiVoyage | Unattended ocean preparation and post-voyage maintenance motivate replaceable modules; this is not at-sea servicing during qualification. This is design motivation or an implementation choice, not a satisfaction implication. |
| sustainedEnergyFeasibility | hawaiiVoyage | The ocean ambition requires sustained energy autonomy; route-specific resources remain unresolved. This is design motivation or an implementation choice, not a satisfaction implication. |
| cruisePerformance | hawaiiVoyage | cruisePerformance is a selected engineering objective supporting hawaiiVoyage. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionReliability | hawaiiVoyage | missionReliability is a selected engineering objective supporting hawaiiVoyage. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: L-001 MissionReliability](<requirements-l-001.md>)

[Continue: Q-001 CruisePerformance](<requirements-q-001.md>)

[Continue: E-200 SustainedEnergyFeasibility](<requirements-e-200.md>)

[Continue: P-003 Serviceability](<requirements-p-003.md>)

[Continue: S-005 RegulatoryClassification](<requirements-s-005.md>)

[Continue: S-002 OperatingBoundary](<requirements-s-002.md>)

[Continue: N-020 OceanEnvironment](<requirements-n-020.md>)

[Continue: N-001 EnvironmentalEnvelope](<requirements-n-001.md>)

[Continue: E-007 MissionEvidence](<requirements-e-007.md>)

[Continue: E-003 ResetRecovery](<requirements-e-003.md>)

[Continue: E-005 Communications](<requirements-e-005.md>)

[Continue: E-002 NavigationAndControl](<requirements-e-002.md>)

[Continue: M-002 MultiDayEndurance](<requirements-m-002.md>)
