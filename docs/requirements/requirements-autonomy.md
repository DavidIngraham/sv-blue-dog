# Autonomous sailing, navigation and wind sensing

Autonomy turns the mission into onboard decisions. Navigation and wind observations supply the controller; recovery behavior keeps faults from silently becoming mission failures.

[Requirements overview](../requirements.md) · [Modeling method](../methods/modeling.md)

Arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision, and **dependency** records a design basis. Each view retains its upstream context; statements are rendered from the model.

- [Navigation and control](#navigation-and-control)
- [Wind observation](#wind-observation)
- [Fault recovery and mission evidence](#fault-recovery-and-mission-evidence)

## Navigation and control

```sysml-view Page_autonomy_3::thread direction=BT statements=true
package Page_autonomy_3 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::guidanceUpdateCadence { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::headingAccuracy { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationDegradedTransition { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::navigationValidEpochs { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::positionAccuracy { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::sailCommandCadence { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::staleNavigationInvalidation { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::staleNavigationUseInhibition { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::steeringCommandCadence { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::trafficSafety { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::windObservation { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 2800; }
    }
}
```


## Wind observation

```sysml-view Page_autonomy_4::thread direction=BT statements=true
package Page_autonomy_4 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::invalidWindUseInhibition { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::windDirectionAccuracy { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::windLossResponse { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::windObservation { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::windSampleCadence { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::windSensingEndurance { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::windSpeedAccuracy { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::windStaleInvalidation { x = 960; y = 800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 1200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 1200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 1200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 1200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 1600; }
    }
}
```

[Sensor configurations and budgets](../energy.md#wind-sensing-configurations) distinguish the Bluetooth testbed sensor from the wired challenge installation.

## Fault recovery and mission evidence

### Ingress protection and restart response

```sysml-view Page_autonomy_5::thread direction=BT statements=true
package Page_autonomy_5 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::unknownQualificationFallback;
        expose BlueDogRequirements::weedBlockageResponse;
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
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::ingressDetection { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::ingressElectronicsProtection { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::ingressEventDeadline { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::ingressFlotation { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::ingressPositionContinuity { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::ingressRecoveryRequest { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::reconnectLogPreservation { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::restartDeadline { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 2800; }
        metadata Layout about BlueDogRequirements::unknownQualificationFallback { x = 320; y = 2800; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::liveObservation { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 640; y = 3200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 3200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 3600; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 3600; }
    }
}
```

### Restoring mission state after reset

```sysml-view Page_autonomy_6::thread direction=BT statements=true
package Page_autonomy_6 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::weedBlockageResponse;
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
        metadata Layout about BlueDogRequirements::energyAwareness { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::gateProgressRestoration { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::missionStateRestoration { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::qualificationRestoration { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::resetRestrictionPreservation { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 3200; }
    }
}
```

### Recording trustworthy mission evidence

```sysml-view Page_autonomy_7::thread direction=BT statements=true
package Page_autonomy_7 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
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
        expose BlueDogRequirements::safeRecovery;
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
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::invalidTimestampMarking { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::logGapIndication { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::logInterruptionDurability { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::logRetention { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::logTimestampAccuracy { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAndControl { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::navigationAvailability { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 2400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 2400; }
        metadata Layout about GorgeChallenge::liveObservation { x = 640; y = 2400; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 2400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 2800; }
    }
}
```
