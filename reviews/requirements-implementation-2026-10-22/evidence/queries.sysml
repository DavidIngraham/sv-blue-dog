package RequirementsAuditQueries {
    private import DocumentQueries::*;
    calc def Elements :> Query {
        Descendants(source = Named(qualifiedName = ("GorgeChallenge", "BlueDog", "BlueDogRequirements", "BlueDogStructure", "BlueDogRequirementVerification", "GorgeChallengeVerification", "BlueDogRequirementBasis")))
    }
    calc def Uses :> Query {
        Project(source = WhereType(source = Elements(), type = "RequirementUsage"),
            properties = ("name", "type"), columns = (
            Column(name = "Verifiers", cell = { in row : SysML::RequirementUsage;
                RelatedElements(source = row, relationshipKind = "verification", direction = "incoming", maxDepth = 1) }),
            Column(name = "Satisfiers", cell = { in row : SysML::RequirementUsage;
                RelatedElements(source = row, relationshipKind = "satisfaction", direction = "incoming", maxDepth = 1) }),
            Column(name = "Refines", cell = { in row : SysML::RequirementUsage;
                RelatedElements(source = row, relationshipKind = "refinement", direction = "outgoing", maxDepth = 1) })))
    }
    calc def Dependencies :> Query {
        Project(source = WhereType(source = Elements(), type = "Dependency"), columns = (
            Column(name = "Client", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Supplier", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    calc def Basis :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogRequirementBasis")), type = "MetadataUsage"),
            columns = (Column(name = "About", path = "annotatedElement"),
                       Column(name = "Kind", path = "kind"),
                       Column(name = "Rationale", path = "rationale")))
    }
    calc def AllDependencies :> Query {
        in roots : KerML::Root::Element[0..*];
        Project(source = WhereType(source = Descendants(source = roots), type = "Dependency"), columns = (
            Column(name = "Client", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Supplier", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    calc def AllRefinements :> Query {
        in roots : KerML::Root::Element[0..*];
        WhereMetadata(source = WhereType(source = Descendants(source = roots), type = "Dependency"), 'metadata' = "ModelingMetadata::Refinement")
    }
    calc def AllVerification :> Query {
        in roots : KerML::Root::Element[0..*];
        Project(source = WhereType(source = Descendants(source = roots), type = "VerificationCaseDefinition"),
            properties = ("shortName", "documentation"), columns = (
            Column(name = "Verifies", cell = { in row : SysML::VerificationCaseDefinition;
                RelatedElements(source = row, relationshipKind = "verification", direction = "outgoing", maxDepth = 1) })))
    }
    calc def BasisTargets :> Query {
        WhereMetadata(source = WhereType(source = Elements(), type = "RequirementDefinition"), 'metadata' = "BlueDogRequirementBasis::Basis")
    }
    calc def AllAllocationSources :> Query {
        in roots : KerML::Root::Element[0..*];
        WhereText(source = Project(source = Descendants(source = roots), columns = (
            Column(name = "Targets", cell = { in row : KerML::Root::Element;
                RelatedElements(source = row, relationshipKind = "allocation", direction = "outgoing", maxDepth = 1) }))),
            columns = ("Targets"), operator = "!=", value = "")
    }
    calc def AllDerivations :> Query {
        in roots : KerML::Root::Element[0..*];
        WhereText(source = Project(source = WhereMetadata(source = WhereType(source = Descendants(source = roots), type = "ConnectionUsage"), 'metadata' = "RequirementDerivation::DerivationMetadata"), columns = (
            Column(name = "Original", cell = { in row : KerML::Kernel::Connector;
                WhereMetadata(source = row.connectorEnd, 'metadata' = "RequirementDerivation::OriginalRequirementMetadata")->ControlFunctions::collect { in e : KerML::Core::Feature; e.ownedReferenceSubsetting.referencedFeature } }),
            Column(name = "Derived", cell = { in row : KerML::Kernel::Connector;
                WhereMetadata(source = row.connectorEnd, 'metadata' = "RequirementDerivation::DerivedRequirementMetadata")->ControlFunctions::collect { in e : KerML::Core::Feature; e.ownedReferenceSubsetting.referencedFeature } }))),
            columns = ("Original"), operator = "!=", value = "")
    }
}
