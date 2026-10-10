package BlueDogSailingDocuments {
    private import DocumentQueries::*;
    calc def LegCases :> Query {
        Named(qualifiedName = ("BlueDogSailingExamples::upstreamBeat", "BlueDogSailingExamples::upstreamRun", "BlueDogSailingExamples::downstreamBeat", "BlueDogSailingExamples::downstreamRun", "BlueDogSailingExamples::oceanDemand"))
    }
    calc def PolarDemand :> Query {
        Project(source = LegCases(), columns = (Column(name = "Case", path = "name"),
            Column(name = "Required ground VMG", path = "requiredGroundVMG"),
            Column(name = "Required clean polar speed", path = "requiredCleanPolarSpeed"),
            Column(name = "Knots", path = "requiredCleanKnots")))
    }
    calc def HullScreen :> Query {
        Project(source = LegCases(), columns = (Column(name = "Case", path = "name"),
            Column(name = "Froude at clean demand", path = "requiredCleanFroude"),
            Column(name = "Froude at degraded operating speed", path = "requiredOperatingFroude"),
            Column(name = "Wave-reference waterline at clean demand", path = "equivalentWaveLength")))
    }
    calc def WindDemand :> Query {
        Project(source = Named(qualifiedName = ("BlueDogSailingExamples::lightWindDemand", "BlueDogSailingExamples::upstreamBeat", "BlueDogSailingExamples::strongWindDemand", "BlueDogSailingExamples::highWindDemand")), columns = (
            Column(name = "True wind speed", path = "sampledWindSpeed"),
            Column(name = "Required clean speed / true wind speed", path = "requiredSpeedWindRatio"),
            Column(name = "Evidence ready", path = "evidenceReady")))
    }
    calc def Voyages :> Query {
        Named(qualifiedName = ("BlueDogSailingExamples::westerlyPassage", "BlueDogSailingExamples::easterlyPassage"))
    }
    calc def Passage :> Query {
        Project(source = Voyages(), columns = (Column(name = "Case", path = "name"),
            Column(name = "Allocated hours including holds", path = "allocatedHours"),
            Column(name = "Candidate passage hours", path = "voyageHours"),
            Column(name = "Critical-rate budget per hour", path = "allowableRatePerHour")))
    }
    calc def Evidence :> Query {
        Project(source = Voyages(), columns = (Column(name = "Case", path = "name"),
            Column(name = "Time allocation valid", path = "allocationValid"),
            Column(name = "Candidate numerically feasible", path = "modeledFeasible"),
            Column(name = "Voyage supported by evidence", path = "voyageSupported")))
    }
    calc def Traces :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogSailing")), type = "Dependency"), columns = (
            Column(name = "Dependent model", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Basis", cell = { in row : KerML::Root::Dependency; row.supplier })))
    }
    calc def Inputs :> Query {
        Project(source = Named(qualifiedName = ("BlueDogSailingExamples::upstreamHeadwind", "BlueDogSailingExamples::upstreamTailwind", "BlueDogSailingExamples::downstreamHeadwind", "BlueDogSailingExamples::downstreamTailwind", "BlueDogSailingExamples::oceanIllustration")), columns = (
            Column(name = "Case", path = "label"), Column(name = "Leg distance", path = "distance"),
            Column(name = "Along-current", path = "currentVMG"), Column(name = "Moving-time allocation", path = "allocatedTime")))
    }
    calc def SailingInputs :> Query {
        Project(source = Named(qualifiedName = ("BlueDogSailingExamples::upstreamHeadwind", "BlueDogSailingExamples::upstreamTailwind", "BlueDogSailingExamples::downstreamHeadwind", "BlueDogSailingExamples::downstreamTailwind", "BlueDogSailingExamples::oceanIllustration")), columns = (
            Column(name = "Case", path = "label"), Column(name = "True wind speed", path = "trueWindSpeed"),
            Column(name = "TWA (radians)", path = "trueWindAngle"), Column(name = "Candidate clean boat speed", path = "cleanPolarSpeed"),
            Column(name = "Waterline length", path = "waterlineLength")))
    }
    part def SailingReport :> Document {
        attribute redefines title = "Required polars and hull-speed screening";
        part guide : Paragraph { part link : Link { attribute redefines text = "Method, assumptions and hull-regime interpretation"; attribute redefines target = "sailing-performance.md"; } }
        part context : Paragraph { attribute redefines text = "Synthetic design probes, not measured polars, selected hull dimensions or new mission requirements. The named inputs below are evaluated from the scenario model. The offshore case is a sizing probe, not an approved Hawaii route or operating window."; }
        part inputs : Section { attribute redefines title = "Declared scenario inputs"; part route : Table { calc rows : Inputs; } part sailing : Table { calc rows : SailingInputs; } }
        part polar : Section { attribute redefines title = "Inverse polar demand"; part values : Table { calc rows : PolarDemand; } }
        part hull : Section { attribute redefines title = "Hull screening";
            part meaning : Paragraph { attribute redefines text = "Wave-reference length inverts c = sqrt(g L / (2 pi)). It is neither a minimum allowable hull length nor a planing criterion. Froude numbers use water speed, not ground speed or VMG."; }
            part values : Table { calc rows : HullScreen; }
        }
        part wind : Section { attribute redefines title = "Demand across wind strength";
            part meaning : Paragraph { attribute redefines text = "The mission imposes the same required speed at each sampled wind strength; a measured or validated polar must establish whether that speed is available. No wind-to-speed prediction is made."; }
            part values : Table { calc rows : WindDemand; }
        }
        part passage : Section { attribute redefines title = "Candidate polars through cruise and reliability";
            part meaning : Paragraph { attribute redefines text = "The candidate speeds listed above are synthetic feasibility probes, not predicted polars. Westerly and easterly scenarios use different points of sail; rate assumptions are inherited from the existing cruise illustration."; }
            part values : Table { calc rows : Passage; }
            part evidence : Table { calc rows : Evidence; }
        }
        part trace : Section { attribute redefines title = "Analysis dependencies"; part values : Table { calc rows : Traces; } }
    }
}
