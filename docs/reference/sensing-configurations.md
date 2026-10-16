# Physical sensing configurations to measure

**Supplier review: 16 October 2026.** I need a physical installation to test against IC-01’s sensing assumptions. These three configurations name cameras, processing, interfaces and mounting concepts. They are bench candidates, not selected equipment or evidence that the boat meets the class-specific observation allocations. No sensing simulation has been changed for this comparison.

The [model record](../../models/configurations/sensing-equipment.sysml) separates supplier specifications from project allowances and leaves installed-budget, detection, latency and independent-recovery acceptance false. The [source register](../../evidence/sensing/2026-10-16/sources.json) records URLs, retrieval date, source scope and available response hashes.

The [acoustic alternatives](acoustic-sensing.md) add a synchronized hydrophone
array, a narrow-beam forward sonar and a multibeam imaging sonar to the trade.
They address different observations and have their own installation limits;
none is credited as a complete replacement for traffic awareness.

## Three optical primary installations

All three use on-camera RVC2 inference, a **Raspberry Pi 4 Model B** for track association, AIS fusion, logging and guidance messages, an externally powered USB 3 hub, and a **Quark QK-A026 AIS/GPS receiver** connected by USB. The cameras use their factory fixed-focus lenses. AIS supplies cooperative reports; it cannot cover non-transmitting craft or define a tow’s full boundary. VHF/GPS antennas, lengths of coax and the final powered-hub SKU remain procurement items within the support allowance.

| Configuration | Specific camera and mounting | Why investigate it | Principal limitation |
| --- | --- | --- | --- |
| **SC-01: fixed high-resolution ring** | Four OAK-1 W IMX378 cameras at 90° azimuth intervals; 4056 × 3040 pixels and 95° horizontal field per camera | Simultaneous observation with more angular samples for small distant targets | Only 5° nominal overlap; four camera loads already exceed the 8 W increment before host and installation losses |
| **SC-02: fixed global-shutter ring** | Three OAK-1 W OV9782 cameras at 120° intervals; 1280 × 800 pixels and 127° horizontal field per camera | One fewer camera and global-shutter images during motion | 7° nominal overlap, much less angular detail; workload and complete installation still need a new budget |
| **SC-03: scanning high-resolution head** | One SC-01 camera on a Hitec HS-785HB azimuth winch, commanded by a Pololu Micro Maestro 6; bounded sweep followed by a cable-safe return | Lower camera count and a direct measurement of the power-versus-revisit trade | Does not observe all bearings simultaneously; sweep, return, settling and inference add blind intervals |

The field and sensor variants come from [Luxonis’ current hardware documentation](https://docs.luxonis.com/hardware/products/OAK-1%20W.md). The simple overlap calculation assumes unobstructed, horizontal optical axes. It is not a coverage guarantee when the boat heels or the rig masks a sector. I would mount the fixed cameras around a common mast bracket with clear windows, then map the actual masked bearings through rig travel and heel. The choice must work with any of the three open rig concepts.

A rough angular-sampling check uses the historical 750 m comparison distance to explain why resolution matters; it is not a current universal requirement. A one-metre-wide target at 750 m spans about 0.076°. Dividing that angle by the full horizontal field gives about **3.3 average image pixels for SC-01** and **0.77 for SC-02** at full sensor width. These are analyst calculations using average angular sampling, not lens-calibrated image projections or detection predictions. Lens distortion, target contrast, blur, crop and neural-network input downsampling can make the useful observation much worse. Neither catalogue provides a demonstrated Blue Dog detection range or end-to-end response time.

**The non-AIS ranging architecture is still unresolved.** Each installation is monocular: seeing a target and estimating its bearing does not supply metric range or closing speed. The fixed rings' small adjacent overlaps do not establish stereo coverage around the boat, and scanning alone does not establish range. Any image-based range method would need identified geometric assumptions, camera calibration, boat attitude and uncertainty bounds; estimating motion over time also needs observable target tracks and known own-boat motion. Those capabilities must be demonstrated or supplied by complementary equipment before this becomes a complete avoidance pipeline.

For the scanner, Hitec lists 3.5 turns of travel, 110 g mass and a nominal 1.38 s/60° speed at 6 V. On that stated speed basis, one 360° sweep alone takes **8.28 seconds**, before dwell, settling or return. I would verify the angle/speed convention and loaded motion on the bench; even the ideal value is incompatible with treating this as a fresh all-bearing observation every second. The servo is splash-proof, not qualified for immersion. Its 6 V no-load current is 250 mA and its stall current 1.8 A, so moving and jammed states require separate supply checks. [Hitec specifications](https://hitecrcd.com/hs-785hb-karbonite-3-5-turn-winch-servo/). The [Maestro controller](https://www.pololu.com/product/1350/specs) adds 4.8 g; its quoted controller current excludes servo demand.

## Power: component subtotals are not installed consumption

Luxonis gives **2.5–3 W for streaming**, up to **1 W for AI**, and up to **0.5 W for encoding** per camera. For this monocular installation I do not add its generic stereo-processing allowance. The resulting camera-only planning cases are:

| Configuration | Streaming subtotal | Streaming high + AI + encoding allowances |
| --- | --- | --- |
| SC-01, four cameras | 10–12 W | 18 W |
| SC-02, three cameras | 7.5–9 W | 13.5 W |
| SC-03, one camera | 2.5–3 W | 4.5 W, plus scanner/controller |

These workload cases are not measured minimum/maximum installed powers. Simultaneously achieving useful frame rate, inference and latency must be demonstrated. Reducing frame rate changes the observation problem as well as the budget. [Camera power basis](https://docs.luxonis.com/hardware/products/OAK-1%20W.md).

The QK-A026’s legacy manufacturer manual specifies less than 120 mA at 5 V, giving a **0.6 W component ceiling** for the stated unit. The reviewed manual is dated 2016; the delivered hardware/firmware revision must be checked. [QK-A026 manual](https://quark-elec.com/doc/QK-A026_application_note.pdf).

I reserve the following **unmeasured project planning allowances**, not supplier promises:

| Support item | Planning treatment |
| --- | --- |
| Pi 4B host under the actual pipeline | 3–6 W exploratory load cases; benchmark and replace |
| Powered USB hub | 0.3–1 W exploratory electronics loss, excluding power delivered to cameras |
| DC conversion to regulated rails | 90% efficiency placeholder; test across load and battery voltage |
| Storage, fusing, harness and connectors | Included in common support mass; electrical losses and leakage need measurement |
| Optical windows, mounts, condensation control, cleaning/heating | Mass allowance below; cleaning/heating demand unresolved, not zero |
| Recovery-side observation and processing | Separate unresolved installation, not hidden in the primary subtotal |

The Pi’s recommended supply rating is not its operating consumption. Its USB ports also cannot simply power the ring: the published Pi 4 total peripheral limit is 1.2 A, below the four cameras’ streaming demand at 5 V. The powered hub needs an adequate rail, no unintended backfeed and a measured combined bandwidth/latency budget. [Raspberry Pi hardware documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).

IC-01 allocates **8 W additional sensing/compute plus a 4.5 W base electronics lump**. SC-01’s cameras alone exceed the increment; SC-02 has almost none left even in its lowest streaming case. With the provisional 3 W host and 0.3 W hub cases and the AIS ceiling, SC-02 totals 11.4 W at component rails, or about 12.67 W at 90% conversion, before other mission electronics. That is an illustrative planning case, not a lower bound or measured demand. It shows why claiming the whole 12.5 W as freely available would be misleading. The base also carries functions that a new host may not replace. I must identify those replacements explicitly and resize the boat if the reconciled installation exceeds its budget. SC-03 might reduce average demand, but its blind intervals prevent crediting the existing timing envelope.

## Mass and packaging

Luxonis lists **53.1 g** for OAK-1 W; the procurement check must confirm the chosen variant and included hardware. This excludes the boat’s protective windows, mounting and wiring. [Product specification](https://shop.luxonis.com/products/oak-1-w).

For a first packaging target I allow **450 g common primary support**, including Pi, hub, receiver/antennas, storage, power distribution, common case and wiring; **80 g per fixed-camera housing/mount**; or **150 g for the scanner’s sealed bearing/mount**, plus its 110 g servo and 4.8 g controller. These are deliberately visible project allocations, not a completed bill of materials.

| Configuration | Quoted camera/mechanism mass | Primary subtotal with those planning allowances | Remainder against IC-01’s 1.2 kg added-equipment allocation |
| --- | --- | --- | --- |
| SC-01 | 212.4 g cameras | 982.4 g | 217.6 g |
| SC-02 | 159.3 g cameras | 849.3 g | 350.7 g |
| SC-03 | 167.9 g camera, servo and controller | 767.9 g | 432.1 g |

**The remainder is not free payload.** The 1.2 kg allocation also has to accommodate the intended additional recovery equipment; its battery mass is handled separately in IC-01. Independent recovery sensing, any remaining recovery hardware, structural reinforcement and cleaning equipment are not closed by these primary subtotals. These tables identify packaging experiments, not a passing installed-mass claim.

## The independent recovery blocker

None of these primary installations realizes IC-01’s independently observed upright/inverted recovery assumption. A shared Pi, hub, regulator or mast failure can remove every primary camera at once. Inversion can immerse or obscure the optical windows and antennas; sealing alone does not restore an above-water view.

A physical recovery concept needs its own processor, navigation and observation inputs, isolated power/data boundaries and useful fields of view in each admitted attitude. One approach worth packaging is separate upright- and inverted-facing observation heads, each located to remain above the relevant waterline, with an independent controller in a sealed compartment. The inverted waterline and rig geometry must establish whether those locations exist. Duplicating two cameras does not automatically provide all-bearing coverage, independent navigation or enough recovery-bank endurance. I leave the components, mass and power of that subsystem unresolved rather than assume a cheap backup detector.

Before claiming qualification-preserving capsize recovery, the boat must also retain its required safety functions while inverted and restore upright control unassisted. These candidate installations provide no such evidence. Powered recovery remains a separate disqualified path.

## Underwater option and a radar rejection

**Ping360 is an optional underwater experiment, not the third primary traffic solution.** Its manufacturer specifies 510 g with cable and 5 W maximum, and a full scan at its 50 m range setting takes 33 seconds. A restricted forward sector can trade coverage for revisit time. Catalogue range does not establish thin-weed detection, and underwater returns do not cover above-water hazards. Its 0–30°C temperature range, mount, drag, snagging and whether it remains submerged after inversion all matter. Adding it to SC-02’s provisional primary mass already exceeds 1.2 kg before a sonar mount or independent backup. The page was out of stock at review, so availability is another explicit dependency. [Blue Robotics specifications](https://bluerobotics.com/store/sonars/imaging-sonars/ping360-sonar-r1-rp/).

**Garmin GMR Fantom 18x is ruled out as an IC-01 drop-in.** The radome alone weighs 6.35 kg; published maximum electrical demand is 33 W transmitting normally or 24 W in power-save mode, with 4 W standby. It exceeds the current mass and power allowances before installation and interface hardware. Its advertised 50 W is RF output, not battery consumption. I retain it as a scale comparison rather than pretend that “radar-assisted” names an affordable allocation on this boat. [Garmin installation manual](https://static.garmin.com/pumac/GMR_Fantom_Domes_18x_24x_Install_EN-US.pdf).

## What I would measure first

I would begin with one camera of each fixed-ring variant on the same target scenes, recording original images, delivered tracks, latency and power against independently measured target range and motion. I would test whether a proposed ranging method can distinguish relevant distances and closing motion, retain its uncertainty and identify cases where range is unobservable. Detecting a few target pixels is not enough. This tests both the angular-resolution trade and the unresolved ranging architecture before buying a complete ring. Next I would build the chosen ring with the actual host, hub, windows and power rails and measure simultaneous performance, heating, coverage through heel and rig movement, and fault behavior. The scanner is a timing-limited comparison, not the preferred way to satisfy the present response requirement.

No candidate is selected, and none receives an invented day/night range. The immediate decisions are whether either fixed layout can produce useful tracks within a revised load budget, and whether a physically independent recovery observation installation fits the boat at all. The [synchronized measurement procedure](sensing-measurements.md) records those results before any later sensing simulation uses them.
