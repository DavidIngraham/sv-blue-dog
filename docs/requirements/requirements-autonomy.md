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
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::criticalEventRecording;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::guidanceUpdateCadence;
        expose BlueDog::Requirements::headingAccuracy;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationAvailability;
        expose BlueDog::Requirements::navigationDegradedTransition;
        expose BlueDog::Requirements::navigationValidEpochs;
        expose BlueDog::Requirements::positionAccuracy;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::sailCommandCadence;
        expose BlueDog::Requirements::staleNavigationInvalidation;
        expose BlueDog::Requirements::staleNavigationUseInhibition;
        expose BlueDog::Requirements::steeringCommandCadence;
        expose BlueDog::Requirements::trafficSafety;
        expose BlueDog::Mission::Challenge::trafficCoexistence;
        expose BlueDog::Requirements::windObservation;
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
        metadata Layout about BlueDog::Requirements::guidanceUpdateCadence { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::headingAccuracy { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::navigationAvailability { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::navigationDegradedTransition { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::navigationValidEpochs { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::positionAccuracy { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::sailCommandCadence { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::staleNavigationInvalidation { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::staleNavigationUseInhibition { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::steeringCommandCadence { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::trafficSafety { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::windObservation { x = 640; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 960; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 0; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 320; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 640; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 960; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 0; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::trafficCoexistence { x = 0; y = 3200; }
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
        expose BlueDog::Requirements::invalidWindUseInhibition;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::windDirectionAccuracy;
        expose BlueDog::Requirements::windLossResponse;
        expose BlueDog::Requirements::windObservation;
        expose BlueDog::Requirements::windSampleCadence;
        expose BlueDog::Requirements::windSensingEndurance;
        expose BlueDog::Requirements::windSpeedAccuracy;
        expose BlueDog::Requirements::windStaleInvalidation;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::invalidWindUseInhibition { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::windDirectionAccuracy { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::windLossResponse { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::windObservation { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::windSampleCadence { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::windSensingEndurance { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::windSpeedAccuracy { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::windStaleInvalidation { x = 640; y = 800; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 960; y = 800; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 0; y = 1200; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 320; y = 1200; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 640; y = 1200; }
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
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::criticalEventRecording;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::ingressDetection;
        expose BlueDog::Requirements::ingressElectronicsProtection;
        expose BlueDog::Requirements::ingressEventDeadline;
        expose BlueDog::Requirements::ingressFlotation;
        expose BlueDog::Requirements::ingressPositionContinuity;
        expose BlueDog::Requirements::ingressRecoveryRequest;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::motorQualificationInvariant;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationAvailability;
        expose BlueDog::Requirements::reconnectLogPreservation;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::restartDeadline;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::unknownQualificationFallback;
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
        metadata Layout about BlueDog::Requirements::ingressDetection { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::ingressElectronicsProtection { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::ingressEventDeadline { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::ingressFlotation { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::ingressPositionContinuity { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::ingressRecoveryRequest { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::motorQualificationInvariant { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::navigationAvailability { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::reconnectLogPreservation { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 640; y = 2000; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 960; y = 2000; }
        metadata Layout about BlueDog::Requirements::restartDeadline { x = 0; y = 2400; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 2400; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 640; y = 2400; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 960; y = 2400; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 1120; y = 2580; }
        metadata Layout about BlueDog::Requirements::unknownQualificationFallback { x = 0; y = 2800; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 320; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 640; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 960; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 0; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 320; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 640; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 960; y = 3200; }
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
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::freshRecoveryCommand;
        expose BlueDog::Requirements::gateProgressRestoration;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::logInterruptionDurability;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::missionStateRestoration;
        expose BlueDog::Requirements::motorQualificationInvariant;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::qualificationPersistence;
        expose BlueDog::Requirements::qualificationRestoration;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::resetRestrictionPreservation;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
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
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::envelopeTransition { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::freshRecoveryCommand { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::gateProgressRestoration { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::logInterruptionDurability { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::missionStateRestoration { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::motorQualificationInvariant { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::qualificationPersistence { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::qualificationRestoration { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::resetRestrictionPreservation { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 640; y = 2000; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 960; y = 2000; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 1120; y = 2180; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 0; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 320; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 640; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 960; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 0; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 320; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 640; y = 2800; }
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
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::criticalEventRecording;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::invalidTimestampMarking;
        expose BlueDog::Requirements::logGapIndication;
        expose BlueDog::Requirements::logInterruptionDurability;
        expose BlueDog::Requirements::logRetention;
        expose BlueDog::Requirements::logTimestampAccuracy;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::navigationAvailability;
        expose BlueDog::Requirements::periodicLogCadence;
        expose BlueDog::Requirements::qualificationPersistence;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
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
        metadata Layout about BlueDog::Requirements::invalidTimestampMarking { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::logGapIndication { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::logInterruptionDurability { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::logRetention { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::logTimestampAccuracy { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::navigationAvailability { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::periodicLogCadence { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::qualificationPersistence { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 640; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 960; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 0; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 320; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 640; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 960; y = 2400; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 0; y = 2800; }
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
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::communicationOutageAutonomy;
        expose BlueDog::Mission::Challenge::weatherOutageContinuation;
        expose BlueDog::Mission::Challenge::forecastAdmission;
        expose BlueDog::Mission::Challenge::unassistedAttempt;
        expose BlueDog::Mission::Challenge::liveObservation;
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::communicationOutageAutonomy { x = 320; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::weatherOutageContinuation { x = 640; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::forecastAdmission { x = 0; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 320; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 640; y = 400; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
