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

In [IC-01](../models/analyses/integrated-candidate.sysml), the main sensing and control system sails the mission. A separately powered recovery system must observe hazards, navigate and propel the boat after a primary failure, including while inverted. The practical question is whether those backup functions can survive the fault that disabled sailing. Shared water damage could still defeat both systems; isolation needs testing.

The [integration study](validation-plan.md#exercise-decisions-before-physical-integration) checks those responsibilities together using one boat's mass, sailing performance and energy budget. The next step is to turn the allocated capabilities into compatible hardware and test their interfaces.

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

I use OOSEM to work from what the mission needs to what each part of the boat must do. The three scenarios below describe normal sailing, avoiding traffic and recovering after an abort. OpenSysML renders these views from the shared model.

The [mission supervisor](mission-simulation.md#executable-supervisory-logic) implements part of these scenarios: it responds to events, permits or inhibits sailing, and remembers an abort so that sailing cannot silently resume. Sensor processing, steering decisions and physical actuation still need their own implementations and tests.

### Normal sailing

Each sailing cycle starts with a wind estimate carrying its value, timestamp and validity. Guidance chooses a command and the actuators carry it out. If wind observations disappear, the supervisor inhibits sailing; when they return, sailing can resume unless the attempt has already been aborted.

```sysml-view Page_architecture_normal::scenario direction=LR
package Page_architecture_normal {
    private import OOSEM::*;
    view scenario : LogicalScenarioView {
        expose BlueDogMethod::Scenarios::NormalSailing;
    }
}
```

### Traffic encounter

Observe, assess, maneuver and reassess. The Automatic Identification System (AIS) broadcasts information from equipped vessels, but Blue Dog must also detect traffic that does not transmit. In the simulator, a predicted conflict triggers traffic-avoidance mode; the guidance calculation then chooses a maneuver. The [encounter study](encounter-feasibility.md) asks how early an observation must arrive for that response to work.

```sysml-view Page_architecture_traffic::scenario direction=LR
package Page_architecture_traffic {
    private import OOSEM::*;
    view scenario : LogicalScenarioView {
        expose BlueDogMethod::Scenarios::TrafficEncounter;
    }
}
```

### Abort and recover

Capsize alone need not end qualification: the boat may recover unassisted and continue if it retains the required safety capabilities and uses no recovery motor. Motor use, outside intervention or loss of a required safety capability ends qualification. IC-01’s inverted powered-recovery hypothesis is therefore an abort path.

An abort ends the attempt. The boat records and signals the event, selects a reachable shore destination and attempts recovery without waiting for an operator or communications acknowledgment. The recovery leg may use the motor.

```sysml-view Page_architecture_recovery::scenario direction=LR
package Page_architecture_recovery {
    private import OOSEM::*;
    view scenario : LogicalScenarioView {
        expose BlueDogMethod::Scenarios::AbortAndRecover;
    }
}
```

These responsibilities put estimation and decisions onboard. The wired wind sensor is a concrete starting point, while processor choice, software boundaries and backup equipment remain open. I need timing, power and fault tests to select compatible implementations. The [method model](../models/vehicle/method.sysml) records the assignments; the [current assessment](current-assessment.md) identifies the next investigations.

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
        expose BlueDogUseCases::sailGorge;
        expose BlueDogUseCases::avoidTraffic;
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
        expose BlueDogUseCases::monitor;
        expose BlueDogUseCases::recover;
        filter @SysML::UseCaseUsage;
    }
}
```

Launch, service, ocean sailing and navigation signaling remain in the [complete use-case model](../models/vehicle/use-cases.sysml).

</details>

## From mission to verification

Read this view from the challenge obligation to its vehicle refinement and planned verification. A satisfy link allocates responsibility; it does not assert a passed test.

```sysml-view Page_architecture_3::MissionSemantics direction=BT
package Page_architecture_3 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view MissionSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirementVerification::RoundTripVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 200; }
        metadata Layout about BlueDogRequirementVerification::RoundTripVerification { x = 360; y = 200; }
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
        expose BlueDogRequirements::desktopManufacture;
        expose BlueDog::Architecture::missionContext::boat::hullAndRig::printedHull;
        expose BlueDogRequirementVerification::DesktopManufactureVerification;
        metadata Layout about BlueDogRequirements::desktopManufacture { x = 0; y = 0; }
        metadata Layout about BlueDog::Architecture::missionContext::boat::hullAndRig::printedHull { x = 360; y = 0; }
        metadata Layout about BlueDogRequirementVerification::DesktopManufactureVerification { x = 0; y = 200; }
    }
}
```

**Next:** [Establishing operating constraints](operating-constraints.md) · [Series guide](index.md)
