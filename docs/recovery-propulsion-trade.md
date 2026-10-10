# Recovery propulsion trade: water propeller versus air propeller

Decision status: open. Both concepts provide auxiliary propulsion for development and recovery only; neither may propel a qualifying challenge attempt. The existing `RecoveryPropulsion` architecture element remains medium-neutral. This is a preliminary engineering comparison, not a product selection or measured performance result.

## Mission and decision gates

R-001 currently proposes 0.5 m/s speed over ground against 1.5 m/s current for 30 minutes at maximum mission load in sheltered conditions. That implies approximately **2.0 m/s through-water speed** on the directly upstream leg. Hull resistance at that speed is unknown and could make this target impractical for a small displacement hull; measure it before sizing either motor. R-002 sizes reserve from measured electrical power, not nominal motor ratings.

Both candidates must pass N-056 powered passage through the milfoil-equivalent patch, N-051/N-052 capsize recovery, S-003 isolation and R-001 challenge inhibition. N-053/N-054 sailing weed tolerance still matters: an air propeller does not remove weeds from the keel or rudder. Printed mounts/guards must satisfy P-002's 250 × 250 × 250 mm job envelope; that does not limit the diameter of a purchased propeller or assembled guard to 250 mm.

## Comparison

The judgments below are engineering hypotheses to verify on the installed boat. No numerical score or weighting is assigned without measured performance and an agreed priority.

| Criterion / requirement | Submerged water propeller | Above-water air propeller | Evidence needed |
| --- | --- | --- | --- |
| Thrust versus energy, R-001/R-002 | Dense working fluid favors compact low-speed thrust; actual losses depend on diameter, pitch, immersion and installation | Lower density drives greater disk area or induced velocity for comparable static thrust; battery demand may dominate | Hull tow test, installed thrust/power curves and recovery run |
| Milfoil, N-053–N-056 | Blades, shaft and guard can wrap or collect stems; a duct/guard is not automatically weed-proof | Rotor avoids submerged stems while upright, but hull/keel/rudder can still anchor the boat in vegetation | Same patch and snag tests, including restart after blockage |
| Sailing drag and packaging | Submerged installation adds drag; folding/retracting concepts introduce moving parts and new failure modes | Adds windage, deck volume, possible sail interference and elevated mass | Coast/tow drag, wind-load and sail-clearance measurements |
| Capsize and waves, N-051/N-052 | Can ventilate or leave water while heeled; immersed motor/shaft sealing is central | Rotor can strike water, guard or rig during heel/capsize; restart while wet must be qualified | Heel clearances, disabled-rotor immersion, self-righting and post-capsize restart |
| Steering and reverse | Rudder-in-slipstream or steerable pod possible; reverse depends on selected propeller/drive | Air rudder, vectored thrust or differential thrust may be needed at low boat speed; ordinary air propellers are not assumed efficient in reverse | Low-speed turning, stopping and control-loss tests |
| Guarding and handling, S-003 | Contact hazard at launch/recovery; guards can collect weeds and add drag | Accessible high-speed rotor needs physical separation/guarding; larger guard increases windage and mass | Isolation timing, access assessment, guard deflection/clearance under loads |
| Corrosion and maintenance, N-042/P-003 | Continuous immersion, seals/bearings and dissimilar metals need attention | Less continuous immersion but still salt spray, condensation and capsize exposure | Exposure campaign and timed replacement |
| Wind sensitivity | Hull wind load still affects recovery; underwater inflow follows boat/current | Propeller inflow also changes directly with apparent wind and yaw | Installed testing across recovery wind headings |
| Cost and manufacturability | Waterproof drive hardware may add complexity; custom printed rotating blades are not assumed qualified | Hobby components may simplify prototyping, but marine protection and guards remain additional work | Actual BOM, mass, print jobs and supplier operating limits |

## First-order physics, not motor sizing

For an ideal stationary actuator disk, `P_induced = T^(3/2) / sqrt(2 rho A)`. This follows from momentum theory; it omits profile, swirl, motor/controller and installation losses. NASA's treatment explains the ideal disk model and its limitations. [NASA propeller thrust](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/propeller-thrust/)

Using illustrative densities of 1.225 kg/m³ air and 1000 kg/m³ freshwater, a 250 mm disk producing 5 N has ideal static induced powers of approximately **32.2 W in air versus 1.13 W in water**. The same-thrust/same-area ratio is approximately 28.6. This is a density/disk-loading illustration, **not a prediction that an installed air drive consumes 28.6 times a water drive's power**. Underway the advance speed relative to each medium differs, and hull/wind drag and real propeller curves govern. Neither 5 N nor this disk diameter is a selected design point.

Use manufacturer data for the actual propeller, intended fluid and RPM range. APC, for example, publishes different RPM limits for different air-propeller families; a generic motor power rating does not establish an acceptable propeller installation. [APC RPM limits](https://www.apcprop.com/technical-information/rpm-limits/)

## Down-select plan

1. Tow the maximum-load hull with representative appendages through 0.5–2.0 m/s; measure drag and identify whether R-001's upstream recovery target is feasible. Record a lower-current/cross-current recovery alternative if necessary, without silently changing R-001.
2. Bench each complete guarded drive for thrust, electrical power and thermal rise, then measure installed performance. Static thrust alone is insufficient.
3. Run identical N-056 weed-patch trials and locked-propulsor shutdown tests. Record speed retention, clearing success, energy and damage. Do not reward an air propeller for avoiding rotor fouling if keel/rudder fouling still prevents recovery.
4. Check capsize/righting, wet restart, rig clearance, manual isolation, handling mass and serviceability with each installation.
5. Reject candidates that fail the mission/safety gates. Among those passing, compare measured recovery watt-hours, clearing reliability, added sailing drag, mass and cost; update R-002 from measured electrical demand.

Provisional direction: retain a water propeller as the compact, energy-focused reference and an air propeller as the submerged-rotor-fouling alternative. Milfoil makes the air concept worth testing, but it is not enough to select it without hull-drag and installed-energy evidence. No architecture commitment is made by this study.
