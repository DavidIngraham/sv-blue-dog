# Manufacturing, structure and recovery

The printed prototype taught us to treat construction as part of sizing. Printed walls and ribs, wet glass/epoxy, seams and finish contribute to mass. The source CAD explores manufacturing and wing concepts; it does not define the challenge vessel.

The current stiffness calculation uses finite laminate sections from inward offsets of the actual geometry. This replaced a thin-wall approximation that could predict more stiffness than a solid section. We credit the glass laminate for bending while treating printed support, joints and attachments as separate evidence obligations.

```sysml-view Page_structures_and_recovery_0::StrengthRelationships direction=BT
package Page_structures_and_recovery_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view StrengthRelationships : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogStructure::structuralIntegrity;
        expose BlueDogStructure::bendingStrength;
        expose BlueDogStructure::panelStrength;
        expose BlueDogStructure::rootProofLoad;
        metadata Layout about BlueDogStructure::structuralIntegrity { x = 400; y = 0; }
        metadata Layout about BlueDogStructure::bendingStrength { x = 0; y = 240; }
        metadata Layout about BlueDogStructure::panelStrength { x = 400; y = 240; }
        metadata Layout about BlueDogStructure::rootProofLoad { x = 800; y = 240; }
    }
}
```

```sysml-view Page_structures_and_recovery_1::StiffnessRelationships direction=BT
package Page_structures_and_recovery_1 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view StiffnessRelationships : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogStructure::structuralIntegrity;
        expose BlueDogStructure::appendageDeflection;
        expose BlueDogStructure::hullDeflection;
        expose BlueDogStructure::panelDeflection;
        metadata Layout about BlueDogStructure::structuralIntegrity { x = 400; y = 0; }
        metadata Layout about BlueDogStructure::appendageDeflection { x = 0; y = 240; }
        metadata Layout about BlueDogStructure::hullDeflection { x = 400; y = 240; }
        metadata Layout about BlueDogStructure::panelDeflection { x = 800; y = 240; }
    }
}
```

We solve displaced volume and its centroid at a specified attitude, balance heave and pitch, then inspect full-roll restoring curves for several mast positions. Positive roll moments do not establish a dynamic recovery path, particularly on a pitch-unstable branch. Sealed, freely flooded and retained-water cases answer different questions and remain separate.

The model owns material assumptions, numerical allocations, practical handling constraints and their rationale. Wet coupons, assembly proof tests, ingress/drainage and dynamic releases must replace those assumptions with evidence before qualification.

[Sizing method](sizing.md) · [Recorded numerical evidence](results.md)
