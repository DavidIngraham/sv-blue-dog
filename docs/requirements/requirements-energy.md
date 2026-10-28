# Energy and recovery propulsion

[Requirements overview](../requirements.md) · [Current assessment](../current-assessment.md)

Energy is a mission capability: the boat needs enough usable storage and power delivery for the planned passage, while preserving a reachable recovery option. Low-energy behavior must protect navigation and collision avoidance before optional loads. IC-01 allocates a separate recovery battery; the [energy analysis](../energy.md) evaluates that design choice against these obligations.

## Energy awareness and low-energy response

Available energy and route-dependent reserve must be estimated often enough to act before the boat loses its recovery option. Optional payloads yield to essential functions.

### Preserving essential functions at low energy

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_energy_8::thread direction=BT statements=true
package Page_energy_8 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::criticalEventRecording;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::lowEnergyCollisionContinuity;
        expose BlueDog::Requirements::lowEnergyEntry;
        expose BlueDog::Requirements::lowEnergyExit;
        expose BlueDog::Requirements::lowEnergyNavigationContinuity;
        expose BlueDog::Requirements::lowEnergyPayloadInhibition;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::motorQualificationInvariant;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationAvailability;
        expose BlueDog::Requirements::payloadRestartPermission;
        expose BlueDog::Requirements::periodicLogCadence;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::telemetryDeliveryCadence;
        expose BlueDog::Requirements::weedBlockageResponse;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::emergencyIntervention;
        expose BlueDog::Mission::Challenge::liveObservation;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::commandIntegrity { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::communications { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::criticalEventRecording { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::envelopeTransition { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::lowEnergyCollisionContinuity { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyEntry { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyExit { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyNavigationContinuity { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyPayloadInhibition { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::motorQualificationInvariant { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::navigationAvailability { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::payloadRestartPermission { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::periodicLogCadence { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 640; y = 2000; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 960; y = 2000; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 0; y = 2400; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 320; y = 2400; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 640; y = 2400; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 800; y = 2580; }
        metadata Layout about BlueDog::Requirements::telemetryDeliveryCadence { x = 960; y = 2400; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 0; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 320; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 640; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 960; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 0; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 320; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 640; y = 3200; }
    }
}
```

</details>

### Estimating available energy and reserve

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_energy_9::thread direction=BT statements=true
package Page_energy_9 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::conservativeEnergyEstimate;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::energyEstimateAccuracy;
        expose BlueDog::Requirements::energyEstimateCadence;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::reserveEstimateCadence;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        metadata Layout about BlueDog::Requirements::conservativeEnergyEstimate { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::energyEstimateAccuracy { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::energyEstimateCadence { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::reserveEstimateCadence { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 960; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 0; y = 800; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 320; y = 800; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 640; y = 800; }
    }
}
```

</details>


## Sustained energy feasibility

This repeating-energy objective belongs to future sustained operation. The current Gorge mission requires adequate energy and protected reserve throughout its finite campaign.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_energy_10::thread direction=BT statements=true
package Page_energy_10 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDog::Requirements::energyEvidenceReadiness;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::peakSupplyCapability;
        expose BlueDog::Requirements::recoveryEnergy;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::repeatableCycleBalance;
        expose BlueDog::Requirements::harvestCampaignCoverage;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::sustainedEnergyFeasibility;
        expose BlueDog::Requirements::sustainedReserveProtection;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::emergencyIntervention;
        expose BlueDog::Mission::Challenge::repeatedOperation;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::energyEvidenceReadiness { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::peakSupplyCapability { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::recoveryEnergy { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::repeatableCycleBalance { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::sustainedEnergyFeasibility { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::sustainedReserveProtection { x = 640; y = 800; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 960; y = 800; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 0; y = 1200; }
        metadata Layout about BlueDog::Mission::Challenge::repeatedOperation { x = 320; y = 1200; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 640; y = 1200; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::harvestCampaignCoverage { x = 0; y = 1600; }
    }
}
```

</details>


## Recovery propulsion and reserves

The motor is inhibited during qualification. Recovery requires explicit authority, a fresh valid command and sufficient reserve; stopping the motor or restarting the controller does not restore the attempt.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_energy_11::thread direction=BT statements=true
package Page_energy_11 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::criticalEventRecording;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::freshRecoveryCommand;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::launchEnergyAdmission;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::motorQualificationInvariant;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationAvailability;
        expose BlueDog::Requirements::qualificationPersistence;
        expose BlueDog::Requirements::recoveryEnergy;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::sustainedReserveProtection;
        expose BlueDog::Requirements::weedBlockageResponse;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::emergencyIntervention;
        expose BlueDog::Mission::Challenge::liveObservation;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::commandIntegrity { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::communications { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::criticalEventRecording { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::envelopeTransition { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::freshRecoveryCommand { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::launchEnergyAdmission { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::motorQualificationInvariant { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::navigationAvailability { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::qualificationPersistence { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryEnergy { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 640; y = 2000; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 960; y = 2000; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 1120; y = 2180; }
        metadata Layout about BlueDog::Requirements::sustainedReserveProtection { x = 0; y = 2400; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 320; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 640; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 960; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 0; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 320; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 640; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 960; y = 2800; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
