# Coupled sizing method

We first seek a feasible design, then minimize length while allowing the represented hull, rig, appendage, ballast, structure and energy variables to change together. Numerical brackets describe model coverage and search limits. A bound hit requires investigation before claiming a minimum size.

SysML owns the physical equations, named configurations, bounds, assumptions and acceptance criteria. Python evaluates geometric intersections and section properties, interpolates saved aerodynamic evidence and drives SciPy. Compiled array interfaces are confined to the runtime boundary. Reusable libraries have no dependency on Blue Dog requirements; application analyses connect them to the mission.

The model combines attached-flow wing forces and moments, underwater appendage forces, hull resistance, static buoyancy, material accounting, laminate screens and actuator energy. Both tacks contribute to progress with weights that cancel crosswind drift. Current changes sign between the legs; an easterly makes the upstream leg windward.

Feasibility restoration precedes the local size search. Derivatives respect interpolation-grid breakpoints. Small mesh reserves protect against numerical drift; they are separate from physical uncertainty. Refined replay re-solves operating states with energy constraints, then reports any energy-unconstrained diagnostic explicitly. A failed local solve is not proof of physical impossibility.

## Run the workflow

Use the package-free uv environment from the repository root. Native compiled execution uses Linux/GCC, including WSL. Keep Windows and Linux virtual environments separate.

```sh
uv sync --locked
uv run python -m tools.boat_analysis.cli install
uv run python -m tools.boat_analysis.cli validate
uv run python -m tools.boat_analysis.cli prepare
uv run python -m tools.boat_analysis.cli solve
uv run python -m tools.boat_analysis.cli replay
uv run python -m tools.boat_analysis.cli recovery
uv run python -m tools.boat_analysis.cli pitch
uv run python -m tools.boat_analysis.cli audit
```

Preparation exports model inputs and compiles native calculations. Solving writes a candidate; replay and recovery are separate assessments. Outputs go to ignored `build/analysis`, not to authored documentation. The committed baseline is an immutable exploratory run, identified by its original source revision. Reorganizing code does not relabel that run as fresh evidence.

OpenVSP uses the separate package-free environment under `tools/boat_analysis/aerodynamics/vsp` because the pinned binary has its own Python ABI. Run its modules from the repository root with that uv project. The saved grid permits routine analysis without rerunning VSPAERO. Mesh convergence and a direct candidate comparison test numerical consistency; viscous drag, stall, broadside flow, thickness effects and dynamic sailing still need evidence.

The reusable geometry checks include analytic section properties, displaced-volume oracles, mass moments, force and torque invariance, and native/interpreted parity. Qualification remains broader than those software checks.

[Recorded outcomes](results.md) · [Sail concepts](sail-trade.md) · [Structures and recovery](structures-and-recovery.md)

## Refresh external wing evidence

The supported VSP installation is Windows with Python 3.13. From the repository root, use the separate locked environment:

```powershell
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.install_vsp
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.extract_sections
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.reference_vsp --mesh 32
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.polar_grid
uv run --project tools/boat_analysis/aerodynamics/vsp python -m tools.boat_analysis.aerodynamics.vsp.check_candidate
```

Run the grid only when its CAD, coverage or solver settings change; it is substantially more expensive than document publication. New evidence is written under `build/analysis`. Regenerate native inputs after changing geometry evidence. Review results and provenance before archiving a new run and projecting it into the model; never overwrite an archived run in place.
