# Mission, context and architecture

**Object-Oriented Systems Engineering Method (OOSEM):** Mission and context · Logical architecture · [Current assessment](current-assessment.md)

What does this little boat actually have to do? I start with one finite, independent Gorge challenge, then work through the people, environment and equipment it will interact with. Those responsibilities give me a basis for comparing designs before selecting equipment.

![Map of the Gorge challenge corridor along the Columbia River, from Bingen to buoy 16 near Stevenson and back.](figures/gorge-course-map.svg)

*Bingen → Stevenson → Bingen. Water extent and course references: NOAA electronic navigational charts.*

### Start, finish and turnaround in shore context

The scored course starts and finishes at the proposed gate south of **Buoy 39 near Bingen**. Launch and retrieval at Bingen Point lie outside the scored circuit. The reference paths retain their geographic coordinates; solid orange and dashed cyan strokes distinguish coincident legs without moving either track away from the river.

![Satellite and aerial view of Bingen's start/finish gate, Buoy 39 and both river shores.](figures/course-bingen-satellite.svg)

The western end is a **port rounding of Buoy 16 near Stevenson**, passing the north, west and south checkpoints in order before returning upstream. It is a turnaround, not a separate finish or a shore landing.

![Satellite and aerial view of Buoy 16 near Stevenson, the port-rounding checkpoints and surrounding shoreline.](figures/course-stevenson-satellite.svg)

Imagery: [Esri World Imagery](https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer), with provider credits on each image. These close-ups show shore context; mosaic acquisition dates vary and the imagery is not a current navigation chart. The model's gate offsets remain proposed and require field confirmation. The images show reference paths, not a simulated voyage or an approved launch/recovery approach.

The return leg has to make progress over the ground, not just through the water. The representative westerly puts that return downwind against the current, while the outbound leg is windward with it. Easterlies reverse those roles. I will choose a favorable weather window for the challenge and use a separate seasonal profile for winter testing; the [weather analysis](operating-constraints.md#gorge-weather-and-launch-windows) explains the distinction. The challenge is sail-only and unassisted; I want live observation without making a shore connection necessary for control. Year-round operation and Hawai‘i have separate future requirements. For this boat, I want to explore how speed and shorter exposure affect the [chance of completing the round trip](reliability.md#can-a-faster-boat-be-more-likely-to-finish).

![Vessel concept with wing, hull, rudder, keel, ballast, solar collection and electronics.](figures/boat-concept.svg)

The hull and rig turn wind into motion; the rudder steers; onboard sensing and control choose where to go. Batteries supply those functions and a separate recovery system. I use the model to assign each responsibility before selecting hardware.

In [IC-01](../models/blue-dog.sysml), the main sensing and control system sails the mission. A separately powered recovery system must observe hazards, navigate and propel the boat after a primary failure, including while inverted. The practical question is whether those backup functions can survive the fault that disabled sailing. Shared water damage could still defeat both systems; isolation needs testing.

The [integration study](validation-plan.md#exercise-decisions-before-physical-integration) checks those responsibilities together using one boat's mass, sailing performance and energy budget. The [named IC-01 configuration](../models/blue-dog.sysml) owns its complete design and integration assumptions. The next step is to turn the allocated capabilities into compatible hardware and test their interfaces.

## Logical responsibilities and the candidate boat

Navigation estimates position and attitude; wind estimation supplies the sailing condition; traffic observation and collision assessment identify conflicts. Guidance chooses a sailing command. Mission supervision decides whether that command may be used, whether a gate crossing can count, and whether an abort has ended the attempt. Energy management supplies the reserve assessment. Recovery management plans and commands shore recovery; recovery actuation executes permitted propulsion commands. Recording and communications preserve and expose those decisions.

These are responsibilities, independent of processor or software boundaries. The [logical architecture](../models/blue-dog.sysml) connects them with typed observations, permissions, commands and records. A navigation estimate includes validity and time; a safety observation explicitly confirms which required capabilities remain available.

```sysml-view Page_architecture_logical::responsibilities direction=TB
package Page_architecture_logical {
    private import StandardViewDefinitions::*;
    view responsibilities : InterconnectionView {
        expose BlueDog::Architecture::Logical::LogicalVessel;
    }
}
```

The candidate physical assembly allocates those responsibilities to a primary sailing path and a recovery path with its own battery, navigation, observation, controller and propulsor. Wired wind sensing is a provisional equipment choice. The assembly identifies power and data interfaces; connectors, bus timing, equipment ratings and common-cause isolation remain open engineering questions. Recording and telemetry power assignment needs to be reconciled with both energy budgets.

The context description, logical responsibilities and candidate assembly answer different questions. The context's `Boat` groups responsibilities and places the vessel among external actors. The logical model defines their exchanges. IC-01 proposes equipment to implement them. [Named correspondences](../models/blue-dog.sysml) explain how these descriptions connect, including the portion assigned to each element and the candidate configuration it concerns.

A responsibility can need several implementation contributions. Navigation needs an estimate source and controller-side validation. Recording needs storage and controller-side scheduling. Recovery needs route assessment, commands and a propulsor, supported by its power and sensing interfaces. Assigning several responsibilities to one controller also creates internal interactions whose software timing and fault behavior I still need to establish.

<details>
<summary>Logical responsibilities and their IC-01 contributions</summary>

The table follows the model's allocation links. Each named allocation records its scope in the [correspondence model](../models/blue-dog.sysml). Primary and recovery identify implementation paths; shared equipment still needs a supply and fault-survival decision. These links describe the candidate, not accepted equipment or a demonstrated software deployment.

```sysml-report BlueDogArchitectureDocuments::ResponsibilityRegister
```

</details>

<details>
<summary>How logical exchanges reach candidate interfaces</summary>

Each logical transfer maps to one or more candidate transfers or to an internal interaction within a controller. One navigation transfer can serve several logical consumers. Internal mappings identify work the controller implementation must perform; they do not establish an implemented software call, scheduling guarantee or accepted latency.

```sysml-report BlueDogArchitectureDocuments::ExchangeRegister
```

The payload definitions preserve quantities, observation timestamps and validity where those features are defined. Installed encoding, freshness limits, arbitration and fault handling still need interface decisions and tests. Navigation signaling has a context responsibility and requirements, but its detailed logical interface and IC-01 equipment allocation remain open. The optional observation payload and future harvesting need separate configuration decisions.

</details>

```sysml-view Page_architecture_physical::candidate direction=TB
package Page_architecture_physical {
    private import StandardViewDefinitions::*;
    view candidate : InterconnectionView {
        expose BlueDog::Architecture::Physical::IC01Candidate;
    }
}
```

IC-01 is a working integration candidate, not a qualified assembly or a universally selected design. Its wing geometry supports the current sizing calculations; soft sail, tail-controlled rigid wing and directly rotated fixed-camber wing retain equal development standing. Owner decisions such as the finite mission, one-person handling and print volume govern the concept. Proposed equipment and interface assignments remain choices to test.

## What counts as an attempt

The boat must complete the scored circuit under sail, unattached and without outside assistance. Safe waiting is allowed. Refuge, grounding, anchoring, intervention or recovery propulsion ends qualification; a later attempt starts again at the departure gate. A component failure does not by itself end the attempt if a demonstrated backup preserves the required function.

I monitor position, mode and health from shore. The boat makes its own navigation and weather decisions. It may poll weather services autonomously; manual data pushes are intervention. Communications loss alone does not end a safe attempt, and critical alerts can wait in a queue while autonomous decisions continue.

I also want to build and handle the boat myself. Printed parts must fit a 250 × 250 × 250 mm build volume, while joined assemblies can be larger. Removable components and simple handling aids must make transport, launch and retrieval practical for one person. These owner constraints sit alongside the mission obligations in the [requirements](requirements.md).

The context view places the boat among the people and conditions it must respond to.

```sysml-view Page_architecture_0::context direction=TB
package Page_architecture_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view context : OOSEM::SystemContextView {
        expose BlueDog::Architecture::MissionContext;
    }
}
```

## From use cases to allocated behavior

I use OOSEM to work from what the mission needs to what each part of the boat must do. The scenarios below describe interactions that the boat must support. OpenSysML renders these views from the shared model.

The [mission supervisor](mission-simulation.md#executable-supervisory-logic) implements part of these scenarios: it responds to events, permits or inhibits sailing, and keeps an abort in effect for the rest of the attempt. Sensor processing, steering decisions and physical actuation need their own implementations and tests.

### Normal sailing

Each sailing cycle starts with a wind estimate carrying its value, timestamp and validity. Guidance receives navigation and supervisor permission as well as wind, then chooses a command. Actuation receives the permission explicitly and must check that both command and permission remain applicable. If wind observations disappear, the supervisor inhibits sailing; when they return, sailing can resume unless the attempt has already been aborted.

```sysml-view Page_architecture_normal::scenario direction=LR
package Page_architecture_normal {
    private import OOSEM::*;
    view scenario : LogicalScenarioView {
        expose BlueDog::Method::Scenarios::NormalSailing;
    }
}
```

### Traffic encounter

Observe, assess, maneuver and reassess. The Automatic Identification System (AIS) broadcasts information from equipped vessels, but Blue Dog must also detect traffic that does not transmit. In the simulator, a predicted conflict triggers traffic-avoidance mode; the guidance calculation then chooses a maneuver. The [encounter study](encounter-feasibility.md) asks how early an observation must arrive for that response to work.

```sysml-view Page_architecture_traffic::scenario direction=LR
package Page_architecture_traffic {
    private import OOSEM::*;
    view scenario : LogicalScenarioView {
        expose BlueDog::Method::Scenarios::TrafficEncounter;
    }
}
```

### Abort and recover

Capsize alone need not end qualification: the boat may recover unassisted and continue if it retains the required safety capabilities and uses no recovery motor. Motor use, outside intervention or loss of a required safety capability ends qualification. IC-01’s inverted powered-recovery hypothesis is therefore an abort path.

An abort ends the attempt. The boat records and signals the event, selects a reachable shore destination and attempts recovery without waiting for an operator or communications acknowledgment. The recovery leg may use the motor.

The recovery cycle explicitly supplies navigation, traffic, boundary and reserve assessments to shore planning, then durably records disqualification before passing an acknowledged authorization to recovery actuation. The actuator produces a separate execution-disposition record; sending a command does not establish the achieved response. The candidate implements these exchanges through the recovery sensors, controller and propulsor. Shore capture and one-person pickup remain physical and operator tasks; a propulsion command or simulated approach does not establish retrieval.

```sysml-view Page_architecture_recovery::scenario direction=LR
package Page_architecture_recovery {
    private import OOSEM::*;
    view scenario : LogicalScenarioView {
        expose BlueDog::Method::Scenarios::AbortAndRecover;
    }
}
```

### Capsize, safety and unassisted righting

An inversion suspends sailing and gate scoring. The supervisor needs explicit confirmation that required safety capability remains available while the boat is inverted. It can then wait for an observed unassisted return to upright control. A later upright observation cannot clear an earlier safety abort, motor use or intervention.

```sysml-view Page_architecture_capsize::scenario direction=LR
package Page_architecture_capsize {
    private import OOSEM::*;
    view scenario : LogicalScenarioView {
        expose BlueDog::Method::Scenarios::CapsizeAndResume;
    }
}
```

The scenario carries a safety observation into a permission decision, applies that permission and retains its record. The native supervisor executes this decision policy in the simulator; it does not predict whether the hull will right itself. Low reserve or lost safety capability can interrupt the wait for righting, including during a communications outage. Physical inverted sensing, righting, restored control and recovery thrust remain tests to perform on an identified boat.

These responsibilities put estimation and decisions onboard. The wired wind sensor is a concrete starting point, while processor choice, software boundaries and backup equipment remain open. I need timing, power and fault tests to select compatible implementations. The [method model](../models/blue-dog.sysml) records the assignments; the [current assessment](current-assessment.md) identifies the next investigations.

### Navigation, outages, reserve, launch and maintenance

Navigation passes a time-stamped estimate through validity assessment before guidance can use it. A communications outage preserves records onboard and queues alerts for later delivery; losing the shore link does not itself remove autonomous control. Energy management assesses the protected recovery reserve and can request an abort before it is exhausted.

Before launch, the scenario combines an identified configuration, evidence readiness and the admitted operating conditions into a release decision. Maintenance records the configuration and work performed before a new release. These [typed scenarios](../models/blue-dog.sysml) describe the necessary exchanges and responsible functions. Their presence does not implement a launcher, maintenance system, sensor estimator or communications protocol. The supervisor and numerical demonstrations execute the bounded decisions identified in the [runtime reference](reference/model-runtime.md#run-the-named-integration-candidate).

The [mission simulator](mission-simulation.md#executable-supervisory-logic) records the resulting decisions and motion, including the time between sending a command and completing a maneuver. That connection lets a scenario expose a missing capability rather than merely describe an intended sequence.

<details>
<summary>Subsystem responsibilities and supporting use cases</summary>

## Sailing hardware

Hull and rig provide the physical platform; actuation trims and steers it. The diagram names the responsibilities before I choose equipment.

```sysml-view Page_architecture_1::sailing direction=TB
package Page_architecture_1 {
    private import StandardViewDefinitions::*;
    view sailing : GeneralView {
        expose BlueDog::Architecture::HullAndRig;
        expose BlueDog::Architecture::SailAndSteeringActuation;
        expose BlueDog::Architecture::EnergySubsystem;
        filter @SysML::PartDefinition;
    }
}
```

## Autonomy and observation

Sensing feeds autonomous decisions; communications let me observe them. Losing a link must not turn shore support into the boat’s controller.

```sysml-view Page_architecture_5::autonomy direction=TB
package Page_architecture_5 {
    private import StandardViewDefinitions::*;
    view autonomy : GeneralView {
        expose BlueDog::Architecture::NavigationAndSensing;
        expose BlueDog::Architecture::GuidanceAndControl;
        expose BlueDog::Architecture::Communications;
        filter @SysML::PartDefinition;
    }
}
```

## Recovery and records

Health and recovery address failures, signaling makes the boat observable to traffic, and recording preserves what happened. The optional observation payload remains a later increment.

```sysml-view Page_architecture_6::support direction=TB
package Page_architecture_6 {
    private import StandardViewDefinitions::*;
    view support : GeneralView {
        expose BlueDog::Architecture::HealthAndRecovery;
        expose BlueDog::Architecture::NavigationSignaling;
        expose BlueDog::Architecture::DataRecording;
        filter @SysML::PartDefinition;
    }
}
```

Use cases connect operator and environmental interactions to the requirements they serve.

## Sail among other vessels

Traffic is an actor in the operating context, not just an environmental number. The sailing and avoidance cases connect that interaction to mission and safety obligations.

```sysml-view Page_architecture_2::operations direction=TB
package Page_architecture_2 {
    private import StandardViewDefinitions::*;
    view operations : GeneralView {
        expose BlueDog::Mission::UseCases::sailGorge;
        expose BlueDog::Mission::UseCases::avoidTraffic;
        filter @SysML::UseCaseUsage;
    }
}
```

## Observe and recover

Monitoring supports live observation; recovery is a separate operation that can end a qualifying attempt.

```sysml-view Page_architecture_7::supportOperations direction=TB
package Page_architecture_7 {
    private import StandardViewDefinitions::*;
    view supportOperations : GeneralView {
        expose BlueDog::Mission::UseCases::monitor;
        expose BlueDog::Mission::UseCases::recover;
        filter @SysML::UseCaseUsage;
    }
}
```

Launch, service, ocean sailing and navigation signaling remain in the [complete use-case model](../models/blue-dog.sysml).

</details>

## Interface meaning and applicability

A connected port needs a shared interpretation of its payload. Observations identify their source, configuration, clock and producer restart epoch; navigation and traffic values also identify their coordinate or angular references. Commands carry authority, configuration, issuance and expiry context. These are candidate interface definitions; transport encoding and installed equipment support remain open.

The [interface contract model](../models/blue-dog.sysml) separates producer validity from consumer usability. Its native predicates check a supplied age bound, an established time basis and applicable context. Command applicability also requires accepted authority and ordering. A valid link-down observation differs from missing link data; an empty traffic list does not establish detection coverage. Numerical refresh cadence does not establish a safe freshness limit.

The [executable consumer contracts](../models/blue-dog.sysml) reuse those predicates and separate sailing permission from recovery enable. Sailing checks current command and permission applicability, navigation, wind, safety and persistent restrictions. Motor enable requires known nonqualifying state, durable disqualification, established recovery authorization, an available path and no active inhibit. These partial logical actions are tested through native execution; the scalar mission simulator does not yet implement the message/storage protocol or hardware interlocks.

I use [NASA interface management guidance](https://www.nasa.gov/reference/6-3-interface-management/) to connect these definitions to integration checks and change control. The [historical NASA interface design guidance](https://swehb.nasa.gov/spaces/7150/pages/16450621/SWE-112%2B-%2BInterface%2BDesign%2BDescription) supplies the detailed review topics. Freshness allocations, clock uncertainty, reference transformations, controller arbitration and physical compatibility need engineering decisions and evidence before these contracts can support deployment. The conceptual simulator does not yet consume these message envelopes.

## From mission to verification

Read this view from the challenge obligation to its vehicle refinement and planned verification. A satisfy link states the design's intended satisfaction claim; that claim still needs evidence. Allocation separately maps logical responsibilities to physical elements.

```sysml-view Page_architecture_3::MissionSemantics direction=BT
package Page_architecture_3 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view MissionSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Verification::Requirements::RoundTripVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 360; y = 0; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 0; y = 200; }
        metadata Layout about BlueDog::Verification::Requirements::RoundTripVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
}
```

[Focused requirements](requirements.md) keep each derivation small enough to read. I distinguish mission obligations from independent owner constraints such as transport and manufacture.

```sysml-view Page_architecture_4::ManufacturingSemantics direction=BT
package Page_architecture_4 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view ManufacturingSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::desktopManufacture;
        expose BlueDog::Architecture::missionContext::boat::hullAndRig::printedHull;
        expose BlueDog::Verification::Requirements::DesktopManufactureVerification;
        metadata Layout about BlueDog::Requirements::desktopManufacture { x = 0; y = 0; }
        metadata Layout about BlueDog::Architecture::missionContext::boat::hullAndRig::printedHull { x = 360; y = 0; }
        metadata Layout about BlueDog::Verification::Requirements::DesktopManufactureVerification { x = 0; y = 200; }
    }
}
```

## Identify the study and the installation

A candidate name does not identify a built boat. IC-01 owns the working design
and integration allowances. The retained 440 Wh replay, the earlier Bingen design,
recorded sizing explorations and synthetic examples answer different questions.
Search brackets bound a calculation; they are not selected dimensions or vessel
requirements. Shared parameter assumptions also need their own revision context.

<details>
<summary>Configuration contexts and the planned IC-01 installation</summary>

```sysml-report BlueDogConfigurationDocuments::ConfigurationRegister
```

</details>

The intended installation references IC-01's design and candidate assembly.
Actual article, hardware, software/data, procedure and reconciliation records
remain unset. I need those identities to compare a test with the boat it is meant
to support. The archived numerical origin is useful provenance; it is not the
current hardware revision. A source fingerprint identifies the model used by a
calculation, while configuration reconciliation checks what was actually built.

This approach follows [NASA configuration management](https://www.nasa.gov/reference/6-5-configuration-management/)
and the [defense SE guidebook, section 6.1.6](https://www.cto.mil/wp-content/uploads/2026/09/SE-Guidebook-2026.pdf),
with project-specific scope rather than acquisition review gates. A hardware or
software change needs its affected interfaces, safety, budgets, analyses and
verification evidence reconciled together.

**Next:** [Establishing operating constraints](operating-constraints.md) · [Series guide](index.md)
