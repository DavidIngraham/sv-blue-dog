# Manufacturing, structure and recovery

Can I manufacture the boat this way without making it too heavy—and will it come back upright? I use the candidate geometry, printed construction, glass laminate and flooding assumptions to connect [sizing](development-plan.md#virtual-design) with [detailed design](development-plan.md#detailed-design). Coupon and recovery experiments will decide how much confidence those calculations deserve.

Working through the testbed design made construction part of the sizing problem. Printed walls and ribs, wet glass/epoxy, seams and finish contribute to mass. The source CAD explores manufacturing and wing concepts; it does not define the challenge vessel.

![SolidWorks rendering of the original testbed, showing the wing's internal structure and the hull, drive, keel and ballast arrangement.](figures/testbed-solidworks.png)

The [weather-window mission](operating-constraints.md#gorge-weather-and-launch-windows) changes which sailing performance we emphasize, not the need to withstand loads or recover from a capsize. We keep those screens as hard constraints. Winter trials also need material, sealing and recovery evidence applicable to their temperature and weather conditions.

![Construction section: a glass and epoxy skin surrounds the printed support and hollow interior.](figures/laminate-section.svg)

*Glass and epoxy form the outer skin around printed walls and ribs. The mass model includes both; the bending model credits the glass laminate.*

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

![Recovery concepts: a sealed wing retains air volume, a freely flooded wing exchanges water, and a water-retaining wing carries trapped water.](figures/recovery-states.svg)

*Water ingress changes the wing’s buoyancy and carried mass. Recovery depends on both roll restoration and pitch stability.*

The sizing search uses a coarse fixed-pitch recovery screen alongside sailing, structure and energy constraints. We then solve displaced volume and its centroid at a specified attitude, balance heave and pitch, and inspect full-roll restoring curves for several mast positions at the selected geometry. Positive roll moments do not establish a dynamic recovery path, particularly on a pitch-unstable branch. Sealed, freely flooded and retained-water cases answer different questions and remain separate. Restricting sailing heel in the aerodynamic policy does not restrict the full-roll recovery assessment or relax its requirements.

The smaller finite-passage candidates are checked separately from the older full-curve study. Their current sealed-wing probe samples six roll angles at four locked mast positions and records pitch stability as well as restoring direction. See the [current sizing results](results.md) for those outcomes and the material-stiffness sensitivity. Positive roll restoration alone has not established self-righting.

The following archived 2.009 m reference study covers sealed, freely flooded and retained-water states in fresh and salt water. It contains pitch-unstable equilibria and adverse flooded-wing restoring samples. These are historical sensitivity results, not a replay of the smaller candidate; sealed-wing results cannot establish ingress tolerance.

```sysml-report BlueDogEvidenceDocuments::Recovery
```

<details>
<summary>Archived full recovery curves for the 2.009 m reference</summary>

![Restoring moment versus heel for the archived 2.009 m reference, comparing sealed, freely flooded and water-retaining wing states. Crosses mark pitch-unstable equilibria.](figures/coupled-recovery.svg)

</details>

The model owns material assumptions, numerical allocations, practical handling constraints and their rationale. Wet coupons, assembly proof tests, ingress/drainage and dynamic releases must replace those assumptions with evidence before qualification.

[Sizing method](sizing.md) · [Recorded numerical evidence](results.md)


**Next:** [Passage time and reliability](reliability.md).
