package BlueDogDesignPhysics {
    private import ScalarValues::*;
    doc /* Authoritative reduced-order search equations. Float arrays are a
     * native-compilation boundary; SI units and positions are declared by
     * BlueDogDesignSearch::SearchInputs. No Python copy of these equations.
     * The wave-drag term, mass scaling and small-angle hydrostatics are unvalidated
     * proxies. No dynamic planing lift, waves, capsize or collision simulation.
     */
    calc def EvaluateCase {
        in d : Real [*] ordered nonunique;
        in p : Real [*] ordered nonunique;
        in s : Real [*] ordered nonunique;
        attribute lwl_m : Real = d#(1);
        attribute beam_m : Real = d#(2);
        attribute sail_m2 : Real = d#(3);
        attribute sail_AR : Real = d#(4);
        attribute keel_m2 : Real = d#(5);
        attribute keel_span_m : Real = d#(6);
        attribute rudder_m2 : Real = d#(7);
        attribute rudder_span_m : Real = d#(8);
        attribute ballast_kg : Real = d#(9);
        attribute sail_x_fraction : Real = d#(10);
        attribute battery_Wh : Real = d#(11);
        attribute panel_m2 : Real = d#(12);
        attribute servo_Nm : Real = d#(13);
        attribute g : Real = p#(1);
        attribute rho_air : Real = p#(2);
        attribute rho_water : Real = p#(3);
        attribute rho_ballast : Real = p#(4);
        attribute nu_air : Real = p#(5);
        attribute nu_water : Real = p#(6);
        attribute block_coefficient : Real = p#(7);
        attribute waterplane_inertia_factor : Real = p#(8);
        attribute skin_kg_m2 : Real = p#(9);
        attribute wing_kg_m2 : Real = p#(10);
        attribute foil_kg_m2 : Real = p#(11);
        attribute fixed_mass_kg : Real = p#(12);
        attribute panel_kg_m2 : Real = p#(13);
        attribute battery_Wh_kg : Real = p#(14);
        attribute servo_base_kg : Real = p#(15);
        attribute servo_kg_Nm : Real = p#(16);
        attribute freeboard_m : Real = p#(17);
        attribute wing_efficiency : Real = p#(18);
        attribute foil_efficiency : Real = p#(19);
        attribute wing_cd0 : Real = p#(20);
        attribute foil_cd0 : Real = p#(21);
        attribute wing_cl_limit : Real = p#(22);
        attribute foil_cl_limit : Real = p#(23);
        attribute wing_alpha_limit_deg : Real = p#(24);
        attribute foil_alpha_limit_deg : Real = p#(25);
        attribute rudder_inflow_ratio : Real = p#(26);
        attribute rudder_arm_fraction : Real = p#(27);
        attribute hinge_fraction : Real = p#(28);
        attribute friction_Nm : Real = p#(29);
        attribute wave_coefficient : Real = p#(30);
        attribute viscous_form_factor : Real = p#(31);
        attribute max_froude : Real = p#(32);
        attribute min_wing_Re : Real = p#(33);
        attribute min_foil_Re : Real = p#(34);
        attribute heel_reserve_deg : Real = p#(35);
        attribute load_factor : Real = p#(36);
        attribute yaw_reserve_Nm : Real = p#(37);
        attribute control_speed_m_s : Real = p#(38);
        attribute control_wind_m_s : Real = p#(39);
        attribute peak_irradiance_W_m2 : Real = p#(40);
        attribute panel_efficiency : Real = p#(41);
        attribute harvest_efficiency : Real = p#(42);
        attribute solar_resource_factor : Real = p#(43);
        attribute charge_efficiency : Real = p#(44);
        attribute discharge_efficiency : Real = p#(45);
        attribute usable_fraction : Real = p#(46);
        attribute initial_fraction : Real = p#(47);
        attribute charge_C_rate : Real = p#(48);
        attribute discharge_C_rate : Real = p#(49);
        attribute self_discharge_W : Real = p#(50);
        attribute dark_hours : Real = p#(51);
        attribute solar_hours : Real = p#(52);
        attribute electronics_W : Real = p#(53);
        attribute actuator_idle_W : Real = p#(54);
        attribute actuator_efficiency : Real = p#(55);
        attribute holding_W_Nm : Real = p#(56);
        attribute wing_rate_rad_s : Real = p#(57);
        attribute rudder_rate_rad_s : Real = p#(58);
        attribute wing_duty : Real = p#(59);
        attribute rudder_duty : Real = p#(60);
        attribute planning_retention : Real = p#(61);
        attribute maneuver_retention : Real = p#(62);
        attribute adverse_current_m_s : Real = p#(63);
        attribute leg_m : Real = p#(64);
        attribute hold_hours : Real = p#(65);
        attribute min_ground_m_s : Real = p#(66);
        attribute mission_hours : Real = p#(67);
        attribute assembly_limit_kg : Real = p#(68);
        attribute max_wing_height_m : Real = p#(69);
        attribute deck_panel_fraction : Real = p#(70);
        attribute equilibrium_tolerance : Real = p#(71);
        attribute margin_tolerance : Real = p#(72);
        attribute reserve_Wh : Real = p#(73);
        attribute wind : Real = s#(1);
        attribute upwind : Boolean = s#(2) > 0.5;
        attribute foul : Real = s#(3);
        attribute v : Real = s#(4);
        attribute theta : Real = TrigFunctions::rad(s#(5));
        attribute alpha : Real = TrigFunctions::rad(s#(6));
        attribute beta : Real = TrigFunctions::rad(s#(7));
        attribute delta : Real = TrigFunctions::rad(s#(8));
        attribute heel : Real = TrigFunctions::rad(s#(9));
        attribute cb : Real = TrigFunctions::cos(beta);
        attribute sb : Real = TrigFunctions::sin(beta);
        attribute ch : Real = TrigFunctions::cos(heel);
        attribute wingHeight : Real = RealFunctions::sqrt(sail_m2 * sail_AR);
        attribute wingChord : Real = sail_m2 / wingHeight;
        attribute keelChord : Real = keel_m2 / keel_span_m;
        attribute rudderChord : Real = rudder_m2 / rudder_span_m;
        attribute wingMass : Real = wing_kg_m2 * sail_m2;
        attribute batteryMass : Real = battery_Wh / battery_Wh_kg;
        attribute panelMass : Real = panel_kg_m2 * panel_m2;
        attribute actuatorMass : Real = 2 * (servo_base_kg + servo_kg_Nm * servo_Nm);
        attribute foilMass : Real = foil_kg_m2 * (keel_m2 + rudder_m2);
        attribute fixedMass : Real = fixed_mass_kg + wingMass + batteryMass + panelMass + actuatorMass + foilMass + ballast_kg + 2 * skin_kg_m2 * lwl_m * beam_m;
        // Solve displacement with hull side-shell mass depending on draft.
        attribute draft : Real = (fixedMass - rho_water * ballast_kg / rho_ballast) / (rho_water * lwl_m * beam_m * block_coefficient - 2 * skin_kg_m2 * (lwl_m + beam_m));
        attribute shellMass : Real = skin_kg_m2 * (2 * lwl_m * beam_m + 2 * draft * (lwl_m + beam_m));
        attribute mass : Real = fixedMass + 2 * skin_kg_m2 * draft * (lwl_m + beam_m);
        attribute keelAssembly : Real = ballast_kg + foil_kg_m2 * keel_m2;
        attribute bodyMass : Real = mass - keelAssembly;
        attribute wingZ : Real = freeboard_m + wingHeight / 2;
        attribute keelZ : Real = draft + keel_span_m / 2;
        attribute rudderZ : Real = draft + rudder_span_m / 2;
        attribute ballastZ : Real = draft + keel_span_m;
        attribute hullVolume : Real = lwl_m * beam_m * draft * block_coefficient;
        attribute waterplaneI : Real = waterplane_inertia_factor * lwl_m * beam_m * beam_m * beam_m / 12;
        // Weight first moment about waterline; fixed equipment and shell at WL.
        attribute weightMoment : Real = wingMass * wingZ + panelMass * freeboard_m - batteryMass * draft / 2 - foil_kg_m2 * (keel_m2 * keelZ + rudder_m2 * rudderZ) - ballast_kg * ballastZ;
        attribute buoyancyMoment : Real = -rho_water * (hullVolume * draft / 2 + ballast_kg / rho_ballast * ballastZ);
        attribute rightingCoefficient : Real = g * (rho_water * waterplaneI + buoyancyMoment - weightMoment);
        attribute righting : Real = rightingCoefficient * TrigFunctions::sin(heel);
        attribute awx : Real = wind * TrigFunctions::cos(theta) + v * cb;
        attribute awy : Real = wind * TrigFunctions::sin(theta) - v * sb;
        attribute va : Real = RealFunctions::sqrt(awx * awx + awy * awy);
        attribute qa : Real = 0.5 * rho_air * va * va;
        attribute wingSlope : Real = 2 * TrigFunctions::pi / (1 + 2 / (wing_efficiency * sail_AR));
        attribute cl : Real = wingSlope * alpha;
        attribute cd : Real = wing_cd0 + cl * cl / (TrigFunctions::pi * wing_efficiency * sail_AR);
        attribute xs : Real = qa * sail_m2 * (cl * ch * awy - cd * awx) / va;
        attribute ys : Real = qa * sail_m2 * (cl * ch * awx + cd * awy) / va;
        attribute drive : Real = xs * cb + ys * sb;
        attribute sideNormal : Real = ys * cb - xs * sb;
        attribute qk : Real = 0.5 * rho_water * v * v;
        attribute qr : Real = qk * rudder_inflow_ratio * rudder_inflow_ratio;
        attribute ark : Real = keel_span_m * keel_span_m / keel_m2;
        attribute arr : Real = rudder_span_m * rudder_span_m / rudder_m2;
        attribute foilAlphaLimit : Real = TrigFunctions::rad(foil_alpha_limit_deg);
        attribute clk : Real = 2 * TrigFunctions::pi / (1 + 2 / (foil_efficiency * ark)) * beta * ch;
        attribute clr : Real = 2 * TrigFunctions::pi / (1 + 2 / (foil_efficiency * arr)) * (beta + delta) * ch;
        attribute lk : Real = qk * keel_m2 * clk * ch;
        attribute lr : Real = qr * rudder_m2 * clr * ch;
        attribute dk : Real = qk * keel_m2 * (foil_cd0 * foul + clk * clk / (TrigFunctions::pi * foil_efficiency * ark));
        attribute dr : Real = qr * rudder_m2 * (foil_cd0 * foul + clr * clr / (TrigFunctions::pi * foil_efficiency * arr));
        attribute fn : Real = v / RealFunctions::sqrt(g * lwl_m);
        attribute hullRe : Real = v * lwl_m / nu_water;
        attribute logRe : Real = OpenSysMLMathFunctions::ln(hullRe) / OpenSysMLMathFunctions::ln(10);
        attribute cf : Real = 0.075 / ((logRe - 2) * (logRe - 2));
        attribute wetted : Real = lwl_m * beam_m + 2 * draft * (lwl_m + beam_m);
        attribute hullDrag : Real = qk * wetted * cf * viscous_form_factor * foul + mass * g * wave_coefficient * fn * fn * fn * fn;
        attribute resistance : Real = hullDrag + dk + dr;
        attribute sailX : Real = sail_x_fraction * lwl_m;
        attribute rudderX : Real = -rudder_arm_fraction * lwl_m;
        attribute heeling : Real = ys * wingZ * ch + ((lk * cb + dk * sb) * keelZ + (lr * cb + dr * sb) * rudderZ + hullDrag * sb * draft / 2) * ch;
        attribute wingTorque : Real = qa * sail_m2 * RealFunctions::sqrt(cl * cl + cd * cd) * hinge_fraction * wingChord + friction_Nm;
        attribute rudderTorque : Real = qr * rudder_m2 * RealFunctions::sqrt(clr * clr + foil_cd0 * foil_cd0) * hinge_fraction * rudderChord + friction_Nm;
        attribute rudderEnvelopeTorque : Real = qr * rudder_m2 * foil_cl_limit * hinge_fraction * rudderChord + friction_Nm;
        attribute waterVMG : Real = (if upwind ? 1 else -1) * v * TrigFunctions::cos(theta + beta);
        attribute groundVMG : Real = planning_retention * maneuver_retention * waterVMG - adverse_current_m_s;
        attribute wingRe : Real = va * wingChord / nu_air;
        attribute keelRe : Real = v * keelChord / nu_water;
        attribute rudderRe : Real = v * rudder_inflow_ratio * rudderChord / nu_water;
        attribute featherSide : Real = 0.5 * rho_air * control_wind_m_s * control_wind_m_s * sail_m2 * wing_cd0;
        attribute controlRudderCapacity : Real = 0.5 * rho_water * control_speed_m_s * control_speed_m_s * rudder_inflow_ratio * rudder_inflow_ratio * rudder_m2 * foil_cl_limit / load_factor;
        attribute controlKeelCapacity : Real = 0.5 * rho_water * control_speed_m_s * control_speed_m_s * keel_m2 * foil_cl_limit / load_factor;
        attribute averagePower : Real = electronics_W + actuator_idle_W + holding_W_Nm * (wingTorque + rudderTorque) + (wingTorque * wing_rate_rad_s * wing_duty + rudderTorque * rudder_rate_rad_s * rudder_duty) / actuator_efficiency;
        attribute peakPower : Real = electronics_W + actuator_idle_W + holding_W_Nm * (wingTorque + rudderTorque) + (wingTorque * wing_rate_rad_s + rudderTorque * rudder_rate_rad_s) / actuator_efficiency;
        attribute harvestPower : Real = panel_m2 * peak_irradiance_W_m2 * panel_efficiency * harvest_efficiency * solar_resource_factor;
        attribute nightRate : Real = -averagePower / discharge_efficiency - self_discharge_W;
        attribute dayRate : Real = (if harvestPower >= averagePower ? NumericalFunctions::min((harvestPower - averagePower) * charge_efficiency, charge_C_rate * battery_Wh) else (harvestPower - averagePower) / discharge_efficiency) - self_discharge_W;
        attribute cycleEnergy : Real = dark_hours * nightRate + solar_hours * dayRate;
        attribute reserveMargin : Real = initial_fraction * usable_fraction * battery_Wh + dark_hours * nightRate - reserve_Wh;
        return values : Real [*] ordered nonunique;
        ((drive - resistance) / 10,
         (sideNormal - lk - lr) / 10,
         (-ys * sailX + (lr * cb + dr * sb) * rudderX) / 10,
         (righting - heeling) / 20,
         (groundVMG - min_ground_m_s) / min_ground_m_s,
         (max_wing_height_m - wingHeight) / max_wing_height_m,
         (assembly_limit_kg - bodyMass) / assembly_limit_kg,
         (assembly_limit_kg - keelAssembly) / assembly_limit_kg,
         (deck_panel_fraction * lwl_m * beam_m - panel_m2) / panel_m2,
         (beam_m / 2 - draft) / (beam_m / 2),
         rightingCoefficient / (mass * g),
         (max_froude - fn) / max_froude,
         (wing_cl_limit - RealFunctions::abs(cl)) / wing_cl_limit,
         (foil_cl_limit - RealFunctions::abs(clk)) / foil_cl_limit,
         (foil_cl_limit - RealFunctions::abs(clr)) / foil_cl_limit,
         (foilAlphaLimit - RealFunctions::abs(beta * ch)) / foilAlphaLimit,
         (foilAlphaLimit - RealFunctions::abs((beta + delta) * ch)) / foilAlphaLimit,
         (rightingCoefficient * TrigFunctions::sin(TrigFunctions::rad(heel_reserve_deg)) - load_factor * RealFunctions::abs(heeling)) / 20,
         (servo_Nm - load_factor * rudderEnvelopeTorque) / servo_Nm,
         (servo_Nm - load_factor * wingTorque) / servo_Nm,
         (controlRudderCapacity * (-rudderX) - featherSide * RealFunctions::abs(sailX) - yaw_reserve_Nm) / yaw_reserve_Nm,
         (controlKeelCapacity - featherSide - (yaw_reserve_Nm + featherSide * RealFunctions::abs(sailX)) / (-rudderX)) / 10,
         (wingRe - min_wing_Re) / min_wing_Re,
         (keelRe - min_foil_Re) / min_foil_Re,
         (rudderRe - min_foil_Re) / min_foil_Re,
         (control_speed_m_s * rudder_inflow_ratio * rudderChord / nu_water - min_foil_Re) / min_foil_Re,
         cycleEnergy / 100,
         reserveMargin / 100,
         (discharge_C_rate * battery_Wh - peakPower / discharge_efficiency - self_discharge_W) / 100,
         v,
         groundVMG,
         waterVMG,
         mass,
         bodyMass,
         keelAssembly,
         draft,
         wingHeight,
         wingChord,
         cl,
         cd,
         clk,
         clr,
         s#(9),
         s#(5),
         s#(6),
         s#(7),
         s#(8),
         hullDrag,
         dk + dr,
         drive,
         heeling,
         righting,
         wingRe,
         keelRe,
         rudderRe,
         averagePower,
         peakPower,
         harvestPower,
         cycleEnergy,
         reserveMargin,
         wingTorque,
         rudderTorque,
         fn)
    }
}
