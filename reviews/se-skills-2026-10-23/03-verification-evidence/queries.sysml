package BlueDogVerificationDocuments {
    private import DocumentQueries::*;
    calc def Plans :> Query {
        in roots : ScalarValues::String [1..*] ordered default = (
            "BlueDogRequirementVerification", "GorgeChallengeVerification", "BlueDogVerificationPlanning", "BlueDogEnergy", "BlueDogReliability");
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = roots)),
            type = "VerificationCaseDefinition"), columns = (
            Column(name = "Case", path = "name"),
            Column(name = "Planned methods", path = "VerificationCases::VerificationMethod::kind"),
            Column(name = "Objectives", cell = { in row : SysML::VerificationCaseDefinition;
                RelatedElements(source = row, relationshipKind = "verification", direction = "outgoing", maxDepth = 1) })))
    }
    calc def PlannedVerdicts :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = (
            "BlueDogRequirementVerification", "GorgeChallengeVerification", "BlueDogVerificationPlanning"))),
            type = "VerificationCaseDefinition"), columns = (
            Column(name = "Case", path = "name"), Column(name = "Declared plan result", path = "verdict")))
    }
    calc def IntegrationConfigurations :> Query {
        Project(source = Named(qualifiedName = ("BlueDogVerificationPlanning::interfaceBench",
            "BlueDogVerificationPlanning::recoveryUseTrial")), columns = (
            Column(name = "Plan", path = "name"), Column(name = "Planned design", path = "plannedDesign"),
            Column(name = "Planned assembly", path = "plannedAssembly"), Column(name = "Purpose", path = "purpose"),
            Column(name = "Actual article", path = "articleIdentity"), Column(name = "Released procedure", path = "procedureIdentity"),
            Column(name = "Instruments", path = "instrumentConfiguration")))
    }
    part def MethodRegister :> Document {
        attribute redefines title = "Planned verification methods and objectives";
        part context : Paragraph { attribute redefines text = "Methods identify planned assessment work. This register executes no verification and accepts no evidence. Numerical verification definitions require an identified subject and inputs before producing results."; }
        part plans : Table { calc rows : Plans; }
    }
    part def IntegrationRegister :> Document {
        attribute redefines title = "Planned IC-01 integration and recovery-use configurations";
        part configurations : Table { calc rows : IntegrationConfigurations; }
    }
}
