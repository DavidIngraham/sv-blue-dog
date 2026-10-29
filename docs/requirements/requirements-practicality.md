# Manufacturing, handling and serviceability

[Requirements overview](../requirements.md) · [Current assessment](../current-assessment.md)

I want to manufacture, transport, assemble, launch and retrieve the boat myself. Printed parts must fit my 250 × 250 × 250 mm printer; assembled structures may be larger. Those owner constraints shape the construction and handling of the intended IC-01-scale first build.

## Construction

The owner-selected printer envelope and construction process are design constraints. The sizing study assumes 230 mm tiles for seams and mass. Actual tiles may be larger when their complete print job, including supports and clearance, fits the owner-selected 250 mm cube.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_practicality_construction::thread direction=BT statements=true
package Page_practicality_construction {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        expose BlueDog::DesignIntent;
        expose BlueDog::Requirements::desktopManufacture;
        expose BlueDog::Requirements::Structure::hybridConstruction;
        expose BlueDog::Requirements::Structure::printTileEnvelope;
        metadata Layout about BlueDog::DesignIntent { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::desktopManufacture { x = 400; y = 0; }
        metadata Layout about BlueDog::Requirements::Structure::hybridConstruction { x = 800; y = 0; }
        metadata Layout about BlueDog::Requirements::Structure::printTileEnvelope { x = 0; y = 400; }
    }
}
```

The structural tile envelope refines the same owner printer limit; its verification also requires an accepted build configuration.

```sysml-view Page_practicality_printEnvelope::thread direction=BT statements=true
package Page_practicality_printEnvelope {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::desktopManufacture;
        expose BlueDog::Requirements::Structure::printTileEnvelope;
        metadata Layout about BlueDog::Requirements::desktopManufacture { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::Structure::printTileEnvelope { x = 0; y = 300; }
    }
}
```
</details>

## Construction qualification

Load, deflection, wet laminate coupon and glass-to-print bond criteria establish whether the chosen process can carry the modeled loads. These requirements derive from structural integrity; selecting the construction process does not demonstrate compliance. Material strength and stiffness are qualified inputs, not fixed minimum targets. Functional deformation limits require evidence; the preliminary sizing percentages do not close these requirements. See [requirements versus design assumptions](../methods/modeling.md#requirements-versus-design-assumptions).

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_practicality_materials::thread direction=BT statements=true
package Page_practicality_materials {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDog::Requirements::roundTrip;
        expose BlueDog::Requirements::environmentalEnvelope;
        expose BlueDog::Requirements::marineDurability;
        expose BlueDog::Requirements::wetMechanicalIntegrity;
        expose BlueDog::Requirements::Structure::structuralIntegrity;
        expose BlueDog::Requirements::Structure::wetCouponStrength;
        expose BlueDog::Requirements::Structure::wetCouponStiffness;
        expose BlueDog::Requirements::Structure::bondProof;
        expose BlueDog::Requirements::Structure::bendingStrength;
        expose BlueDog::Requirements::Structure::appendageDeflection;
        expose BlueDog::Requirements::Structure::hullDeflection;
        expose BlueDog::Requirements::Structure::panelStrength;
        expose BlueDog::Requirements::Structure::panelDeflection;
        expose BlueDog::Requirements::Structure::rootProofLoad;
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::roundTrip { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::environmentalEnvelope { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::marineDurability { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::wetMechanicalIntegrity { x = 640; y = 400; }
        metadata Layout about BlueDog::Requirements::Structure::structuralIntegrity { x = 960; y = 400; }
        metadata Layout about BlueDog::Requirements::Structure::wetCouponStrength { x = 0; y = 800; }
        metadata Layout about BlueDog::Requirements::Structure::wetCouponStiffness { x = 320; y = 800; }
        metadata Layout about BlueDog::Requirements::Structure::bondProof { x = 640; y = 800; }
        metadata Layout about BlueDog::Requirements::Structure::bendingStrength { x = 960; y = 800; }
        metadata Layout about BlueDog::Requirements::Structure::appendageDeflection { x = 0; y = 1200; }
        metadata Layout about BlueDog::Requirements::Structure::hullDeflection { x = 320; y = 1200; }
        metadata Layout about BlueDog::Requirements::Structure::panelStrength { x = 640; y = 1200; }
        metadata Layout about BlueDog::Requirements::Structure::panelDeflection { x = 960; y = 1200; }
        metadata Layout about BlueDog::Requirements::Structure::rootProofLoad { x = 0; y = 1600; }
    }
}
```

</details>

[Structural load and deflection requirements](../structures-and-recovery.md)

<a id="transport-and-manufacture"></a>

## Transport and handling

Assess the assembled mass, component breakdown and handling aids together. One-person operation must work at the actual launch and retrieval sites, not only in the workshop.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_practicality_23::thread direction=BT statements=true
package Page_practicality_23 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::liftMass;
        expose BlueDog::Requirements::packDuration;
        expose BlueDog::Requirements::setupDuration;
        expose BlueDog::Requirements::soloLaunch;
        expose BlueDog::Requirements::soloRetrieval;
        expose BlueDog::Requirements::soloTransport;
        expose BlueDog::Requirements::transportability;
        metadata Layout about BlueDog::Requirements::liftMass { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::packDuration { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::setupDuration { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::soloLaunch { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::soloRetrieval { x = 0; y = 400; }
        metadata Layout about BlueDog::Requirements::soloTransport { x = 320; y = 400; }
        metadata Layout about BlueDog::Requirements::transportability { x = 640; y = 400; }
    }
}
```

</details>


## Serviceability

Inspection, repair and replacement need accessible interfaces. Those practical tasks belong in the design before the sealed installation is built.

<details>
<summary>Model relationships and authoritative requirement statements</summary>

```sysml-view Page_practicality_24::thread direction=BT statements=true
package Page_practicality_24 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Requirements::nondestructiveService;
        expose BlueDog::Requirements::postServiceActuation;
        expose BlueDog::Requirements::postServiceSealing;
        expose BlueDog::Requirements::replacementDuration;
        expose BlueDog::Requirements::serviceability;
        metadata Layout about BlueDog::Requirements::nondestructiveService { x = 0; y = 0; }
        metadata Layout about BlueDog::Requirements::postServiceActuation { x = 320; y = 0; }
        metadata Layout about BlueDog::Requirements::postServiceSealing { x = 640; y = 0; }
        metadata Layout about BlueDog::Requirements::replacementDuration { x = 960; y = 0; }
        metadata Layout about BlueDog::Requirements::serviceability { x = 0; y = 400; }
    }
}
```

</details>

**Continue:** [Candidate results](../results.md), or return to the [requirements overview](../requirements.md).
