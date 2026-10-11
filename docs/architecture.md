# Mission, context and architecture

The challenge remains independent of the vehicle so a convenient hardware choice cannot redefine success. The Gorge mission is a proving ground for the eventual ocean voyage. Traffic, shore support and live monitoring belong in the system context; the vessel must make its own decisions during a qualifying attempt.

We decompose responsibilities before choosing hardware. A satisfy link identifies intended responsibility, while a verification case identifies how that allocation will be tested. Neither means the vessel has passed a physical test.

```sysml-view Page_architecture_0::context direction=TB
package Page_architecture_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view context : GeneralView {
        expose BlueDog::Architecture::missionContext;
        render Views::asInterconnectionDiagram;
    }
}
```

```sysml-view Page_architecture_1::architecture direction=TB
package Page_architecture_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view architecture : GeneralView {
        expose BlueDog::Architecture::Boat;
        expose BlueDog::Architecture::NavigationSignaling;
        expose BlueDog::Architecture::HullAndRig;
        expose BlueDog::Architecture::EnergySubsystem;
        expose BlueDog::Architecture::NavigationAndSensing;
        expose BlueDog::Architecture::GuidanceAndControl;
        expose BlueDog::Architecture::SailAndSteeringActuation;
        expose BlueDog::Architecture::Communications;
        expose BlueDog::Architecture::HealthAndRecovery;
        expose BlueDog::Architecture::DataRecording;
        expose BlueDog::Architecture::ObservationPayload;
        filter @SysML::PartDefinition;
    }
}
```

Use cases connect operator and environmental interactions to the requirements they serve.

```sysml-view Page_architecture_2::operations direction=TB
package Page_architecture_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view operations : GeneralView {
        expose BlueDogUseCases::*;
        filter @SysML::UseCaseUsage;
    }
}
```

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

[Focused requirements](requirements.md) keep each derivation small enough to read. We distinguish mission obligations from independent owner constraints such as transport and manufacture.

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
