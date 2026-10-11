# Reading the recorded sizing evidence

The recorded candidate is an exploratory numerical result. Its model instances preserve the source revision, configuration and scenario outcomes. They are a projection of that run, not a claim that the current source has completed a new optimization.

Nominal and adverse cases are reviewed separately. The model keeps operating feasibility, sampled static restoring behavior and evidence acceptance distinct. In particular, a positive sampled roll result on an unstable pitch branch is not proof of self-righting.

The build publishes the native record review below. Read the [sizing method](sizing.md) for how the result was obtained and the [source evidence](../evidence/runs/2026-10-10-coupled/manifest.json) for its provenance.

```sysml-report BlueDogEvidenceDocuments::Summary
```

```sysml-view Page_results_0::candidate direction=TB
package Page_results_0 {
    private import StandardViewDefinitions::*;
    view candidate : GeneralView {
        expose BlueDogRecordedSizing::candidate;
    }
}
```

The [OpenVSP experiment gallery](sail-trade.md#what-we-have-actually-run-in-openvsp) includes the tested geometry, alpha sweeps, mesh sensitivity and induced-drag polars from the archived aerodynamic runs.
