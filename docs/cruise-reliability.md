# Cruise speed, exposure and reliability

A slower boat must keep working longer. Current, tacking, weeds and time waiting for usable wind can matter more than a favorable straight-line speed. This analysis connects the [cruise requirements](figures/requirements-q-001.md) to [mission reliability](figures/requirements-l-001.md) and the [architecture DFMEA](dfmea.md).

The proposed targets are **0.5 m/s minimum along-route progress during planned sailing legs**, and a **90% lower reliability bound at 95% confidence** for each declared voyage. These are engineering starting points, not approved challenge rules or measured capabilities. Qualification conditions and unresolved decisions remain in the [context report](requirements-context.md).

## Native analysis

[cruise-reliability.sysml](../models/cruise-reliability.sysml) defines `CruiseReliability`, with typed distances, speeds and durations. It executes these relationships:

- Ground velocity made good = water-relative VMG × retained-performance factor + signed along-route current.
- Elapsed exposure = sum of leg distance / ground VMG + weather holds and maneuvering time.
- Constant-hazard reliability = exp(−combined critical failure rate × exposure).
- Allowed critical failure rate = −ln(0.90) / exposure hours.
- Required zero-failure test exposure = −ln(0.05) / allowed failure rate.

Water VMG must already account for heading and tacking. A polar solver is not implemented. The retained-performance factor represents a declared degradation allowance, such as fouling; it must not double-count losses already in measured VMG. Nonpositive ground progress is infeasible, not a zero-duration passage. Waiting belongs in exposure even while propulsion demand is low.

These constant-hazard and zero-failure relationships follow the [NIST exponential reliability model](https://itl.nist.gov/div898/handbook/apr/section1/apr161.htm) and [one-sided zero-failure confidence bound](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm). `exp` and `ln` use the bundled non-normative `OpenSysMLMathFunctions` library; the model and constraints remain SysML.

## Illustrative result

The [generated results](cruise-reliability-results.md) and [native analysis JSON](analysis/cruise-reliability.json) use two **synthetic 100 km legs**, 2.5 m/s water VMG, 80% retained performance, ±1.5 m/s current and six hours of holds. These distances are not surveyed challenge gates; 2.5 m/s is an assumed input, not a prediction for this hull or sail.

The result is about **69.5 hours** elapsed exposure. The proposed target permits about **0.00152 critical failures/hour**. A zero-critical-failure demonstration requires about **1,976 representative test hours**. The illustrative 2,000-hour input is not actual test evidence. All evidence acceptance flags are false, and the native verification verdict is inconclusive.

Lower VMG or longer holds tightens the failure-rate budget. The same model accepts a separate Hawaii profile once route, environment and operating assumptions are defined. A Gorge profile cannot stand in for that voyage. Indefinite operation cannot be demonstrated by a finite constant-hazard calculation: with positive critical hazard, survival probability falls as exposure grows.

## Evidence and boundaries

The model distinguishes a numerical estimate from a confidence-qualified claim. Both the rate-budget check and zero-failure demonstration must pass, using accepted profile, rate and constant-hazard evidence. Observing a critical failure invalidates the zero-failure method; another statistical method is then needed. Missing rates are errors, not zeros. Individual component confidence bounds need a joint-confidence argument before combination.

The failure-rate sum assumes independent, non-overlapping random critical modes, plus an explicit common-cause term. It does not establish wear-out life, systematic software reliability, weather availability, repairability or hazard acceptability. The initial DFMEA deliberately assigns no probabilities or RPNs. Passing a reliability budget does not disposition a safety-critical mode.

Qualified autonomous duration is an evidence input. A dependency links this analysis to `BlueDogEnergy::SustainedOperation`, but no energy campaign is automatically stretched to match the voyage. Run an energy campaign covering the full cruise-derived exposure, with a matching configuration, weather/hold profile and recovery reserve, before accepting that duration. Longer waits may improve harvest while still increasing failure exposure.

## Architecture DFMEA

[dfmea.sysml](../models/dfmea.sysml) defines the reusable `FailureMode`, `Review` and `DesignFailureReview` elements. Twelve starter modes reference actual architecture parts, with native dependencies to affected requirements. Each records function, cause, local and mission effects, proposed detection, action, owner role and evidence state. `RiskMetadata::Risk` is present without invented probability scores.

The native review currently reports **12 open actions and 10 unresolved safety-critical modes**. Those criticality classifications are initial engineering judgments. Scope review is also false. Its inventory objective only checks that rows exist; `reviewReady` is a separate result and remains false. Completing this starter table cannot prove exhaustive hazard coverage.

Next steps are to freeze a candidate sailing profile, measure a loaded-vessel polar and weed degradation, review the DFMEA against interfaces and mission phases, and turn prioritized actions into fault-injection/qualification evidence.

## Run and inspect

```sh
uv run python scripts/render_requirements.py
uv run pytest tests/test_reliability.py -v
uv run python scripts/render_requirements.py --check
```

Publishing uses native OpenSysML document queries for the result and DFMEA tables. Pytest exercises the native analysis, including adverse currents, holds, common-cause rates, invalid inputs and evidence gates; it does not implement a second reliability calculator.
