# Autonomous sailing, navigation and wind sensing

[Requirements overview](../requirements.md) · [Current assessment](../current-assessment.md)

The boat must make navigation and safety decisions onboard, using observations that are timely and valid. A restart must preserve qualification status and restrictions; losing shore communications must not remove its ability to act. The [mission supervisor](../mission-simulation.md#executable-supervisory-logic) exercises these decisions in simulation. Sensor quality and achieved control response need separate evidence.

## Navigation and control

Navigation estimates, guidance decisions and commands must remain coherent over time. The obligations below specify availability, cadence and command behavior so later tests can check more than whether the boat followed a plausible track.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_autonomy_3::thread direction=BT statements=true
package Page_autonomy_3 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::criticalEventRecording;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::guidanceUpdateCadence;
        expose BlueDogRequirements::headingAccuracy;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::navigationDegradedTransition;
        expose BlueDogRequirements::navigationValidEpochs;
        expose BlueDogRequirements::positionAccuracy;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::sailCommandCadence;
        expose BlueDogRequirements::staleNavigationInvalidation;
        expose BlueDogRequirements::staleNavigationUseInhibition;
        expose BlueDogRequirements::steeringCommandCadence;
        expose BlueDogRequirements::trafficSafety;
        expose GorgeChallenge::trafficCoexistence;
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
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::guidanceUpdateCadence { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::headingAccuracy { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationDegradedTransition { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationValidEpochs { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::positionAccuracy { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::sailCommandCadence { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::staleNavigationInvalidation { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::staleNavigationUseInhibition { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::steeringCommandCadence { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::windObservation { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::trafficCoexistence { x = 0; y = 3200; }
    }
}
```

</details>


## Wind observation

Wind estimates need accuracy, update cadence and a clear response to stale or missing samples. A numerically valid sensor value is not enough if its timestamp makes it unusable for control.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_autonomy_4::thread direction=BT statements=true
package Page_autonomy_4 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::invalidWindUseInhibition;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::windDirectionAccuracy;
        expose BlueDogRequirements::windLossResponse;
        expose BlueDogRequirements::windObservation;
        expose BlueDogRequirements::windSampleCadence;
        expose BlueDogRequirements::windSensingEndurance;
        expose BlueDogRequirements::windSpeedAccuracy;
        expose BlueDogRequirements::windStaleInvalidation;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::invalidWindUseInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::windDirectionAccuracy { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::windLossResponse { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::windObservation { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::windSampleCadence { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::windSensingEndurance { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::windSpeedAccuracy { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::windStaleInvalidation { x = 640; y = 800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 1200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 1200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 1200; }
    }
}
```

</details>

The [sensor budget](../energy.md#wind-sensing-configurations) identifies the wired mission installation and its electrical demand.

## Fault recovery and mission evidence

Ingress, resets and interrupted logging must not silently restore permission to sail or erase the event that ended qualification. Records must preserve enough timing and state to reconstruct the attempt.

### Ingress protection and restart response

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_autonomy_5::thread direction=BT statements=true
package Page_autonomy_5 {
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
        expose BlueDogRequirements::ingressDetection;
        expose BlueDogRequirements::ingressElectronicsProtection;
        expose BlueDogRequirements::ingressEventDeadline;
        expose BlueDogRequirements::ingressFlotation;
        expose BlueDogRequirements::ingressPositionContinuity;
        expose BlueDogRequirements::ingressRecoveryRequest;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::reconnectLogPreservation;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::restartDeadline;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::emergencyControl;
        expose BlueDogRequirements::capsizeResilience;
        expose BlueDogRequirements::vegetationResilience;
        expose BlueDogRequirements::unknownQualificationFallback;
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
        metadata Layout about BlueDogRequirements::ingressDetection { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::ingressElectronicsProtection { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::ingressEventDeadline { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::ingressFlotation { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::ingressPositionContinuity { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::ingressRecoveryRequest { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::restartDeadline { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::emergencyControl { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::capsizeResilience { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::vegetationResilience { x = 1120; y = 2580; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 0; y = 2800; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 3200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 960; y = 3200; }
    }
}
```

</details>

### Restoring mission state after reset

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_autonomy_6::thread direction=BT statements=true
package Page_autonomy_6 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::commandIntegrity;
        expose BlueDogRequirements::communications;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::freshRecoveryCommand;
        expose BlueDogRequirements::gateProgressRestoration;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::logInterruptionDurability;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::missionStateRestoration;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::qualificationRestoration;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::resetRestrictionPreservation;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::emergencyControl;
        expose BlueDogRequirements::capsizeResilience;
        expose BlueDogRequirements::vegetationResilience;
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
        metadata Layout about BlueDogRequirements::energyAwareness { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::gateProgressRestoration { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::missionStateRestoration { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::qualificationRestoration { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRestrictionPreservation { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::emergencyControl { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::capsizeResilience { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::vegetationResilience { x = 1120; y = 2180; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 2800; }
    }
}
```

</details>

### Recording trustworthy mission evidence

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_autonomy_7::thread direction=BT statements=true
package Page_autonomy_7 {
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
        expose BlueDogRequirements::invalidTimestampMarking;
        expose BlueDogRequirements::logGapIndication;
        expose BlueDogRequirements::logInterruptionDurability;
        expose BlueDogRequirements::logRetention;
        expose BlueDogRequirements::logTimestampAccuracy;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::navigationAndControl;
        expose BlueDogRequirements::navigationAvailability;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::qualificationPersistence;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::emergencyControl;
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
        metadata Layout about BlueDogRequirements::invalidTimestampMarking { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::logGapIndication { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::logRetention { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::logTimestampAccuracy { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::emergencyControl { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 2800; }
    }
}
```

</details>

## Onboard decisions during service outages

A weather-service outage differs from an invalid forecast. The boat may continue using an applicable held forecast; it must respond when that basis no longer supports continued operation.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view SRR_Thread_autonomy::thread direction=BT statements=true
package SRR_Thread_autonomy {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::communicationOutageAutonomy;
        expose GorgeChallenge::weatherOutageContinuation;
        expose GorgeChallenge::forecastAdmission;
        expose GorgeChallenge::unassistedAttempt;
        expose GorgeChallenge::liveObservation;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::communicationOutageAutonomy { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::weatherOutageContinuation { x = 640; y = 0; }
        metadata Layout about GorgeChallenge::forecastAdmission { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 400; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
