package BlueDogViews {
    private import StandardViewDefinitions::*;
    view requirements : GeneralView {
        expose GorgeChallenge::*;
        expose BlueDog::Requirements::*;
        filter @SysML::RequirementUsage;
    }
}
