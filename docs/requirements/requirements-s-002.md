# S-002 OperatingBoundary relationships

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_s_002_0::operatingBoundary1 direction=BT statements=true
package Page_requirements_requirements_s_002_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view operatingBoundary1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::boundaryEvaluationCadence;
        expose BlueDogRequirements::boundaryAvoidanceDeadline;
        expose BlueDogRequirements::boundaryAvoidanceRecording;
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryEvaluationCadence { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceDeadline { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryAvoidanceRecording { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_s_002_1::operatingBoundary2 direction=BT statements=true
package Page_requirements_requirements_s_002_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view operatingBoundary2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::operatingBoundary;
        expose BlueDogRequirements::boundaryStartInhibition;
        expose BlueDogRequirements::boundaryDegradedEvidence;
        metadata Layout about BlueDogRequirements::operatingBoundary { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::boundaryStartInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::boundaryDegradedEvidence { x = 300; y = 200; }
    }
}
```
