package BlueDogReliabilityDocuments {
    private import DocumentQueries::*;
    calc def Modes :> Query {
        Named(qualifiedName = ("BlueDogDFMEA::starter::hullLeak", "BlueDogDFMEA::starter::keelLoss", "BlueDogDFMEA::starter::steeringJam", "BlueDogDFMEA::starter::sailJam", "BlueDogDFMEA::starter::batteryFault", "BlueDogDFMEA::starter::harvestLoss", "BlueDogDFMEA::starter::powerCommonCause", "BlueDogDFMEA::starter::navigationFault", "BlueDogDFMEA::starter::controlLockup", "BlueDogDFMEA::starter::trafficMiss", "BlueDogDFMEA::starter::radioLoss", "BlueDogDFMEA::starter::motorUncommanded"))
    }
    calc def Functions :> Query {
        Project(source = Modes(), columns = (Column(name = "ID", path = "identifier"),
            Column(name = "Model element", path = "name"), Column(name = "Function", path = "intendedFunction"), Column(name = "Failure mode", path = "failureMode")))
    }
    calc def Effects :> Query {
        Project(source = Modes(), columns = (Column(name = "ID", path = "identifier"),
            Column(name = "Cause", path = "cause"), Column(name = "Local effect", path = "localEffect"), Column(name = "Mission effect", path = "missionEffect")))
    }
    calc def Actions :> Query {
        Project(source = Modes(), columns = (Column(name = "ID", path = "identifier"),
            Column(name = "Proposed detection", path = "proposedDetection"), Column(name = "Recommended action", path = "recommendedAction"), Column(name = "Owner role", path = "ownerRole")))
    }
    calc def Dispositions :> Query {
        Project(source = Modes(), columns = (Column(name = "ID", path = "identifier"),
            Column(name = "Safety-critical", path = "safetyCritical"), Column(name = "Disposition accepted", path = "dispositionAccepted"),
            Column(name = "Action evidence accepted", path = "actionEvidenceAccepted"), Column(name = "Evidence", path = "evidenceReference")))
    }
    calc def Traces :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogDFMEA")), type = "Dependency"),
            columns = (Column(name = "From", cell = { in row : KerML::Root::Dependency; row.client }),
                       Column(name = "To", cell = { in row : KerML::Root::Dependency; row.supplier })))
    }
    part def DFMEA :> Document {
        attribute redefines title = "Initial architecture DFMEA";
        part intro : Paragraph { attribute redefines text = "Initial hypotheses for the logical architecture. Detection and prevention actions are proposed, not implemented controls. Risks are unassessed; no probabilities or RPNs are assigned. Scope completeness and every disposition remain open. Read cruise-reliability.md for the exposure model."; }
        part functions : Section { attribute redefines title = "Functions and failure modes"; part rows : Table { calc rows : Functions; } }
        part guide : Paragraph { part link : Link { attribute redefines text = "Cruise and reliability analysis guide"; attribute redefines target = "cruise-reliability.md"; } }
        part effects : Section { attribute redefines title = "Causes and effects"; part rows : Table { calc rows : Effects; } }
        part actions : Section { attribute redefines title = "Detection, actions and evidence"; part rows : Table { calc rows : Actions; } }
        part dispositions : Section { attribute redefines title = "Disposition and evidence"; part rows : Table { calc rows : Dispositions; } }
        part traces : Section { attribute redefines title = "Architecture and requirement links"; part rows : Table { calc rows : Traces; } }
    }
    calc def PassageSummary :> Query {
        Project(source = Named(qualifiedName = "BlueDogReliabilityExamples::gorgeAssessment"),
            columns = (Column(name = "Voyage hours", path = "voyageHours"), Column(name = "Ground speeds", path = "groundSpeeds")))
    }
    calc def BudgetSummary :> Query {
        Project(source = Named(qualifiedName = "BlueDogReliabilityExamples::gorgeAssessment"),
            columns = (Column(name = "Maximum critical failures/hour", path = "allowableRatePerHour"), Column(name = "Modeled reliability", path = "modeledReliability")))
    }
    calc def EvidenceSummary :> Query {
        Project(source = Named(qualifiedName = "BlueDogReliabilityExamples::gorgeAssessment"),
            columns = (Column(name = "Required zero-failure hours", path = "requiredZeroFailureHours"),
                Column(name = "Evidence ready", path = "evidenceReady"), Column(name = "Reliability supported", path = "reliabilitySupported")))
    }
    part def CruiseReport :> Document {
        attribute redefines title = "Cruise and reliability example results";
        part intro : Paragraph { attribute redefines text = "Synthetic sensitivity example, not measured boat performance, a surveyed route, or a reliability demonstration. See cruise-reliability.md for assumptions, equations and evidence requirements."; }
        part guide : Paragraph { part link : Link { attribute redefines text = "Cruise and reliability analysis guide"; attribute redefines target = "cruise-reliability.md"; } }
        part passage : Section { attribute redefines title = "Passage exposure"; part values : Table { calc rows : PassageSummary; } }
        part budget : Section { attribute redefines title = "Conditional failure budget"; part values : Table { calc rows : BudgetSummary; } }
        part evidence : Section { attribute redefines title = "Evidence gate"; part values : Table { calc rows : EvidenceSummary; } }
    }
}
