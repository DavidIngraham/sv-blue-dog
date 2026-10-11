# L-001 Mission reliability: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_l_001_0::thread direction=BT statements=true
package Page_requirements_l_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::criticalFailureDisposition;
        expose BlueDogRequirements::failureRateBudget;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::reliabilityEvidence;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::criticalFailureDisposition { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::failureRateBudget { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::reliabilityEvidence { x = 960; y = 1600; }
    }
}
```
