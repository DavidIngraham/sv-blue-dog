package RequirementQualityTests {
    private import DocumentQueries::*;
    calc def Trace :> Query {
        Project(source = Named(qualifiedName = (
            "GorgeChallenge::navigationRuleApplicability", "GorgeChallenge::navigationRuleBaseline",
            "GorgeChallenge::navigationEntryEvidence", "GorgeChallenge::operatorSafetyIntervention",
            "GorgeChallenge::navigationAdjudication", "BlueDog::Requirements::capsizeResilience",
            "BlueDog::Requirements::vegetationResilience", "BlueDog::Requirements::serviceability",
            "BlueDog::Requirements::wetElectricalIntegrity")), columns = (
            Column(name = "Verifiers", cell = { in row : SysML::RequirementUsage;
                RelatedElements(source = row, relationshipKind = "verification", direction = "incoming", maxDepth = 1) }),
            Column(name = "Satisfiers", cell = { in row : SysML::RequirementUsage;
                RelatedElements(source = row, relationshipKind = "satisfaction", direction = "incoming", maxDepth = 1) })))
    }
}
