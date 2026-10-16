# Sizing workflow and numerical diagnostics

The current comparison uses overall-length caps with separate mass and conditional-passage-time objectives. Fixed-length continuation and the original length-minimization solver are diagnostic or historical workflows.

## Current frontier comparison

After installing the pinned environment and preparing the model, run:

```sh
uv run python -m tools.boat_analysis.optimization.frontier --caps 0.8 1.0 1.2
```

## Diagnostic continuation

Feasibility restoration precedes the local size search. Derivatives respect interpolation-grid breakpoints. Small mesh reserves protect against numerical drift; they are separate from physical uncertainty. Continuation starts from the named appendage-screened archive and restores it against the current constraints before reducing length, targets 0.2 m length reductions, and halves unsuccessful steps down to 0.025 m. Each stage first seeks the closest feasible design with constrained SLSQP, then uses least-squares restoration if needed. Each method receives a budget of 60 iterations or residual evaluations respectively, with up to two extensions when violation norm improves by at least 5 percent. A failed stage also tries a wider-hull, reduced-wing/ballast starting guess; those changes are not constraints. A stage stops once an accepted iterate passes the unchanged feasibility tolerance; it does not continue polishing proximity to the seed. Separate records retain the smallest feasible design and best infeasible attempt, and restoration uses the best intermediate constrained correction rather than discarding it for a worse final iterate. No stage relaxes physical acceptance criteria. This is local feasibility tracing, not a proof that a failed length cannot work. Refined replay re-solves operating states with peak-power constraints, then identifies any diagnostic solve that removes that check. The finite energy and volume screens also run in refined replay; chronological mission evaluation remains necessary for actual weather and traffic histories. A failed local solve is not proof of physical impossibility.



## Prepare the environment and reproduce diagnostic runs

Use the package-free uv environment from the repository root. Native compiled execution uses Linux/GCC, including WSL. Keep Windows and Linux virtual environments separate.

```sh
python tools/boat_analysis/model/install.py
uv sync --locked
uv run python -m tools.boat_analysis.cli validate
uv run python -m tools.boat_analysis.cli prepare
uv run python -m tools.boat_analysis.cli continue-sizing --target 1.2
uv run python -m tools.boat_analysis.mission.campaign --count 32 --candidate build/analysis/sizing-continuation.json
uv run python -m tools.boat_analysis.optimization.credibility build/analysis/sizing-continuation.json
# The original unconstrained-length search remains available:
uv run python -m tools.boat_analysis.cli solve
uv run python -m tools.boat_analysis.cli replay
uv run python -m tools.boat_analysis.cli recovery
uv run python -m tools.boat_analysis.cli pitch
uv run python -m tools.boat_analysis.cli audit
```

Continuation writes `build/analysis/sizing-continuation.json` and leaves the replay candidate untouched; a continuation result must be selected explicitly before refined replay. Preparation exports model inputs and compiles native calculations. Solving writes a candidate; replay and recovery are separate assessments. Outputs go to ignored `build/analysis`, not to authored documentation. Accepted records are archived without overwriting earlier runs and projected into named model instances for publication. The current run is identified on the [results page](../results.md).

Replay holds the selected geometry fixed and re-solves controls for six hypotheses: the conservative primary case (stored as `nominal`), construction, additional aerodynamic degradation, hydrodynamic degradation, energy degradation, and their combination. These scenarios test sensitivity; they are neither probabilities nor demonstrated worst cases. An operating failure or pitch-unstable recovery sample remains visible even if the coarse sizing screen passed.

OpenVSP uses the separate package-free environment under `tools/boat_analysis/aerodynamics/vsp` because the pinned binary has its own Python ABI. Run its modules from the repository root with that uv project. The saved grid permits routine analysis without rerunning VSPAERO. Mesh convergence and a direct candidate comparison test numerical consistency; viscous drag, stall, broadside flow, thickness effects and dynamic sailing still need evidence.

The [results page](../results.md) reports which configuration and objective each search used and whether it reached feasibility. A diagnostic trial remains useful for replay when a search stops before feasibility. The reusable geometry checks include analytic section properties, displaced-volume oracles, mass moments, force and torque invariance, and native/interpreted parity. Qualification remains broader than those software checks.

[Recorded outcomes](../results.md) · [Sail concepts](../sail-trade.md) · [Structures and recovery](../structures-and-recovery.md)

## Refresh external wing evidence

The supported VSP installation is Windows with Python 3.13. From the repository root, use the separate locked environment:

```powershell
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.install_vsp
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.extract_sections
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.reference_vsp --mesh 32
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.polar_grid
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.convergence
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.check_candidate
```

Run the grid only when its CAD, coverage or solver settings change; it is substantially more expensive than document publication. New evidence is written under `build/analysis`. Regenerate native inputs after changing geometry evidence. Review results and provenance before archiving a new run and projecting it into the model; never overwrite an archived run in place.



## Generating the concept geometry

The geometry exporter extracts oriented exterior surfaces from the same tetrahedra used for buoyancy and geometric metrics. Named hull, wing, keel, rudder and ballast components are exported in metres as GLB. A neutral-pose calculation supplies mass, center of gravity and the fixed-pitch upright waterline. Exported volume and bounds must agree with the analysis geometry; the mesh carries no invented internal equipment or manufacturing detail.

`uv run python -m tools.publishing.concepts --figures docs/figures` regenerates the archived starting and smallest accepted concepts, metadata and equal-scale fixed views. The model publishing workflow supplies the mesh assets; the existing blog renders the interactive comparison inside the sizing article. Each accepted continuation stage exports its own mesh and metadata outside the optimizer's evaluation loop. Source hashes identify the candidate and exporter; changing the geometry basis requires a new analysis record.
