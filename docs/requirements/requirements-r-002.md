# R-002 Recovery energy: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_r_002_0::thread direction=BT statements=true
package Page_requirements_r_002_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::repeatedOperation;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::launchEnergyAdmission;
        expose BlueDogRequirements::sustainedReserveProtection;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::launchEnergyAdmission { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 320; y = 2000; }
    }
}
```
