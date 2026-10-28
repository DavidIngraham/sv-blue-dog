package BlueDogSafetyDocuments {
    private import DocumentQueries::*;
    calc def Hazards :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogSafety::gorge")),
            type = "BlueDogSafety::HazardRecord"), columns = (
            Column(name = "ID", path = "identifier"), Column(name = "Condition", path = "condition"),
            Column(name = "Potential mishap", path = "potentialMishap"), Column(name = "Modes", path = "modes"),
            Column(name = "Owner role", path = "ownerRole"), Column(name = "Configuration", path = "configuration"),
            Column(name = "Control intent", path = "controlIntent")))
    }
    calc def Basis :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogSafety")),
            type = "Dependency"), columns = (
            Column(name = "Link", path = "name"),
            Column(name = "Client", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Supporting element", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    calc def Dispositions :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogSafety::gorge")),
            type = "BlueDogSafety::HazardRecord"), columns = (
            Column(name = "ID", path = "identifier"),
            Column(name = "Implementation evidence", path = "implementationEvidenceAccepted"),
            Column(name = "Effectiveness evidence", path = "effectivenessEvidenceAccepted"),
            Column(name = "Residual-risk assessment", path = "residualRiskAssessmentAccepted"),
            Column(name = "Risk disposition", path = "riskDispositionAccepted"),
            Column(name = "Control evidence record", path = "controlEvidenceRecord"),
            Column(name = "Acceptance record", path = "acceptanceRecord"),
            Column(name = "Acceptance authority", path = "acceptanceAuthority"),
            Column(name = "Closed preconditions", path = "closed")))
    }
    calc def FailureModes :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogDFMEA::starter")),
            type = "FailureAnalysis::ReviewRow"), columns = (
            Column(name = "ID", path = "identifier"), Column(name = "Safety critical", path = "safetyCritical"),
            Column(name = "Owner role", path = "ownerRole"), Column(name = "Disposition accepted", path = "dispositionAccepted"),
            Column(name = "Action evidence accepted", path = "actionEvidenceAccepted")))
    }
    part def HazardRegister :> Document {
        attribute redefines title = "Initial Gorge hazard and control basis";
        part hazards : Table { calc rows : Hazards; }
        part links : Table { calc rows : Basis; }
    }
    part def DispositionRegister :> Document {
        attribute redefines title = "Hazard evidence and disposition status";
        part dispositions : Table { calc rows : Dispositions; }
    }
}
