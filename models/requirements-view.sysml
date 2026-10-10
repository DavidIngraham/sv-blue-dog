package BlueDogViews {
    private import StandardViewDefinitions::*;
    view requirements : GeneralView {
        expose BlueDog::Requirements::*;
        filter @SysML::RequirementUsage;
    }
}
