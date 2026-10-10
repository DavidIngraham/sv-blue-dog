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
