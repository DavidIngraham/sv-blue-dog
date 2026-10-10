package BlueDogArchitectureViews {
    private import StandardViewDefinitions::*;
    view architecture : GeneralView {
        expose BlueDog::Architecture::Boat;
        render Views::asInterconnectionDiagram;
    }
    view context : GeneralView {
        expose BlueDog::Architecture::missionContext;
        render Views::asInterconnectionDiagram;
    }
}
