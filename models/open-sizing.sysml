package BlueDogOpenSizing {
    private import ScalarValues::*;
    private import BlueDogDesignSearch::settings;
    doc /* Joint sizing experiment, not a voyage qualification. Numerical bounds
     * are expandable search brackets, except placement inside the hull and
     * conservative ceilings implied by the 15 kg assembly requirement.
     * Aerodynamic/material coefficients remain assumptions, not design freedoms.
     * Structural strength, minimum safe freeboard and actual route weather are
     * unresolved. A boundary-limited solution is not a selected design. */
    analysis def Inputs {
        out attribute designNames : String [*] ordered nonunique = (settings.designNames, "freeboard_m", "rudder_arm_fraction");
        out attribute lower : Real [*] ordered nonunique = (0.8, 0.1, 0.05, 0.75, 0.002, 0.08, 0.002, 0.08, 0, -0.5, 30, 0.03, 0.05, 0.01, 0.05);
        out attribute upper : Real [*] ordered nonunique = (10, 2, 10, 12, 0.4, 3, 0.3, 2, settings.assembly_limit_kg, 0.5,
            settings.assembly_limit_kg * settings.battery_Wh_kg, settings.assembly_limit_kg / settings.panel_kg_m2,
            settings.assembly_limit_kg / (2 * settings.servo_kg_Nm), 0.5, 0.5);
        out attribute expandableLower : Boolean [*] ordered nonunique = (true, true, true, true, true, true, true, true, false, false, true, true, true, true, true);
        out attribute expandableUpper : Boolean [*] ordered nonunique = (true, true, true, true, true, true, true, true, false, false, false, false, false, true, false);
    }
    calc def EvaluateCase {
        in d : Real [*] ordered nonunique;
        in p : Real [*] ordered nonunique;
        in s : Real [*] ordered nonunique;
        // Freeboard shell mass is carried by the hull. The inherited moment
        // surrogate places shell/equipment at waterline; it is not a detailed CG model.
        attribute parameters : Real [*] ordered nonunique = (1..SequenceFunctions::size(p))->ControlFunctions::collect { in i : Integer;
            if i == 12 ? p#(i) + 2 * p#(9) * d#(14) * (d#(1) + d#(2)) else
            if i == 17 ? d#(14) else if i == 27 ? d#(15) else p#(i) };
        attribute legacy : Real [*] ordered nonunique = BlueDogDesignPhysics::EvaluateCase(
            (1..13)->ControlFunctions::collect { in i : Integer; d#(i) }, parameters, s);
        return values : Real [*] ordered nonunique;
        // Remove the exploratory wing-height inequality, preserving the output
        // layout for replay. Wing mass, moments and geometry remain calculated.
        (legacy#(1), legacy#(2), legacy#(3), legacy#(4), legacy#(5), 1.0, legacy#(7), legacy#(8), legacy#(9), legacy#(10), legacy#(11), legacy#(12), legacy#(13), legacy#(14), legacy#(15), legacy#(16), legacy#(17), legacy#(18), legacy#(19), legacy#(20), legacy#(21), legacy#(22), legacy#(23), legacy#(24), legacy#(25), legacy#(26), legacy#(27), legacy#(28), legacy#(29), legacy#(30), legacy#(31), legacy#(32), legacy#(33), legacy#(34), legacy#(35), legacy#(36), legacy#(37), legacy#(38), legacy#(39), legacy#(40), legacy#(41), legacy#(42), legacy#(43), legacy#(44), legacy#(45), legacy#(46), legacy#(47), legacy#(48), legacy#(49), legacy#(50), legacy#(51), legacy#(52), legacy#(53), legacy#(54), legacy#(55), legacy#(56), legacy#(57), legacy#(58), legacy#(59), legacy#(60), legacy#(61), legacy#(62), legacy#(63))
    }
    part def Candidate {
        attribute design : Real [*] ordered nonunique;
        attribute scenario : Real [*] ordered nonunique;
    }
    analysis def Audit {
        subject trial : Candidate;
        out attribute rows : Real [*] ordered nonunique = EvaluateCase(trial.design, settings.parameterValues, trial.scenario);
        objective calculation { require constraint { SequenceFunctions::size(rows) == SequenceFunctions::size(settings.outputNames) } }
    }
    dependency handling from Inputs to BlueDogRequirements::liftMass;
    dependency progress from Audit to BlueDogRequirements::legProgress;
}
