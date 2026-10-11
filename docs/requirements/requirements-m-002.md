# M-002 Multi day endurance: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_m_002_0::thread direction=BT statements=true
package Page_requirements_m_002_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::unassistedAttempt;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::energyEvidenceReadiness;
        expose BlueDogRequirements::harvestCampaignCoverage;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::peakSupplyCapability;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::windObservation;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::windSensingEndurance;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 580; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::harvestCampaignCoverage { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 0; y = 1380; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 1380; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::windObservation { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::windSensingEndurance { x = 320; y = 2000; }
    }
}
```

## Continue the breakdown

- [Energy awareness](requirements-e-001.md)
- [Low energy recovery](requirements-e-004.md)
