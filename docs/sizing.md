# Coupled sizing method

How small can Blue Dog be and still make headway upriver? For [preliminary design](development-plan.md#virtual-design), I start with the route, wind and current assumptions, then vary the hull, wing, ballast and energy system together. I want to find which designs are worth developing and which assumptions I most need to test.

![Qualitative force sketch: wing drive must overcome hull drag, while the keel resists side force and ballast supplies a restoring moment. Ground progress also includes current.](figures/sailing-forces.svg)

*A good wing is not enough. The whole boat must balance forces and moments, and its velocity through the water must still produce useful progress over the ground.*

```mermaid
flowchart TB
    accTitle: How the sizing study makes a candidate
    accDescr: The outer search changes the design. For each design, geometry and mass feed an inner operating solve. Constraint failures send the outer search back to a revised design. Independent replay and recovery challenge the selected trial.
    design["Outer search: hull, rig, ballast, structure, energy"] --> physics["Geometry and mass + aerodynamic / water-force models"]
    physics --> operating["Inner solve: trim and sailing equilibrium in each scenario"]
    operating --> screens["Progress, loads, energy, handling and recovery screens"]
    screens -->|revise design| design
    screens -->|feasible, then reduce length| trial["Selected trial"]
    screens -->|stop before feasibility: retain best trial| diagnosis["Diagnostic trial: current run"]
    diagnosis --> replay
    trial --> replay["Independent finer replay and recovery studies"]
    replay --> experiment["Identify the next measurement or design change"]
```

We first seek a feasible design, then minimize length while allowing the represented hull, rig, appendage, ballast, structure and energy variables to change together. Numerical brackets describe model coverage and search limits. A bound hit requires investigation before claiming a minimum size.

SysML owns the physical equations, named configurations, bounds, assumptions and acceptance criteria. Python evaluates geometric intersections and section properties, interpolates saved aerodynamic evidence and drives SciPy. Compiled array interfaces are confined to the runtime boundary. Reusable libraries have no dependency on Blue Dog requirements; application analyses connect them to the mission.

The model combines provisional attached-flow wing forces and moments, underwater appendage forces, hull resistance, static buoyancy, material accounting, laminate screens and actuator energy. Both tacks contribute to progress with weights that cancel crosswind drift. Current changes sign between the legs; an easterly makes the upstream leg windward.

The [aerodynamic policy](../models/analyses/aerodynamic-policy.sysml) makes the former adverse aerodynamic assumptions the primary sizing case. It limits nominal incidence and heel, reduces lift credit, increases drag, and assigns an independent pitching-moment allowance. These are engineering assumptions, not measured uncertainty bounds. All 29 geometry, structure and energy variables remain free; the restricted controls prevent the search from relying as heavily on high incidence and large heel.

VSPAERO supplies finite-wing trends within the archived grid. We retain the provisional upright-polar cosine projection in the force balance; the separate heel study demonstrates why this is a limitation. Published crescent-wing results do not match this CAD section closely enough to supply measured coefficients. Representative mesh/wake checks assess numerical sensitivity, while physical section polars, stall and moment measurements remain open evidence needs.

Feasibility restoration precedes the local size search. Derivatives respect interpolation-grid breakpoints. Small mesh reserves protect against numerical drift; they are separate from physical uncertainty. A continuation can start from the best point without changing requirements or bounds; the record retains its exact normalized seed and checkpoint hash. Refined replay re-solves operating states with energy constraints, then reports any energy-unconstrained diagnostic explicitly. A failed local solve is not proof of physical impossibility.

<details>
<summary>Reproduce the search and refresh aerodynamic evidence</summary>

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

Preparation exports model inputs and compiles native calculations. Solving writes a candidate; replay and recovery are separate assessments. Outputs go to ignored `build/analysis`, not to authored documentation. Accepted records are archived without overwriting earlier runs and projected into named model instances for publication. The current run is identified on the [results page](results.md).

Replay holds the selected geometry fixed and re-solves controls for six hypotheses: the conservative primary case (stored as `nominal`), construction, additional aerodynamic degradation, hydrodynamic degradation, energy degradation, and their combination. These scenarios test sensitivity; they are neither probabilities nor demonstrated worst cases. An operating failure or pitch-unstable recovery sample remains visible even if the coarse sizing screen passed.

OpenVSP uses the separate package-free environment under `tools/boat_analysis/aerodynamics/vsp` because the pinned binary has its own Python ABI. Run its modules from the repository root with that uv project. The saved grid permits routine analysis without rerunning VSPAERO. Mesh convergence and a direct candidate comparison test numerical consistency; viscous drag, stall, broadside flow, thickness effects and dynamic sailing still need evidence.

The current search and one continuation stopped just outside the coarse feasibility tolerance; no minimum-length result was established. We retain the selected trial for refined replay rather than relabel its near-pass as success. The reusable geometry checks include analytic section properties, displaced-volume oracles, mass moments, force and torque invariance, and native/interpreted parity. Qualification remains broader than those software checks.

[Recorded outcomes](results.md) · [Sail concepts](sail-trade.md) · [Structures and recovery](structures-and-recovery.md)

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


</details>

**Next:** [Compare the sail concepts](sail-trade.md).
