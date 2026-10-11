# N-035 EnvelopeTransition relationships

This focused view supports [virtual design and PDR](../development-plan.md#virtual-design). It takes envelope-transition obligations and environmental limits from the authoritative model and informs detection and response behavior when operating conditions change. The relationships define the design and evidence obligations; they do not record a completed test.

[Requirement views](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_requirements_n_035_0::envelopeTransition1 direction=BT statements=true
package Page_requirements_requirements_n_035_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view envelopeTransition1 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::survivalEntryDeadline;
        expose BlueDogRequirements::survivalTransitionRecording;
        expose BlueDogRequirements::sailingResumptionDeadline;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::survivalEntryDeadline { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::survivalTransitionRecording { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::sailingResumptionDeadline { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_035_1::envelopeTransition2 direction=BT statements=true
package Page_requirements_requirements_n_035_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view envelopeTransition2 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::sailingResumptionInhibition;
        expose BlueDogRequirements::resumptionBlockEvidence;
        expose BlueDogRequirements::periodicLogCadence;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sailingResumptionInhibition { x = 0; y = 200; }
        metadata Layout about BlueDogRequirements::resumptionBlockEvidence { x = 300; y = 200; }
        metadata Layout about BlueDogRequirements::periodicLogCadence { x = 600; y = 200; }
    }
}
```

```sysml-view Page_requirements_requirements_n_035_2::envelopeTransition3 direction=BT statements=true
package Page_requirements_requirements_n_035_2 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view envelopeTransition3 : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::envelopeTransition;
        expose BlueDogRequirements::motorQualificationInvariant;
        metadata Layout about BlueDogRequirements::envelopeTransition { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::motorQualificationInvariant { x = 0; y = 200; }
    }
}
```
