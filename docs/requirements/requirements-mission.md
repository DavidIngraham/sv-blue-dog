# Mission, course completion and endurance

The Gorge round trip is the first challenge; sustained operation and Hawaii extend the design horizon. These threads connect those goals to course performance and mission reliability.

[Requirements overview](../requirements.md) · [Modeling method](../methods/modeling.md)

Arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision, and **dependency** records a design basis. Each view retains its upstream context; statements are rendered from the model.

- [Mission and challenge rules](#mission-and-challenge-rules)
- [Endurance and cruise performance](#endurance-and-cruise-performance)
- [Mission reliability](#mission-reliability)

## Mission and challenge rules

```sysml-view Page_mission_0::thread direction=BT statements=true
package Page_mission_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::regulatoryClassification;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::windObservation;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::serviceability { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::windObservation { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::liveObservation { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 960; y = 2400; }
    }
}
```


## Endurance and cruise performance

```sysml-view Page_mission_1::thread direction=BT statements=true
package Page_mission_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::cruiseEvidence;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::energyEvidenceReadiness;
        expose BlueDogRequirements::harvestCampaignCoverage;
        expose BlueDogRequirements::legProgress;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::passageDuration;
        expose BlueDogRequirements::peakSupplyCapability;
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::windObservation;
        expose BlueDogRequirements::windSensingEndurance;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::cruiseEvidence { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::harvestCampaignCoverage { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::legProgress { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::passageDuration { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::windObservation { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::windSensingEndurance { x = 960; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 2400; }
    }
}
```


## Mission reliability

```sysml-view Page_mission_2::thread direction=BT statements=true
package Page_mission_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::criticalFailureDisposition;
        expose BlueDogRequirements::failureRateBudget;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::reliabilityEvidence;
        expose BlueDogRequirements::roundTrip;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalFailureDisposition { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::failureRateBudget { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::reliabilityEvidence { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 800; }
    }
}
```
