# Environment, durability and self-righting

The Gorge and ocean environments set the loads and exposure conditions. The breakdown connects those environments to measurable limits, capsize recovery and weed tolerance.

[Requirements overview](../requirements.md) · [Modeling method](../methods/modeling.md)

Arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision, and **dependency** records a design basis. Each view retains its upstream context; statements are rendered from the model.

- [Operating environments](#operating-environments)
- [Marine exposure and integrity](#marine-exposure-and-integrity)
- [Stability and capsize recovery](#stability-and-capsize-recovery)
- [Weed tolerance](#weed-tolerance)

## Operating environments

### Gorge conditions and survival transitions

```sysml-view Page_environment_12::thread direction=BT statements=true
package Page_environment_12 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::freshwaterExposure;
        expose BlueDogRequirements::gorgeCurrent;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::gorgeSurvivalWaves;
        expose BlueDogRequirements::gorgeSurvivalWind;
        expose BlueDogRequirements::gorgeWaves;
        expose BlueDogRequirements::gorgeWind;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::missionEvidence;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::periodicLogCadence;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::resumptionBlockEvidence;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::sailingResumptionDeadline;
        expose BlueDogRequirements::sailingResumptionInhibition;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::survivalEntryDeadline;
        expose BlueDogRequirements::survivalTransitionRecording;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedSnagShedding;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeCurrent { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWaves { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWind { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::gorgeWaves { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::gorgeWind { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::resumptionBlockEvidence { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::sailingResumptionDeadline { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::sailingResumptionInhibition { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 2800; }
        metadata Layout about BlueDogRequirements::survivalEntryDeadline { x = 320; y = 2800; }
        metadata Layout about BlueDogRequirements::survivalTransitionRecording { x = 640; y = 2800; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 960; y = 2800; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 3200; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 960; y = 3200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 3600; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 3600; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 640; y = 3600; }
    }
}
```

### Temperature, humidity and visibility

```sysml-view Page_environment_13::thread direction=BT statements=true
package Page_environment_13 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::airTemperature;
        expose BlueDogRequirements::calmOperation;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::humidity;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::restrictedVisibilityCollisionAssessment;
        expose BlueDogRequirements::restrictedVisibilityEntry;
        expose BlueDogRequirements::restrictedVisibilityEvidence;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::visibilityNavigationCapability;
        expose BlueDogRequirements::visibilityTrafficCapability;
        expose BlueDogRequirements::waterTemperature;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::airTemperature { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::calmOperation { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::humidity { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityCollisionAssessment { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEntry { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEvidence { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::visibilityNavigationCapability { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::visibilityTrafficCapability { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::waterTemperature { x = 960; y = 1200; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 1600; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 1600; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 1600; }
    }
}
```

### Ocean conditions

```sysml-view Page_environment_14::thread direction=BT statements=true
package Page_environment_14 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::oceanCurrent;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanSurvivalWaves;
        expose BlueDogRequirements::oceanSurvivalWind;
        expose BlueDogRequirements::oceanWaves;
        expose BlueDogRequirements::oceanWind;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::saltwaterExposure;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::oceanCurrent { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWaves { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWind { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::oceanWaves { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::oceanWind { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 640; y = 800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 1200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 1200; }
    }
}
```


## Marine exposure and integrity

```sysml-view Page_environment_15::thread direction=BT statements=true
package Page_environment_15 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::batteryChargeTemperatureInhibition;
        expose BlueDogRequirements::enclosureSealing;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::freshwaterExposure;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::hotSunBatteryTemperature;
        expose BlueDogRequirements::hotSunElectronicsOperation;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::printedMaterialAging;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::saltwaterExposure;
        expose BlueDogRequirements::solarHeating;
        expose BlueDogRequirements::wetConductorResistance;
        expose BlueDogRequirements::wetElectricalIntegrity;
        expose BlueDogRequirements::wetInsulationResistance;
        expose BlueDogRequirements::wetJointIntegrity;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogRequirements::wetMechanismTravel;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::batteryChargeTemperatureInhibition { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::enclosureSealing { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::hotSunBatteryTemperature { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::hotSunElectronicsOperation { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::printedMaterialAging { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::solarHeating { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::wetConductorResistance { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::wetInsulationResistance { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::wetJointIntegrity { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::wetMechanismTravel { x = 960; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 2000; }
    }
}
```


## Stability and capsize recovery

```sysml-view Page_environment_16::thread direction=BT statements=true
package Page_environment_16 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::capsizeBallastRetention;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::capsizeElectronicsSealing;
        expose BlueDogRequirements::capsizeGateProgressRetention;
        expose BlueDogRequirements::capsizeQualificationRetention;
        expose BlueDogRequirements::capsizeRestrictionRetention;
        expose BlueDogRequirements::capsizeRigRetention;
        expose BlueDogRequirements::controlRecoveryDeadline;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::rightingDeadline;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedSnagShedding;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeBallastRetention { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeElectronicsSealing { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeGateProgressRetention { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::capsizeQualificationRetention { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::capsizeRestrictionRetention { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::capsizeRigRetention { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::controlRecoveryDeadline { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::rightingDeadline { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::selfRighting { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 2000; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 2400; }
    }
}
```


## Weed tolerance

```sysml-view Page_environment_17::thread direction=BT statements=true
package Page_environment_17 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::energyAwareness;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::ingressResponse;
        expose BlueDogRequirements::lockedPropulsorShutdown;
        expose BlueDogRequirements::lowEnergyRecovery;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::poweredWeedCurrent;
        expose BlueDogRequirements::poweredWeedSpeed;
        expose BlueDogRequirements::poweredWeedTemperature;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::resetRecovery;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedBlockageContingency;
        expose BlueDogRequirements::weedBlockageFault;
        expose BlueDogRequirements::weedBlockageLocation;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedPassageSpeed;
        expose BlueDogRequirements::weedPassageSteering;
        expose BlueDogRequirements::weedSnagShedding;
        expose BlueDogRequirements::weedSnagSpeedRecovery;
        expose BlueDogRequirements::weedSnagSteeringRecovery;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::repeatedOperation;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::lockedPropulsorShutdown { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::poweredWeedCurrent { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::poweredWeedSpeed { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::poweredWeedTemperature { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageContingency { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageFault { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageLocation { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::weedPassageSpeed { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::weedPassageSteering { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::weedSnagSpeedRecovery { x = 0; y = 2800; }
        metadata Layout about BlueDogRequirements::weedSnagSteeringRecovery { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::repeatedOperation { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 640; y = 3200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 960; y = 3200; }
    }
}
```
