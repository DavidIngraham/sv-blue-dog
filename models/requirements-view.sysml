package BlueDogViews {
    private import StandardViewDefinitions::*;
    view requirements : GeneralView {
        expose GorgeChallenge::*;
    expose BlueDog::Goals::*;
        expose BlueDogRequirements::*;
        filter @SysML::RequirementUsage;
    }
}
