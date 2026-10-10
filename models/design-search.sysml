package BlueDogDesignSearch {
    private import ScalarValues::*;
    private import SI::*;
    doc /* First coupled search: an external SciPy numerical engine evaluates
     * OpenSysML-compiled equations in design-physics.sysml. This package owns
     * bounds and assumptions and audits reported numerical margins. It does not
     * independently verify the external physics or qualify a physical vessel.
     * All numeric input suffixes indicate SI units except Wh, hours and degrees.
     * Bounds are exploratory engineering choices, not added requirements.
     */
    analysis def SearchInputs {
        out attribute g : Real = 9.80665;
        out attribute rho_air : Real = 1.225;
        out attribute rho_water : Real = 1000;
        out attribute rho_ballast : Real = 7800;
        out attribute nu_air : Real = 1.5e-05;
        out attribute nu_water : Real = 1e-06;
        out attribute block_coefficient : Real = 0.55;
        out attribute waterplane_inertia_factor : Real = 0.65;
        out attribute skin_kg_m2 : Real = 1.2;
        out attribute wing_kg_m2 : Real = 1.0;
        out attribute foil_kg_m2 : Real = 8.0;
        out attribute fixed_mass_kg : Real = 2.5;
        out attribute panel_kg_m2 : Real = 2.0;
        out attribute battery_Wh_kg : Real = 140;
        out attribute servo_base_kg : Real = 0.08;
        out attribute servo_kg_Nm : Real = 0.15;
        out attribute freeboard_m : Real = 0.08;
        out attribute wing_efficiency : Real = 0.75;
        out attribute foil_efficiency : Real = 0.7;
        out attribute wing_cd0 : Real = 0.025;
        out attribute foil_cd0 : Real = 0.012;
        out attribute wing_cl_limit : Real = 1.0;
        out attribute foil_cl_limit : Real = 0.8;
        out attribute wing_alpha_limit_deg : Real = 12;
        out attribute foil_alpha_limit_deg : Real = 12;
        out attribute rudder_inflow_ratio : Real = 0.8;
        out attribute rudder_arm_fraction : Real = 0.42;
        out attribute hinge_fraction : Real = 0.02;
        out attribute friction_Nm : Real = 0.02;
        out attribute wave_coefficient : Real = 0.35;
        out attribute viscous_form_factor : Real = 1.15;
        out attribute max_froude : Real = 0.65;
        out attribute min_wing_Re : Real = 60000;
        out attribute min_foil_Re : Real = 30000;
        out attribute heel_reserve_deg : Real = 30;
        out attribute load_factor : Real = 1.5;
        out attribute yaw_reserve_Nm : Real = 0.5;
        out attribute control_speed_m_s : Real = 0.5;
        out attribute control_wind_m_s : Real = 5;
        out attribute peak_irradiance_W_m2 : Real = 1000;
        out attribute panel_efficiency : Real = 0.2;
        out attribute harvest_efficiency : Real = 0.85;
        out attribute solar_resource_factor : Real = 0.6;
        out attribute charge_efficiency : Real = 0.9;
        out attribute discharge_efficiency : Real = 0.9;
        out attribute usable_fraction : Real = 0.8;
        out attribute initial_fraction : Real = 0.9;
        out attribute charge_C_rate : Real = 0.5;
        out attribute discharge_C_rate : Real = 1.5;
        out attribute self_discharge_W : Real = 0.02;
        out attribute dark_hours : Real = 18;
        out attribute solar_hours : Real = 6;
        out attribute electronics_W : Real = 4.5;
        out attribute actuator_idle_W : Real = 0.2;
        out attribute actuator_efficiency : Real = 0.35;
        out attribute holding_W_Nm : Real = 0.5;
        out attribute wing_rate_rad_s : Real = 0.25;
        out attribute rudder_rate_rad_s : Real = 0.6;
        out attribute wing_duty : Real = 0.02;
        out attribute rudder_duty : Real = 0.05;
        out attribute planning_retention : Real = 0.8;
        out attribute maneuver_retention : Real = 0.95;
        out attribute adverse_current_m_s : Real = 1.5;
        out attribute leg_m : Real = 100000;
        out attribute hold_hours : Real = 6;
        out attribute min_ground_m_s : Real = 0.5;
        out attribute mission_hours : Real = 72;
        out attribute assembly_limit_kg : Real = 15;
        out attribute max_wing_height_m : Real = 2.0;
        out attribute deck_panel_fraction : Real = 0.6;
        out attribute equilibrium_tolerance : Real = 0.001;
        out attribute margin_tolerance : Real = 0.0001;
        out attribute reserve_Wh : Real = BlueDogRequirements::RecoveryReserveDemand(50 [W], 8 [W]) / (3600 [J]);
        out attribute parameterNames : String [*] ordered = ("g", "rho_air", "rho_water", "rho_ballast", "nu_air", "nu_water", "block_coefficient", "waterplane_inertia_factor", "skin_kg_m2", "wing_kg_m2", "foil_kg_m2", "fixed_mass_kg", "panel_kg_m2", "battery_Wh_kg", "servo_base_kg", "servo_kg_Nm", "freeboard_m", "wing_efficiency", "foil_efficiency", "wing_cd0", "foil_cd0", "wing_cl_limit", "foil_cl_limit", "wing_alpha_limit_deg", "foil_alpha_limit_deg", "rudder_inflow_ratio", "rudder_arm_fraction", "hinge_fraction", "friction_Nm", "wave_coefficient", "viscous_form_factor", "max_froude", "min_wing_Re", "min_foil_Re", "heel_reserve_deg", "load_factor", "yaw_reserve_Nm", "control_speed_m_s", "control_wind_m_s", "peak_irradiance_W_m2", "panel_efficiency", "harvest_efficiency", "solar_resource_factor", "charge_efficiency", "discharge_efficiency", "usable_fraction", "initial_fraction", "charge_C_rate", "discharge_C_rate", "self_discharge_W", "dark_hours", "solar_hours", "electronics_W", "actuator_idle_W", "actuator_efficiency", "holding_W_Nm", "wing_rate_rad_s", "rudder_rate_rad_s", "wing_duty", "rudder_duty", "planning_retention", "maneuver_retention", "adverse_current_m_s", "leg_m", "hold_hours", "min_ground_m_s", "mission_hours", "assembly_limit_kg", "max_wing_height_m", "deck_panel_fraction", "equilibrium_tolerance", "margin_tolerance", "reserve_Wh");
        out attribute parameterValues : Real [*] ordered nonunique = (g, rho_air, rho_water, rho_ballast, nu_air, nu_water, block_coefficient, waterplane_inertia_factor, skin_kg_m2, wing_kg_m2, foil_kg_m2, fixed_mass_kg, panel_kg_m2, battery_Wh_kg, servo_base_kg, servo_kg_Nm, freeboard_m, wing_efficiency, foil_efficiency, wing_cd0, foil_cd0, wing_cl_limit, foil_cl_limit, wing_alpha_limit_deg, foil_alpha_limit_deg, rudder_inflow_ratio, rudder_arm_fraction, hinge_fraction, friction_Nm, wave_coefficient, viscous_form_factor, max_froude, min_wing_Re, min_foil_Re, heel_reserve_deg, load_factor, yaw_reserve_Nm, control_speed_m_s, control_wind_m_s, peak_irradiance_W_m2, panel_efficiency, harvest_efficiency, solar_resource_factor, charge_efficiency, discharge_efficiency, usable_fraction, initial_fraction, charge_C_rate, discharge_C_rate, self_discharge_W, dark_hours, solar_hours, electronics_W, actuator_idle_W, actuator_efficiency, holding_W_Nm, wing_rate_rad_s, rudder_rate_rad_s, wing_duty, rudder_duty, planning_retention, maneuver_retention, adverse_current_m_s, leg_m, hold_hours, min_ground_m_s, mission_hours, assembly_limit_kg, max_wing_height_m, deck_panel_fraction, equilibrium_tolerance, margin_tolerance, reserve_Wh);
        out attribute outputNames : String [*] ordered = ("eq_drive", "eq_side", "eq_yaw", "eq_heel", "progress", "wing_height", "body_assembly", "keel_assembly", "deck_area", "hull_draft", "positive_stability", "froude_limit", "wing_lift", "keel_lift", "rudder_lift", "keel_incidence", "rudder_incidence", "heel_reserve", "rudder_torque", "wing_torque", "low_speed_yaw", "low_speed_keel", "wing_Re", "keel_Re", "rudder_Re", "control_rudder_Re", "energy_cycle", "energy_reserve", "peak_supply", "boatSpeed", "groundVMG", "waterVMG", "totalMass", "bodyMass", "keelAssembly", "draft", "wingHeight", "wingChord", "wingCL", "wingCD", "keelCL", "rudderCL", "heelDegrees", "headingDegrees", "alphaDegrees", "leewayDegrees", "rudderDegrees", "hullDrag", "foilDrag", "drive", "heelingMoment", "rightingMoment", "wingRe", "keelRe", "rudderRe", "averagePower", "peakPower", "harvestPower", "cycleEnergyWh", "reserveMarginWh", "wingTorque", "rudderTorque", "Froude");
        out attribute equationCount : Integer = 4;
        out attribute marginCount : Integer = 25;
        out attribute designNames : String [*] ordered nonunique = ("lwl_m", "beam_m", "sail_m2", "sail_AR", "keel_m2", "keel_span_m", "rudder_m2", "rudder_span_m", "ballast_kg", "sail_x_fraction", "battery_Wh", "panel_m2", "servo_Nm");
        out attribute lower : Real [*] ordered nonunique = (1.2, 0.2, 0.25, 1.5, 0.008, 0.25, 0.005, 0.14, 2, -0.15, 150, 0.2, 0.3);
        out attribute upper : Real [*] ordered nonunique = (3.5, 0.7, 1.8, 4.5, 0.08, 0.85, 0.05, 0.5, 13, 0.1, 500, 1.0, 4.0);
        out attribute stateLowerUp : Real [*] ordered nonunique = (0.2, 30, 0, -10, -20, -20);
        out attribute stateUpperUp : Real [*] ordered nonunique = (4.5, 80, 12, 10, 20, 20);
        out attribute stateLowerDown : Real [*] ordered nonunique = (0.2, 100, 0, -10, -20, -20);
        out attribute stateUpperDown : Real [*] ordered nonunique = (4.5, 170, 12, 10, 20, 20);
        out attribute winds : Real [*] ordered nonunique = (3, 3, 5, 5, 15, 15, 5, 5);
        out attribute windward : Boolean [*] ordered nonunique = (true, false, true, false, true, false, true, false);
        out attribute foulingDrag : Real [*] ordered nonunique = (1, 1, 1, 1, 1, 1, 1.5, 1.5);
    }
    analysis settings : SearchInputs;
    calc def Within {
        in values : Real [*] ordered nonunique;
        in lower : Real [*] ordered nonunique;
        in upper : Real [*] ordered nonunique;
        return fits : Boolean;
        if SequenceFunctions::size(values) != SequenceFunctions::size(lower) or SequenceFunctions::size(values) != SequenceFunctions::size(upper) ? false else
            (1..SequenceFunctions::size(values))->ControlFunctions::forAll { in i : Integer; values#(i) >= lower#(i) - 0.0000001 and values#(i) <= upper#(i) + 0.0000001 }
    }
    part def OperatingPoint {
        attribute index : Integer;
        attribute operatingValues : Real [6] ordered nonunique;
    }
    part def SearchResult {
        attribute label : String;
        attribute design : Real [*] ordered nonunique;
        part points : OperatingPoint [1..*] ordered;
        attribute evidenceAccepted : Boolean;
    }
    analysis def SearchAudit {
        subject trial : SearchResult;
        out attribute boundsValid : Boolean = Within(trial.design, settings.lower, settings.upper) and
            trial.points->ControlFunctions::forAll { in point : OperatingPoint;
                point.index >= 1 and point.index <= SequenceFunctions::size(settings.winds) and
                Within(point.operatingValues, if settings.windward#(point.index) ? settings.stateLowerUp else settings.stateLowerDown,
                    if settings.windward#(point.index) ? settings.stateUpperUp else settings.stateUpperDown) };
        assert constraint validBounds { boundsValid }
        attribute width : Integer = SequenceFunctions::size(settings.outputNames);
        out attribute rows : Real [*] ordered nonunique = trial.points->ControlFunctions::collect { in point : OperatingPoint;
            BlueDogDesignPhysics::EvaluateCase(trial.design, settings.parameterValues,
                (settings.winds#(point.index), (if settings.windward#(point.index) ? 1 else 0), settings.foulingDrag#(point.index), point.operatingValues)) };
        attribute equations : Real [*] ordered nonunique = (1..SequenceFunctions::size(trial.points))->ControlFunctions::collect { in i : Integer;
            (1..settings.equationCount)->ControlFunctions::collect { in j : Integer; RealFunctions::abs(rows#((i-1)*width+j)) } };
        attribute margins : Real [*] ordered nonunique = (1..SequenceFunctions::size(trial.points))->ControlFunctions::collect { in i : Integer;
            (1..settings.marginCount)->ControlFunctions::collect { in j : Integer; rows#((i-1)*width+settings.equationCount+j) } };
        out attribute maxEquilibriumResidual : Real = equations->ControlFunctions::reduce { in a : Real; in b : Real; NumericalFunctions::max(a, b) };
        out attribute minimumMargin : Real = margins->ControlFunctions::reduce { in a : Real; in b : Real; NumericalFunctions::min(a, b) };
        out attribute numericalFeasible : Boolean = boundsValid and maxEquilibriumResidual <= settings.equilibrium_tolerance and minimumMargin >= -settings.margin_tolerance;
        out attribute caseLabel : String = trial.label;
        attribute scenarioIndices : Integer [*] ordered nonunique = trial.points->ControlFunctions::collect { in point : OperatingPoint; point.index };
        out attribute fullEnvelopeCovered : Boolean = SequenceFunctions::size(trial.points) == SequenceFunctions::size(settings.winds) and
            (1..SequenceFunctions::size(trial.points))->ControlFunctions::forAll { in i : Integer; scenarioIndices#(i) == i };
        out attribute groundSpeeds : Real [*] ordered nonunique = (1..SequenceFunctions::size(trial.points))->ControlFunctions::collect { in i : Integer; rows#((i-1)*width+31) };
        out attribute worstGroundVMG : Real = groundSpeeds->ControlFunctions::reduce { in a : Real; in b : Real; NumericalFunctions::min(a, b) };
        out attribute passagePossible : Boolean = worstGroundVMG > 0;
        out attribute conservativeRoundTripHours : Real [0..1] = if passagePossible ?
            settings.leg_m / worstGroundVMG / 3600 + settings.leg_m / (worstGroundVMG + 2 * settings.adverse_current_m_s) / 3600 + settings.hold_hours else null;
        out attribute missionTimeMet : Boolean = if passagePossible ? conservativeRoundTripHours <= settings.mission_hours else false;
        out attribute evidenceReady : Boolean = trial.evidenceAccepted;
        return supportedDesign : Boolean = numericalFeasible and missionTimeMet and fullEnvelopeCovered and evidenceReady;
        objective assessment { require constraint { boundsValid } }
    }
    dependency engineBasis from SearchAudit to BlueDogSailing::PolarDemandAndHullScreen;
    dependency energyBasis from SearchAudit to BlueDogEnergy::SustainedOperation;
    dependency stabilityBasis from SearchAudit to BlueDogRequirements::selfRighting;
    dependency handlingBasis from SearchAudit to BlueDogRequirements::liftMass;
    dependency progressBasis from SearchAudit to BlueDogRequirements::legProgress;
}
