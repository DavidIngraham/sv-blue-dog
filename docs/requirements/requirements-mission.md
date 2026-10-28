# Mission, course completion and endurance

[Requirements overview](../requirements.md) · [Current assessment](../current-assessment.md)

The job is a finite, unassisted round trip from Bingen around Buoy 16 near Stevenson and back under sail. Course completion depends on progress over the ground, allowed launch conditions and preserved qualification throughout the attempt. These requirements define success before I choose a hull, rig or battery.

## Mission and challenge rules

The course, length limit, propulsion and independence rules define the attempt. A convenient implementation cannot redefine those conditions.

C-007 explicitly requires the U.S. Inland Navigation Rules and applicable local navigation provisions for the approved course. The organizer reviews the governing rule and notice baseline, each entrant's applicability assessment and evidence for the admitted conditions. Entrants justify their own sensing distances, margins and maneuver capability.

A collision, established rule breach or unsafe conduct requiring safety intervention disqualifies the attempt. Operator intervention or motor propulsion also ends qualification when used for safety. Compliant autonomous avoidance can preserve qualification; missing evidence leaves the outcome unconfirmed. Safety action must never wait to protect a score. The [navigation compliance assessment](../validation-plan.md#navigation-rule-entry-review-and-adjudication) connects the legal sources to planned model verification cases.


<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_mission_0::thread direction=BT statements=true
package Page_mission_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::challengeMotorInhibition;
        expose BlueDog::Requirements::commandIntegrity;
        expose BlueDog::Requirements::communications;
        expose BlueDog::Requirements::cruisePerformance;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::gorgeEnvironment;
        expose BlueDog::Requirements::ingressResponse;
        expose BlueDog::Requirements::missionEvidence;
        expose BlueDog::Requirements::missionReliability;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::operatingBoundary;
        expose BlueDog::Mission::Challenge::restrictedWaters;
        expose BlueDog::Requirements::regulatoryClassification;
        expose BlueDog::Requirements::resetRecovery;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::serviceability;
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
        metadata Layout about BlueDog::Requirements::cruisePerformance { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::gorgeEnvironment { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::ingressResponse { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::missionEvidence { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::missionReliability { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::operatingBoundary { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::regulatoryClassification { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::resetRecovery { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::serviceability { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::windObservation { x = 320; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 640; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 960; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::liveObservation { x = 0; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 320; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 640; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 960; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::restrictedWaters { x = 0; y = 2400; }
    }
}
```

</details>


## Endurance and cruise performance

The finite passage needs enough energy for its duration and delays, with protected recovery reserve. There is no fixed 72-hour deadline, daily energy-neutrality requirement or sailing-speed floor for this mission.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_mission_1::thread direction=BT statements=true
package Page_mission_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::cruiseEvidence;
        expose BlueDog::Requirements::cruisePerformance;
        expose BlueDog::Requirements::energyAwareness;
        expose BlueDog::Requirements::energyEvidenceReadiness;
        expose BlueDog::Requirements::legProgress;
        expose BlueDog::Requirements::lowEnergyRecovery;
        expose BlueDog::Requirements::multiDayEndurance;
        expose BlueDog::Requirements::navigationAndControl;
        expose BlueDog::Requirements::passageDuration;
        expose BlueDog::Requirements::peakSupplyCapability;
        expose BlueDog::Requirements::recoveryEnergy;
        expose BlueDog::Requirements::recoveryPropulsion;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::emergencyControl;
        expose BlueDog::Requirements::sustainedReserveProtection;
        expose BlueDog::Requirements::windObservation;
        expose BlueDog::Requirements::windSensingEndurance;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::emergencyIntervention;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::unassistedAttempt;
        metadata Layout about BlueDog::Requirements::cruiseEvidence { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::cruisePerformance { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::energyAwareness { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::energyEvidenceReadiness { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::legProgress { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::lowEnergyRecovery { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::multiDayEndurance { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::navigationAndControl { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::passageDuration { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::peakSupplyCapability { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::recoveryEnergy { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::recoveryPropulsion { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::emergencyControl { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::sustainedReserveProtection { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::windObservation { x = 0; y = 1600; }
        metadata Layout about BlueDog::Requirements::windSensingEndurance { x = 320; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 640; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::emergencyIntervention { x = 960; y = 1600; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 0; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 320; y = 2000; }
        metadata Layout about BlueDog::Mission::Challenge::unassistedAttempt { x = 640; y = 2000; }
    }
}
```

</details>


## Mission reliability

I use L-101 and L-102 as provisional study objectives for mission success probability and combined failure rate. They do not set launch or mission-acceptance thresholds. L-103 requires evidence for the reliability estimate, and L-104 requires a disposition for critical failures and residual risk. Synthetic completion fractions do not establish real-world reliability.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_mission_2::thread direction=BT statements=true
package Page_mission_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::criticalFailureDisposition;
        expose BlueDog::Requirements::failureRateBudget;
        expose BlueDog::Requirements::missionReliability;
        expose BlueDog::Requirements::missionSuccessProbability;
        expose BlueDog::Requirements::reliabilityEvidence;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Mission::Challenge::courseCompletion;
        expose BlueDog::Mission::Challenge::sailingPropulsion;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        metadata Layout about BlueDog::Requirements::criticalFailureDisposition { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::failureRateBudget { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::missionReliability { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::missionSuccessProbability { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::reliabilityEvidence { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 320; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::courseCompletion { x = 640; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::sailingPropulsion { x = 960; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 0; y = 800; }
    }
}
```

</details>

## Qualification and launch admission

Launch admission must consider the forecast and the boat’s supported capability. Safe waiting can preserve qualification; refuge, grounding, anchoring, intervention or recovery propulsion ends it.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view SRR_Thread_mission::thread direction=BT statements=true
package SRR_Thread_mission {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Mission::Challenge::transGorgeChallenge;
        expose BlueDog::Mission::Challenge::overallLength;
        expose BlueDog::Mission::Challenge::unattachedPassage;
        expose BlueDog::Mission::Challenge::abortPersistence;
        expose BlueDog::Mission::Challenge::nightOperation;
        expose BlueDog::Mission::Challenge::forecastAdmission;
        metadata Layout about BlueDog::Mission::Challenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::overallLength { x = 320; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::unattachedPassage { x = 640; y = 0; }
        metadata Layout about BlueDog::Mission::Challenge::abortPersistence { x = 0; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::nightOperation { x = 320; y = 400; }
        metadata Layout about BlueDog::Mission::Challenge::forecastAdmission { x = 640; y = 400; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
