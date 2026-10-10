# Sail architecture trade study

Preliminary qualitative development selection. All physical requirement gates remain unknown. No numeric reliability rates or arbitrary weighted scores are assigned. Neither rigid concept is mission-qualified; the soft sail is deprioritized, not proven noncompliant. Sources and decision rationale: sail-trade.md.

## Native analysis conclusion

| Candidate | Development decision | Requirement verdict |
| --- | --- | --- |
| Tail-controlled rigid wing | Co-leading development candidate | Inconclusive: evidence missing |
| Fixed-camber rotating-mast wing | Co-leading development candidate | Inconclusive: evidence missing |
| Triangular soft sail | Deprioritize for long unattended service; retain prototype benchmark | Inconclusive: evidence missing |

## Candidate definitions

| Candidate | Definition |
| --- | --- |
| Tail-controlled rigid wing | Freely rotating main wing, provisionally symmetric, with a tail and actuated elevator-like trim tab. Tail/wing aerodynamic moments set incidence; no assumption of a powered whole-wing bearing. |
| Fixed-camber rotating-mast wing | Owner-defined fixed-camber CrescentWing with whole-mast rotation for trim. Square-sail/downwind mode and reaching mode; no camber reversal, flap or tail mechanism is assumed. Evaluate a non-backdrivable gearbox for unpowered position holding as an actuator option, not a selected component. |
| Triangular soft sail | Triangular woven-polyester sail on mast and boom with sheet control. Reefing/furling is a design option requiring explicit mechanism, mass and fault analysis; battens and reinforcement are not excluded. |

## Durability and energy

| Candidate | Durability and reliability | Energy |
| --- | --- | --- |
| Tail-controlled rigid wing | Avoids sailcloth flogging and sheets; retains bearing, tab linkage, tail-boom, skin/joint and wave-impact failure modes. Rigid wings are not automatically storm-proof. | Low trim-energy potential from aerodynamic balance; measure bearing friction, tab hinge moment and failure-state power. No transfer of full-size Saildrone wattage to Blue Dog. |
| Fixed-camber rotating-mast wing | Avoids cloth flogging and camber-changing joints; retains skin, seam, mast-bearing and trim-drive fatigue and wave-impact loads. Verify holding torque and wear under shock, vibration, lubrication and temperature variation; do not assume every worm gearbox self-locks. | Non-backdrivable gearing may eliminate motor holding current, but not controller standby power or trim energy. Compare measured daily move, hold and idle energy against tail control; include starting friction, gearbox efficiency, trim frequency and gust response. A balanced pivot can reduce drive torque. |
| Triangular soft sail | Flogging, flutter, chafe, UV/stitching degradation and sheet wear create unattended-maintenance concerns. Durable cloth, battens and anti-chafe design can mitigate them; no lifetime failure is established. | Sheet/winch energy and holding strategy must be measured; self-locking or balanced arrangements may have low static draw. Do not assume a continuously powered servo. |

## Performance and capsize

| Candidate | Sailing performance | Recovery geometry |
| --- | --- | --- |
| Tail-controlled rigid wing | Test both tacks and low-Reynolds-number main-wing/tail interaction. Tail authority, stall, gust response and faulted-tab loads remain open. | Include main wing, tail, boom, tab, actuator and any counterweight as separate mass/volume bodies. Check free, jammed and failed trim states plus sealed, flooded and draining states. |
| Fixed-camber rotating-mast wing | Measure full-angle lift, drag and moment on both tacks, including drag-dominated square/downwind and lift-dominated reaching modes and transitions. Do not inherit symmetric linear-wing polars. Inspect edge geometry before assuming leading/trailing-edge interchange. | Use actual crescent/swept geometry, dry and retained-water CG, sealed volume, trim angle and failed-drive position. A self-locking drive retains the last trim angle on power loss and cannot passively feather without a release mechanism. Assess locked-angle storm/capsize states and any clutch or emergency depower strategy. Manufacturing CAD is not qualified challenge-vessel geometry. |
| Triangular soft sail | Both-tack sailing is conventional in principle; actual reefed and unreefed low-Re polars are needed. Useful benchmark for mass and performance. | Lower membrane mass and negligible sealed cloth volume can help, but model mast/boom buoyancy, immersion drag, trapped water and sheet snagging separately. |

## Manufacturing and evidence

| Candidate | Construction | Next evidence |
| --- | --- | --- |
| Tail-controlled rigid wing | Compatible in principle with printed ribs and glass skins; extra bearings, waterproof actuation, alignment and tail clearance need design. | Low-speed trim bench; unpowered and jammed-tab gust tests; wet-cycle endurance; actual rig mass/CG and compartment geometry. |
| Fixed-camber rotating-mast wing | Closest to existing CAD and useful for coupons/prototypes. Fixed section and rotating mast avoid tail/tab/boom parts; bearing, drive and waterproofing details remain to be designed. | Inspect CAD section and stations; measure both-mode, both-tack polars, trim moments and drive energy, including depower and jam states; compare against MaxiMOOP and Oshen PC13 directly driven wingsail precedent. Bench-test motor-off holding, wet-cycle wear, daily energy and failed-power depower/recovery; include gearbox mass and CG. |
| Triangular soft sail | Simple sailmaking and repair, low rig-mass potential; requires sailcloth and rigging rather than printing every component. Hull FDM/glass requirement does not prohibit a soft sail. | Unattended flogging/chafe/UV exposure and sheet fault tests over declared mission hours; autonomous depower and recovery demonstration. |

## Requirement and architecture links

| Analysis element | Requirement / architecture |
| --- | --- |
| TradeAssessment | wetMechanicalIntegrity |
| TradeAssessment | gorgeSurvivalWind |
| TradeAssessment | oceanSurvivalWaves |
| TradeAssessment | sustainedEnergyFeasibility |
| TradeAssessment | legProgress |
| TradeAssessment | selfRighting |
| TradeAssessment | capsizeControlRecovery |
| TradeAssessment | liftMass |
| TradeAssessment | missionSuccessProbability |
| TradeAssessment | reliabilityEvidence |
| Candidate | HullAndRig |
| TradeAssessment | sailJam |
| RigBody | selfRighting |
