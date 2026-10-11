# Conservative sizing: reading the results

This run searches the complete 29-variable design with the conservative aerodynamic policy and restricted operating angles. The search and one continuation stopped just outside the coarse feasibility tolerance, so the minimum-length phase did not run. The reported dimensions describe a near-feasible trial, not an established minimum or a qualified boat. A failed local search does not establish that no feasible design exists.

The limiting search margins include additional numerical reserves. In particular, a shortfall against the upstream progress reserve is not automatically a failure of the underlying mission progress requirement. The refined replay below assesses the selected geometry independently, using the actual operating screens and finer geometry.

The conservative primary case (stored as `nominal`) and five additional stress cases are reviewed separately. Replay fixes geometry and re-solves controls with finer geometry and free pitch. Durations from infeasible or energy-unconstrained diagnostic cases are numerical outputs, not predictions of successful sustained voyages. The model keeps operating feasibility, sampled static restoring behavior and evidence acceptance distinct: a positive roll result on an unstable pitch branch is not proof of self-righting.

The conservative primary replay balances the sailing states and passes the modeled energy and route screens. Its combined verdict still fails because the finer geometry exceeds the body-handling mass allocation. Additional aerodynamic degradation produces a substantial upstream-progress and passage-duration failure; construction and hydrodynamic stresses also lose upstream progress. The energy stress case requires diagnostic controls in all eight states. The combined stress case has negative easterly upstream progress and fails energy screens; its internal duration penalty is not a voyage-time prediction. These are conditional numerical findings, not measured sailing performance.

The build publishes the native record review below. Read the [sizing method](sizing.md) for how the result was obtained and the [current run manifest](../evidence/runs/2026-10-11-conservative/manifest.json) for exact source and evidence hashes. The earlier run remains archived as history and is not relabelled as a result of the revised method.

```sysml-report BlueDogEvidenceDocuments::Summary
```

```sysml-view Page_results_0::candidate direction=TB
package Page_results_0 {
    private import StandardViewDefinitions::*;
    view candidate : GeneralView {
        expose BlueDogCurrentSizing::candidate;
    }
}
```

The [ingress assessment](structures-and-recovery.md) finds negative restoring moments with a flooded or water-retaining wing. Even the positive sealed-wing roll samples include pitch-unstable equilibria. Self-righting therefore remains unproven.

The [OpenVSP experiment gallery](sail-trade.md#what-we-have-actually-run-in-openvsp) includes tested geometry, alpha and heel sweeps, mesh/wake sensitivity, induced-drag polars and a direct interpolation check at the trial's aspect ratio and camber. Those experiments support exploratory trends; measured low-Reynolds-number polars, stall, real drag and moment data are still missing. None of these numerical outcomes qualifies the vessel for the challenge.
