package BlueDogDocuments {
    private import DocumentQueries::*;
    calc def ModelElements :> Query {
        Descendants(source = Named(qualifiedName = ("GorgeChallenge", "BlueDog::Goals", "BlueDogRequirements")))
    }
    calc def Requirements :> Query {
        Project(source = WhereType(source = ModelElements(), type = "RequirementDefinition"),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name"), Column(name = "Status", path = "workStatus.status"), Column(name = "Statement", path = "documentation")))
    }
    calc def Derivations :> Query {
        Project(source = WhereType(source = ModelElements(), type = "ConnectionUsage"),
            columns = (
                Column(name = "Original", cell = { in row : KerML::Kernel::Connector;
                    WhereMetadata(source = row.connectorEnd, 'metadata' = "RequirementDerivation::OriginalRequirementMetadata")->ControlFunctions::collect { in e : KerML::Core::Feature; e.ownedReferenceSubsetting.referencedFeature } }),
                Column(name = "Derived", cell = { in row : KerML::Kernel::Connector;
                    WhereMetadata(source = row.connectorEnd, 'metadata' = "RequirementDerivation::DerivedRequirementMetadata")->ControlFunctions::collect { in e : KerML::Core::Feature; e.ownedReferenceSubsetting.referencedFeature } }),
                Column(name = "Status", path = "workStatus.status"), Column(name = "Rationale", path = "documentation")))
    }
    calc def UseCaseLinks :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogUseCases")), type = "UseCaseUsage"),
            properties = ("name", "documentation"),
            columns = (Column(name = "Requirement", cell = { in row : SysML::UseCaseUsage;
                row.objectiveRequirement.ownedSubsetting.subsettedFeature })))
    }

    calc def SatisfactionLinks :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogRequirements")), type = "RequirementUsage"),
            properties = ("name"),
            columns = (Column(name = "Design element", cell = { in row : SysML::RequirementUsage;
                RelatedElements(source = row, relationshipKind = "satisfaction", direction = "incoming", maxDepth = 1) })))
    }
    part def Traceability :> Document {
        attribute redefines title = "Use-case and architecture traceability";
        part caution : Paragraph { attribute redefines text = "Use-case objectives subset the referenced requirements. Satisfy relationships express intended design allocations, not verified compliance; criteria and evidence remain open."; }
        part useCases : Section {
            attribute redefines title = "Use-case objectives";
            part entries : Table { calc rows : UseCaseLinks; }
        }
        part satisfaction : Section {
            attribute redefines title = "Architecture satisfaction allocations";
            part entries : Table { calc rows : SatisfactionLinks; }
        }
    }
    part def RequirementsRegister :> Document {
        attribute redefines title = "Requirement derivation register";
        part intro : Paragraph {
            attribute redefines text = "Generated natively by OpenSysML from the project models. Status describes work on the model element, not verification. Derivations record design reasoning, not proof of satisfaction.";
        }
        part requirements : Section {
            attribute redefines title = "Requirements";
            part entries : Table { calc rows : Requirements; }
        }
        part derivations : Section {
            attribute redefines title = "Derivations";
            part entries : Table { calc rows : Derivations; }
        }
    }
}
