# E-200 Sustained energy feasibility: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_e_200_0::thread direction=BT statements=true
package Page_requirements_e_200_0 {
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
        expose BlueDogRequirements::energyEvidenceReadiness;
        expose BlueDogRequirements::peakSupplyCapability;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::repeatableCycleBalance;
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::sustainedReserveProtection;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::repeatableCycleBalance { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 2000; }
    }
}
```
