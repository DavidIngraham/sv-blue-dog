# Mission, course completion and endurance

**Design phase:** Mission and requirements · SRR · [Development plan](../development-plan.md)

One Gorge round trip is the current design mission. These threads connect that finite challenge to course performance and reliability. Hawaii and repeated operation have separate future constraints.

The [ocean envelope](requirements-environment.md#future-hawaii-mission-ocean-conditions) and [repeating-energy objective](requirements-energy.md#sustained-energy-feasibility) are retained as future work. They do not set acceptance criteria for the current Gorge vessel.

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
        expose BlueDogRequirements::operatingBoundary;
        expose GorgeChallenge::restrictedWaters;
        expose BlueDogRequirements::regulatoryClassification;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::serviceability;
        expose BlueDogRequirements::windObservation;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::windObservation { x = 320; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 1600; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 1600; }
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::restrictedWaters { x = 0; y = 2400; }
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
        expose BlueDogRequirements::cruiseEvidence;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::energyEvidenceReadiness;
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
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::windObservation;
        expose BlueDogRequirements::windSensingEndurance;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::cruiseEvidence { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::legProgress { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::passageDuration { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::windObservation { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::windSensingEndurance { x = 320; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 1600; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 1600; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 2000; }
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
        expose BlueDogRequirements::criticalFailureDisposition;
        expose BlueDogRequirements::failureRateBudget;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::reliabilityEvidence;
        expose BlueDogRequirements::roundTrip;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDogRequirements::criticalFailureDisposition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::failureRateBudget { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::missionReliability { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::reliabilityEvidence { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 800; }
    }
}
```

## Qualification and launch admission

```sysml-view SRR_Thread_mission::thread direction=BT statements=true
package SRR_Thread_mission {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::overallLength;
        expose GorgeChallenge::unattachedPassage;
        expose GorgeChallenge::abortPersistence;
        expose GorgeChallenge::nightOperation;
        expose GorgeChallenge::forecastAdmission;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::overallLength { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::unattachedPassage { x = 640; y = 0; }
        metadata Layout about GorgeChallenge::abortPersistence { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::nightOperation { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::forecastAdmission { x = 640; y = 400; }
    }
}
```
