package MarineMass {
    private import ScalarValues::*;

    calc def MassProperties {
        in d : Real [29] ordered nonunique;
        in p : Real [41] ordered nonunique;
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
        attribute equipmentMass : Real = p#(23)+p#(24)+p#(39);
        attribute totalMass : Real = hullMass+wingMass+keelMass+rudderMass+d#(16)+batteryMass+panelMass+wingDriveMass+rudderDriveMass+equipmentMass;
        attribute moment0 : Real = hullSkinKg*geometry#(2)+hullRibKg*geometry#(2)+wingSkinKg*geometry#(14)+wingRibKg*geometry#(18)+keelSkinKg*geometry#(26)+keelRibKg*geometry#(30)+rudderSkinKg*geometry#(38)+rudderRibKg*geometry#(42)+batteryMass*d#(27)*d#(1)+wingDriveMass*d#(10)*d#(1)+-rudderDriveMass*d#(15)*d#(1)+d#(16)*geometry#(49)+p#(39)*p#(40)*d#(1);
        attribute moment1 : Real = hullSkinKg*geometry#(3)+hullRibKg*geometry#(3)+wingSkinKg*geometry#(15)+wingRibKg*geometry#(19)+keelSkinKg*geometry#(27)+keelRibKg*geometry#(31)+rudderSkinKg*geometry#(39)+rudderRibKg*geometry#(43)+d#(16)*geometry#(50);
        attribute moment2 : Real = hullSkinKg*geometry#(4)+hullRibKg*geometry#(4)+wingSkinKg*geometry#(16)+wingRibKg*geometry#(20)+keelSkinKg*geometry#(28)+keelRibKg*geometry#(32)+rudderSkinKg*geometry#(40)+rudderRibKg*geometry#(44)+d#(16)*geometry#(51)+batteryMass*(-d#(3)+(d#(3)+d#(4))*d#(28))+panelMass*d#(4)+-(wingDriveMass+rudderDriveMass+equipmentMass-p#(39))*d#(3)/2+p#(39)*(d#(4)+p#(41));
        return result : Real [*] ordered nonunique;
        (totalMass, hullMass, wingMass, keelMass, rudderMass, batteryMass, panelMass, wingDriveMass, rudderDriveMass, equipmentMass,
         moment0/totalMass,moment1/totalMass,moment2/totalMass,
         hullMaterialVolume,wingMaterialVolume,keelMaterialVolume,rudderMaterialVolume,
         d#(21)/m#(8)+d#(21)*p#(1)/m#(9), d#(22)/m#(8)+d#(22)*p#(1)/m#(9), d#(23)/m#(8)+d#(23)*p#(1)/m#(9), d#(24)/m#(8)+d#(24)*p#(1)/m#(9))
    }
}
