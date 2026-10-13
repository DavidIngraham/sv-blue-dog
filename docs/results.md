# Sizing Blue Dog for the Gorge

**Design phase:** Concept and preliminary design · PDR · [Development plan](development-plan.md)

The revised search has found a coarse-feasible candidate inside the **1.2 m overall-length limit**: about **10.3 kg**, with a conditional steady-westerly passage of about **33.7 hours**. This is encouraging, but the finer replay misses the voyage-energy screen by **0.56%**. It is a candidate to improve, not a build baseline.

This study takes the finite Bingen–Stevenson challenge, manufacturing assumptions and provisional physics as inputs. It informs concept selection and the measurements needed before detailed design. The [sizing method](sizing.md) explains the calculations; the [mission simulation](mission-simulation.md) adds changing weather, traffic and recovery decisions.

## Search for alternatives, then choose a design

Overall length is a constraint on the full operating envelope, including appendage sweeps. Hull length and the other 28 design variables remain free, together with 48 operating-state variables. Separate mass and conditional-passage objectives expose competing choices instead of hiding them in a weighted score. The design team will choose a balance after comparing the candidates.

The bounded local study examines 1.2, 1.0 and 0.8 m overall-length caps. It retains feasible accepted iterates even if a later solver step fails. An unresolved search is not proof that a smaller boat is impossible. These are local monohull alternatives; they do not establish a global optimum or compare every hull architecture.

There is no minimum sailing-speed floor, 72-hour challenge deadline or daily energy-neutrality requirement. Stored energy is sized for a finite passage and protected recovery. The passage multiplier and delay allowance remain provisional design allocations in [the concept policy](../models/analyses/sizing/credibility.sysml).

Both feasible outputs remain effectively the same 1.2 m seed: their masses differ by less than 0.1 g and their conditional passage times by about 2.4 minutes. This bounded run has not yet produced a useful spread of design choices. The 1.0 and 0.8 m searches remain unresolved; infeasible terminal points are listed for diagnosis, not offered as alternatives.

![Coarse-feasible mass and passage-time alternatives, with unresolved length caps identified.](figures/srr-frontier.svg)

```sysml-report BlueDogSRRFrontierDocuments::Summary
```

## What the finer replay tells us

```sysml-report BlueDogSRRFrontierDocuments::SeedReplay
```

The retained 1.2 m seed balances its operating cases at the finer geometry resolution. Its conditional westerly passage changes from 33.66 to 33.74 hours. The voyage-energy margin falls to −0.00556, so the candidate does not pass all refined screens. A small numerical shortfall can still matter when other margins are tight; it should be resolved by re-optimization and sensitivity checks, not rounded away.

The sampled sealed-body recovery curves have pitch equilibria and positive restoring roll moments at all interior samples across four wing trims. That does not establish dynamic capsize recovery, pitch stability, structural integrity or recovery with damaged equipment. The challenge permits limp recovery to shore; self-righting remains one possible vehicle strategy.

This replay applies to the retained seed, not automatically to every frontier alternative. It also does not include a calibrated weather-window completion probability. The environmental and traffic campaign must assess each selected candidate with the same scenario realizations before we compare mission outcomes.

## What needs to improve before selecting a boat

The useful next work is to resolve the refined energy shortfall, test sensitivity to construction and foil assumptions, and connect eligible alternatives to chronological mission and recovery scenarios. Physical measurements of laminate stiffness, joints, actuator loads and wing behavior are still needed to establish model credibility.

Cost and construction effort need a bill of materials and process estimates. Recovery needs assessed shore approaches and casualty capabilities. Until those inputs exist, a mass-versus-time plot represents only part of the design decision.

The [SRR review](srr-review.md) separates the requirements baseline from these preliminary design findings. Neither a solver pass nor SRR approval qualifies a vessel for an unattended trial.

[Archived run and source provenance](../evidence/runs/2026-10-13-srr-frontier/manifest.json) · [Generated model evidence](../models/evidence/srr-frontier.sysml)

**Next:** [How the sizing search works](sizing.md).
