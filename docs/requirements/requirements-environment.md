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
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::freshwaterExposure;
        expose BlueDog::Requirements::gorgeCurrent;
        expose BlueDog::Requirements::gorgeEnvironment;
        expose BlueDog::Requirements::gorgeSurvivalWaves;
        expose BlueDog::Requirements::gorgeSurvivalWind;
        expose BlueDog::Requirements::gorgeWaves;
        expose BlueDog::Requirements::gorgeWind;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::marineDurability;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::motorQualificationInvariant;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::periodicLogCadence;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::resumptionBlockEvidence;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::sailingResumptionDeadline;
        expose BlueDog::Requirements::sailingResumptionInhibition;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::submergedWeedPassage;
        expose BlueDog::Requirements::survivalEntryDeadline;
        expose BlueDog::Requirements::survivalTransitionRecording;
        expose BlueDog::Requirements::weedBlockageResponse;
        expose BlueDog::Requirements::weedSnagShedding;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::emergencyIntervention;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::envelopeTransition { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::freshwaterExposure { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::gorgeCurrent { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::gorgeEnvironment { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::gorgeSurvivalWaves { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::gorgeSurvivalWind { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::gorgeWaves { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::gorgeWind { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::marineDurability { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::motorQualificationInvariant { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::periodicLogCadence { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::resumptionBlockEvidence { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 640; y = 2000; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 960; y = 2000; }
        metadata Layout about BlueDog::Requirements::sailingResumptionDeadline { x = 0; y = 2400; }
        metadata Layout about BlueDog::Requirements::sailingResumptionInhibition { x = 320; y = 2400; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 640; y = 2400; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 800; y = 2580; }
        metadata Layout about BlueDog::Requirements::submergedWeedPassage { x = 960; y = 2400; }
        metadata Layout about BlueDog::Requirements::survivalEntryDeadline { x = 0; y = 2800; }
        metadata Layout about BlueDog::Requirements::survivalTransitionRecording { x = 320; y = 2800; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 640; y = 2800; }
        metadata Layout about BlueDog::Requirements::weedSnagShedding { x = 960; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 0; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 320; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 640; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 960; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 0; y = 3600; }
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
        expose BlueDog::Requirements::airTemperature;
        expose BlueDog::Requirements::calmOperation;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::humidity;
        expose BlueDog::Requirements::marineDurability;
        expose BlueDog::Requirements::restrictedVisibilityCollisionAssessment;
        expose BlueDog::Requirements::restrictedVisibilityEntry;
        expose BlueDog::Requirements::restrictedVisibilityEvidence;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::visibility;
        expose BlueDog::Requirements::visibilityNavigationCapability;
        expose BlueDog::Requirements::visibilityTrafficCapability;
        expose BlueDog::Requirements::waterTemperature;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        metadata Layout about BlueDog::Requirements::airTemperature { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::calmOperation { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::envelopeTransition { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::humidity { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::marineDurability { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::restrictedVisibilityCollisionAssessment { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::restrictedVisibilityEntry { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::restrictedVisibilityEvidence { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 800; y = 980; }
        metadata Layout about BlueDog::Requirements::visibility { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::visibilityNavigationCapability { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::visibilityTrafficCapability { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::waterTemperature { x = 640; y = 1200; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 960; y = 1200; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 0; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 320; y = 1600; }
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
        expose BlueDog::Requirements::oceanCurrent;
        expose BlueDog::Requirements::oceanEnvironment;
        expose BlueDog::Requirements::oceanSurvivalWaves;
        expose BlueDog::Requirements::oceanSurvivalWind;
        expose BlueDog::Requirements::oceanWaves;
        expose BlueDog::Requirements::oceanWind;
        expose BlueDog::Requirements::saltwaterExposure;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::oceanCurrent { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::oceanEnvironment { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::oceanSurvivalWaves { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::oceanSurvivalWind { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::oceanWaves { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::oceanWind { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::saltwaterExposure { x = 640; y = 800; }
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
        expose BlueDog::Requirements::batteryChargeTemperatureInhibition;
        expose BlueDog::Requirements::enclosureSealing;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::freshwaterExposure;
        expose BlueDog::Requirements::gorgeEnvironment;
        expose BlueDog::Requirements::hotSunBatteryTemperature;
        expose BlueDog::Requirements::hotSunElectronicsOperation;
        expose BlueDog::Requirements::marineDurability;
        expose BlueDog::Requirements::printedMaterialAging;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::solarHeating;
        expose BlueDog::Requirements::wetConductorResistance;
        expose BlueDog::Requirements::wetElectricalIntegrity;
        expose BlueDog::Requirements::wetInsulationResistance;
        expose BlueDog::Requirements::wetJointIntegrity;
        expose BlueDog::Requirements::wetMechanicalIntegrity;
        expose BlueDog::Requirements::wetMechanismTravel;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        metadata Layout about BlueDog::Requirements::batteryChargeTemperatureInhibition { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::enclosureSealing { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::freshwaterExposure { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::gorgeEnvironment { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::hotSunBatteryTemperature { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::hotSunElectronicsOperation { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::marineDurability { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::printedMaterialAging { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::solarHeating { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::wetConductorResistance { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::wetElectricalIntegrity { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::wetInsulationResistance { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::wetJointIntegrity { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::wetMechanicalIntegrity { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::wetMechanismTravel { x = 0; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 320; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 640; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 960; y = 1600; }
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
        expose BlueDog::Requirements::capsizeBallastRetention;
        expose BlueDog::Requirements::capsizeControlRecovery;
        expose BlueDog::Requirements::capsizeElectronicsSealing;
        expose BlueDog::Requirements::capsizeGateProgressRetention;
        expose BlueDog::Requirements::capsizeQualificationRetention;
        expose BlueDog::Requirements::capsizeRestrictionRetention;
        expose BlueDog::Requirements::capsizeRigRetention;
        expose BlueDog::Requirements::controlRecoveryDeadline;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::gorgeEnvironment;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::rightingDeadline;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::selfRighting;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::submergedWeedPassage;
        expose BlueDog::Requirements::weedBlockageResponse;
        expose BlueDog::Requirements::weedSnagShedding;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::emergencyIntervention;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        metadata Layout about BlueDog::Requirements::capsizeBallastRetention { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::capsizeControlRecovery { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::capsizeElectronicsSealing { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::capsizeGateProgressRetention { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::capsizeQualificationRetention { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::capsizeRestrictionRetention { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::capsizeRigRetention { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::controlRecoveryDeadline { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::gorgeEnvironment { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::rightingDeadline { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::selfRighting { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 160; y = 1780; }
        metadata Layout about BlueDog::Requirements::submergedWeedPassage { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::weedSnagShedding { x = 960; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 0; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 320; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 640; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 960; y = 2000; }
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
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::envelopeTransition;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::gorgeEnvironment;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::lockedPropulsorShutdown;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::motorQualificationInvariant;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::poweredWeedCurrent;
        expose BlueDog::Requirements::poweredWeedSpeed;
        expose BlueDog::Requirements::poweredWeedTemperature;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::recoveryPropulsorWeeds;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::capsizeResilience;
        expose BlueDog::Requirements::vegetationResilience;
        expose BlueDog::Requirements::submergedWeedPassage;
        expose BlueDog::Requirements::weedBlockageContingency;
        expose BlueDog::Requirements::weedBlockageFault;
        expose BlueDog::Requirements::weedBlockageLocation;
        expose BlueDog::Requirements::weedBlockageResponse;
        expose BlueDog::Requirements::weedPassageSpeed;
        expose BlueDog::Requirements::weedPassageSteering;
        expose BlueDog::Requirements::weedSnagShedding;
        expose BlueDog::Requirements::weedSnagSpeedRecovery;
        expose BlueDog::Requirements::weedSnagSteeringRecovery;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::emergencyIntervention;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::envelopeTransition { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::gorgeEnvironment { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::lockedPropulsorShutdown { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::motorQualificationInvariant { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::poweredWeedCurrent { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::poweredWeedSpeed { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::poweredWeedTemperature { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsorWeeds { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 320; y = 1600; }
        metadata Layout about BlueDog::Requirements::capsizeResilience { x = 640; y = 1600; }
        metadata Layout about BlueDog::Requirements::vegetationResilience { x = 800; y = 1780; }
        metadata Layout about BlueDog::Requirements::submergedWeedPassage { x = 960; y = 1600; }
        metadata Layout about BlueDog::Requirements::weedBlockageContingency { x = 0; y = 2000; }
        metadata Layout about BlueDog::Requirements::weedBlockageFault { x = 320; y = 2000; }
        metadata Layout about BlueDog::Requirements::weedBlockageLocation { x = 640; y = 2000; }
        metadata Layout about BlueDog::Requirements::weedBlockageResponse { x = 960; y = 2000; }
        metadata Layout about BlueDog::Requirements::weedPassageSpeed { x = 0; y = 2400; }
        metadata Layout about BlueDog::Requirements::weedPassageSteering { x = 320; y = 2400; }
        metadata Layout about BlueDog::Requirements::weedSnagShedding { x = 640; y = 2400; }
        metadata Layout about BlueDog::Requirements::weedSnagSpeedRecovery { x = 960; y = 2400; }
        metadata Layout about BlueDog::Requirements::weedSnagSteeringRecovery { x = 0; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 320; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 640; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 960; y = 2800; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 0; y = 3200; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 320; y = 3200; }
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
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::noLittering;
        expose BlueDog::Mission::Challenge::casualtyFlotation;
        expose BlueDog::Mission::Challenge::majorComponentRetention;
        expose BlueDog::Mission::Challenge::capsizeRecovery;
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::noLittering { x = 320; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::casualtyFlotation { x = 640; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::majorComponentRetention { x = 0; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::capsizeRecovery { x = 320; y = 400; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
