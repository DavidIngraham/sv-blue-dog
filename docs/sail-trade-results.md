# Sail architecture trade study

Preliminary qualitative development selection. All physical requirement gates remain unknown. No numeric reliability rates or arbitrary weighted scores are assigned. The lead concept is not mission-qualified; the soft sail is deprioritized, not proven noncompliant. Sources and decision rationale: sail-trade.md.

## Native analysis conclusion

| Candidate | Development decision | Requirement verdict |
| --- | --- | --- |
| Tail-controlled rigid wing | Lead development candidate | Inconclusive: evidence missing |
| Original cambered wing concept | Retain comparison candidate | Inconclusive: evidence missing |
| Triangular soft sail | Deprioritize for long unattended service; retain prototype benchmark | Inconclusive: evidence missing |

## Candidate definitions

| Candidate | Definition |
| --- | --- |
| Tail-controlled rigid wing | Freely rotating main wing, provisionally symmetric, with a tail and actuated elevator-like trim tab. Tail/wing aerodynamic moments set incidence; no assumption of a powered whole-wing bearing. |
| Original cambered wing concept | Original CrescentWing manufacturing concept retained. Camber reversal and the intended trim mechanism have not yet been established; a powered whole-wing trim is only the comparison assumption. |
| Triangular soft sail | Triangular woven-polyester sail on mast and boom with sheet control. Reefing/furling is a design option requiring explicit mechanism, mass and fault analysis; battens and reinforcement are not excluded. |

## Durability and energy

| Candidate | Durability and reliability | Energy |
| --- | --- | --- |
| Tail-controlled rigid wing | Avoids sailcloth flogging and sheets; retains bearing, tab linkage, tail-boom, skin/joint and wave-impact failure modes. Rigid wings are not automatically storm-proof. | Low trim-energy potential from aerodynamic balance; measure bearing friction, tab hinge moment and failure-state power. No transfer of full-size Saildrone wattage to Blue Dog. |
| Original cambered wing concept | Avoids cloth flogging but retains skin, seam, bearing and trim-drive fatigue; a camber-changing mechanism would add joints and failure modes. | Measure whole-wing moment, holding power and jam loads. A balanced pivot could reduce demand; no inherent high-power verdict is assumed. |
| Triangular soft sail | Flogging, flutter, chafe, UV/stitching degradation and sheet wear create unattended-maintenance concerns. Durable cloth, battens and anti-chafe design can mitigate them; no lifetime failure is established. | Sheet/winch energy and holding strategy must be measured; self-locking or balanced arrangements may have low static draw. Do not assume a continuously powered servo. |

## Performance and capsize

| Candidate | Sailing performance | Recovery geometry |
| --- | --- | --- |
| Tail-controlled rigid wing | Test both tacks and low-Reynolds-number main-wing/tail interaction. Tail authority, stall, gust response and faulted-tab loads remain open. | Include main wing, tail, boom, tab, actuator and any counterweight as separate mass/volume bodies. Check free, jammed and failed trim states plus sealed, flooded and draining states. |
| Original cambered wing concept | Measure positive and negative lift polars on both tacks. Fixed camber must not inherit the symmetric-wing model; reversal/flap geometry must be explicit if used. | Use actual crescent/swept geometry, dry and retained-water CG, sealed volume, trim angle and failed-drive position. Manufacturing CAD is not qualified challenge-vessel geometry. |
| Triangular soft sail | Both-tack sailing is conventional in principle; actual reefed and unreefed low-Re polars are needed. Useful benchmark for mass and performance. | Lower membrane mass and negligible sealed cloth volume can help, but model mast/boom buoyancy, immersion drag, trapped water and sheet snagging separately. |

## Manufacturing and evidence

| Candidate | Construction | Next evidence |
| --- | --- | --- |
| Tail-controlled rigid wing | Compatible in principle with printed ribs and glass skins; extra bearings, waterproof actuation, alignment and tail clearance need design. | Low-speed trim bench; unpowered and jammed-tab gust tests; wet-cycle endurance; actual rig mass/CG and compartment geometry. |
| Original cambered wing concept | Closest to the existing CAD and useful for coupons/prototypes. Benefits from fewer tail parts; exact actuator and reversal architecture remain unresolved. | Confirm intended camber/trim mechanism; inspect CAD section and stations; measure both-tack polars and drive power before quantitative comparison. |
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
