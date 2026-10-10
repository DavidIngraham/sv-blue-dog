# C-002 RepeatedOperation relationships

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Conditions, rationale and verification](<../requirements-context.md>)

**C-002 RepeatedOperation** — After its first circuit, the vessel should repeat The Dalles–Bonneville–The Dalles autonomously for as long as practical.

## Design decisions motivated by this requirement

Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here.

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| multiDayEndurance | repeatedOperation | Repeated autonomous journeys motivate the existing endurance and harvesting requirement; M-002 defines an initial 72-hour campaign; indefinite operation remains an objective. This is design motivation or an implementation choice, not a satisfaction implication. |
| sustainedEnergyFeasibility | repeatedOperation | Repeated journeys motivate a repeatable energy cycle, beyond a one-off endurance run. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionReliability | repeatedOperation | missionReliability is a selected engineering objective supporting repeatedOperation. This is design motivation or an implementation choice, not a satisfaction implication. |

[Continue: L-001 MissionReliability](<requirements-l-001.md>)

[Continue: E-200 SustainedEnergyFeasibility](<requirements-e-200.md>)

[Continue: M-002 MultiDayEndurance](<requirements-m-002.md>)
