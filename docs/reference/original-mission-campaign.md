# Original conceptual-vessel mission campaign

This archived 12 October 2026 experiment uses a conceptual vessel and a 65.786 km course revision. It is separate from IC-01 and later course/configuration records.

## Original conceptual-vessel course experiment

The [recorded Bingen–Stevenson campaign](../../evidence/runs/2026-10-12-bingen-mission/mission-campaign.json) preserves the model inputs, source hashes, seeds and voyage histories. The chart-clear reference circuit is **65.786 km**, including the port rounding of buoy 16. The outbound reference path is 32.648 km; the return path and rounding make the two halves slightly different. Sailing tracks include additional tacks and avoidance.

Of 32 seeded voyages, **28 completed**, **three reached the 240-hour numerical horizon**, and **one stopped when the controller could not find a safe maneuver**. Completed voyages took **10.45–30.19 hours**. The horizon is an analysis setting, not a challenge deadline. All three censored cases passed the north and west checkpoints at buoy 16 but did not cross the south checkpoint: the rounding exposes a local guidance limitation worth investigating.

The controller considered **41 potentially conflicting traffic encounters** across the ensemble. Commercial appearances are restricted to charted recommended-track fragments inside the active route's bounding area; archived chart coverage beyond the course does not dilute those arrivals. These are synthetic scenarios, not AIS replay or proof of Navigation Rules compliance. Stored energy stayed above the conceptual boat's allocated reserve; that does not establish endurance for the optimized candidate.

![Thirty-two synthetic Bingen–Stevenson voyage tracks, completion times and battery histories. Red crosses mark unfinished runs; the longest realization is orange.](../figures/mission-campaign.svg)

A numerical check separates the integration step from how often the controller changes commands. The deterministic test checks that refinement of time integration does not shorten maneuver delays. The rounding test separately requires the north, west and south checkpoints in order while excluding the buoy's clearance disk.

This campaign motivated better local tack planning around the rounding mark, paired replays of the same seeds and comparison against fuller polars and measured electrical loads. These counts describe the controller and declared assumptions, not the real boat's mission-success probability.

