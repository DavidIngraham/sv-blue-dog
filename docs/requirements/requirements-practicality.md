# Manufacturing, handling and serviceability

**Design phase:** Mission and requirements · SRR · [Development plan](../development-plan.md)

One-person handling and a 250 mm cubic printer are owner-imposed project constraints. They shape the build and maintenance approach alongside the mission goals.

[Requirements overview](../requirements.md) · [Modeling method](../methods/modeling.md)

Arrows point toward the source: **derive** identifies a derived obligation, **refine** adds precision, and **dependency** records a design basis. Each view retains its upstream context; statements are rendered from the model.

- [Construction](#construction)
- [Construction qualification](#construction-qualification)
- [Transport and handling](#transport-and-handling)
- [Serviceability](#serviceability)

## Construction

The owner-selected printer envelope and construction process are design constraints. The 230 mm structural tile allocation leaves 20 mm per axis for supports and clearance inside the 250 mm print-job envelope; it does not replace the slicer check.

```sysml-view Page_practicality_construction::thread direction=BT statements=true
package Page_practicality_construction {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        expose BlueDog::DesignIntent;
        expose BlueDogRequirements::desktopManufacture;
        expose BlueDogStructure::hybridConstruction;
        expose BlueDogStructure::printTileEnvelope;
        metadata Layout about BlueDog::DesignIntent { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::desktopManufacture { x = 400; y = 0; }
        metadata Layout about BlueDogStructure::hybridConstruction { x = 800; y = 0; }
        metadata Layout about BlueDogStructure::printTileEnvelope { x = 0; y = 400; }
    }
}
```

## Construction qualification

Wet laminate coupons and glass-to-print bonds establish whether the chosen process can carry the modeled loads. These requirements derive from structural integrity; selecting the construction process does not demonstrate compliance.

```sysml-view Page_practicality_materials::thread direction=BT statements=true
package Page_practicality_materials {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::wetMechanicalIntegrity;
        expose BlueDogStructure::structuralIntegrity;
        expose BlueDogStructure::wetCouponStrength;
        expose BlueDogStructure::wetCouponStiffness;
        expose BlueDogStructure::bondProof;
        metadata Layout about BlueDogRequirements::wetMechanicalIntegrity { x = 0; y = 0; }
        metadata Layout about BlueDogStructure::structuralIntegrity { x = 400; y = 0; }
        metadata Layout about BlueDogStructure::wetCouponStrength { x = 800; y = 0; }
        metadata Layout about BlueDogStructure::wetCouponStiffness { x = 0; y = 400; }
        metadata Layout about BlueDogStructure::bondProof { x = 400; y = 400; }
    }
}
```

[Structural load and deflection requirements](../structures-and-recovery.md)

<a id="transport-and-manufacture"></a>

## Transport and handling

```sysml-view Page_practicality_23::thread direction=BT statements=true
package Page_practicality_23 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::liftMass;
        expose BlueDogRequirements::packDuration;
        expose BlueDogRequirements::setupDuration;
        expose BlueDogRequirements::soloLaunch;
        expose BlueDogRequirements::soloRetrieval;
        expose BlueDogRequirements::soloTransport;
        expose BlueDogRequirements::transportability;
        metadata Layout about BlueDogRequirements::liftMass { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::packDuration { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::setupDuration { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::soloLaunch { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::soloRetrieval { x = 0; y = 400; }
        metadata Layout about BlueDogRequirements::soloTransport { x = 320; y = 400; }
        metadata Layout about BlueDogRequirements::transportability { x = 640; y = 400; }
    }
}
```


## Serviceability

```sysml-view Page_practicality_24::thread direction=BT statements=true
package Page_practicality_24 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::nondestructiveService;
        expose BlueDogRequirements::postServiceActuation;
        expose BlueDogRequirements::postServiceSealing;
        expose BlueDogRequirements::replacementDuration;
        expose BlueDogRequirements::serviceability;
        metadata Layout about BlueDogRequirements::nondestructiveService { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::postServiceActuation { x = 320; y = 0; }
        metadata Layout about BlueDogRequirements::postServiceSealing { x = 640; y = 0; }
        metadata Layout about BlueDogRequirements::replacementDuration { x = 960; y = 0; }
        metadata Layout about BlueDogRequirements::serviceability { x = 0; y = 400; }
    }
}
```
