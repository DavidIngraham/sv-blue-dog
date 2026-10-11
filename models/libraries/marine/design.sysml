package MarineDesign {
    private import ScalarValues::*;
    doc /* Named SI numerical contract for a hull, rotating wing, keel and rudder.
     * Names carry units: metres, square metres, kg, Wh, Nm, kg/m2 and rad/s.
     * Fractions and scales are dimensionless. Arrays exist only at the compiled
     * numerical boundary; application configurations own values and evidence. */
    part def Design {
        attribute length_m : Real;
        attribute beam_m : Real;
        attribute bottom_depth_m : Real;
        attribute deck_height_m : Real;
        attribute sail_m2 : Real;
        attribute sail_AR : Real;
        attribute camber_scale : Real;
        attribute wing_thickness_scale : Real;
        attribute mast_fraction : Real;
        attribute mast_x_fraction : Real;
        attribute keel_m2 : Real;
        attribute keel_span_m : Real;
        attribute rudder_m2 : Real;
        attribute rudder_span_m : Real;
        attribute rudder_arm_fraction : Real;
        attribute ballast_kg : Real;
        attribute battery_Wh : Real;
        attribute panel_m2 : Real;
        attribute wing_torque_Nm : Real;
        attribute rudder_torque_Nm : Real;
        attribute hull_glass_kg_m2 : Real;
        attribute wing_glass_kg_m2 : Real;
        attribute keel_glass_kg_m2 : Real;
        attribute rudder_glass_kg_m2 : Real;
        attribute hull_rib_pitch_m : Real;
        attribute foil_rib_pitch_m : Real;
        attribute battery_x_fraction : Real;
        attribute battery_z_fraction : Real;
        attribute hull_fullness_exponent : Real;
    }
    calc def DesignVector {
        in value : Design;
        return vector : Real [29] ordered nonunique;
        (value.length_m, value.beam_m, value.bottom_depth_m, value.deck_height_m, value.sail_m2, value.sail_AR, value.camber_scale, value.wing_thickness_scale, value.mast_fraction, value.mast_x_fraction, value.keel_m2, value.keel_span_m, value.rudder_m2, value.rudder_span_m, value.rudder_arm_fraction, value.ballast_kg, value.battery_Wh, value.panel_m2, value.wing_torque_Nm, value.rudder_torque_Nm, value.hull_glass_kg_m2, value.wing_glass_kg_m2, value.keel_glass_kg_m2, value.rudder_glass_kg_m2, value.hull_rib_pitch_m, value.foil_rib_pitch_m, value.battery_x_fraction, value.battery_z_fraction, value.hull_fullness_exponent)
    }
    part def Parameters {
        attribute resinGlassRatio : Real;
        attribute gearboxEfficiency : Real;
        attribute motorEfficiency : Real;
        attribute wingNoLoadW : Real;
        attribute wingControllerW : Real;
        attribute wingMotorHoldingW : Real;
        attribute wingMoveFraction : Real;
        attribute wingHoldingFraction : Real;
        attribute rudderHoldingWPerNm : Real;
        attribute rudderMoveFraction : Real;
        attribute electronicsW : Real;
        attribute solarResourceFactor : Real;
        attribute batteryWhKg : Real;
        attribute laminateKnockdown : Real;
        attribute profileCd : Real;
        attribute wingClLimit : Real;
        attribute wingLiftScale : Real;
        attribute wingDragScale : Real;
        attribute wingRateRadS : Real;
        attribute rudderRateRadS : Real;
        attribute driveKgPerNm : Real;
        attribute wingDriveBaseKg : Real;
        attribute fixedEquipmentKg : Real;
        attribute attachmentKg : Real;
        attribute residuaryResistanceFactor : Real;
        attribute viscousFormFactor : Real;
        attribute foilClLimit : Real;
        attribute foilEfficiency : Real;
        attribute foilCd : Real;
        attribute airNu : Real;
        attribute waterNu : Real;
        attribute waterDensity : Real;
        attribute airDensity : Real;
        attribute ballastDensity : Real;
        attribute gravity : Real;
        attribute loadFactor : Real;
        attribute assemblyLimitKg : Real;
        attribute panelCoverage : Real;
    }
    calc def ParametersVector {
        in value : Parameters;
        return vector : Real [38] ordered nonunique;
        (value.resinGlassRatio, value.gearboxEfficiency, value.motorEfficiency, value.wingNoLoadW, value.wingControllerW, value.wingMotorHoldingW, value.wingMoveFraction, value.wingHoldingFraction, value.rudderHoldingWPerNm, value.rudderMoveFraction, value.electronicsW, value.solarResourceFactor, value.batteryWhKg, value.laminateKnockdown, value.profileCd, value.wingClLimit, value.wingLiftScale, value.wingDragScale, value.wingRateRadS, value.rudderRateRadS, value.driveKgPerNm, value.wingDriveBaseKg, value.fixedEquipmentKg, value.attachmentKg, value.residuaryResistanceFactor, value.viscousFormFactor, value.foilClLimit, value.foilEfficiency, value.foilCd, value.airNu, value.waterNu, value.waterDensity, value.airDensity, value.ballastDensity, value.gravity, value.loadFactor, value.assemblyLimitKg, value.panelCoverage)
    }
}
