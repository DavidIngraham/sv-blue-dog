# Environment, durability and casualty recovery

[Requirements overview](../requirements.md) · [Current assessment](../current-assessment.md)

The boat must keep its essential functions within a declared operating envelope and recover when it cannot continue safely. That includes wet structures and electronics, weeds, capsize and retention of damaged components. N-003 addresses capsize recovery and N-004 addresses vegetation resilience. Each has its own planned assessment. Self-righting is one recovery solution; powered inverted recovery is another, but motor use ends qualification.

## Operating environments

Operational and casualty exposures serve different decisions. Wind, current, waves, temperature and visibility must be assessed in relevant combinations rather than treated as unrelated worst-case numbers.

### Gorge conditions and survival transitions

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_environment_12::thread direction=BT statements=true
package Page_environment_12 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
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
        expose BlueDogRequirements::emergencyControl;
        expose BlueDogRequirements::sailingResumptionDeadline;
        expose BlueDogRequirements::sailingResumptionInhibition;
        expose BlueDogRequirements::capsizeResilience;
        expose BlueDogRequirements::vegetationResilience;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::survivalEntryDeadline;
        expose BlueDogRequirements::survivalTransitionRecording;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedSnagShedding;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeCurrent { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWaves { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::gorgeSurvivalWind { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::gorgeWaves { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::gorgeWind { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::resumptionBlockEvidence { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::emergencyControl { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::sailingResumptionDeadline { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::sailingResumptionInhibition { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::capsizeResilience { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::vegetationResilience { x = 800; y = 2580; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::survivalEntryDeadline { x = 0; y = 2800; }
        metadata Layout about BlueDogRequirements::survivalTransitionRecording { x = 320; y = 2800; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 640; y = 2800; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 3200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 3200; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 3200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 0; y = 3600; }
    }
}
```

</details>

### Temperature, humidity and visibility

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_environment_13::thread direction=BT statements=true
package Page_environment_13 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
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
        expose BlueDogRequirements::capsizeResilience;
        expose BlueDogRequirements::vegetationResilience;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::visibilityNavigationCapability;
        expose BlueDogRequirements::visibilityTrafficCapability;
        expose BlueDogRequirements::waterTemperature;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDogRequirements::airTemperature { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::calmOperation { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::humidity { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityCollisionAssessment { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEntry { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::restrictedVisibilityEvidence { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::capsizeResilience { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::vegetationResilience { x = 800; y = 980; }
        metadata Layout about BlueDogRequirements::visibility { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::visibilityNavigationCapability { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::visibilityTrafficCapability { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::waterTemperature { x = 640; y = 1200; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 960; y = 1200; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 0; y = 1600; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 1600; }
    }
}
```

</details>

### Future Hawaii mission: ocean conditions

These candidate ocean limits are deferred to a separate Hawaii mission; they do not constrain Gorge acceptance.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_environment_14::thread direction=BT statements=true
package Page_environment_14 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose BlueDogRequirements::oceanCurrent;
        expose BlueDogRequirements::oceanEnvironment;
        expose BlueDogRequirements::oceanSurvivalWaves;
        expose BlueDogRequirements::oceanSurvivalWind;
        expose BlueDogRequirements::oceanWaves;
        expose BlueDogRequirements::oceanWind;
        expose BlueDogRequirements::saltwaterExposure;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::oceanCurrent { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::oceanEnvironment { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWaves { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::oceanSurvivalWind { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::oceanWaves { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::oceanWind { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::saltwaterExposure { x = 640; y = 800; }
    }
}
```

</details>


## Marine exposure and integrity

Wet material behavior, sealing and ingress response connect the environmental envelope to flotation, structure and essential electronics.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_environment_15::thread direction=BT statements=true
package Page_environment_15 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::batteryChargeTemperatureInhibition;
        expose BlueDogRequirements::enclosureSealing;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::freshwaterExposure;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::hotSunBatteryTemperature;
        expose BlueDogRequirements::hotSunElectronicsOperation;
        expose BlueDogRequirements::marineDurability;
        expose BlueDogRequirements::printedMaterialAging;
        expose BlueDogRequirements::roundTrip;
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
        metadata Layout about BlueDogRequirements::batteryChargeTemperatureInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::enclosureSealing { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::freshwaterExposure { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::hotSunBatteryTemperature { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::hotSunElectronicsOperation { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::marineDurability { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::printedMaterialAging { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::solarHeating { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::wetConductorResistance { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::wetElectricalIntegrity { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::wetInsulationResistance { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::wetJointIntegrity { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::wetMechanismTravel { x = 0; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 1600; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 1600; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 1600; }
    }
}
```

</details>


## Stability and capsize recovery

Capsize alone need not end the attempt. Unassisted recovery may preserve qualification if no motor or outside intervention is used and the required safety capabilities remain available. The physical test must establish the actual recovery behavior.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_environment_16::thread direction=BT statements=true
package Page_environment_16 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
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
        expose BlueDogRequirements::emergencyControl;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::capsizeResilience;
        expose BlueDogRequirements::vegetationResilience;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedSnagShedding;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        metadata Layout about BlueDogRequirements::capsizeBallastRetention { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeElectronicsSealing { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeGateProgressRetention { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::capsizeQualificationRetention { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::capsizeRestrictionRetention { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::capsizeRigRetention { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::controlRecoveryDeadline { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::rightingDeadline { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::emergencyControl { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::selfRighting { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::capsizeResilience { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::vegetationResilience { x = 160; y = 1780; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 960; y = 1600; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 2000; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 2000; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 2000; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 960; y = 2000; }
    }
}
```

</details>


## Weed tolerance

Fouling can reduce steering and recovery authority before it stops the boat completely. Detection and response therefore belong alongside the appendage and propulsor design.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_environment_17::thread direction=BT statements=true
package Page_environment_17 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
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
        expose BlueDogRequirements::emergencyControl;
        expose BlueDogRequirements::capsizeResilience;
        expose BlueDogRequirements::vegetationResilience;
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
        expose GorgeChallenge::sailingPropulsion;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::unassistedAttempt;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyAwareness { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::ingressResponse { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::lockedPropulsorShutdown { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::lowEnergyRecovery { x = 960; y = 400; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::poweredWeedCurrent { x = 640; y = 800; }
        metadata Layout about BlueDogRequirements::poweredWeedSpeed { x = 960; y = 800; }
        metadata Layout about BlueDogRequirements::poweredWeedTemperature { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::resetRecovery { x = 960; y = 1200; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::emergencyControl { x = 320; y = 1600; }
        metadata Layout about BlueDogRequirements::capsizeResilience { x = 640; y = 1600; }
        metadata Layout about BlueDogRequirements::vegetationResilience { x = 800; y = 1780; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 960; y = 1600; }
        metadata Layout about BlueDogRequirements::weedBlockageContingency { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageFault { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageLocation { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::weedPassageSpeed { x = 0; y = 2400; }
        metadata Layout about BlueDogRequirements::weedPassageSteering { x = 320; y = 2400; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 640; y = 2400; }
        metadata Layout about BlueDogRequirements::weedSnagSpeedRecovery { x = 960; y = 2400; }
        metadata Layout about BlueDogRequirements::weedSnagSteeringRecovery { x = 0; y = 2800; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 2800; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 640; y = 2800; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 960; y = 2800; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 3200; }
        metadata Layout about GorgeChallenge::unassistedAttempt { x = 320; y = 3200; }
    }
}
```

</details>

## No littering and casualty recovery

The casualty case includes flotation, retained major components and a recoverable boat. Reaching a modeled shore approach does not establish capture, retention or retrieval.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view SRR_Thread_environment::thread direction=BT statements=true
package SRR_Thread_environment {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::noLittering;
        expose GorgeChallenge::casualtyFlotation;
        expose GorgeChallenge::majorComponentRetention;
        expose GorgeChallenge::capsizeRecovery;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::noLittering { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::casualtyFlotation { x = 640; y = 0; }
        metadata Layout about GorgeChallenge::majorComponentRetention { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::capsizeRecovery { x = 320; y = 400; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
