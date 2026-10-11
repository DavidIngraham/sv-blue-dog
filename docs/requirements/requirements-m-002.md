# M-002 MultiDayEndurance relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes multi-day endurance obligations and their supporting requirements from the authoritative model and informs mission duration, energy management and integrated endurance test planning. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_m_002_0::multiDayEndurance1 direction=BT statements=true
package Page_requirements_requirements_m_002_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view multiDayEndurance1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::peakSupplyCapability;
        expose BlueDogRequirements::harvestCampaignCoverage;
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::peakSupplyCapability { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::harvestCampaignCoverage { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_m_002_1::multiDayEndurance2 direction=BT statements=true
package Page_requirements_requirements_m_002_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view multiDayEndurance2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::multiDayEndurance;
        expose BlueDogRequirements::energyEvidenceReadiness;
        metadata Layout about BlueDogRequirements::multiDayEndurance { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::energyEvidenceReadiness { x = 0; y = 200; }
    }
}
```
