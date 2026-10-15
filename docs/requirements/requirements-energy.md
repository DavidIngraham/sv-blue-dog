# Energy and recovery propulsion

**OOSEM:** System requirements and scenarios · [Maturity assessment](../development-plan.md)

The energy budget must support sailing continuously and retain a deliberate recovery capability. These threads separate energy awareness, sustained balance and the motor rules for a qualifying attempt.

[Requirements overview](../requirements.md) · [Modeling method](../methods/modeling.md)

Arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision, and **dependency** records a design basis. Each view retains its upstream context; statements are rendered from the model.

- [Energy awareness and low-energy response](#energy-awareness-and-low-energy-response)
- [Sustained energy feasibility](#sustained-energy-feasibility)
- [Recovery propulsion and reserves](#recovery-propulsion-and-reserves)

## Energy awareness and low-energy response

### Preserving essential functions at low energy

```sysml-view Page_energy_8::thread direction=BT statements=true
package Page_energy_8 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::lowEnergyCollisionContinuity;
        expose BlueDogRequirements::lowEnergyEntry;
        expose BlueDogRequirements::lowEnergyExit;
        expose BlueDogRequirements::lowEnergyNavigationContinuity;
        expose BlueDogRequirements::lowEnergyPayloadInhibition;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::payloadRestartPermission;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::telemetryDeliveryCadence;
        expose BlueDogRequirements::weedBlockageResponse;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyCollisionContinuity { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyEntry { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyExit { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyNavigationContinuity { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyPayloadInhibition { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::payloadRestartPermission { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::telemetryDeliveryCadence { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::liveObservation { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 3200; }
    }
}
```

### Estimating available energy and reserve

```sysml-view Page_energy_9::thread direction=BT statements=true
package Page_energy_9 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::conservativeEnergyEstimate;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::energyEstimateAccuracy;
        expose BlueDogRequirements::energyEstimateCadence;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::reserveEstimateCadence;
        expose BlueDogRequirements::roundTrip;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDogRequirements::conservativeEnergyEstimate { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::energyEstimateAccuracy { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::energyEstimateCadence { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::reserveEstimateCadence { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 960; y = 400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 800; }
    }
}
```


## Sustained energy feasibility

This repeating-energy objective belongs to future sustained operation. The current Gorge mission requires adequate energy and protected reserve throughout its finite campaign.

```sysml-view Page_energy_10::thread direction=BT statements=true
package Page_energy_10 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::energyEvidenceReadiness;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::peakSupplyCapability;
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::repeatableCycleBalance;
        expose BlueDogRequirements::harvestCampaignCoverage;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::repeatableCycleBalance { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 640; y = 800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 1200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 1200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 1200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::harvestCampaignCoverage { x = 0; y = 1600; }
    }
}
```


## Recovery propulsion and reserves

```sysml-view Page_energy_11::thread direction=BT statements=true
package Page_energy_11 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::freshRecoveryCommand;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::launchEnergyAdmission;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::recoveryEnergy;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::weedBlockageResponse;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::liveObservation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::commandIntegrity { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::communications { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::launchEnergyAdmission { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryEnergy { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 960; y = 2800; }
    }
}
```
