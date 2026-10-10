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

## Implementation and evidence boundary

The historical two-metre study remains a reproducible comparison. The coupled workflow uses separate models so its CAD-derived wing, mass, hydrostatics and drive calculations cannot be mistaken for those historical results.

| Responsibility | Implementation |
|---|---|
| Geometry | Parameterized hull, CAD-midsection wing, elliptic appendages and a volume-normalized ballast bulb; common geometry supplies mass, stiffness and buoyancy inputs. |
| Aerodynamics | OpenVSP/VSPAERO aspect/camber/incidence grids for both chord orientations; bounded interpolation with independent profile drag, lift caps and discrepancy factors. |
| Physics | Native SysML mass/CG, force and moment balance, gearbox/motor energy, structural screens, tack weighting and route arithmetic. |
| Numerical search | SciPy operating-state and shared-design solves. Feasibility precedes length minimization; 28 vessel variables remain free within declared brackets. |
| Recovery | Native immersed-volume calculations; coarse fixed-pitch search screens followed by finer free-pitch curves. Static screening does not verify dynamic releases. |

The wing's aerodynamic moment contributes to both yaw balance and actuator torque. Its physical rotation also moves its mass and displaced volume. Opposite-tack performance uses the reversed-chord grid with the corresponding camber/sign transformation. The coordinate mapping follows [OpenVSP's body/wind-axis definitions](https://groups.google.com/g/openvsp/c/4HD1bI3jCYo/m/8vUXYf_HEQAJ).

| Requirement family | Executable screening | Evidence still required |
|---|---|---|
| Q-101/102/103 cruise | Both-tack force balance, lateral-drift-cancelling tack weights, signed current and round-trip duration | Accepted polar and environmental profile, fouling and weather holds; the synthetic route is not a mission qualification |
| E-200 sustained energy | Drive losses, controller/holding loads, day/night balance, reserve and peak supply | Measured duty, selected hardware, seasonal harvesting and calm/survival loads |
| P-102 handling | Mass of separate body, wing, battery and keel assemblies | Detailed attachments and physical handling demonstration |
| T-101–105 structure | Skin bending, deflection and hull-panel pressure screens | Wet/jointed properties, buckling, fatigue, impact, ribs and joints; full environmental load cases |
| N-051/052 recovery | Geometry-based static restoring curves across mast positions | Dynamic releases, retained water, damage, control restoration and rig integrity |

Numerical convergence, physical-model adequacy and mission verification are distinct verdicts. The VLM model does not establish viscous drag, stall, broadside behavior or aerodynamic thickness sensitivity. The geometry family and unqualified material/actuator scalings remain explicit assumptions.

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

## Coupled execution

[Coupled inputs](coupled-inputs.md) records the geometry/mass replay and VSPAERO grid. The [operation model](../models/coupled-operation.sysml) connects these to force balance, drive energy, structural margins and route assessment. [Sensitivity inputs](../models/coupled-uncertainty.sysml) distinguish nominal assumptions from adverse material, aerodynamic and energy cases; these are engineering brackets, not measured probability distributions.

After generating the VSPAERO grid, export the native kernels with the main uv environment on Windows:

```powershell
uv run --project analysis/wing python analysis/wing/polar_grid.py
uv run python -m scripts.native_hydrostatics
uv run python -m scripts.native_coupled
uv run python -m scripts.native_coupled_operation
uv run python -m scripts.prepare_coupled_uncertainty
```

Run `scripts.study_coupled`, `scripts.optimize_coupled` and `scripts.verify_coupled` as Python modules in the Linux SciPy/GCC environment. The first establishes both-tack reference operating states, the second runs shared-design feasibility and length search, and the third performs finer operating/recovery replay and sensitivity cases. Kernel preparation checks the generated C output representation; pytest checks native/interpreted parity, geometry, reference-moment invariance, gearbox accounting and tack weighting.

The [earlier recovery diagnostic](hydrostatics.md) remains a sensitivity comparison using the old design's mass. It must not be substituted for the new geometry-consistent replay.
