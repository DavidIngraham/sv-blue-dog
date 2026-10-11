# Passage time, reliability and failure analysis

A slower voyage demands more hours of successful unattended operation. We therefore connect sailing progress, passage duration and reliability exposure rather than assigning reliability independently of the mission.

```sysml-view Page_reliability_0::CruiseSemantics direction=BT
package Page_reliability_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view CruiseSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::cruisePerformance;
        expose BlueDogRequirements::legProgress;
        expose BlueDogRequirements::LegProgressCriterion;
        expose BlueDogReliability::VoyageReliabilityVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about BlueDogRequirements::cruisePerformance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::legProgress { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::LegProgressCriterion { x = 0; y = 200; }
        metadata Layout about BlueDogReliability::VoyageReliabilityVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
}
```

```sysml-view Page_reliability_1::ReliabilitySemantics direction=BT
package Page_reliability_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view ReliabilitySemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::missionReliability;
        expose BlueDogRequirements::missionSuccessProbability;
        expose BlueDogRequirements::MissionReliabilityCriterion;
        expose BlueDogReliability::VoyageReliabilityVerification;
        expose BlueDog::Architecture::missionContext::boat;
        metadata Layout about BlueDogRequirements::missionReliability { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::missionSuccessProbability { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::MissionReliabilityCriterion { x = 0; y = 200; }
        metadata Layout about BlueDogReliability::VoyageReliabilityVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 0; y = 400; }
    }
}
```

The DFMEA links functional failure modes to architecture responsibilities, requirements and needed evidence. Its concerns guide design and tests; they are not fabricated failure probabilities. Numerical rate-budget examples remain conditional on their assumptions and evidence disposition.

Weed contact is a concrete operating interaction. It affects both the sailing appendages and recovery propulsion, so loss of speed, steering and recovery capability are assessed separately.

```sysml-view Page_reliability_2::WeedSemantics direction=BT
package Page_reliability_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view WeedSemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedPassageSpeed;
        expose BlueDogRequirements::weedPassageSteering;
        expose BlueDog::Architecture::missionContext::boat;
        expose BlueDogRequirementVerification::SubmergedWeedPassageVerification;
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::weedPassageSpeed { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::weedPassageSteering { x = 0; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat { x = 360; y = 200; }
        metadata Layout about BlueDogRequirementVerification::SubmergedWeedPassageVerification { x = 0; y = 400; }
    }
}
```

The [DFMEA model](../models/analyses/dfmea.sysml) owns the failure hypotheses, effects, proposed actions and architecture/requirement dependencies. The [reliability analysis](../models/analyses/reliability.sysml) owns the exposure calculation and evidence gates. Neither an open DFMEA action nor a synthetic rate estimate establishes achieved reliability.
