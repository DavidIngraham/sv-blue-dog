package BlueDogCoupledOperation {
    private import ScalarValues::*;
    doc /* Quasi-steady force balance. VSPAERO supplies inviscid CL/CDi/CMy;
     * discrepancy factors and viscous drag remain provisional model inputs.
     * Hydrostatic heave/pitch and mast-trim geometry are external geometry solves.
     * No wave-motion, dynamic planing, separated-flow or dynamic recovery claim. */
    analysis Inputs {
        doc /* Search brackets are numerical/domain limits, not new vessel requirements.
         * Aspect/camber are limited by the VSPAERO interpolation grid; thickness
         * remains a geometric sensitivity without validated viscous-drag response. */
        out attribute designLower : Real [28] ordered nonunique = (0.8,0.2,0.02,0.05,0.2,2,0.5,0.5,0.1,-0.4,0.02,0.15,0.005,0.08,0.25,0.5,50,0.05,0.05,0.05,0.2,0.2,0.2,0.2,0.01,0.01,-0.35,0.05);
        out attribute designUpper : Real [28] ordered nonunique = (4,1.2,0.3,0.5,4,8,1.5,2,0.9,0.4,0.5,1.1,0.2,0.6,0.65,14.5,1000,1,20,10,4,4,8,4,0.23,0.23,0.35,0.9);
        out attribute routeParameters : Real [6] ordered nonunique = (0.95,0.5,1.0,100000,72,0.5);
        out attribute structureValues : Real [10] ordered nonunique = (BlueDogStructure::material.laminateModulus, BlueDogStructure::material.laminateAllowable, BlueDogStructure::material.pressure, BlueDogStructure::material.tipProofForce, BlueDogStructure::material.minimumFreeboard, BlueDogStructure::material.reserveFraction, BlueDogStructure::material.launchDepth-BlueDogStructure::material.bottomClearance, BlueDogStructure::material.appendageDeflectionFraction, BlueDogStructure::material.hullDeflectionFraction, BlueDogStructure::material.panelDeflectionFraction);
    }
    calc def Evaluate {
        in d : Real [28] ordered nonunique;
        in p : Real [38] ordered nonunique;
        in q : Real [*] ordered nonunique;
        in s : Real [9] ordered nonunique;
        in aero : Real [3] ordered nonunique;
        in massData : Real [21] ordered nonunique;
        in hydro : Real [3] ordered nonunique;
        doc /* s: wind, windward flag, fouling multiplier, speed, wind-from heading,
         * incidence, leeway, rudder angle, heel (angles degrees). hydro:
         * waterline Z, restoring moment, wetted hull area. aero moment at midchord.
         * Axes and equations preserve the existing body-frame convention. */
        attribute lwl_m : Real = d#(1);
        attribute beam_m : Real = d#(2);
        attribute sail_m2 : Real = d#(5);
        attribute sail_AR : Real = d#(6);
        attribute keel_m2 : Real = d#(11);
        attribute keel_span_m : Real = d#(12);
        attribute rudder_m2 : Real = d#(13);
        attribute rudder_span_m : Real = d#(14);
        attribute ballast_kg : Real = d#(16);
        attribute sail_x_fraction : Real = d#(10);
        attribute battery_Wh : Real = d#(17);
        attribute panel_m2 : Real = d#(18);
        attribute rudder_arm_fraction : Real = d#(15);
        attribute g : Real = p#(35);
        attribute rho_air : Real = p#(33);
        attribute rho_water : Real = p#(32);
        attribute rho_ballast : Real = p#(34);
        attribute nu_air : Real = p#(30);
        attribute nu_water : Real = p#(31);
        attribute foil_efficiency : Real = p#(28);
        attribute wing_cd0 : Real = p#(15);
        attribute foil_cd0 : Real = p#(29);
        attribute wing_cl_limit : Real = p#(16);
        attribute foil_cl_limit : Real = p#(27);
        attribute load_factor : Real = p#(36);
        attribute wave_coefficient : Real = p#(25);
        attribute viscous_form_factor : Real = p#(26);
        attribute solar_resource_factor : Real = p#(12);
        attribute electronics_W : Real = p#(11);
        attribute foil_alpha_limit_deg : Real = q#(25);
        attribute rudder_inflow_ratio : Real = q#(26);
        attribute hinge_fraction : Real = q#(28);
        attribute friction_Nm : Real = q#(29);
        attribute max_froude : Real = q#(32);
        attribute min_wing_Re : Real = q#(33);
        attribute min_foil_Re : Real = q#(34);
        attribute control_speed_m_s : Real = q#(38);
        attribute control_wind_m_s : Real = q#(39);
        attribute peak_irradiance_W_m2 : Real = q#(40);
        attribute panel_efficiency : Real = q#(41);
        attribute harvest_efficiency : Real = q#(42);
        attribute charge_efficiency : Real = q#(44);
        attribute discharge_efficiency : Real = q#(45);
        attribute usable_fraction : Real = q#(46);
        attribute initial_fraction : Real = q#(47);
        attribute charge_C_rate : Real = q#(48);
        attribute discharge_C_rate : Real = q#(49);
        attribute self_discharge_W : Real = q#(50);
        attribute dark_hours : Real = q#(51);
        attribute solar_hours : Real = q#(52);
        attribute reserve_Wh : Real = q#(73);
        attribute yaw_reserve_Nm : Real = q#(37);
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
        attribute mass : Real = massData#(1);
        attribute draft : Real = hydro#(1)+d#(3);
        attribute wingZ : Real = d#(4)+wingHeight/2-hydro#(1);
        attribute keelZ : Real = draft+keel_span_m/2;
        attribute rudderZ : Real = draft+rudder_span_m/2;
        attribute righting : Real = hydro#(2);
        attribute awx : Real = wind * TrigFunctions::cos(theta) + v * cb;
        attribute awy : Real = wind * TrigFunctions::sin(theta) - v * sb;
        attribute va : Real = RealFunctions::sqrt(awx * awx + awy * awy);
        attribute qa : Real = 0.5 * rho_air * va * va;
        attribute cl : Real = aero#(1)*p#(17);
        attribute cd : Real = (aero#(2)+p#(15))*p#(18);
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
        attribute wetted : Real = hydro#(3);
        attribute hullDrag : Real = qk * wetted * cf * viscous_form_factor * foul + mass * g * wave_coefficient * fn * fn * fn * fn;
        attribute resistance : Real = hullDrag + dk + dr;
        attribute sailX : Real = sail_x_fraction * lwl_m;
        attribute rudderX : Real = -rudder_arm_fraction * lwl_m;
        attribute heeling : Real = ys * wingZ * ch + ((lk * cb + dk * sb) * keelZ + (lr * cb + dr * sb) * rudderZ + hullDrag * sb * draft / 2) * ch;
        attribute rudderTorque : Real = qr * rudder_m2 * RealFunctions::sqrt(clr * clr + foil_cd0 * foil_cd0) * hinge_fraction * rudderChord + friction_Nm;
        attribute rudderEnvelopeTorque : Real = qr * rudder_m2 * foil_cl_limit * hinge_fraction * rudderChord + friction_Nm;
        attribute waterVMG : Real = (if upwind ? 1 else -1) * v * TrigFunctions::cos(theta + beta);
        attribute wingRe : Real = va * wingChord / nu_air;
        attribute keelRe : Real = v * keelChord / nu_water;
        attribute rudderRe : Real = v * rudder_inflow_ratio * rudderChord / nu_water;
        attribute normalCoefficient : Real = cl*TrigFunctions::cos(alpha)+cd*TrigFunctions::sin(alpha);
        attribute mastMomentCoefficient : Real = aero#(3)*p#(17)+((if s#(5)<0 ? 1-d#(9) else d#(9))-0.5)*normalCoefficient;
        attribute wingTorque : Real = BlueDogWingActuator::MastTorque(rho_air,va,sail_m2,wingChord,mastMomentCoefficient,friction_Nm);
        attribute wingPower : Real [3] ordered nonunique = BlueDogWingActuator::DrivePower(wingTorque,p#(19),p#(3),p#(2),p#(4),p#(5),p#(6),p#(7),p#(8));
        attribute rudderPower : Real [3] ordered nonunique = BlueDogWingActuator::DrivePower(rudderTorque,p#(20),p#(3),1,1,0.1,p#(9)*rudderTorque,p#(10),1-p#(10));
        attribute averagePower : Real = electronics_W+wingPower#(1)+rudderPower#(1);
        attribute peakPower : Real = electronics_W+wingPower#(2)+rudderPower#(2);
        attribute harvestPower : Real = panel_m2 * peak_irradiance_W_m2 * panel_efficiency * harvest_efficiency * solar_resource_factor;
        attribute nightRate : Real = -averagePower / discharge_efficiency - self_discharge_W;
        attribute dayRate : Real = (if harvestPower >= averagePower ? NumericalFunctions::min((harvestPower - averagePower) * charge_efficiency, charge_C_rate * battery_Wh) else (harvestPower - averagePower) / discharge_efficiency) - self_discharge_W;
        attribute cycleEnergy : Real = dark_hours * nightRate + solar_hours * dayRate;
        attribute reserveMargin : Real = initial_fraction * usable_fraction * battery_Wh + dark_hours * nightRate - reserve_Wh;
        attribute surgeResidual : Real = (drive-resistance)/10;
        attribute swayResidual : Real = (sideNormal-lk-lr)/10;
        attribute yawResidual : Real = (-ys*sailX+(lr*cb+dr*sb)*rudderX-qa*sail_m2*wingChord*mastMomentCoefficient)/10;
        attribute rollResidual : Real = (righting-heeling)/20;
        attribute wingLiftMargin : Real = 1-RealFunctions::abs(cl)/wing_cl_limit;
        attribute keelLiftMargin : Real = 1-RealFunctions::abs(clk)/foil_cl_limit;
        attribute rudderLiftMargin : Real = 1-RealFunctions::abs(clr)/foil_cl_limit;
        attribute keelAngleMargin : Real = 1-RealFunctions::abs(beta*ch)/foilAlphaLimit;
        attribute rudderAngleMargin : Real = 1-RealFunctions::abs((beta+delta)*ch)/foilAlphaLimit;
        attribute wingDriveMargin : Real = 1-load_factor*wingTorque/d#(19);
        attribute rudderDriveMargin : Real = 1-load_factor*rudderEnvelopeTorque/d#(20);
        attribute froudeMargin : Real = 1-fn/max_froude;
        attribute wingReMargin : Real = wingRe/min_wing_Re-1;
        attribute keelReMargin : Real = keelRe/min_foil_Re-1;
        attribute rudderReMargin : Real = rudderRe/min_foil_Re-1;
        attribute cycleMargin : Real = cycleEnergy/100;
        attribute reserveMarginScaled : Real = reserveMargin/100;
        attribute peakMargin : Real = (discharge_C_rate*battery_Wh-peakPower/discharge_efficiency-self_discharge_W)/100;
        attribute wingResultant : Real = qa*sail_m2*RealFunctions::sqrt(cl*cl+cd*cd);
        attribute keelResultant : Real = RealFunctions::sqrt(lk*lk+dk*dk);
        attribute rudderResultant : Real = RealFunctions::sqrt(lr*lr+dr*dr);
        return result : Real [*] ordered nonunique;
        (surgeResidual, swayResidual, yawResidual, rollResidual, wingLiftMargin, keelLiftMargin, rudderLiftMargin, keelAngleMargin, rudderAngleMargin, wingDriveMargin, rudderDriveMargin, froudeMargin, wingReMargin, keelReMargin, rudderReMargin, cycleMargin, reserveMarginScaled, peakMargin, waterVMG, v, cl, cd, clk, clr, drive, resistance, heeling, righting, wingTorque, rudderTorque, averagePower, peakPower, harvestPower, cycleEnergy, reserveMargin, wingRe, keelRe, rudderRe, ys, lk, lr, hullDrag, dk, dr, wingResultant, keelResultant, rudderResultant)
    }
    dependency sustained from Evaluate to BlueDogRequirements::sustainedEnergyFeasibility;
    dependency progress from Evaluate to BlueDogRequirements::legProgress;
    dependency control from Evaluate to BlueDogRequirements::capsizeControlRecovery;
    calc def DesignMargins {
        in d : Real [28] ordered nonunique;
        in p : Real [38] ordered nonunique;
        in m : Real [21] ordered nonunique;
        in g : Real [51] ordered nonunique;
        in r : Real [10] ordered nonunique;
        in loads : Real [3] ordered nonunique;
        in waterline : Real;
        doc /* Global bending uses the worst-direction thin-skin section modulus.
         * Proof-tip, ballast lateral inertia and operating loads are separate maxima.
         * No FDM bending credit; no buckling, fatigue, impact or joint qualification. */
        attribute modulus : Real = r#(1)*p#(14);
        attribute allowable : Real = r#(2)*p#(14);
        attribute hullI : Real = g#(9)*m#(18);
        attribute wingI : Real = g#(21)*m#(19);
        attribute keelI : Real = g#(33)*m#(20);
        attribute rudderI : Real = g#(45)*m#(21);
        attribute wingSpan : Real = RealFunctions::sqrt(d#(5)*d#(6));
        attribute wingForce : Real = loads#(1)*p#(36);
        attribute keelForce : Real = loads#(2)*p#(36);
        attribute rudderForce : Real = loads#(3)*p#(36);
        attribute hullMoment : Real = m#(1)*p#(35)*d#(1)/4;
        attribute wingMoment : Real = NumericalFunctions::max(wingForce/2,r#(4))*wingSpan;
        attribute keelTipForce : Real = NumericalFunctions::max(r#(4),d#(16)*p#(35)*p#(36));
        attribute keelMoment : Real = NumericalFunctions::max(keelForce/2,keelTipForce)*d#(12);
        attribute rudderMoment : Real = NumericalFunctions::max(rudderForce/2,r#(4))*d#(14);
        attribute hullStressMargin : Real = 1-hullMoment/(g#(10)*m#(18)*allowable);
        attribute wingStressMargin : Real = 1-wingMoment/(g#(22)*m#(19)*allowable);
        attribute keelStressMargin : Real = 1-keelMoment/(g#(34)*m#(20)*allowable);
        attribute rudderStressMargin : Real = 1-rudderMoment/(g#(46)*m#(21)*allowable);
        attribute hullDeflectionMargin : Real = 1-5*2*m#(1)*p#(35)*d#(1)*d#(1)/(384*modulus*hullI*r#(9));
        attribute wingDeflectionMargin : Real = 1-NumericalFunctions::max(wingForce/8,r#(4)/3)*wingSpan*wingSpan/(modulus*wingI*r#(8));
        attribute keelDeflectionMargin : Real = 1-NumericalFunctions::max(keelForce/8,keelTipForce/3)*d#(12)*d#(12)/(modulus*keelI*r#(8));
        attribute rudderDeflectionMargin : Real = 1-NumericalFunctions::max(rudderForce/8,r#(4)/3)*d#(14)*d#(14)/(modulus*rudderI*r#(8));
        attribute panelStressMargin : Real = 1-0.75*r#(3)*d#(25)*d#(25)/(m#(18)*m#(18)*allowable);
        attribute panelDeflectionMargin : Real = 1-5*r#(3)*d#(25)*d#(25)*d#(25)/(32*modulus*m#(18)*m#(18)*m#(18)*r#(10));
        attribute bodyAssembly : Real = m#(2)+m#(5)+m#(7)+m#(8)+m#(9)+m#(10);
        attribute bodyHandlingMargin : Real = 1-bodyAssembly/p#(37);
        attribute wingHandlingMargin : Real = 1-m#(3)/p#(37);
        attribute keelHandlingMargin : Real = 1-(m#(4)+d#(16))/p#(37);
        attribute batteryHandlingMargin : Real = 1-m#(6)/p#(37);
        attribute freeboardMargin : Real = (d#(4)-waterline)/r#(5)-1;
        attribute reserveVolumeMargin : Real = p#(32)*g#(5)/((1+r#(6))*m#(1))-1;
        attribute launchDepthMargin : Real = (r#(7)-(waterline-(2*g#(51)+d#(3)+d#(12))))/r#(7);
        attribute panelAreaMargin : Real = p#(38)*TrigFunctions::pi*d#(1)*d#(2)/(4*d#(18))-1;
        attribute hullPackingMargin : Real = 1-m#(14)/g#(5);
        attribute wingPackingMargin : Real = 1-m#(15)/g#(17);
        attribute keelPackingMargin : Real = 1-m#(16)/g#(29);
        attribute rudderPackingMargin : Real = 1-m#(17)/g#(41);
        return result : Real [*] ordered nonunique;
        (hullStressMargin,wingStressMargin,keelStressMargin,rudderStressMargin,hullDeflectionMargin,wingDeflectionMargin,keelDeflectionMargin,rudderDeflectionMargin,panelStressMargin,panelDeflectionMargin,bodyHandlingMargin,wingHandlingMargin,keelHandlingMargin,batteryHandlingMargin,freeboardMargin,reserveVolumeMargin,launchDepthMargin,panelAreaMargin,hullPackingMargin,wingPackingMargin,keelPackingMargin,rudderPackingMargin)
    }
    dependency strength from DesignMargins to BlueDogStructure::structuralIntegrity;
    dependency handling from DesignMargins to BlueDogRequirements::liftMass;
    calc def TackAverage {
        in a : Real; in b : Real; in lateralA : Real; in lateralB : Real;
        return vmg : Real;
        (a*RealFunctions::abs(lateralB)+b*RealFunctions::abs(lateralA))/(RealFunctions::abs(lateralA)+RealFunctions::abs(lateralB))
    }
    calc def Route {
        in water : Real [8] ordered nonunique;
        in states : Real [48] ordered nonunique;
        in policy : Real [6] ordered nonunique;
        doc /* Cases ordered by wind 5 then 8 m/s, windward then leeward, tack + then -.
         * Each state contains speed, heading, incidence, leeway, rudder and heel.
         * Tack times cancel crosswind displacement. Equal route fractions per wind
         * and 0.5/1.0 m/s downstream current are illustrative, not weather evidence. */
        attribute cross0 : Real = states#(1)*TrigFunctions::sin(TrigFunctions::rad(states#(2)+states#(4)));
        attribute cross1 : Real = states#(7)*TrigFunctions::sin(TrigFunctions::rad(states#(8)+states#(10)));
        attribute cross2 : Real = states#(13)*TrigFunctions::sin(TrigFunctions::rad(states#(14)+states#(16)));
        attribute cross3 : Real = states#(19)*TrigFunctions::sin(TrigFunctions::rad(states#(20)+states#(22)));
        attribute cross4 : Real = states#(25)*TrigFunctions::sin(TrigFunctions::rad(states#(26)+states#(28)));
        attribute cross5 : Real = states#(31)*TrigFunctions::sin(TrigFunctions::rad(states#(32)+states#(34)));
        attribute cross6 : Real = states#(37)*TrigFunctions::sin(TrigFunctions::rad(states#(38)+states#(40)));
        attribute cross7 : Real = states#(43)*TrigFunctions::sin(TrigFunctions::rad(states#(44)+states#(46)));
        attribute vmg0 : Real = TackAverage(water#(1),water#(2),cross0,cross1);
        attribute vmg1 : Real = TackAverage(water#(3),water#(4),cross2,cross3);
        attribute vmg2 : Real = TackAverage(water#(5),water#(6),cross4,cross5);
        attribute vmg3 : Real = TackAverage(water#(7),water#(8),cross6,cross7);
        attribute downstream : Real = policy#(1)*(vmg0+vmg2)/2+(policy#(2)+policy#(3))/2;
        attribute upstream : Real = policy#(1)*(vmg1+vmg3)/2-(policy#(2)+policy#(3))/2;
        attribute duration : Real = if downstream>0 and upstream>0 ? policy#(4)/3600*(1/downstream+1/upstream) else 1000000.0;
        return result : Real [6] ordered nonunique;
        (downstream/policy#(6)-1,upstream/policy#(6)-1,1-duration/policy#(5),downstream,upstream,duration)
    }
    dependency routeProgress from Route to BlueDogRequirements::legProgress;
    dependency routeTime from Route to BlueDogRequirements::passageDuration;
}
