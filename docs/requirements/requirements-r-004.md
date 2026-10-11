# R-004 ChallengeMotorInhibition relationships

This focused view supports [detailed design and build readiness](../development-plan.md#detailed-design). It takes challenge motor-inhibition obligations and propulsion rules from the authoritative model and informs mode interlocks and tests separating qualifying sailing from powered recovery. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_r_004_0::challengeMotorInhibition1 direction=BT statements=true
package Page_requirements_requirements_r_004_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view challengeMotorInhibition1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::motorQualificationInvariant;
        expose BlueDogRequirements::freshRecoveryCommand;
        expose BlueDogRequirements::qualificationPersistence;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::freshRecoveryCommand { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::qualificationPersistence { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_r_004_1::challengeMotorInhibition2 direction=BT statements=true
package Page_requirements_requirements_r_004_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view challengeMotorInhibition2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::challengeMotorInhibition;
        expose BlueDogRequirements::criticalEventRecording;
        metadata Layout about BlueDogRequirements::challengeMotorInhibition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::criticalEventRecording { x = 0; y = 200; }
    }
}
```
