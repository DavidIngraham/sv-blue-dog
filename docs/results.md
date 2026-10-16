# Sizing Blue Dog for the Gorge

**OOSEM:** Trades, optimization and analysis · [Maturity assessment](development-plan.md)

The current integration question is whether **IC-01** supports sensing, guidance, sailing energy and independent recovery as one coherent candidate. Its [allocation](../models/analyses/integrated-candidate.sysml) includes sensing/compute demand and recovery equipment in a fresh coupled evaluation. The [virtual acceptance requirement](development-plan.md#integration-milestone) combines those sizing results with representative mission and casualty simulations. It does not select catalog hardware or establish physical qualification.

## Integrated candidate sizing

The [IC-01 coupled replay](../evidence/runs/2026-10-15-integrated-candidate/integrated-sizing.json) passes the nominal Gorge static screens with all eight operating states balanced and screen-feasible at 5 and 8 m/s wind. Accepted states can come from the feasible solve phase even when the subsequent speed-maximization phase stops at its iteration limit; these results establish a feasible allocated candidate, not an optimum.

| Quantity | IC-01 nominal result |
| --- | --- |
| Overall swept length / hull beam | 1.200 m / 0.420 m |
| Total modeled mass | 20.061 kg |
| Wing area | 0.400 m² |
| Main / independent recovery battery | 1,300 Wh / 60 Wh nameplate |
| Maximum sampled average / peak sailing bus load | 12.916 W / 15.633 W |
| Conditional westerly passage / energy exposure allowance | 38.884 h / 54.605 h |
| Main-pack departure / required energy | 936.000 Wh / 833.938 Wh |
| Main-pack headroom after allocated reserve | 102.062 Wh |

The energy allowance includes the existing 25% passage multiplier and six-hour delay, with no harvest credit. The 15 kg handling limit applies to individual modeled assemblies, not total vessel mass; those assembly screens pass. Structural, installation-volume and sampled static righting screens also pass under their provisional material and geometry assumptions. Resistance-domain checks are necessary bounds, not experimental validation of every hull within them. Neither these screens nor the larger energy margin establish real sensing, dynamic capsize recovery or full-course safety.

## Retained nominal sizing reference

The **1.2 m overall-length, 440 Wh reference** passes the nominal refined Gorge static screens on the selected Hood River bridge route. It has a 260 mm hull beam, weighs **10.313 kg**, predicts a **33.87-hour** conditional westerly passage, and retains **3.97 Wh** beyond the allocated voyage energy. This is a separate configuration from IC-01. It remains a preliminary design requiring sensitivity studies and physical evidence. Its structural margins use the provisional analysis basis; they do not qualify material properties, functional deformation limits or casualty flotation.

The [power and energy budgets](energy.md#current-candidate-budget) distinguish the two configurations and break the retained reference's demand into electronics, wind sensing, actuation, discharge losses, self-discharge and protected recovery reserve. Both identify the remaining installation evidence needs.

```sysml-report BlueDogSRRCurrentDocuments::Summary
```

[Current replay, mission outcomes and limitations](srr-appendix.md#current-baseline-evidence)

This study takes the finite Bingen–Stevenson challenge, manufacturing assumptions and provisional physics as inputs. It informs concept selection and the measurements needed before detailed design. The [sizing method](sizing.md) explains the calculations; the [mission simulation](mission-simulation.md) adds changing weather, traffic and recovery decisions.

The [development spirals](simulation-spirals.md#develop-the-trades-alongside-the-voyage) place these results alongside the open rig and recovery trades and the working assumptions that make each comparison possible.

## Search for alternatives, then choose a design

Overall length is a constraint on the full operating envelope, including appendage sweeps. Hull length and the other 28 design variables remain free, together with 48 operating-state variables. Separate mass and conditional-passage objectives expose competing choices instead of hiding them in a weighted score. The design team will choose a balance after comparing the candidates.

The bounded local study examines 1.2, 1.0 and 0.8 m overall-length caps. It retains feasible accepted iterates even if a later solver step fails. An unresolved search is not proof that a smaller boat is impossible. These are local monohull alternatives; they do not establish a global optimum or compare every hull architecture.

There is no minimum sailing-speed floor, 72-hour challenge deadline or daily energy-neutrality requirement. Stored energy is sized for a finite passage and protected recovery. The passage multiplier and delay allowance remain provisional design allocations in [the concept policy](../models/analyses/sizing/credibility.sysml).

In the archived search configuration, both coarse-feasible outputs remained effectively the same 1.2 m seed: their masses differ by less than 0.1 g and their conditional passage times by about 2.4 minutes. This bounded run has not yet produced a useful spread of design choices. The 1.0 and 0.8 m searches remain unresolved; infeasible terminal points are listed for diagnosis, not offered as alternatives.

<details>
<summary>Search evidence and configuration limits</summary>

These figures describe their archived configuration. Their feasibility verdicts do not apply to the current course.

![Coarse-feasible mass and passage-time alternatives, with unresolved length caps identified.](figures/srr-frontier.svg)

```sysml-report BlueDogSRRFrontierDocuments::Summary
```

## What the finer replay tells us

```sysml-report BlueDogSRRFrontierDocuments::SeedReplay
```

In the archived seed replay, the retained 1.2 m seed balanced its operating cases, but the voyage-energy margin fell to −0.00556 as conditional passage changed from 33.66 to 33.74 hours. That seed is distinct from the 440 Wh candidate assessed above.

The sampled sealed-body recovery curves have pitch equilibria and positive restoring roll moments at all interior samples across four wing trims. That does not establish dynamic capsize recovery, pitch stability, structural integrity or recovery with damaged equipment. The challenge permits limp recovery to shore; self-righting remains one possible vehicle strategy.

This replay applies to the retained seed, not automatically to every frontier alternative. It also does not include a calibrated weather-window completion probability. The environmental and traffic campaign must assess each selected candidate with the same scenario realizations before we compare mission outcomes.

</details>

## What needs to improve before selecting a boat

The useful next work is to test sensitivity to construction and foil assumptions, and connect eligible alternatives to chronological mission and recovery scenarios. Physical measurements of laminate stiffness, joints, actuator loads and wing behavior are still needed to establish model credibility.

Cost and construction effort need a bill of materials and process estimates. Recovery needs assessed shore approaches and casualty capabilities. Until those inputs exist, a mass-versus-time plot represents only part of the design decision.

The [mission and design assessment](srr-review.md) connects these findings to the requirements and remaining evidence. A solver pass does not qualify a vessel for an unattended trial.

[Archived run and source provenance](../evidence/runs/2026-10-13-srr-frontier/manifest.json) · [Generated model evidence](../models/evidence/srr-frontier.sysml)

**Next:** [How the sizing search works](sizing.md).
