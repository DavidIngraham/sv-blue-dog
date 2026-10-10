package BlueDogOpenSizing {
    private import ScalarValues::*;
    private import BlueDogDesignSearch::settings;
    doc /* Joint sizing experiment, not a voyage qualification. Numerical bounds
     * are expandable search brackets, except placement inside the hull and
     * conservative ceilings implied by the 15 kg assembly requirement.
     * Aerodynamic/material coefficients remain assumptions, not design freedoms.
     * Structural and hydrostatic screens use BlueDogStructure allocations;
     * laminate, bond, buckling and actual route evidence remain unresolved. A boundary-limited solution is not a selected design. */
    analysis def Inputs {
        out attribute designNames : String [*] ordered nonunique = (settings.designNames, "freeboard_m", "rudder_arm_fraction", "hull_glass_kg_m2", "wing_glass_kg_m2", "keel_glass_kg_m2", "rudder_glass_kg_m2", "rib_pitch_m");
        out attribute lower : Real [*] ordered nonunique = (0.8, 0.1, 0.05, 0.75, 0.002, 0.08, 0.002, 0.08, 0, -0.5, 30, 0.03, 0.05, 0.01, 0.05, 0.4, 0.2, 0.4, 0.4, 0.025);
        out attribute upper : Real [*] ordered nonunique = (10, 2, 10, 12, 0.4, 3, 0.3, 2, settings.assembly_limit_kg, 0.5,
            settings.assembly_limit_kg * settings.battery_Wh_kg, settings.assembly_limit_kg / settings.panel_kg_m2,
            settings.assembly_limit_kg / (2 * settings.servo_kg_Nm), 0.5, 0.5, 2.0, 1.6, 3.2, 2.0, 0.23);
        out attribute expandableLower : Boolean [*] ordered nonunique = (true, true, true, true, true, true, true, true, false, false, true, true, true, true, true, false, false, false, false, true);
        out attribute expandableUpper : Boolean [*] ordered nonunique = (true, true, true, true, true, true, true, true, false, false, false, false, false, true, false, true, true, true, true, false);
        out attribute parameterNames : String [*] ordered nonunique = (settings.parameterNames, "petgDensity", "glassDensity", "epoxyDensity", "resinGlassRatio", "laminateModulus", "laminateAllowable", "hullPrintWall", "foilPrintWall", "ribHeight", "foilInfill", "foilThicknessRatio", "finishingMass", "tapeWidth", "tapeDryMass", "printTile", "minimumFreeboard", "reserveFraction", "launchDepth", "bottomClearance", "pressure", "tipProofForce", "appendageDeflectionFraction", "hullDeflectionFraction", "panelDeflectionFraction");
        out attribute parameterValues : Real [*] ordered nonunique = (settings.parameterValues, BlueDogStructure::material.petgDensity, BlueDogStructure::material.glassDensity, BlueDogStructure::material.epoxyDensity, BlueDogStructure::material.resinGlassRatio, BlueDogStructure::material.laminateModulus, BlueDogStructure::material.laminateAllowable, BlueDogStructure::material.hullPrintWall, BlueDogStructure::material.foilPrintWall, BlueDogStructure::material.ribHeight, BlueDogStructure::material.foilInfill, BlueDogStructure::material.foilThicknessRatio, BlueDogStructure::material.finishingMass, BlueDogStructure::material.tapeWidth, BlueDogStructure::material.tapeDryMass, BlueDogStructure::material.printTile, BlueDogStructure::material.minimumFreeboard, BlueDogStructure::material.reserveFraction, BlueDogStructure::material.launchDepth, BlueDogStructure::material.bottomClearance, BlueDogStructure::material.pressure, BlueDogStructure::material.tipProofForce, BlueDogStructure::material.appendageDeflectionFraction, BlueDogStructure::material.hullDeflectionFraction, BlueDogStructure::material.panelDeflectionFraction);
        out attribute marginCount : Integer = 42;
        out attribute outputNames : String [*] ordered nonunique = (
            (1..29)->ControlFunctions::collect { in i : Integer; if i == 6 ? "wing_height_unconstrained" else settings.outputNames#(i) },
            "hull_bending", "hull_deflection", "panel_strength", "panel_deflection", "wing_bending", "wing_deflection", "keel_bending", "keel_deflection", "rudder_bending", "rudder_deflection", "deck_freeboard", "reserve_buoyancy", "launch_clearance", "wing_skin_geometry", "keel_skin_geometry", "rudder_skin_geometry", "positive_draft",
            (30..63)->ControlFunctions::collect { in i : Integer; settings.outputNames#(i) },
            "hullArealMass", "wingStructuralMass", "keelStructuralMass", "rudderStructuralMass", "keelStressMPa", "keelTipDeflection", "deckEdgeFreeboard", "reserveDisplacementFraction", "immersedDepth");
    }
    analysis sizingSettings : Inputs;
    calc def EvaluateCase {
        in d : Real [*] ordered nonunique;
        in p : Real [*] ordered nonunique;
        in s : Real [*] ordered nonunique;
        private import BlueDogStructure::*;
        attribute hullAreal : Real = HullArealMass(d#(16), p, d#(20));
        attribute height : Real = RealFunctions::sqrt(d#(3) * d#(4));
        attribute chord : Real = d#(3) / height;
        attribute keelChord : Real = d#(5) / d#(6);
        attribute rudderChord : Real = d#(7) / d#(8);
        attribute wingAreal : Real = FoilArealMass(chord, d#(17), p);
        attribute keelAreal : Real = FoilArealMass(keelChord, d#(18), p);
        attribute rudderAreal : Real = FoilArealMass(rudderChord, d#(19), p);
        attribute foilAreal : Real = (keelAreal * d#(5) + rudderAreal * d#(7)) / (d#(5) + d#(7));
        attribute parameters : Real [*] ordered nonunique = (1..SequenceFunctions::size(p))->ControlFunctions::collect { in i : Integer;
            if i == 9 ? hullAreal else if i == 10 ? wingAreal else if i == 11 ? foilAreal else
            if i == 12 ? p#(i) + 2 * hullAreal * d#(14) * (d#(1) + d#(2)) else
            if i == 17 ? d#(14) else if i == 27 ? d#(15) else p#(i) };
        attribute legacy : Real [*] ordered nonunique = BlueDogDesignPhysics::EvaluateCase(
            (1..13)->ControlFunctions::collect { in i : Integer; d#(i) }, parameters, s);
        attribute mass : Real = legacy#(33);
        attribute draft : Real = legacy#(36);
        attribute keelAssembly : Real = d#(9) + keelAreal * d#(5);
        attribute bodyMass : Real = mass - keelAssembly;
        attribute heel : Real = TrigFunctions::rad(s#(9));
        // Correct the inherited equal-areal-foil and zero-height shell CG approximations.
        // Shell includes top, bottom and four sides; PETG ribs follow the same shell distribution.
        attribute shellMoment : Real = hullAreal * (d#(1) * d#(2) * (d#(14) - draft) +
            (d#(1) + d#(2)) * (d#(14) * d#(14) - draft * draft));
        attribute foilMomentCorrection : Real = -(keelAreal - foilAreal) * d#(5) * (draft + d#(6)/2) -
            (rudderAreal - foilAreal) * d#(7) * (draft + d#(8)/2);
        attribute rightingCorrection : Real = -p#(1) * (shellMoment + foilMomentCorrection);
        attribute rightingCoefficient : Real = legacy#(11) * mass * p#(1) + rightingCorrection;
        attribute righting : Real = legacy#(52) + rightingCorrection * TrigFunctions::sin(heel);
        attribute hullDepth : Real = draft + d#(14);
        attribute hullThickness : Real = LaminateThickness(d#(16), p);
        attribute wingThickness : Real = LaminateThickness(d#(17), p);
        attribute keelThickness : Real = LaminateThickness(d#(18), p);
        attribute rudderThickness : Real = LaminateThickness(d#(19), p);
        attribute hullI : Real = ShellInertia(d#(2), hullDepth, hullThickness);
        attribute wingI : Real = ShellInertia(chord, p#(84) * chord, wingThickness);
        attribute keelI : Real = ShellInertia(keelChord, p#(84) * keelChord, keelThickness);
        attribute rudderI : Real = ShellInertia(rudderChord, p#(84) * rudderChord, rudderThickness);
        attribute wingForce : Real = (legacy#(61) - p#(29)) / (p#(28) * chord);
        attribute keelForce : Real = 0.5 * p#(3) * s#(4) * s#(4) * d#(5) * RealFunctions::abs(legacy#(41));
        attribute rudderForce : Real = 0.5 * p#(3) * s#(4) * s#(4) * p#(26) * p#(26) * d#(7) * RealFunctions::abs(legacy#(42));
        attribute hullMoment : Real = 2 * mass * p#(1) * d#(1) / 8;
        attribute wingLimitForce : Real = NumericalFunctions::max(p#(36) * wingForce, 2 * wingAreal * d#(3) * p#(1));
        attribute wingMoment : Real = wingLimitForce * height / 2;
        attribute keelTipForce : Real = NumericalFunctions::max(p#(94), 2 * d#(9) * p#(1));
        attribute keelMoment : Real = NumericalFunctions::max(p#(36) * keelForce * d#(6) / 2, keelTipForce * d#(6));
        attribute rudderMoment : Real = NumericalFunctions::max(p#(36) * rudderForce * d#(8) / 2, p#(94) * d#(8));
        attribute hullStress : Real = hullMoment * hullDepth / (2 * hullI);
        attribute wingStress : Real = wingMoment * p#(84) * chord / (2 * wingI);
        attribute keelStress : Real = keelMoment * p#(84) * keelChord / (2 * keelI);
        attribute rudderStress : Real = rudderMoment * p#(84) * rudderChord / (2 * rudderI);
        attribute hullDeflection : Real = 5 * 2 * mass * p#(1) * d#(1) * d#(1) * d#(1) / (384 * p#(78) * hullI);
        attribute wingDeflection : Real = wingLimitForce * height * height * height / (8 * p#(78) * wingI);
        attribute keelDeflection : Real = NumericalFunctions::max(p#(36) * keelForce / 8, keelTipForce / 3) * d#(6) * d#(6) * d#(6) / (p#(78) * keelI);
        attribute rudderDeflection : Real = NumericalFunctions::max(p#(36) * rudderForce / 8, p#(94) / 3) * d#(8) * d#(8) * d#(8) / (p#(78) * rudderI);
        attribute panelStress : Real = 0.75 * p#(93) * d#(20) * d#(20) / (hullThickness * hullThickness);
        attribute panelDeflection : Real = 5 * p#(93) * d#(20) * d#(20) * d#(20) * d#(20) / (32 * p#(78) * hullThickness * hullThickness * hullThickness);
        attribute deckFreeboard : Real = d#(14) * TrigFunctions::cos(TrigFunctions::rad(20)) - d#(2)/2 * TrigFunctions::sin(TrigFunctions::rad(20));
        attribute reserveFraction : Real = p#(3) * d#(1) * d#(2) * p#(7) * d#(14) / mass;
        attribute immersedDepth : Real = draft + NumericalFunctions::max(d#(6), d#(8));
        return values : Real [*] ordered nonunique;
        // Explicit Real tuple preserves the compiled numeric sequence ABI.
        (legacy#(1),
         legacy#(2),
         legacy#(3),
         (righting - legacy#(51)) / 20,
         legacy#(5),
         1.0,
         (p#(68) - bodyMass) / p#(68),
         (p#(68) - keelAssembly) / p#(68),
         legacy#(9),
         legacy#(10),
         rightingCoefficient / (mass * p#(1)),
         legacy#(12),
         legacy#(13),
         legacy#(14),
         legacy#(15),
         legacy#(16),
         legacy#(17),
         (rightingCoefficient * TrigFunctions::sin(TrigFunctions::rad(p#(35))) - p#(36) * RealFunctions::abs(legacy#(51))) / 20,
         legacy#(19),
         legacy#(20),
         legacy#(21),
         legacy#(22),
         legacy#(23),
         legacy#(24),
         legacy#(25),
         legacy#(26),
         legacy#(27),
         legacy#(28),
         legacy#(29),
         1 - hullStress / p#(79),
         1 - hullDeflection / (p#(96) * d#(1)),
         1 - panelStress / p#(79),
         1 - panelDeflection / (p#(97) * d#(20)),
         1 - wingStress / p#(79),
         1 - wingDeflection / (p#(95) * height),
         1 - keelStress / p#(79),
         1 - keelDeflection / (p#(95) * d#(6)),
         1 - rudderStress / p#(79),
         1 - rudderDeflection / (p#(95) * d#(8)),
         deckFreeboard / p#(89) - 1,
         reserveFraction / p#(90) - 1,
         (p#(91) - p#(92) - immersedDepth) / (p#(91) - p#(92)),
         1 - 4 * wingThickness / (p#(84) * chord),
         1 - 4 * keelThickness / (p#(84) * keelChord),
         1 - 4 * rudderThickness / (p#(84) * rudderChord),
         draft / d#(2),
         legacy#(30),
         legacy#(31),
         legacy#(32),
         legacy#(33),
         bodyMass,
         keelAssembly,
         legacy#(36),
         legacy#(37),
         legacy#(38),
         legacy#(39),
         legacy#(40),
         legacy#(41),
         legacy#(42),
         legacy#(43),
         legacy#(44),
         legacy#(45),
         legacy#(46),
         legacy#(47),
         legacy#(48),
         legacy#(49),
         legacy#(50),
         legacy#(51),
         righting,
         legacy#(53),
         legacy#(54),
         legacy#(55),
         legacy#(56),
         legacy#(57),
         legacy#(58),
         legacy#(59),
         legacy#(60),
         legacy#(61),
         legacy#(62),
         legacy#(63),
         hullAreal,
         wingAreal * d#(3),
         keelAreal * d#(5),
         rudderAreal * d#(7),
         keelStress / 1000000,
         keelDeflection,
         deckFreeboard,
         reserveFraction,
         immersedDepth)
    }
    part def Candidate {
        attribute design : Real [*] ordered nonunique;
        attribute scenario : Real [*] ordered nonunique;
    }
    analysis def Audit {
        subject trial : Candidate;
        out attribute rows : Real [*] ordered nonunique = EvaluateCase(trial.design, sizingSettings.parameterValues, trial.scenario);
        objective calculation { require constraint { SequenceFunctions::size(rows) == 89 } }
    }
    dependency handling from Inputs to BlueDogRequirements::liftMass;
    dependency strengthBasis from EvaluateCase to BlueDogStructure::bendingStrength;
    dependency stiffnessBasis from EvaluateCase to BlueDogStructure::appendageDeflection;
    dependency hullStiffnessBasis from EvaluateCase to BlueDogStructure::hullDeflection;
    dependency panelStrengthBasis from EvaluateCase to BlueDogStructure::panelStrength;
    dependency panelStiffnessBasis from EvaluateCase to BlueDogStructure::panelDeflection;
    dependency rootLoadBasis from EvaluateCase to BlueDogStructure::rootProofLoad;
    dependency freeboardBasis from EvaluateCase to BlueDogStructure::loadedFreeboard;
    dependency buoyancyBasis from EvaluateCase to BlueDogStructure::reserveBuoyancy;
    dependency launchBasis from EvaluateCase to BlueDogStructure::launchClearance;
    dependency manufacturingBasis from EvaluateCase to BlueDogStructure::printTileEnvelope;
    dependency progress from Audit to BlueDogRequirements::legProgress;
}
