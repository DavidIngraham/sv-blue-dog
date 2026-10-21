package BlueDogAudit {
    private import DocumentQueries::*;
    calc def GoverningElements :> Query {
        Descendants(source = Named(qualifiedName = ("GorgeChallenge", "BlueDog::Goals", "BlueDogRequirements", "BlueDogStructure")))
    }
    calc def Coverage :> Query {
        Project(source = WhereType(source = GoverningElements(), type = "RequirementUsage"), columns = (
            Column(name = "Requirement", path = "qualifiedName"),
            Column(name = "Definitions", cell = { in row : SysML::RequirementUsage; RelatedElements(source = row, relationshipKind = "typing", direction = "outgoing", maxDepth = 1) }),
            Column(name = "Verification", cell = { in row : SysML::RequirementUsage; RelatedElements(source = row, relationshipKind = "verification", direction = "incoming", maxDepth = 1) }),
            Column(name = "Satisfaction", cell = { in row : SysML::RequirementUsage; RelatedElements(source = row, relationshipKind = "satisfaction", direction = "incoming", maxDepth = 1) })))
    }
    calc def Deferred :> Query {
        WhereFeature(source = Project(source = WhereMetadata(source = WhereType(source = GoverningElements(), type = "RequirementDefinition"), 'metadata' = "BlueDogMissionScope::Applicability"), columns = (
            Column(name = "Mission", path = "BlueDogMissionScope::Applicability::mission"))), 'feature' = "Mission", operator = "matches", value = "future(Ocean|Endurance)$")
    }
    calc def StudyObjectives :> Query {
        WhereMetadata(source = WhereType(source = GoverningElements(), type = "RequirementDefinition"), 'metadata' = "BlueDogRequirementBasis::StudyObjective")
    }
    calc def Derivations :> Query {
        Project(source = WhereMetadata(source = GoverningElements(), 'metadata' = "RequirementDerivation::DerivationMetadata"), columns = (
            Column(name = "Original", cell = { in row : KerML::Kernel::Connector;
                WhereMetadata(source = row.connectorEnd, 'metadata' = "RequirementDerivation::OriginalRequirementMetadata")->ControlFunctions::collect { in e : KerML::Core::Feature; e.ownedReferenceSubsetting.referencedFeature } }),
            Column(name = "Derived", cell = { in row : KerML::Kernel::Connector;
                WhereMetadata(source = row.connectorEnd, 'metadata' = "RequirementDerivation::DerivedRequirementMetadata")->ControlFunctions::collect { in e : KerML::Core::Feature; e.ownedReferenceSubsetting.referencedFeature } }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    calc def Dependencies :> Query {
        in roots : ScalarValues::String [1..*] ordered;
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = roots)), type = "Dependency"), columns = (
            Column(name = "Client", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Supplier", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    calc def Refinements :> Query {
        in roots : ScalarValues::String [1..*] ordered;
        WhereMetadata(source = WhereType(source = Descendants(source = Named(qualifiedName = roots)), type = "Dependency"), 'metadata' = "ModelingMetadata::Refinement")
    }
    calc def Impact :> Query {
        in element : ScalarValues::String;
        in relationship : ScalarValues::String;
        in direction : ScalarValues::String;
        in depth : ScalarValues::Integer;
        Project(source = RelatedElements(source = Named(qualifiedName = element), relationshipKind = relationship, direction = direction, maxDepth = depth), properties = ("qualifiedName", "name"))
    }
}
