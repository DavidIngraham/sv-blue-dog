# Requirements: mission to implementation

**OOSEM:** System requirements and scenarios · [Maturity assessment](development-plan.md)

Six topic pages connect the mission goals to testable requirements and design obligations. Each contains related breakdowns with their upstream context, generated from the authoritative SysML model. Start with the topic relevant to the design decision you are making.

## [Mission, course completion and endurance](requirements/requirements-mission.md)

One finite Gorge round trip is the current design mission. Hawaii and repeated operation retain separate future constraints.

## [Autonomous sailing, navigation and wind sensing](requirements/requirements-autonomy.md)

Autonomy turns the mission into onboard decisions. Navigation and wind observations supply the controller; recovery behavior keeps faults from silently becoming mission failures.

## [Energy and recovery propulsion](requirements/requirements-energy.md)

The energy budget must support sailing continuously and retain a deliberate recovery capability. These threads separate energy awareness, sustained balance and the motor rules for a qualifying attempt.

## [Environment, durability and casualty recovery](requirements/requirements-environment.md)

The Gorge and ocean environments set the loads and exposure conditions. The breakdown connects those environments to measurable limits, capsize recovery and weed tolerance.

## [Traffic safety, communications and monitoring](requirements/requirements-safety.md)

Other river users are part of the operating context. The vessel must remain observable, respect its operating boundary and distinguish monitoring from intervention that ends a qualifying attempt.

## [Manufacturing, handling and serviceability](requirements/requirements-practicality.md)

One-person handling and a 250 mm cubic printer are owner-imposed project constraints. They shape the build and maintenance approach alongside the mission goals.

[Mission and architecture](architecture.md) · [Development plan](development-plan.md) · [How we model requirements](methods/modeling.md)
