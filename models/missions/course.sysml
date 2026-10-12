package TransGorgeCourse {
    private import ScalarValues::*;

    part def MarkerGate {
        attribute markerName : String;
        attribute lightListNumber : Integer;
        attribute longitudeDeg : Real;
        attribute latitudeDeg : Real;
        attribute bearingFromMarkerDeg : Real;
        attribute nearOffsetM : Real;
        attribute farOffsetM : Real;
        attribute sourceCell : String;
        attribute sourceEditionUpdate : String;
    }

    part west : MarkerGate {
        attribute :>> markerName = "Bonneville Pool Light 7";
        attribute :>> lightListNumber = 11790;
        attribute :>> longitudeDeg = -121.9105283;
        attribute :>> latitudeDeg = 45.655125;
        attribute :>> bearingFromMarkerDeg = 135;
        attribute :>> nearOffsetM = 80;
        attribute :>> farOffsetM = 220;
        attribute :>> sourceCell = "US5WA3CJ";
        attribute :>> sourceEditionUpdate = "2.1";
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed Bonneville-reach virtual turnaround, upstream of the dam/lock approaches. Light 7 supplies a fixed reference; the gate extends southeast into charted water, not to the structure. NOAA ENC coordinates agree with USCG LLNR 11790 in the 2026-10-07 Light List. Offset distances are project allocations, not statutory stand-offs. The gate overlaps the navigation fairway; a crossing must not impede channel traffic."; }
    }

    part east : MarkerGate {
        attribute :>> markerName = "Bonneville Pool Lighted Buoy 69";
        attribute :>> lightListNumber = 12130;
        attribute :>> longitudeDeg = -121.1478525;
        attribute :>> latitudeDeg = 45.6092578;
        attribute :>> bearingFromMarkerDeg = 180;
        attribute :>> nearOffsetM = 80;
        attribute :>> farOffsetM = 220;
        attribute :>> sourceCell = "US5WA3CT";
        attribute :>> sourceEditionUpdate = "2.0";
        metadata rationale : ModelingMetadata::Rationale { text = "Proposed start/finish west of The Dalles highway bridge and dam restrictions. Use the published nominal buoy position, not its instantaneous swinging position. The southward offset lies in charted depth areas; the gate overlaps the fairway. No rounding of, contact with, or attachment to the buoy is required. NOAA ENC and 2026-10-07 Light List LLNR 12130 identify the reference."; }
    }

    part temporaryWorks {
        attribute longitudeDeg : Real = -121.5225;
        attribute latitudeDeg : Real = 45.7283333333;
        attribute screeningRadiusM : Real = 250;
        metadata rationale : ModelingMetadata::Rationale { text = "2026-10-07 Northwest LNM week 40 page 2 locates railroad bridge work at White Salmon confluence, RM 168.2, through 2026-12-31. The derrick barge stays on station outside work hours. Source: https://www.navcen.uscg.gov/sites/default/files/pdf/lnms/lnm13402026.pdf . Exclude a 250 m analysis buffer around the published point for this snapshot."; }
        metadata issue : ModelingMetadata::Issue { text = "The radius is a conservative scenario allocation, not a surveyed work footprint or statutory stand-off. Replace with confirmed work extent and current notices before release; do not silently expire this exclusion using the computer clock."; }
    }
    part policy {
        attribute coordinateDatum : String = "WGS84 longitude/latitude degrees; bearings clockwise from true north; offsets in meters";
        attribute chartEvidence : String = "evidence/course/2026-10-11/chart-features.geojson";
        attribute sourceCatalog : String = "https://www.charts.noaa.gov/ENCs/ENCProdCat_19115.xml";
        attribute sourceLightList : String = "https://www.navcen.uscg.gov/sites/default/files/pdf/lightLists/weeklyUpdates/v6WeeklyChanges.pdf";
        attribute chartCatalogDate : String = "2026-10-10";
        attribute lightListDate : String = "2026-10-07";
        attribute gatesAcceptedForLaunch : Boolean = false;
        attribute damTransitPermitted : Boolean = false;
        attribute lockApproachTransitPermitted : Boolean = false;
        attribute hasCompletionDeadline : Boolean = false;
        attribute minimumChartDepthM : Real = 2;
        attribute shoreClearanceM : Real = 30;
        attribute restrictionClearanceM : Real = 50;
        attribute obstacleClearanceM : Real = 30;
        attribute routingGridM : Real = 40;
        metadata routingRationale : ModelingMetadata::Rationale { text = "Initial routing allocations for the small-vessel analysis: chart depth at least 2 m, 30 m from charted land/obstructions and 50 m from excluded charted areas. These are project planning margins, not legal stand-off distances. Actual draft, pool stage, maneuvering, uncertainty and bridge clearances require separate assessment. Grid resolution is a numerical setting, not a vessel requirement."; }
        attribute gateNames : String [4] ordered nonunique = ("eastGate", "westGate", "westGate", "eastGate");
        attribute gateDirections : Integer [4] ordered nonunique = (-1,-1,1,1);
        attribute crossingSequence : String = "Cross east gate downstream to start; cross west gate downstream then upstream to turn; cross east gate upstream to finish. Count finite-segment crossings in this order; touching a line without changing side is not a crossing.";
        metadata rationale : ModelingMetadata::Rationale { text = "The route stays in Bonneville Pool. Gate segments are defined relative to existing aids, with 80 m minimum nominal marker offset. Chart-derived polygons, water depth and local notices constrain route planning; neither the marker-to-marker chord nor the commercial fairway is the whole permitted sailing corridor. Completion has no elapsed-time deadline. A computational horizon reports censoring rather than failure."; }
        metadata issue : ModelingMetadata::Issue { text = "Gate proposal for mission analysis, not a launch release. Verify complete segment clearance and maneuvering/drift margins, current MSI notices, current pool stage, bridge passage and autonomous traffic avoidance. A route through charted water does not establish safe operation. No universal vessel stand-off distance is inferred from navigation rules."; }
    }
    dependency courseBasis from policy to GorgeChallenge::courseCompletion;

    analysis GateGeometry {
        out attribute temporaryWorks : Real [3] ordered nonunique = (TransGorgeCourse::temporaryWorks.longitudeDeg, TransGorgeCourse::temporaryWorks.latitudeDeg, TransGorgeCourse::temporaryWorks.screeningRadiusM);
        out attribute westGate : Real [5] ordered nonunique = (west.longitudeDeg, west.latitudeDeg, west.bearingFromMarkerDeg, west.nearOffsetM, west.farOffsetM);
        out attribute eastGate : Real [5] ordered nonunique = (east.longitudeDeg, east.latitudeDeg, east.bearingFromMarkerDeg, east.nearOffsetM, east.farOffsetM);
        out attribute routing : Real [5] ordered nonunique = (policy.minimumChartDepthM, policy.shoreClearanceM, policy.restrictionClearanceM, policy.obstacleClearanceM, policy.routingGridM);
    }
}
