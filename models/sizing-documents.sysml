package BlueDogSizingDocuments {
    private import DocumentQueries::*;
    calc def Cases :> Query {
        Named(qualifiedName = ("BlueDogSizingExamples::referenceSizing", "BlueDogSizingExamples::lowRigSizing", "BlueDogSizingExamples::slowSizing", "BlueDogSizingExamples::gustSizing", "BlueDogSizingExamples::resistanceSizing"))
    }
    calc def Flow :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Boat speed", path = "boatSpeed"),
            Column(name = "True wind", path = "trueWindSpeed"),
            Column(name = "TWA (rad)", path = "trueWindAngle"),
            Column(name = "Apparent wind", path = "apparentWindSpeed")))
    }
    calc def Inputs :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Bare hull resistance", path = "hullResistance"),
            Column(name = "Sail area", path = "candidateSailArea"),
            Column(name = "Keel area", path = "candidateKeelArea"),
            Column(name = "Rudder area", path = "candidateRudderArea")))
    }
    calc def StabilityInputs :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Effort height", path = "effortHeight"),
            Column(name = "Underwater force depth", path = "lateralForceDepth"),
            Column(name = "Ballast", path = "candidateBallastMass"),
            Column(name = "Other mass", path = "otherMass"),
            Column(name = "Mass budget", path = "massBudget")))
    }
    calc def SailDemand :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Drive roots exist", path = "driveSolutionExists"),
            Column(name = "Min area for drive", path = "minimumSailArea"),
            Column(name = "Upper drive root", path = "maximumDriveSailArea"),
            Column(name = "Max area for heel", path = "maximumHeelSailArea"),
            Column(name = "Drive/heel interval exists", path = "sailIntervalExists")))
    }
    calc def FoilDemand :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Minimum keel area", path = "minimumKeelArea"),
            Column(name = "Minimum rudder area", path = "minimumRudderArea"),
            Column(name = "Ballast required", path = "minimumBallastMass")))
    }
    calc def Geometry :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Keel span", path = "keelSpan"),
            Column(name = "Keel mean chord", path = "keelMeanChord"),
            Column(name = "Rudder span", path = "rudderSpan"),
            Column(name = "Rudder mean chord", path = "rudderMeanChord")))
    }
    calc def Loads :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Drive margin", path = "driveMargin"),
            Column(name = "Keel trim load", path = "keelTrimForce"),
            Column(name = "Rudder trim load (signed)", path = "rudderTrimForce"),
            Column(name = "Heel moment", path = "heelingMoment"),
            Column(name = "Righting moment", path = "availableRightingMoment")))
    }
    calc def Actuation :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Demand torque", path = "requiredRudderTorque"),
            Column(name = "Coefficient-envelope torque", path = "rudderEnvelopeTorque"),
            Column(name = "Available torque", path = "availableTorque"),
            Column(name = "Keel foil root side moment", path = "keelRootSideMoment"),
            Column(name = "Rudder root side moment", path = "rudderRootSideMoment")))
    }
    calc def Scaling :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Sail Reynolds", path = "sailReynolds"),
            Column(name = "Keel Reynolds", path = "keelReynolds"),
            Column(name = "Rudder Reynolds", path = "rudderReynolds"),
            Column(name = "Keel aspect ratio", path = "keelAspectRatio"),
            Column(name = "Rudder aspect ratio", path = "rudderAspectRatio")))
    }
    calc def Gates :> Query {
        Project(source = Cases(), columns = (Column(name = "Case", path = "caseLabel"),
            Column(name = "Drive", path = "driveMet"),
            Column(name = "Heel", path = "heelMet"),
            Column(name = "Keel", path = "keelMet"),
            Column(name = "Rudder", path = "rudderMet"),
            Column(name = "Torque", path = "torqueMet"),
            Column(name = "Mass", path = "massMet"),
            Column(name = "Numerical fit", path = "modeledFit"),
            Column(name = "Supported sizing", path = "supportedSizing")))
    }
    part def SizingReport :> Document {
        attribute redefines title = "Sail, keel and rudder sizing screen";
        part guide : Paragraph { part link : Link { attribute redefines text = "Method, limitations and design interpretation"; attribute redefines target = "appendage-sizing.md"; } }
        part context : Paragraph { attribute redefines text = "Synthetic inputs, not selected hardware. Zero area outputs when driveSolutionExists is false are invalid-result sentinels, not zero demand. Computation validity is distinct from modeledFit and supportedSizing. Read all gates together. Changing geometry or ballast requires resistance and hydrostatics to be updated."; }
        part flowInputs : Section { attribute redefines title = "Flow"; part values : Table { calc rows : Flow; } }
        part inputs : Section { attribute redefines title = "Inputs"; part values : Table { calc rows : Inputs; } }
        part stabilityinputs : Section { attribute redefines title = "StabilityInputs"; part values : Table { calc rows : StabilityInputs; } }
        part saildemand : Section { attribute redefines title = "SailDemand"; part values : Table { calc rows : SailDemand; } }
        part foildemand : Section { attribute redefines title = "FoilDemand"; part values : Table { calc rows : FoilDemand; } }
        part geometry : Section { attribute redefines title = "Geometry"; part values : Table { calc rows : Geometry; } }
        part loads : Section { attribute redefines title = "Loads"; part values : Table { calc rows : Loads; } }
        part actuation : Section { attribute redefines title = "Actuation"; part values : Table { calc rows : Actuation; } }
        part scaling : Section { attribute redefines title = "Scaling"; part values : Table { calc rows : Scaling; } }
        part gates : Section { attribute redefines title = "Gates"; part values : Table { calc rows : Gates; } }
    }
}
