package BlueDogDesignSearchDocuments {
    private import DocumentQueries::*;
    calc def Cases :> Query {
        Named(qualifiedName = ("BlueDogDesignResults::full_envelopeAudit", "BlueDogDesignResults::nominal_5msAudit"))
    }
    calc def Summary :> Query {
        Project(source = Cases(), columns = (
            Column(name = "Study", path = "caseLabel"),
            Column(name = "Bounds valid", path = "boundsValid"),
            Column(name = "Maximum scaled equilibrium error", path = "maxEquilibriumResidual"),
            Column(name = "Minimum scaled margin", path = "minimumMargin"),
            Column(name = "Numerical fit", path = "numericalFeasible"),
            Column(name = "Full scenario set", path = "fullEnvelopeCovered"),
            Column(name = "Evidence accepted", path = "evidenceReady"),
            Column(name = "Supported design", path = "supportedDesign")))
    }
    calc def Passage :> Query {
        Project(source = Cases(), columns = (
            Column(name = "Study", path = "caseLabel"),
            Column(name = "Worst upstream VMG (m/s)", path = "worstGroundVMG"),
            Column(name = "Upstream passage possible", path = "passagePossible"),
            Column(name = "Conservative round trip (h)", path = "conservativeRoundTripHours"),
            Column(name = "Mission time met", path = "missionTimeMet")))
    }
    part def SearchReport :> Document {
        attribute redefines title = "Coupled design search: native replay";
        part guide : Paragraph { part link : Link { attribute redefines text = "Search method, results and limitations"; attribute redefines target = "design-search.md"; } }
        part context : Paragraph { attribute redefines text = "Recomputed from the saved geometry and operating states using the current SysML equations. A valid audit does not mean a feasible design. The nominal study covers only 5 m/s wind; neither study establishes physical compliance. An absent passage duration means upstream progress is nonpositive."; }
        part gates : Section { attribute redefines title = "Numerical checks"; part values : Table { calc rows : Summary; } }
        part passage : Section { attribute redefines title = "Mission consequence"; part values : Table { calc rows : Passage; } }
    }
}
