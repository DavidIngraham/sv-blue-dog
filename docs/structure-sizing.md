# Giving the structure a real mass budget

Removing the early dimension caps let the optimizer propose an extremely long keel and almost no freeboard. That was a useful sign that the physics needed more work. The current model treats the boat as a printed PETG structure with wet-layup glass/epoxy skins, and makes the structural and hydrostatic tradeoffs visible.

The [earlier stationary-screen results](open-sizing-results.md) and [native requirement definitions, focused derivation diagrams and design-basis table](structure-requirements.md) are generated from the model. Geometry remains free within expandable search brackets; structural limits are constraints with explicit design bases, not a return to arbitrary hull-length or sail-area caps.

## Manufacturing model

Hull mass includes printed walls, a two-direction rib grid, dry glass, retained mixed epoxy, seam reinforcement and a finishing allowance. Foil and wing mass include both skins, printed walls, infill volume and seam reinforcement. They use separate layup variables and separate component masses. No resin left in mixing cups or on tools is counted as vessel mass.

| Input | Current basis |
| --- | --- |
| PETG density | 1,270 kg/m³ from the [Prusament PETG datasheet](https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf). Its printed strength data are process-specific; they are not credited as primary bending strength here. |
| Cured epoxy density | 1,180 kg/m³ from [WEST SYSTEM 105/206](https://www.westsystem.com/app/uploads/2022/12/105-206-Epoxy-Resin.pdf). This is a density reference, not selection of a qualified resin/cure schedule, laminate strength or adhesion to PETG. |
| Glass and resin | Glass density 2,550 kg/m³ and retained mixed-resin/dry-glass mass ratio 1:1 are project assumptions. Manufacturer [hand-layup guidance](https://www.westsystem.com/product-categories/reinforcing-materials/) supports estimating by fabric weight, but actual resin retention and finishing must be weighed. |
| Print recipe | Initial 0.8 mm hull walls, 0.4 mm wing/foil walls, 8% foil infill and 10 mm hull ribs. These are selected process assumptions, not demonstrated printable or qualified scantlings. Rib pitch is optimized. |
| Glass layup | Hull, wing, keel and rudder dry-glass areal masses are optimized independently. Each is rounded upward to whole 200 g/m² plies, then geometry and trim are reoptimized for that recipe. This is not a globally optimal mixed-integer search. |
| Stiffness and strength | Effective wet/jointed laminate targets of 10 GPa and 50 MPa are proposed coupon requirements. They are assumptions in the current calculations, not measured properties or neat-resin datasheet values. |

The selected layup counts and resulting dimensions appear only in the generated results. Structural output units are kg for masses, kg/m² for areal mass, metres for lengths and deflections, MPa for stress, and dimensionless for ratios. The compact output table shows the first listed operating point; the saved record retains every point and its governing margins. The full material parameter set is in [structure.sysml](../models/structure.sysml), and the saved input contract records the exact values used in each run.

## What the structural screen checks

Glass skins carry bending in the model. The wing and appendages use finite-thickness opposed skins with their actual geometric separation; no stiffness is credited to PETG or to unmodeled carbon spars. A 12% foil thickness ratio is retained as an explicit shape assumption. Skin-fit constraints prevent the optimizer from putting more laminate inside a foil than its section can contain.

Hull bending uses a simply supported beam with twice the loaded weight distributed along the waterline. Wing loading includes both factored aerodynamic loading and transverse self-weight. Keel loading includes sailing force, a separate 100 N tip proof case and twice ballast weight transverse at the tip. The rudder includes sailing force and the tip proof case. The equations select the governing separate load case rather than adding mutually exclusive cases. Deflection is screened alongside stress.

Hull panels are screened as simply supported glass strips spanning the rib pitch under 10 kPa pressure. The printed ribs provide assumed support; their load transfer and the glass-to-print bond remain proof-test obligations. The model does not establish resistance to slamming, shell buckling, core crushing, creep, fatigue, full grounding impacts or delamination. These are remaining analyses, not outcomes inferred from positive beam margins.

Separate keel and rudder mass contributions now enter both handling and stability. Hull top, bottom and side-shell vertical mass moments are included. The righting calculation remains a small-angle surrogate; it is not a self-righting or damaged-stability demonstration.

## Practical requirements and traceability

The new requirements keep acceptance statements short and separate their conditions and rationale. Numerical allocations are marked open. Native derivation relationships connect structural acceptance criteria to the structural-integrity requirement; dependencies distinguish owner choices and engineering allocations from logical requirement derivation. Satisfaction links identify intended architecture responsibility and do not claim verification.

- **Freeboard:** at least 50 mm at the low deck edge under 20° heel in calm water. This does not promise a dry deck in Gorge waves.
- **Reserve buoyancy:** intact enclosed volume above the loaded waterline provides reserve displacement at least equal to loaded mass. Unsealed infill receives no buoyancy credit.
- **Launch clearance:** at least 0.30 m bottom clearance in 1.50 m water, a proposed site allocation supporting solo launch/retrieval. Actual launch-site depth must be established.
- **Printing:** structural tiles fit within 230 mm in each axis, reserving 20 mm for supports and clearance inside the owner's 250 mm cube. This estimates seam mass; it does not replace CAD and slicer envelope checks.
- **Handling:** the existing 15 kg limit per lifted assembly remains active. Setup time, total carried bulk and practical transport-module geometry still need demonstration.

These values are deliberately reviewable in the [requirement report](structure-requirements.md). They are not presented as regulatory or certified small-craft limits.

The current [two-metre route-sizing workflow](mission-sizing.md) supersedes the stationary optimizer as the design direction. It uses removable wing/battery assemblies, an explicit ribbed construction option and a mass-center screen. The earlier stationary study remains reproducible for comparison.

## Route progress versus environmental tolerance

A separate native assessment now evaluates a declared time-weighted route profile using signed currents. Negative progress intervals are retained in the mean; passage duration includes holds and an explicit hold-drift distance input. The demonstration profile uses synthetic time fractions for the solved wind/fouling states, with downstream current assisting one leg and opposing the return leg.

The sizing optimizer still runs the conservative stationary screens. The route assessment is a separate interpretation of Q-101 and Q-102, not a route optimizer or a validated launch window. Weather evidence and a safe hold strategy are required before its `missionSupported` result can be true. The [generated route result](open-sizing-results.md#declared-route-profile) is calculated from the same vessel and native sailing states.

## Evidence to collect next

Manufacture representative wall/rib panels, foil sections and reinforced tile joints. Weigh them after cure to check the mass model, then measure wet flexural stiffness, strength and bond performance using the declared production process. Those results should replace the proposed material allowables before we select a vessel design. Structural coupon success would still leave hull resistance, wing polars, large-angle stability and route evidence to establish.
