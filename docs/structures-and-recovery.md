# Manufacturing, structure and recovery

Can I manufacture the boat this way without making it too heavy—and will it come back upright? I use the candidate geometry, printed construction, glass laminate and flooding assumptions to connect [sizing](development-plan.md#virtual-design) with [detailed design](development-plan.md#detailed-design). Coupon and recovery experiments will decide how much confidence those calculations deserve.

Working through the testbed design made construction part of the sizing problem. Printed walls and ribs, wet glass/epoxy, seams and finish contribute to mass. The source CAD explores manufacturing and wing concepts; it does not define the challenge vessel.

![Construction section: a glass and epoxy skin surrounds the printed support and hollow interior. Joints and attachments need their own load evidence.](figures/laminate-section.svg)

*The sketch shows the construction idea, not specified layer thicknesses. I count both skin and printed support in mass, while the bending calculation credits the finite glass laminate section.*

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

![Recovery concepts: a sealed wing retains air volume, a freely flooded wing exchanges water, and a water-retaining wing carries trapped water. Roll restoration and pitch stability must both be assessed.](figures/recovery-states.svg)

*A wing that helps when sealed can behave very differently after ingress. Coming upright in roll is only part of recovery: an unstable pitch equilibrium still prevents a self-righting claim.*

The sizing search uses a coarse fixed-pitch recovery screen alongside sailing, structure and energy constraints. We then solve displaced volume and its centroid at a specified attitude, balance heave and pitch, and inspect full-roll restoring curves for several mast positions at the selected geometry. Positive roll moments do not establish a dynamic recovery path, particularly on a pitch-unstable branch. Sealed, freely flooded and retained-water cases answer different questions and remain separate. Restricting sailing heel in the aerodynamic policy does not restrict the full-roll recovery assessment or relax its requirements.

The current trial has positive sealed-wing roll samples but includes pitch-unstable equilibria, so it has not demonstrated self-righting. It also loses positive sampled restoring behavior when the wing is freely flooded or retains water. Sealed-wing roll results cannot stand in for ingress tolerance. The native summary below combines the four locked mast positions for each state and water density; negative restoring moments and unstable pitch samples remain visible.

```sysml-report BlueDogEvidenceDocuments::Recovery
```

The model owns material assumptions, numerical allocations, practical handling constraints and their rationale. Wet coupons, assembly proof tests, ingress/drainage and dynamic releases must replace those assumptions with evidence before qualification.

[Sizing method](sizing.md) · [Recorded numerical evidence](results.md)


**Next:** [Passage time and reliability](reliability.md).
