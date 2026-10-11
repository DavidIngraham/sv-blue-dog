# S-005 RegulatoryClassification relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_s_005_0::regulatoryClassification1 direction=BT statements=true
package Page_requirements_requirements_s_005_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view regulatoryClassification1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::regulatoryClassification;
        expose BlueDogRequirements::deploymentComplianceRecord;
        expose BlueDogRequirements::deploymentReleaseGate;
        metadata Layout about BlueDogRequirements::regulatoryClassification { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::deploymentComplianceRecord { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::deploymentReleaseGate { x = 300; y = 200; }
    }
}
```
