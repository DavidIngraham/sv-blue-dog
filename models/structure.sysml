package BlueDogStructure {
    private import ScalarValues::*;
    private import RequirementDerivation::*;
    doc /* Owner-selected FDM plus wet-layup construction. Numerical targets are
     * proposed allocations with open evidence, not certified scantlings. */
    requirement def <'T-001'> HybridConstruction {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The primary shell structure shall use an FDM substrate with wet-layup glass/epoxy reinforcement. */
        comment conditions /* Owner-selected construction architecture. PETG is the initial candidate, not a qualified material. */
        metadata rationale : ModelingMetadata::Rationale { text = "Owner-selected construction architecture. PETG is the initial candidate, not a qualified material."; }
    }
    requirement hybridConstruction : HybridConstruction;
    dependency basisHybridConstruction from hybridConstruction to BlueDog::DesignIntent { metadata rationale : ModelingMetadata::Rationale { text = "Selected design allocation; the numerical value is not logically implied by the parent requirement."; } }
    requirement def <'T-100'> StructuralIntegrity {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The primary structure shall carry its declared limit loads throughout the specified wet exposure. */
        comment conditions /* Apply T-101 through T-109 independently. Current screening allocations do not cover impact, fatigue, buckling or qualified adhesive strength. */
    }
    requirement structuralIntegrity : StructuralIntegrity;
    dependency structuralBasis from structuralIntegrity to BlueDogRequirements::wetMechanicalIntegrity;
    requirement def <'T-101'> BendingStrength {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each primary structural member shall retain nonnegative bending-strength margin under the declared limit-load cases. */
        comment conditions /* Use the documented wet/jointed laminate allowable. Analyze hull, wing, keel and rudder separately; no FDM strength credit. Grounding and ballast inertia are separate load cases. */
        metadata rationale : ModelingMetadata::Rationale { text = "Use the documented wet/jointed laminate allowable. Analyze hull, wing, keel and rudder separately; no FDM strength credit. Grounding and ballast inertia are separate load cases."; }
        attribute stressPa : Real;
        require constraint acceptance { RealFunctions::abs(stressPa) <= material.laminateAllowable }
    }
    requirement bendingStrength : BendingStrength;
    #derivation connection deriveBendingStrength { end #original source ::> structuralIntegrity; end #derive target ::> bendingStrength; }
    requirement def <'T-102'> AppendageDeflection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each wing, keel and rudder tip deflection shall be no greater than 2 percent of its unsupported span under the declared limit loads. */
        comment conditions /* Proposed stiffness allocation preserves approximate foil geometry. Beam calculations do not cover shell buckling, fatigue or bond failure. */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed stiffness allocation preserves approximate foil geometry. Beam calculations do not cover shell buckling, fatigue or bond failure."; }
        attribute fraction : Real;
        require constraint acceptance { fraction >= 0 and fraction <= material.appendageDeflectionFraction }
    }
    requirement appendageDeflection : AppendageDeflection;
    #derivation connection deriveAppendageDeflection { end #original source ::> structuralIntegrity; end #derive target ::> appendageDeflection; }
    requirement def <'T-103'> HullDeflection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Hull longitudinal deflection shall be no greater than 0.5 percent of waterline length under the declared wave-bending load. */
        comment conditions /* Proposed simply supported screening case: twice loaded vessel weight, uniformly distributed over waterline length. Not an ISO scantling assessment. */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed simply supported screening case: twice loaded vessel weight, uniformly distributed over waterline length. Not an ISO scantling assessment."; }
        attribute fraction : Real;
        require constraint acceptance { fraction >= 0 and fraction <= material.hullDeflectionFraction }
    }
    requirement hullDeflection : HullDeflection;
    #derivation connection deriveHullDeflection { end #original source ::> structuralIntegrity; end #derive target ::> hullDeflection; }
    requirement def <'T-104'> PanelStrength {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each hull skin panel shall retain nonnegative bending-strength margin under 10 kPa differential pressure. */
        comment conditions /* Proposed local pressure screen, approximately a metre of freshwater head; not a slamming or full survival-wave load. A simply supported strip spans between printed ribs. */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed local pressure screen, approximately a metre of freshwater head; not a slamming or full survival-wave load. A simply supported strip spans between printed ribs."; }
        attribute stressPa : Real;
        require constraint acceptance { RealFunctions::abs(stressPa) <= material.laminateAllowable }
    }
    requirement panelStrength : PanelStrength;
    #derivation connection derivePanelStrength { end #original source ::> structuralIntegrity; end #derive target ::> panelStrength; }
    requirement def <'T-105'> PanelDeflection {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Hull skin panel deflection shall be no greater than 1 percent of rib spacing under 10 kPa differential pressure. */
        comment conditions /* Glass-only flat-strip stiffness is credited; printed ribs supply the assumed support. Rib and bond validation remain required. */
        metadata rationale : ModelingMetadata::Rationale { text = "Glass-only flat-strip stiffness is credited; printed ribs supply the assumed support. Rib and bond validation remain required."; }
        attribute fraction : Real;
        require constraint acceptance { fraction >= 0 and fraction <= material.panelDeflectionFraction }
    }
    requirement panelDeflection : PanelDeflection;
    #derivation connection derivePanelDeflection { end #original source ::> structuralIntegrity; end #derive target ::> panelDeflection; }
    requirement def <'T-106'> RootProofLoad {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each appendage root attachment shall retain its load path under its declared limit-load proof test. */
        comment conditions /* Independently test the largest calculated bending case, a 100 N tip load, and twice ballast weight transverse at the keel tip. Computed beam stress alone does not verify this attachment. */
        metadata rationale : ModelingMetadata::Rationale { text = "Independently test the largest calculated bending case, a 100 N tip load, and twice ballast weight transverse at the keel tip. Computed beam stress alone does not verify this attachment."; }
    }
    requirement rootProofLoad : RootProofLoad;
    #derivation connection deriveRootProofLoad { end #original source ::> structuralIntegrity; end #derive target ::> rootProofLoad; }
    requirement def <'T-107'> WetCouponStrength {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Wet-conditioned production laminate coupons shall demonstrate a bending allowable of at least 50 MPa. */
        comment conditions /* Proposed target for the selected print, layup, joint and cure process after N-044 exposure. A datasheet value for neat resin is not laminate evidence. Use a lower measured allowable and re-size if this target is not substantiated. */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed target for the selected print, layup, joint and cure process after N-044 exposure. A datasheet value for neat resin is not laminate evidence. Use a lower measured allowable and re-size if this target is not substantiated."; }
        attribute allowablePa : Real;
        require constraint acceptance { allowablePa >= material.laminateAllowable }
    }
    requirement wetCouponStrength : WetCouponStrength;
    #derivation connection deriveWetCouponStrength { end #original source ::> structuralIntegrity; end #derive target ::> wetCouponStrength; }
    requirement def <'T-108'> WetCouponStiffness {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Wet-conditioned production laminate coupons shall demonstrate a flexural modulus of at least 10 GPa. */
        comment conditions /* Proposed effective laminate target including joints; not a manufacturer claim or demonstrated property. Coupon orientation must cover the modeled primary directions. */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed effective laminate target including joints; not a manufacturer claim or demonstrated property. Coupon orientation must cover the modeled primary directions."; }
        attribute modulusPa : Real;
        require constraint acceptance { modulusPa >= material.laminateModulus }
    }
    requirement wetCouponStiffness : WetCouponStiffness;
    #derivation connection deriveWetCouponStiffness { end #original source ::> structuralIntegrity; end #derive target ::> wetCouponStiffness; }
    requirement def <'T-109'> BondProof {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each representative glass-to-print joint shall retain its load path under its calculated limit-load proof test after N-044 exposure. */
        comment conditions /* No qualified adhesion value is available; bond acceptance remains evidence-gated even when beam margins pass. */
        metadata rationale : ModelingMetadata::Rationale { text = "No qualified adhesion value is available; bond acceptance remains evidence-gated even when beam margins pass."; }
    }
    requirement bondProof : BondProof;
    #derivation connection deriveBondProof { end #original source ::> structuralIntegrity; end #derive target ::> bondProof; }
    requirement def <'T-110'> LoadedFreeboard {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The loaded hull shall retain at least 50 mm of geometric deck-edge freeboard at 20 degrees heel in calm water. */
        comment conditions /* Proposed reserve geometry screen; not a promise of a dry deck in N-012 waves. Evaluate freeboard*cos(heel)-beam/2*sin(heel). */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed reserve geometry screen; not a promise of a dry deck in N-012 waves. Evaluate freeboard*cos(heel)-beam/2*sin(heel)."; }
        attribute freeboardM : Real;
        require constraint acceptance { freeboardM >= material.minimumFreeboard }
    }
    requirement loadedFreeboard : LoadedFreeboard;
    dependency basisLoadedFreeboard from loadedFreeboard to BlueDogRequirements::stabilityAndFouling { metadata rationale : ModelingMetadata::Rationale { text = "Selected design allocation; the numerical value is not logically implied by the parent requirement."; } }
    requirement def <'T-111'> ReserveBuoyancy {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Intact enclosed volume above the loaded waterline shall provide reserve displacement of at least 100 percent of loaded vessel mass. */
        comment conditions /* Proposed intact reserve criterion. Do not credit unsealed printed infill. Damage stability, capsize and downflooding require separate verification. */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed intact reserve criterion. Do not credit unsealed printed infill. Damage stability, capsize and downflooding require separate verification."; }
        attribute fraction : Real;
        require constraint acceptance { fraction >= material.reserveFraction }
    }
    requirement reserveBuoyancy : ReserveBuoyancy;
    dependency basisReserveBuoyancy from reserveBuoyancy to BlueDogRequirements::stabilityAndFouling { metadata rationale : ModelingMetadata::Rationale { text = "Selected design allocation; the numerical value is not logically implied by the parent requirement."; } }
    requirement def <'T-112'> LaunchClearance {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The loaded vessel shall retain at least 0.30 m bottom clearance in 1.50 m water depth. */
        comment conditions /* Proposed launch/retrieval site allocation supporting P-105 and P-106. The resulting immersed-depth limit is 1.20 m; actual site availability remains unverified. */
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed launch/retrieval site allocation supporting P-105 and P-106. The resulting immersed-depth limit is 1.20 m; actual site availability remains unverified."; }
        attribute immersedDepthM : Real;
        require constraint acceptance { immersedDepthM > 0 and immersedDepthM <= material.launchDepth - material.bottomClearance }
    }
    requirement launchClearance : LaunchClearance;
    dependency basisLaunchClearance from launchClearance to BlueDogRequirements::soloLaunch { metadata rationale : ModelingMetadata::Rationale { text = "Selected design allocation; the numerical value is not logically implied by the parent requirement."; } }
    requirement def <'T-113'> PrintTileEnvelope {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* Each structural print tile shall have positive extents no greater than 230 mm in X, Y and Z before supports and clearance. */
        comment conditions /* 20 mm total allowance in each axis leaves room within the owner-selected 250 mm cube. CAD/slicer verification must still establish P-002; the mass model only estimates seam density. */
        metadata rationale : ModelingMetadata::Rationale { text = "20 mm total allowance in each axis leaves room within the owner-selected 250 mm cube. CAD/slicer verification must still establish P-002; the mass model only estimates seam density."; }
        attribute largestExtentM : Real;
        require constraint acceptance { largestExtentM > 0 and largestExtentM <= material.printTile }
    }
    requirement printTileEnvelope : PrintTileEnvelope;
    dependency basisPrintTileEnvelope from printTileEnvelope to BlueDogRequirements::desktopManufacture { metadata rationale : ModelingMetadata::Rationale { text = "Selected design allocation; the numerical value is not logically implied by the parent requirement."; } }
    analysis def MaterialInputs {
        doc /* PETG density: Prusament PETG TDS 2021/10, revision 2022-02-16, 1.27 g/cm3.
         * Epoxy density: WEST SYSTEM 105/206 TDS 2014, cured specific gravity 1.18.
         * Glass density 2550 kg/m3 and 1:1 retained mixed-resin/dry-glass mass ratio
         * are project assumptions. 10 GPa and 50 MPa are proposed effective wet,
         * jointed laminate targets; no manufacturer qualification is claimed.
         * 200 g/m2 ply, PETG wall/infill, finishing and seam budgets are process
         * assumptions. Resin waste in cups/tools is excluded from vessel mass. */
        out attribute petgDensity : Real = 1270;
        out attribute glassDensity : Real = 2550;
        out attribute epoxyDensity : Real = 1180;
        out attribute resinGlassRatio : Real = 1;
        out attribute laminateModulus : Real = 10000000000;
        out attribute laminateAllowable : Real = 50000000;
        out attribute hullPrintWall : Real = 0.0008;
        out attribute foilPrintWall : Real = 0.0004;
        out attribute ribHeight : Real = 0.01;
        out attribute foilInfill : Real = 0.08;
        out attribute foilThicknessRatio : Real = 0.12;
        out attribute finishingMass : Real = 0.10;
        out attribute tapeWidth : Real = 0.03;
        out attribute tapeDryMass : Real = 0.20;
        out attribute printTile : Real = 0.23;
        out attribute minimumFreeboard : Real = 0.05;
        out attribute reserveFraction : Real = 1;
        out attribute launchDepth : Real = 1.5;
        out attribute bottomClearance : Real = 0.3;
        out attribute pressure : Real = 10000;
        out attribute tipProofForce : Real = 100;
        out attribute appendageDeflectionFraction : Real = 0.02;
        out attribute hullDeflectionFraction : Real = 0.005;
        out attribute panelDeflectionFraction : Real = 0.01;
    }
    analysis material : MaterialInputs;
    calc def LaminateThickness {
        in dry : Real; in p : Real [*] ordered nonunique;
        return thickness : Real;
        dry / p#(75) + dry * p#(77) / p#(76)
    }
    calc def ShellInertia {
        in width : Real; in depth : Real; in thickness : Real;
        return inertia : Real;
        // Two broad skins only: no optimistic rectangular side-wall credit.
        2 * width * (thickness * thickness * thickness / 12 + thickness * (depth / 2 - thickness / 2) * (depth / 2 - thickness / 2))
    }
    calc def FoilArealMass {
        in chord : Real; in dry : Real; in p : Real [*] ordered nonunique;
        return areal : Real;
        2 * (1 + p#(84)) * (p#(74) * p#(81) +
            dry * (1 + p#(77)) + p#(85) +
            2 * p#(86) / p#(88) * p#(87) * (1 + p#(77))) +
            p#(74) * p#(83) * 0.6 * p#(84) * chord
    }
    calc def HullArealMass {
        in dry : Real; in p : Real [*] ordered nonunique; in ribPitch : Real;
        return areal : Real;
        p#(74) * (p#(80) + 2 * p#(80) * p#(82) / ribPitch) +
        dry * (1 + p#(77)) + p#(85) +
        2 * p#(86) / p#(88) * p#(87) * (1 + p#(77))
    }
    dependency materialSource from MaterialInputs to hybridConstruction;
    satisfy hybridConstruction by BlueDog::Architecture::missionContext.boat.hullAndRig.printedHull;
    satisfy bendingStrength by BlueDog::Architecture::missionContext.boat.hullAndRig;
    satisfy appendageDeflection by BlueDog::Architecture::missionContext.boat.hullAndRig;
    satisfy loadedFreeboard by BlueDog::Architecture::missionContext.boat.hullAndRig.printedHull;
    satisfy reserveBuoyancy by BlueDog::Architecture::missionContext.boat.hullAndRig.printedHull;
    satisfy launchClearance by BlueDog::Architecture::missionContext.boat.hullAndRig;
    satisfy printTileEnvelope by BlueDog::Architecture::missionContext.boat.hullAndRig.printedHull;
}
package BlueDogStructureDocuments {
    private import DocumentQueries::*;
    calc def Requirements :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogStructure")), type = "RequirementDefinition"),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name"), Column(name = "Statement", path = "documentation"), Column(name = "Basis and conditions", path = "rationale.text")))
    }
    calc def DesignBases :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogStructure")), type = "Dependency"),
            columns = (Column(name = "Dependent element", cell = { in row : KerML::Root::Dependency; row.client }),
                Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
                Column(name = "Rationale", path = "rationale.text")))
    }
    part def StructureReport :> Document {
        attribute redefines title = "FDM and wet-layup structural requirements";
        part caution : Paragraph { attribute redefines text = "Proposed engineering allocations with open evidence. Satisfaction links allocate responsibility, not compliance. Material sources and model limits: structure-sizing.md."; }
        part table : Table { calc rows : Requirements; }
        part loads : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogStructureViews::StrengthRelationships; }
        part stiffness : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogStructureViews::StiffnessRelationships; }
        part practical : Table { calc rows : DesignBases; }
    }
}

package BlueDogStructureViews {
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
