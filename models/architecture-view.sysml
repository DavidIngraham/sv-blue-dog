package BlueDogArchitectureViews {
    private import StandardViewDefinitions::*;
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
    view context : GeneralView {
        expose BlueDog::Architecture::missionContext;
        render Views::asInterconnectionDiagram;
    }
    view detail : GeneralView {
        expose BlueDog::Architecture::*;
        filter @SysML::PartDefinition;
    }
}
