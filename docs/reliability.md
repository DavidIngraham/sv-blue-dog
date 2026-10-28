# Passage time, reliability and failure analysis

**OOSEM:** Trades, optimization and analysis · [Current assessment](current-assessment.md)

A slower voyage demands more hours of successful unattended operation. I use passage estimates and the architecture to ask what can fail during that exposure, and how the boat should respond. This connects [preliminary design](current-assessment.md#virtual-design) to the fault and endurance tests needed for [physical verification](current-assessment.md#physical-validation).

The [candidate passage estimates](results.md) give me exposure times to investigate. I still need evidence about the failures that can occur during those hours.

## Can a faster boat be more likely to finish?

A slow boat has to keep everything working for longer. Under a constant critical-failure rate, survival is `exp(−failure rate × exposure time)`. Halving the passage time permits twice the hourly rate at the same survival probability. The [NIST exponential reliability model](https://itl.nist.gov/div898/handbook/apr/section1/apr161.htm) gives a simple starting point for that trade.

![Equal-survival curves versus passage hours and hourly critical failure rate. A hypothetical 60-hour boat at 0.001 failures per hour has 94.2 percent survival; a 30-hour boat at 0.0015 per hour has 95.6 percent survival.](figures/passage-reliability.svg)

*Each curve connects equal survival probabilities. The faster example has a 50% higher hourly failure rate but lower total exposure. The two points illustrate the arithmetic; they are not estimates for the candidate hulls.*

The Gorge makes useful speed especially valuable. Against a 1 m/s current, increasing water-relative progress from 1.5 to 2 m/s doubles ground progress from 0.5 to 1 m/s. Those are illustrative values, but the relationship matters: a little extra drive near the current threshold can save a lot of time. A shorter passage may also fit more comfortably inside a favorable weather window.

In the representative westerly, the upstream leg is downwind. That gives me a reason to investigate a faster hull, potentially one that planes. It still has to make the windward outbound leg, carry its equipment and recover from a capsize. Peak speed alone will not answer the mission question.

I also need to distinguish speed from nimbleness. A faster boat can have more control authority in one condition and greater control demands in another. Planing is a hypothesis to evaluate, not evidence of either better maneuverability or worse reliability. [Experimental work on planing-hull slamming](https://www.sciencedirect.com/science/article/pii/S0141118719303906) illustrates why wave impacts and structural loading need their own analysis.

The failure mechanisms matter. Electronics faults may accumulate with running time. Weed encounters may depend more on the route traveled. Actuator wear depends on duty and load, while slamming and capsize risk depend on the conditions and how the boat is sailed. I cannot assign all of those a fixed hourly penalty and assume that speed pays for it.

The design comparison I want is therefore **probability of completing the round trip**, evaluated jointly over weather, current, holds, energy use and failures. Each candidate should have an operating policy: sail faster when conditions permit, reduce speed or hold when the accumulated risk would otherwise rise. Unsuccessful routes must remain in that comparison. Traffic safety and accepted critical-failure dispositions remain launch gates.

The native [passage-exposure analysis](../models/blue-dog.sysml) generates the curves and example points. It shares its constant-hazard calculation with the cruise reliability model. The current force-balance solver does not model dynamic planing or speed-dependent failure rates; the contour is a sensitivity study, not a planing-boat selection. A hull comparison with actual performance and loading evidence will deserve its own story.

## Finite endurance and future missions

The current mission has no completion deadline and retains protected recovery reserve. Its battery may finish below its starting charge if reserve and peak-power requirements remain satisfied throughout the voyage. Repeating the same energy cycle indefinitely is a separate future objective.

IC-01 has been exercised in local encounter and recovery simulations. Comparing its chance of completing the mission requires full-course histories with failures tied to the conditions, loads and operating time along each route.

Hawai‘i and repeated operation need separate endurance studies; the present comparison concerns one Gorge round trip.

```sysml-view Page_reliability_0::CruiseSemantics direction=BT
package Page_reliability_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view CruiseSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::cruisePerformance;
        expose BlueDog::Requirements::legProgress;
        expose BlueDog::Verification::Requirements::MissionPerformanceAssessmentVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about BlueDog::Requirements::cruisePerformance { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::legProgress { x = 360; y = 0; }
        metadata Layout about BlueDog::Verification::Requirements::MissionPerformanceAssessmentVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
}
```

```sysml-view Page_reliability_1::ReliabilitySemantics direction=BT
package Page_reliability_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view ReliabilitySemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::missionReliability;
        expose BlueDog::Requirements::missionSuccessProbability;
        expose BlueDog::Analyses::Reliability::VoyageReliabilityVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about BlueDog::Requirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::missionSuccessProbability { x = 360; y = 0; }
        metadata Layout about BlueDog::Analyses::Reliability::VoyageReliabilityVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
}
```

The L-101/L-102 reliability verdict assesses provisional study targets. Q-102 passage duration has a separate conditional verdict; Q-101/Q-103 performance records and L-103 reliability evidence have independent planned reviews. A failed study target does not reject a binding product requirement.

## Combine weather and failure exposure

The [weather-window study](operating-constraints.md#gorge-weather-and-launch-windows) explains how a favorable launch window can change during the passage. IC-01's nominal westerly result does not establish all-season capability.

Weather-route success and hardware survival are different quantities. A useful comparison must combine them over complete trajectories, including failed routes and holds. Applying a hazard rate only to the average successful passage would omit important risk. No weather probability has been accepted as an allocation of the mission reliability target.

The design failure mode and effects analysis (DFMEA) links functional failure modes to architecture responsibilities, requirements and needed evidence. Its concerns guide design and tests; they are not fabricated failure probabilities. Numerical rate-budget examples remain conditional on their assumptions and evidence disposition.

Weed contact is a concrete operating interaction. It affects both the sailing appendages and recovery propulsion, so loss of speed, steering and recovery capability are assessed separately.

```sysml-view Page_reliability_2::WeedSemantics direction=BT
package Page_reliability_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view WeedSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::submergedWeedPassage;
        expose BlueDog::Requirements::weedPassageSpeed;
        expose BlueDog::Requirements::weedPassageSteering;
        expose BlueDog::Architecture::missionContext::boat;
        expose BlueDog::Verification::Requirements::SubmergedWeedPassageVerification;
        metadata Layout about BlueDog::Requirements::submergedWeedPassage { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::weedPassageSpeed { x = 360; y = 0; }
        metadata Layout about BlueDog::Requirements::weedPassageSteering { x = 0; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 360; y = 200; }
        metadata Layout about BlueDog::Verification::Requirements::SubmergedWeedPassageVerification { x = 0; y = 400; }
    }
}
```

## How avoidance can fail

I review avoidance at three levels: the harmful encounter, the failed function,
and the physical concept that could cause that failure. The shared functional
review follows observation, classification, prediction, navigation duties,
command selection, achieved motion and recovery. The concept review then asks
what changes with fixed cameras, a scanning camera, acoustic sensing and each rig.
A scanner jam and a fixed-camera blind sector can both lead to missed detection,
but they need different diagnostics and design actions.

The model contains 17 functional avoidance rows and 15 concept rows, alongside
the 15 whole-boat starter rows. These are linked reviews, not 47 independent risks.
All actions remain open and none of the three reviews is ready for acceptance.
The concept rows identify candidate configurations, including alternatives; they
do not imply that all equipment is installed together.

### A fault tree for loss of safe separation capability

Read the following diagram upward. **OR** means any listed input is enough to
establish that branch's failure proposition. **AND** means every input must hold
within the same encounter response interval. These are qualitative Boolean gates,
not probability calculations or a model of event timing. A box marked **partial
view** has additional inputs or connections outside that diagram. Its gate
still uses the complete input list in the model.

The top event is an encounter for which neither the primary response nor the
fallback provides a supported, timely safe response. It is **loss of capability,
not a prediction that collision occurs**. A fallback counts as available only if
its observation, decisions, transition and achieved maneuver are adequate for
that encounter. An operating motor alone does not establish this.

```sysml-report BlueDogFailureViews::SystemTree
```

The shared power and compute failures each appear once and feed both response
branches. Multiple sensors on the same host or supply therefore do not establish
independent protection. The recovery branch also includes an unsafe transition,
inadequate recovery observation, no safe route and a response that arrives too
late. Those branches are listed in the functional review below. Another river
user avoiding Blue Dog is not credited as a safeguard.

### What sits inside the primary response

```sysml-report BlueDogFailureViews::PrimaryTree
```

The observation branch includes missing, late and false or swapped tracks.
Assessment includes wrong target status, predicted motion or navigation duty.
Command selection includes no feasible response and an unsafe courtesy change.
Execution includes steering or sail-control loss and a failure to notice that
actual motion differs from the plan. Shared power and compute causes are shown
in the preceding tree rather than repeated here.

<details>
<summary>Functional avoidance DFMEA: causes and actions still needed</summary>

```sysml-report BlueDogAvoidanceDocuments::functional
```

</details>

### What changes with the physical concept

For SC-03, one scanning camera, the observation branch has the following causes.
Each input means the fault or condition has already defeated the required
observation within the response interval; a harmless splash or brief delay does
not automatically assert a failure.

```sysml-report BlueDogFailureViews::ScannerTree
```

A fixed camera ring removes scanning motion but retains wet optics, shared-host
failures and coverage gaps caused by the rig and heel. Passive acoustics adds
quiet-target and ambiguous-bearing limitations; active sonar adds clutter,
shadowing and incomplete coverage of above-water riders, rigs and lines. Capsize
can disable an otherwise working installation by immersing an optical aperture
or lifting an acoustic head out of the water. Rig-specific jams affect the
maneuver available after a target is detected.

<details>
<summary>Concept-specific DFMEA: alternatives and proposed tests</summary>

```sysml-report BlueDogAvoidanceDocuments::concepts
```

</details>

The diagrams and tables use the same model events. Standard SysML cause-and-effect
connections carry the causal relationships. A reusable failure-analysis library
supplies the Boolean gates and review records, following the relevant concepts in
[OMG RAAML](https://www.omg.org/spec/RAAML/1.1), a standard for model-based risk
analysis. This is a qualitative SysML v2 subset, not the complete RAAML profile.
Gate symbols come from the modeled types, and each table selects the rows in its
review. Adding another review uses the same definitions and views. Gate calculations are executable and
checked with synthetic cases. The physical causal claims, diagnostic coverage,
common-cause boundaries and completeness remain unverified. No failure rates or
independence assumptions are assigned, and these trees do not yet inject faults
into the mission simulator.

My next comparison needs measured sailing and maneuvering performance, followed by failure evidence appropriate to each mechanism. The [DFMEA](../models/blue-dog.sysml) helps choose those tests; the [reliability analysis](../models/blue-dog.sysml) connects their results to passage exposure.


### Hazard controls and actual disposition

Six initial hazardous scenarios connect the whole-boat failure review to collision,
boundary loss, unintended thrust, flotation or retention loss, electrical or thermal
exposure, and human handling or retrieval. Each identifies modes, the IC-01 candidate,
an owner role, contributing mechanisms, proposed controls and verification plans.
They do not establish complete lifecycle coverage or assign a numerical risk rank.

```sysml-report BlueDogSafetyDocuments::HazardRegister
```

I need evidence that each control is implemented and effective before assessing
residual risk and recording its actual disposition. A role name or a checked flag
cannot substitute for the supporting record and acceptance authority. All six
hazard dispositions remain open, as do all thirteen critical whole-boat FMEA
rows. The fifteen whole-boat rows include capture/retrieval, command-context and
shared-sensing failures; they complement the functional and concept reviews.

```sysml-report BlueDogSafetyDocuments::DispositionRegister
```

This structure applies [MIL-STD-882E Change 1, sections 4.3 and Task 106](https://safety.army.mil/Portals/0/Documents/ON-DUTY/SYSTEMSAFETY/Standard/MIL-STD-882E-change-1.pdf)
and [NASA technical risk management](https://www.nasa.gov/reference/6-4-technical-risk-management/)
as engineering guidance. I have not adopted a DoD risk matrix or acceptance chain.
The unresolved work includes launch, storage, maintenance and disposal coverage,
control side effects, common causes and a project-specific risk assessment basis.

For the numerical reliability illustration, accepting a rate source and a constant
hazard assumption is insufficient. The critical-function partition, dependence
treatment and common-cause coverage must also be reviewed. The [NIST series and
competing-risk models](https://www.itl.nist.gov/div898/handbook/apr/section1/apr182.htm)
explain why component rates cannot simply be added without their applicability
conditions. The equations and provisional targets are unchanged; the new review
preconditions remain false. No physical reliability claim follows from a synthetic
passing example.

**Next:** [From virtual evidence to water trials](validation-plan.md) · [Series guide](index.md)
