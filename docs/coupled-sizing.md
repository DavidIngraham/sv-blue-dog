# Coupled sizing workflow

The sizing baseline is a fixed-camber rotating-mast wing with a non-backdrivable drive option. Tail control remains an alternative in the [sail trade](sail-trade.md). The objective is minimum practical waterline length after finding a feasible design, followed by mass/energy comparison at comparable lengths. This is preliminary engineering analysis, not vessel qualification.

## Model boundary and acceptance

| Element | Treatment in the coupled study |
|---|---|
| Mission | Gorge sail-only round trip; retain explicit route wind/current cases and progress/time constraints. Hawai‘i endurance and survival remain separately tracked objectives. |
| Manufacture | 250 mm cubic print-job envelope from the requirements model; include joints, supports and assembly provisions rather than limiting the overall boat to a print bed. |
| Handling | Existing 15 kg assembly allocation; separately account for hull/body, wing, battery and removable keel assemblies. |
| Design variables | Waterline, beam, freeboard, wing area/aspect/camber, mast position, keel and rudder geometry, ballast, battery, solar and actuator sizing. Construction recipes are discrete choices. |
| Search bounds | Numerical brackets are not requirements. Report and expand active artificial bounds; identify geometry/tool validity limits separately. |
| Aerodynamics | CAD-derived section and OpenVSP/VSPAERO for appropriate attached-flow conditions. Broadside separated flow requires a distinct evidence-supported model and uncertainty bounds. |
| Recovery | Geometry-based immersed volumes and full-angle righting curves at multiple trim/flooding states; dynamic recovery remains a separate verification obligation. |
| Uncertainty | Material properties, aerodynamic coefficients, current/wind exposure and actuator duty are evidence-bounded inputs, not freely optimized improvements. |

## Current implementation gaps

The historical two-metre study fixes waterline at 2 m, models a symmetric linear-lift wing, approximates structural sections and actuator scaling, and uses a below-hull CG allocation rather than a full-angle recovery model. Its results remain a reproducible historical comparison. The next workflow must not relabel them as fixed-camber/VSP results.

1. Extract sections, span stations, surface area and enclosed volume from `cad/SweptCrescentWing.STEP`, recording source hash and units. Distinguish manufactured material volume from displaced sealed volume.
2. Build a parameterized VSP representation and verify geometry against the CAD. Establish axis, incidence, force/moment reference and sail tack conventions before generating polars.
3. Verify aerodynamic runs with symmetry/sign checks and mesh refinement. Record solver version and settings. Bound viscous drag, stall and broadside loads independently; reject interpolation outside valid coverage.
4. Couple geometry to printed structure/glass mass, actuator loads/energy and immersed-body hydrostatics. Replace the CG proxy only after full-angle checks are working.
5. Validate a fixed design, then solve feasibility followed by length minimization under nominal and conservative assumptions. Re-evaluate rounded construction recipes and report active constraints.

Numerical convergence, physical-model adequacy and mission verification are distinct verdicts. A converged solution using unsupported aerodynamic coefficients must remain labeled exploratory.

## Tools

The main package-free uv environment retains OpenSysML and SciPy. `analysis/wing/pyproject.toml` provides a separate package-free Python 3.13 environment because the selected OpenVSP binary uses that Python ABI. OpenVSP binaries stay in ignored `.tools`; source geometry, scripts, dependency lock and compact authoritative results belong in the repository.

Reproduce the current geometry and reference-wing runs from the repository root:

```powershell
uv sync --project analysis/wing --managed-python
uv run --project analysis/wing python analysis/wing/install_vsp.py
uv run --project analysis/wing python analysis/wing/extract_sections.py
uv run --project analysis/wing python analysis/wing/reference_vsp.py --mesh 16
uv run --project analysis/wing python analysis/wing/reference_vsp.py --mesh 32
uv run --project analysis/wing python analysis/wing/reference_vsp.py --mesh 64
uv run python -m scripts.publish_wing_analysis
uv run python -m pytest tests/test_wing_analysis.py
```

The STEP contains a printed/ribbed 300 mm segment, not a complete boat wing. [Extracted sections](figures/wing-sections.png) retain missing outer-envelope samples as missing data. The reference VSP wing uses the complete midspan section in a rectangular planform; it does not claim to reproduce the swept prototype planform. Both ends of the section are rounded, so the wake-shedding assumption needs validation before these potential-flow results enter the optimizer.

[Generated wing-analysis results](wing-analysis-results.md) distinguish the geometry extraction, numerical mesh sensitivity and physical evidence gaps. The coupled optimization remains incomplete until the integration gates above are met.

## Current coupling progress

The [full-angle diagnostic](hydrostatics.md) now computes native SysML immersed volumes and gravity/buoyancy moments, with numerical heave and pitch equilibrium. It exposes a recovery sensitivity to wing buoyancy that the old CG screen misses. The next solve must use geometry-consistent mass and explicit flooded/retained-water cases; the diagnostic has not yet replaced the historical solver's stability constraints.

[wing-actuator.sysml](../models/wing-actuator.sysml) separates output-shaft torque, motor and gearbox efficiencies, moving duty, powered holding and controller consumption. Its accounting example verifies arithmetic only; it is not a selected actuator or a mission energy estimate. These functions still need to be connected to the candidate-specific aerodynamic moments in the coupled search.
