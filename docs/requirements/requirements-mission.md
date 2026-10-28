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
        expose BlueDogRequirements::emergencyControl;
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
        metadata Layout about BlueDogRequirements::emergencyControl { x = 960; y = 1200; }
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
        expose BlueDogRequirements::emergencyControl;
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
        metadata Layout about BlueDogRequirements::emergencyControl { x = 640; y = 1200; }
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

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
