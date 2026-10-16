# From virtual evidence to water trials

**OOSEM:** Verification, validation and learning · [Maturity assessment](development-plan.md)

This is the integration and validation part of the [development plan](development-plan.md#physical-validation). Its inputs are the selected configuration, model-linked verification cases and explicit prediction limits. It informs whether a bounded physical test is ready, what its results establish, and which model assumptions must change. These are planned activities; the challenge vessel has not completed physical qualification.

## Start with measurements that change a decision

Before building the challenge vessel, I want experiments that separate plausible concepts. Construction coupons inform structural mass and joint assumptions. Wing and actuator measurements inform force and energy predictions. Flotation and capsize experiments inform whether recovery remains possible after an upset. The [structure and recovery methods](structures-and-recovery.md), [sail trade](sail-trade.md) and [energy study](energy.md) describe those questions.

Each experiment needs a declared configuration, predicted result, measurement uncertainty and a decision it will inform. A useful experiment can disprove a prediction. Passing a numerical check is not physical validation.

## Exercise decisions before physical integration

The [executable mission logic](mission-simulation.md#executable-supervisory-logic) is exercised with observation outages, interventions and casualty events. The regression cases check sailing inhibition and restoration, a persistent abort latch, and alert queuing without a monitoring link. An isolated change to the modeled event policy changes the simulated response, checking that the logical model actually governs the behavior.

The next evidence is timed sensor and controller replay: feed recorded observations and faults into the decision loop, compare the resulting commands with the modeled intent, then measure the boat’s response. Preserve observation uncertainty and actuator delay when carrying those results into the [mission development spirals](simulation-spirals.md). Passing a supervisory test does not demonstrate detection range, maneuver authority or physical recovery.

## Measure sensing and shared compute as an installation

The [measurement importer](../tools/boat_analysis/mission/measurements.py) accepts synchronized records for one identified sensor/compute stack. Measure the complete declared load at the regulated bus, including acquisition, processing and thermal behavior. State the hardware, pipeline revision, instruments, clock basis, operating conditions, operator and measurement date. Keep raw records and their hashes. No installed measurement is currently available; synthetic regression inputs are labeled `synthetic-test` and cannot qualify hardware.

Use a power CSV with `seconds,voltage_v,current_a` and an observation CSV with `frame_seconds,decision_seconds,target_present,detected`. Each observation row represents an independently confirmed target-present trial; retain misses with `detected=0` and an empty decision time. Use separate cohorts for target class, range, bearing, lighting and obscuration, and retain independent truth alongside the cohort. These minimum files do not characterize false positives, localization error or an operating envelope by themselves.

The metadata JSON requires `installationId`, `pipelineRevision`, `conditions`, `clockBasis`, `instrument`, `operator`, `measuredOn`, `measurementBoundary` (`regulated-bus`) and `evidenceType` (`measured` or `synthetic-test`). To remove a shared baseline load, specify `replacedBaseElectronicsW` and `replacementScope`, identifying exactly which functions the measured stack replaces. The deduction cannot exceed the existing base electronics allocation. Do not deduct a component merely because it uses the same processor.

Run `python -m tools.boat_analysis.mission.measurements --power power.csv --observations observations.csv --metadata metadata.json --output installation.json`. The output records time-integrated mean load, observed peak, maximum sample gap, delivered-frame latency, miss fraction, source hashes and native energy screening. Missed frames remain in the denominator; latency statistics describe delivered detections only. Choose instrument sampling fast enough to characterize relevant transients; an observed peak is not a guaranteed maximum. The fixed-passage capacity lower bound omits feedback from added mass and passage time, so follow it with coupled sizing, packaging, thermal and peak-power checks and chronological replay.

The continuation regression suite checks command timing, maneuver persistence, energy exhaustion and physical consequences at finer integration steps. The archived paired experiment exposes completed courses, contacts and unresolved horizons separately. Neither software checks nor a synthetic log substitutes for installed measurements.

## Integrate in bounded steps

First establish individual sensors, actuators and electrical behavior on the bench. Then exercise integrated state transitions and faults, including unavailable communications, loss of safety capability and the transition from a qualifying attempt to recovery. Follow with controlled flotation and recovery trials, then short local-water missions before extending the operating envelope.

The existing manufacturing and wing testbed can support focused experiments. It is not automatically representative of the eventual challenge vessel; any transfer of evidence must identify what geometry, hardware and operating conditions remain applicable.

## Update maturity from each experiment

Before each water trial, connect the objective to its verification case, identify the actual test article and instrumentation, and check conditions, boundaries, shore retrieval and emergency response. Choose a bounded scope that can answer the question with the available equipment and recovery arrangements.

Afterward, compare measurements with predictions, retain failures and censored observations, and update the model's validity limits. Update the affected OOSEM layers with what the evidence supports, what failed or remains uncertain, and whether the next useful step is repetition, redesign or a wider trial. A successful simulated voyage alone does not establish readiness for the physical challenge.

See the [running maturity assessment](development-plan.md#how-the-assessment-stays-current) for the update method and the [modeling method](methods/modeling.md) for the evidence links.
