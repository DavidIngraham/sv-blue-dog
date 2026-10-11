# N-001 EnvironmentalEnvelope relationships

This focused view supports [mission definition and SRR](../development-plan.md#mission-definition). It takes the environmental-envelope obligation and its parameter-specific requirements from the authoritative model and informs simulation conditions and the environments against which the vessel must later be tested. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_001_0::environmentalEnvelope1 direction=BT statements=true
package Page_requirements_requirements_n_001_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view environmentalEnvelope1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::airTemperature;
        expose BlueDogRequirements::waterTemperature;
        expose BlueDogRequirements::humidity;
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::airTemperature { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::waterTemperature { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::humidity { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_001_1::environmentalEnvelope2 direction=BT statements=true
package Page_requirements_requirements_n_001_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view environmentalEnvelope2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::visibility;
        expose BlueDogRequirements::calmOperation;
        expose BlueDogRequirements::envelopeTransition;
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::visibility { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::calmOperation { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 600; y = 200; }
    }
}
```
