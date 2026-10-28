package BlueDogViews {
    private import StandardViewDefinitions::*;
    view requirements : GeneralView {
        expose BlueDog::Mission::Challenge::*;
        expose BlueDog::Goals::*;
        expose BlueDog::Requirements::*;
        expose BlueDog::Requirements::Structure::*;
        filter @SysML::RequirementUsage;
    }
}
