# From virtual evidence to water trials

**OOSEM:** Verification, validation and learning · [Maturity assessment](development-plan.md)

This is the integration and validation part of the [development plan](development-plan.md#physical-validation). Its inputs are the selected configuration, model-linked verification cases and explicit prediction limits. It informs whether a bounded physical test is ready, what its results establish, and which model assumptions must change. These are planned activities; the challenge vessel has not completed physical qualification.

## Start with measurements that change a decision

Before building the challenge vessel, I want experiments that separate plausible concepts. Construction coupons inform structural mass and joint assumptions. Wing and actuator measurements inform force and energy predictions. Flotation and capsize experiments inform whether recovery remains possible after an upset. The [structure and recovery methods](structures-and-recovery.md), [sail trade](sail-trade.md) and [energy study](energy.md) describe those questions.

Each experiment needs a declared configuration, predicted result, measurement uncertainty and a decision it will inform. A useful experiment can disprove a prediction. Passing a numerical check is not physical validation.

## Integrate in bounded steps

First establish individual sensors, actuators and electrical behavior on the bench. Then exercise integrated state transitions and faults, including unavailable communications, loss of safety capability and the transition from a qualifying attempt to recovery. Follow with controlled flotation and recovery trials, then short local-water missions before extending the operating envelope.

The existing manufacturing and wing testbed can support focused experiments. It is not automatically representative of the eventual challenge vessel; any transfer of evidence must identify what geometry, hardware and operating conditions remain applicable.

## Update maturity from each experiment

Before each water trial, connect the objective to its verification case, identify the actual test article and instrumentation, and check conditions, boundaries, shore retrieval and emergency response. Choose a bounded scope that can answer the question with the available equipment and recovery arrangements.

Afterward, compare measurements with predictions, retain failures and censored observations, and update the model's validity limits. Update the affected OOSEM layers with what the evidence supports, what failed or remains uncertain, and whether the next useful step is repetition, redesign or a wider trial. A successful simulated voyage alone does not establish readiness for the physical challenge.

See the [running maturity assessment](development-plan.md#how-the-assessment-stays-current) for the update method and the [modeling method](methods/modeling.md) for the evidence links.
