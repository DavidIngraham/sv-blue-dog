# Choosing the sail architecture

The [native trade-study analysis](sail-trade-results.md) keeps three candidates: a freely rotating rigid wing with an elevator-like tail trim tab, the original cambered wing concept, and a triangular soft sail. The development conclusion is **tail-controlled and fixed-camber rotating-mast wings as co-leading development candidates; soft sail deprioritized for long unattended service**. This is a qualitative engineering downselect, not a measured reliability ranking or a completed requirement verification.

Tail control and camber are separate design choices: a cambered wing could also use a tail actuator. The tail-controlled configuration provisionally uses a symmetric main section. The original concept has fixed camber and trims by rotating the whole mast, with square-sail/downwind and reaching modes. The trade does not rule out combining the two ideas.

## What distinguishes the rigid candidates?

Its distinguishing feature is aerodynamic control of the main wing's incidence. The actuator moves a small tail control surface rather than directly driving the entire loaded wing. Saildrone describes that wing/tail/tab arrangement in its [design history](https://www.saildrone.com/eu-en/news/how-saildrone-wing-was-born). That supports investigating low trim energy; it does not supply a Blue Dog actuator power value or prove that a jammed actuator will feather safely.

The [Silva et al. wingsail design paper](https://recipp.ipp.pt/bitstream/10400.22/15346/1/CAPL_LSA_MBM_2019.pdf) describes the corresponding moment balance and highlights the tail/counterweight trade: balancing a free wing can add elevated mass and increase its swept envelope. This motivates retaining the tail-controlled candidate, while bearing friction, tail authority, tab faults, submerged loads and counterweight mass must remain explicit design problems.

The original CrescentWing uses **fixed camber and whole-mast rotation**, not a camber-reversal mechanism. It is intended to operate broadside in square-sail/downwind mode and at lift-producing incidence in reaching mode. This removes the previously assumed uncertainty about camber actuation; mast-drive torque, energy and fault behavior still need measurement.

The closest primary precedent found is Miller, Judge, Sewell and Williamson's [*An Alternative Wing Sail Concept for Small Autonomous Sailing Craft*](https://www.researchgate.net/publication/323361410_An_Alternative_Wing_Sail_Concept_for_Small_Autonomous_Sailing_Craft), published in *Robotic Sailing 2017* (2018), DOI 10.1007/978-3-319-72739-4_1. Its abstract reports wind-tunnel and on-water evaluation of a square-sail-derived wing on the 1.2 m MaxiMOOP, with condition-dependent performance and practical advantages over its soft-sail comparator. The [MaxiMOOP platform page](https://www.sailbot.org/maximoop/) associates the asymmetric-wing test platform with the U.S. Naval Academy. This is the closest match located, not a confirmed NPS-authored paper. The accessible abstract supports concept precedent; the full numerical results have not been inspected or imported.

[Crescent-wing research at Chalmers](https://research.chalmers.se/publication/543872/file/543872_Fulltext.pdf) explains how suitable sections exchange leading and trailing edges between tacks. Fixed camber therefore does not inherently require a reversal mechanism. Whether our CAD has the necessary edge geometry remains a geometry check, not an assumed property.

The fixed wing offers fewer tail/control components and relevant small-vessel precedent; the tail-controlled wing offers passive trim-energy potential. Neither advantage establishes an overall winner. Compare full-angle lift, drag and pitching moment versus trim and Reynolds number, on both tacks, including broadside separated flow, mode transitions and depower. The existing symmetric linear-lift sizing model cannot represent the fixed wing's square mode or supply candidate-specific performance evidence.

## Does the soft sail fail the requirements?

Not on the evidence available. A triangular soft sail is attractive for low rig mass, little enclosed membrane volume, familiar construction and inexpensive prototypes. A durable, reinforced and appropriately battened sail is a fair comparator; a fragile racing laminate would bias the trade.

The concern is maintenance-free exposure. North Sails identifies [flogging, flutter and flex fatigue](https://www.northsails.com/en-us/blogs/north-sails-blog/four-fs-sail-fatigue-flex-fiber-compression-flogging-flutter), and recommends [chafe protection, UV protection and inspection](https://www.northsails.com/en-uk/blogs/north-sails-blog/sail-care-maintenance-tips-diy). For Blue Dog, our engineering judgment is that fabric/line wear and autonomous sail handling create an unattractive development burden for persistent service. This does **not** prove a soft sail cannot complete a days-long Gorge passage. A furling or self-locking winch may address some risks, but introduces its own mechanisms and failure cases.

Rigid construction also has real durability limits. Saildrone reports that tall wings were damaged during Southern Ocean attempts; its lower-aspect replacement improved survival while sacrificing upwind capability. That is directly relevant to a mission requiring upstream windward progress. See [Saildrone's account of the Antarctic circumnavigation](https://www.saildrone.com/eu-en/news/unmanned-vehicle-completes-antarctica-circumnavigation). Avoiding sailcloth does not establish wave-impact survival.

## What the executable trade does

Seven evidence gates cover wet/survival durability, energy, sailing progress, capsize/control recovery, manufacturing, lifting and voyage reliability. Every candidate currently has unknown gates. Unknown is not encoded as failed; an observed failed gate is distinct from a development preference. If a candidate passes its declared gates, the assessment marks it eligible for comparison using validated margins, including the soft sail.

The development policy retains both rigid concepts at equal development priority while evidence is incomplete; aerodynamic trim alone does not earn a higher rank. That policy is visible in the SysML analysis; it is not disguised as an optimized score. The study does not fabricate failure rates or convert DFMEA concerns into reliability probabilities. Existing Q-series voyage reliability and N-series capsize criteria remain authoritative. The generated report links the analysis to those requirements and the existing sail-jam DFMEA entry.

No candidate is finally selected, and no sizing results have been relabeled as results for these three rigs. The [two-metre baseline](mission-sizing.md) remains a preliminary generic-wing study until candidate-specific aerodynamic, actuation and mass models replace its assumptions.

## Inputs for the self-righting model

Carry both rigid concepts into actual geometry rather than treating sail area as buoyant volume. `RigBody` in [sail-trade.sysml](../models/sail-trade.sysml) defines the input contract: dry mass and CG, closed volume and its centroid, floodable volume, retained-water mass/CG, fill/drain times, geometry reference and evidence status. Use one body per main wing, tail, boom, tab, actuator, counterweight and mast as appropriate. For the soft sail, include membrane immersion drag, retained water and line snagging; do not assign a fictitious sealed airfoil volume.

Next, intersect the positioned geometry with the water surface over heel, pitch and trim states, solve vessel displacement and calculate total weight/buoyancy moments. Include minimum/maximum load, intact and credible flooded states, free/jammed rig angles and both sides of the existing 90/180-degree release matrix. Check inverted equilibria and dynamic control recovery separately from static righting moment. A stable inverted equilibrium cannot be dismissed because a small-angle GM or below-bottom CG screen passed.

The native sensitivity example gives about **98 N m** for 10 litres of displaced freshwater at a 1 m horizontal lever; changing the lever sign reverses the moment. This is not a candidate volume estimate. Wing buoyancy can help resist inversion in one configuration and impede recovery in another; its effect must come from the actual immersed geometry.

Before freezing geometry, measure a trim prototype's friction, power, failure response, mass and CG; obtain both-tack aerodynamic data; then compare full-angle righting curves. That evidence will determine the downselect between the rigid concepts and can reopen the soft-sail option.
