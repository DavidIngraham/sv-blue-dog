package BlueDogCoupledSizing {
    private import ScalarValues::*;
    private import BlueDogStructure::material;
    doc /* CAD/mesh metrics supply geometry; native calculations own material mass,
     * center of gravity and engineering loads. All numerical process allocations
     * and aerodynamic discrepancy factors remain provisional evidence inputs. */
    analysis Inputs {
        out attribute designNames : String [*] ordered nonunique = ("length_m", "beam_m", "bottom_depth_m", "deck_height_m", "sail_m2", "sail_AR", "camber_scale", "wing_thickness_scale", "mast_fraction", "mast_x_fraction", "keel_m2", "keel_span_m", "rudder_m2", "rudder_span_m", "rudder_arm_fraction", "ballast_kg", "battery_Wh", "panel_m2", "wing_torque_Nm", "rudder_torque_Nm", "hull_glass_kg_m2", "wing_glass_kg_m2", "keel_glass_kg_m2", "rudder_glass_kg_m2", "hull_rib_pitch_m", "foil_rib_pitch_m", "battery_x_fraction", "battery_z_fraction");
        out attribute referenceDesign : Real [*] ordered nonunique = (2, 0.6044368037, 0.0526435889, 0.1632073911, 1.1782673035, 5.2091181581, 1, 1, 0.5, -0.017302668, 0.1417761386, 0.714819707, 0.0120845842, 0.1281684078, 0.5, 11.6735943, 207.468273, 0.231023582, 0.80857335, 0.80857335, 0.6, 0.4, 4.8, 0.4, 0.02975075, 0.04, 0, 0.1);
        out attribute parameterNames : String [*] ordered nonunique = ("resinGlassRatio", "gearboxEfficiency", "motorEfficiency", "wingNoLoadW", "wingControllerW", "wingMotorHoldingW", "wingMoveFraction", "wingHoldingFraction", "rudderHoldingWPerNm", "rudderMoveFraction", "electronicsW", "solarResourceFactor", "batteryWhKg", "laminateKnockdown", "profileCd", "wingClLimit", "wingLiftScale", "wingDragScale", "wingRateRadS", "rudderRateRadS", "driveKgPerNm", "wingDriveBaseKg", "fixedEquipmentKg", "attachmentKg", "waveDragCoefficient", "viscousFormFactor", "foilClLimit", "foilEfficiency", "foilCd", "airNu", "waterNu", "waterDensity", "airDensity", "ballastDensity", "gravity", "loadFactor", "assemblyLimitKg", "panelCoverage");
        out attribute parameterValues : Real [*] ordered nonunique = (1, 0.4, 0.8, 1, 0.1, 0, 0.02, 0.98, 0.5, 0.05, 4.5, 0.6, 140, 1, 0.025, 1, 0.85, 1.15, 0.25, 0.6, 0.15, 0.2, 2.5, 0.6, 0.35, 1.15, 0.8, 0.7, 0.012, 1.5e-05, 1e-06, 1000, 1.225, 7800, 9.80665, 1.5, 15, 0.6);
        out attribute materialValues : Real [*] ordered nonunique = (material.tapeWidth, material.printTile, material.tapeDryMass, material.petgDensity, material.hullPrintWall, material.finishingMass, material.ribHeight, material.glassDensity, material.epoxyDensity, material.foilPrintWall);
    }
    calc def MassProperties {
        in d : Real [28] ordered nonunique;
        in p : Real [38] ordered nonunique;
        in m : Real [10] ordered nonunique;
        in geometry : Real [51] ordered nonunique;
        doc /* Four bodies: hull, wing, keel, rudder. Each geometry block is
         * skin area; skin centroid XYZ; enclosed volume; volume centroid XYZ;
         * minimum thin-wall inertia/thickness; worst bending modulus/thickness;
         * root enclosed area; root perimeter. Last three inputs: ballast centroid XYZ. Geometry units are SI.
         * Foil ribs are unperforated transverse diaphragms. Hull ribs follow
         * a surface-density allocation. Neither earns FDM bending credit. */
        attribute seamKgM2 : Real = 2*m#(1)/m#(2)*m#(3)*(1+p#(1));
        attribute hullSkinKg : Real = geometry#(1)*(m#(4)*m#(5)+d#(21)*(1+p#(1))+m#(6)+seamKgM2);
        attribute hullRibVolume : Real = geometry#(1)*2*m#(5)*m#(7)/d#(25);
        attribute hullRibKg : Real = m#(4)*hullRibVolume;
        attribute hullMass : Real = hullSkinKg+hullRibKg;
        attribute hullMaterialVolume : Real = geometry#(1)*(m#(5)+d#(21)/m#(8)+d#(21)*p#(1)/m#(9))+hullRibVolume;
        attribute wingSkinKg : Real = geometry#(13)*(m#(4)*m#(10)+d#(22)*(1+p#(1))+m#(6)+seamKgM2);
        attribute wingRibVolume : Real = geometry#(17)*m#(5)/d#(26);
        attribute wingRibKg : Real = m#(4)*wingRibVolume;
        attribute wingMass : Real = wingSkinKg+wingRibKg;
        attribute wingMaterialVolume : Real = geometry#(13)*(m#(10)+d#(22)/m#(8)+d#(22)*p#(1)/m#(9))+wingRibVolume;
        attribute keelSkinKg : Real = geometry#(25)*(m#(4)*m#(10)+d#(23)*(1+p#(1))+m#(6)+seamKgM2);
        attribute keelRibVolume : Real = geometry#(29)*m#(5)/d#(26);
        attribute keelRibKg : Real = m#(4)*keelRibVolume;
        attribute keelMass : Real = keelSkinKg+keelRibKg;
        attribute keelMaterialVolume : Real = geometry#(25)*(m#(10)+d#(23)/m#(8)+d#(23)*p#(1)/m#(9))+keelRibVolume;
        attribute rudderSkinKg : Real = geometry#(37)*(m#(4)*m#(10)+d#(24)*(1+p#(1))+m#(6)+seamKgM2);
        attribute rudderRibVolume : Real = geometry#(41)*m#(5)/d#(26);
        attribute rudderRibKg : Real = m#(4)*rudderRibVolume;
        attribute rudderMass : Real = rudderSkinKg+rudderRibKg;
        attribute rudderMaterialVolume : Real = geometry#(37)*(m#(10)+d#(24)/m#(8)+d#(24)*p#(1)/m#(9))+rudderRibVolume;
        attribute batteryMass : Real = d#(17)/p#(13);
        attribute panelMass : Real = 2*d#(18);
        attribute wingDriveMass : Real = p#(22)+p#(21)*d#(19);
        attribute rudderDriveMass : Real = 0.08+p#(21)*d#(20);
        attribute equipmentMass : Real = p#(23)+p#(24);
        attribute totalMass : Real = hullMass+wingMass+keelMass+rudderMass+d#(16)+batteryMass+panelMass+wingDriveMass+rudderDriveMass+equipmentMass;
        attribute moment0 : Real = hullSkinKg*geometry#(2)+hullRibKg*geometry#(2)+wingSkinKg*geometry#(14)+wingRibKg*geometry#(18)+keelSkinKg*geometry#(26)+keelRibKg*geometry#(30)+rudderSkinKg*geometry#(38)+rudderRibKg*geometry#(42)+batteryMass*d#(27)*d#(1)+wingDriveMass*d#(10)*d#(1)+-rudderDriveMass*d#(15)*d#(1)+d#(16)*geometry#(49);
        attribute moment1 : Real = hullSkinKg*geometry#(3)+hullRibKg*geometry#(3)+wingSkinKg*geometry#(15)+wingRibKg*geometry#(19)+keelSkinKg*geometry#(27)+keelRibKg*geometry#(31)+rudderSkinKg*geometry#(39)+rudderRibKg*geometry#(43)+d#(16)*geometry#(50);
        attribute moment2 : Real = hullSkinKg*geometry#(4)+hullRibKg*geometry#(4)+wingSkinKg*geometry#(16)+wingRibKg*geometry#(20)+keelSkinKg*geometry#(28)+keelRibKg*geometry#(32)+rudderSkinKg*geometry#(40)+rudderRibKg*geometry#(44)+d#(16)*geometry#(51)+batteryMass*(-d#(3)+(d#(3)+d#(4))*d#(28))+panelMass*d#(4)+-(wingDriveMass+rudderDriveMass+equipmentMass)*d#(3)/2;
        return result : Real [*] ordered nonunique;
        (totalMass, hullMass, wingMass, keelMass, rudderMass, batteryMass, panelMass, wingDriveMass, rudderDriveMass, equipmentMass,
         moment0/totalMass,moment1/totalMass,moment2/totalMass,
         hullMaterialVolume,wingMaterialVolume,keelMaterialVolume,rudderMaterialVolume,
         d#(21)/m#(8)+d#(21)*p#(1)/m#(9), d#(22)/m#(8)+d#(22)*p#(1)/m#(9), d#(23)/m#(8)+d#(23)*p#(1)/m#(9), d#(24)/m#(8)+d#(24)*p#(1)/m#(9))
    }
    dependency manufacturing from MassProperties to BlueDogStructure::hybridConstruction;
    dependency handling from MassProperties to BlueDogRequirements::liftMass;
    dependency geometryRecovery from MassProperties to BlueDogRequirements::selfRighting;
}
