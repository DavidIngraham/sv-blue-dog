# What acoustic sensing could add

**Supplier review: 16 October 2026.** I would investigate acoustics as a complement to the [optical installations](sensing-configurations.md). A passive array could cue attention toward a noisy vessel. Active forward-looking sonar could measure distance to an underwater reflector without needing that object to make noise. Neither is an installed avoidance system, and neither removes the need to observe small surface craft.

The [source register](../../evidence/sensing/2026-10-16-acoustics/sources.json) distinguishes supplier evidence from installation assumptions. The [equipment model](../../models/configurations/acoustic-equipment.sysml) records those facts and calculates the provisional budgets. No sensing simulation or demonstrated detection distance has changed.

## Three concrete alternatives

| Candidate | Proposed hardware | Useful measurement | Principal limitation |
| --- | --- | --- | --- |
| Passive array | Four Aquarian H3dX hydrophones, one Zoom F6 recorder/interface, Raspberry Pi 4 Model B | Direction of an identifiable underwater sound | No guaranteed source sound or established range estimate |
| Narrow forward sonar | Cerulean Omniscan 450FS, 100 m depth-rated version, Ethernet to Pi 4B | Range to returns in a narrow forward beam | Wider images require motion |
| Multibeam forward sonar | Sonoptix ECHO, Ethernet to Pi 4B | Range and azimuth across a forward sector | Power, mass and unmeasured surface-target performance |

Each needs sealed dry electronics, regulated power, protected wiring, navigation/attitude input and software that turns measurements into tracks. These are research installations. They leave all three rig concepts open.

## Passive listening: direction first, range unresolved

I would start with a rigid **0.6 m fore-and-aft by 0.3 m port-to-starboard rectangle** of four hydrophones within IC-01's plan dimensions. This is a proposed aperture, not an approved mount. Depth below the waterline is unresolved: the heads must remain immersed through normal motion, avoid hull acoustic shadows and be isolated from actuator vibration. Flow shrouds, strain relief, drag and actual head positions need checking.

Each current **H3dX** head is 10 g excluding cable and XLR plug and draws a typical 1.2 mA under the manual's 48 V phantom-power conditions. It includes signal conditioning. Aquarian supports lower phantom voltages and describes flow-noise precautions. I would not substitute specifications from the older H3x. [H3dX manual](https://www.aquarianaudio.com/AqAudDocs/H3dX_manual.pdf).

One **Zoom F6** provides six microphone inputs, 24/48 V phantom supply and multichannel USB audio. Its manual lists 520 g and 1 W for the main unit alone; that is not a measured four-hydrophone load. [F6 manual](https://www.zoom.co.jp/sites/default/files/products/downloads/pdfs/E_F6.pdf).

Using one recorder gives a common multichannel acquisition path instead of four independently clocked USB microphones. I would record separate channels at 48 kHz, disable automatic mixing and added channel delays, and calibrate channel time and phase with a known source. Linux multichannel streaming to the Pi, driver support, dropped samples and end-to-end latency remain unverified. A recorder that saves useful files is not yet a live guidance input; storage activity is part of the workload to measure.

Arrival-time differences can support bearing estimation. This compact planar array does not automatically provide useful range or resolve elevation. Surface, bottom and hull reflections can produce misleading arrivals; unknown source loudness makes received volume a poor distance meter. Motion over time or another sensor might make range observable, but that estimator is unspecified. [NOAA explains the active/passive distinction](https://oceanservice.noaa.gov/facts/sonar.html); the suitability of this geometry is my engineering hypothesis.

A paddler or sailboat can make incidental sound without providing a continuous detectable signal. Even a powered vessel may be masked by flow noise. **No acoustic cue cannot mean no craft.** An underwater array also does not establish the ability to hear airborne navigation sound signals. I would measure misses and false bearings with the boat moving and actuators operating, rather than remove quiet craft from the observation problem.

## Active sonar: a narrow beam or a forward sector

The **Omniscan 450FS 100 m** designation is its depth rating. Supplier specifications list 440 g, 10 W maximum while pinging, 10-30 V supply and Ethernet. The nominal beam is **0.8 degrees wide by 50 degrees high**, with the narrow width specified beyond 5 m. Catalogue maximum range is 120 m and maximum ping rate 20 Hz; these are not one guaranteed operating point or a kayak detection distance. [Cerulean specifications](https://docs.ceruleansonar.com/c/omniscan-450/specifications).

It is a forward-looking sonar, but a fixed bow installation samples a narrow corridor. Motion assembles the wider picture; turning the boat to scan changes the trajectory being protected. A separate scanner would add mass, power and revisit delay. I would first test a fixed submerged bow mount with direct Ethernet to the Pi. The manufacturer's nominal 20-degree downward mounting guidance is a starting point for underwater imaging, not proof of surface-hazard coverage. [Mounting guidance](https://docs.ceruleansonar.com/c/omniscan-450/mechanical-mounting).

The **Sonoptix ECHO** provides 256 beams across 90 degrees horizontally at 400 kHz or 120 degrees at 700 kHz, with 20-degree vertical coverage in the current technical table. It lists 750 g, 9-28 V and 5-25 W; the 1.2 A active-ping example at 12 V is about 14.4 W. Catalogue maximum ranges are 200 m and 30 m respectively, with firmware conditions, and maximum update rate is 25 Hz. I do not combine those maxima into one operating point. Ethernet raw data requires suitable firmware. [Current ECHO specifications](https://bluerobotics.com/store/sonars/imaging-sonars/sonoptix-echo/).

I would mount ECHO forward below the waterline with a clear sector and direct Ethernet to the Pi. An echo supplies range to a reflector; deciding whether it belongs to a hull, paddle, vegetation or bottom still needs processing and trials. Neither sonar sees an above-water sail or establishes a whole tow boundary. Near-surface bubbles, waves, heel and shallow draft make this different from operating a submerged remotely operated vehicle. ECHO is the stronger broad-sector comparison, but neither sonar is an easy addition within the current allocation.

## Component specifications versus installed budgets

IC-01 allocates **8 W incremental sensing/compute**, alongside **4.5 W base electronics**, and **1.2 kg added equipment**. The base load already performs other functions. Additional recovery equipment also needs space within the mass allowance.

| Candidate | Supplier component subtotal | Unmeasured project support allowance | Provisional primary subtotal |
| --- | --- | --- | --- |
| Four H3dX + F6 | 40 + 520 = 560 g, excluding head cables/plugs | 450 g: Pi, cables/plugs, enclosure, regulator, storage, mounts/shrouds | 1,010 g |
| 450FS | 440 g | 300 g: Pi, wiring, regulator, enclosure, bow bracket | 740 g |
| ECHO | 750 g | Same 300 g planning allowance | 1,050 g |

These are proposed standalone acoustic packages, excluding optics and independent recovery. The allowances are not weighed assemblies. Procurement drawings and weighed parts must replace them; remaining protective hardware may increase them.

For passive listening I would explore **1.5-3 W for recorder plus powered heads**, **3-6 W for the Pi**, and 90% conversion efficiency: approximately **5-10 W at the battery**. This is an exploratory project scenario, not a supplier range or measured bound. Phantom power is included once in recorder load. At their stated maximums, either active sonar alone exceeds 8 W before host demand: that matters to electrical sizing, but does not establish the duty-averaged mission load. ECHO's 5-25 W range does not identify the selected operating mode. Reducing ping duty changes observation gaps as well as power; average demand remains unmeasured.

Adding the bare 450FS or ECHO to SC-02's provisional 849.3 g optical package gives **1,289.3 g or 1,599.3 g** before sonar mounting or recovery. Those addition cases already exceed 1.2 kg. Sharing the Pi may avoid a second host, but does not remove cables, mounts, regulators or the whole optical support allowance. Any combined installation needs an itemized reconciliation of shared parts and workloads.

## Inversion and the first useful experiment

A waterproof acoustic head is not independent recovery sensing. A bottom-mounted head may emerge when inverted, and a bow beam may point into an unsuitable sector. Sharing the main Pi, USB interface, regulator or navigation inputs preserves common failure paths. Recovery needs functioning observation, processing and power with verified immersion and coverage in both attitudes. None of these proposals supplies that chain. Passive sound alone cannot establish that a recovery path is clear.

I would start with synchronized shore and moving-boat recordings from the four-head array, known target positions, and both noisy and quiet craft. A borrowed forward sonar could test whether shallow surface targets return usable echoes at the required bearings. Useful results would include misses, false alarms, bearing/range error, time to a usable track, power and masked sectors. Until then, I would retain optical observation and the unresolved range/closing-speed problem in [encounter feasibility](../encounter-feasibility.md).
