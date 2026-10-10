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
                Column(name = "Status", path = "workStatus.status"), Column(name = "Rationale", path = "rationale.text")))
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
        part context : Paragraph {
            part link : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification specifications"; attribute redefines target = "requirements-context.md"; }
        }
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

    calc def EnergyLoads :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogEnergyExamples::sailing"), maxDepth = 1), type = "PartUsage"),
            columns = (Column(name = "Load", path = "label"),
                Column(name = "Active power", path = "activePower"), Column(name = "Idle power", path = "idlePower"),
                Column(name = "Active fraction", path = "activeFraction"), Column(name = "Conversion efficiency", path = "conversionEfficiency"),
                Column(name = "Uncertainty factor", path = "uncertaintyFactor"),
                Column(name = "Average bus power", path = "averagePower"), Column(name = "Peak bus power", path = "peakPower")))
    }
    calc def EnergyTotals :> Query {
        Project(source = Named(qualifiedName = "BlueDogEnergyExamples::sailing"),
            columns = (Column(name = "Budget", path = "name"), Column(name = "Average demand", path = "averagePower"), Column(name = "Coincident peak", path = "peakPower")))
    }
    part def EnergyBudget :> Document {
        attribute redefines title = "Sustained-operation energy roll-up";
        part caution : Paragraph {
            attribute redefines text = "Generated natively from the synthetic example. These are illustrative inputs, not measurements or hardware selections. Conversion losses and uncertainty factors are included per load; peak powers are conservatively coincident. See sustained-operations.md for the executable campaign, evidence checklist and limitations.";
        }
        part loads : Table { calc rows : EnergyLoads; }
        part totals : Table { calc rows : EnergyTotals; }
    }

    calc def RequirementDefinitions :> Query {
        WhereType(source = ModelElements(), type = "RequirementDefinition")
    }
    calc def Conditions :> Query {
        WhereText(source = Project(source = RequirementDefinitions(),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name"),
                Column(name = "Text", cell = { in row : KerML::Root::Element;
                    row.ownedElement->ControlFunctions::select { in e : KerML::Root::Element; e.declaredName == "conditions" }->ControlFunctions::collect { in c : KerML::Root::Comment; c.body } }))),
            columns = ("Text"), operator = "!=", value = "")
    }
    calc def Notes :> Query {
        WhereText(source = Project(source = RequirementDefinitions(),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name"),
                Column(name = "Text", cell = { in row : KerML::Root::Element;
                    row.ownedElement->ControlFunctions::select { in e : KerML::Root::Element; e.declaredName == "notes" }->ControlFunctions::collect { in c : KerML::Root::Comment; c.body } }))),
            columns = ("Text"), operator = "!=", value = "")
    }
    calc def RationaleRows :> Query {
        Project(source = WhereMetadata(source = RequirementDefinitions(), 'metadata' = "ModelingMetadata::Rationale"),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name"), Column(name = "Text", path = "rationale.text")))
    }
    calc def IssueRows :> Query {
        Project(source = WhereMetadata(source = RequirementDefinitions(), 'metadata' = "ModelingMetadata::Issue"),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name"), Column(name = "Text", path = "issue.text")))
    }
    calc def VerificationSpecifications :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = ("BlueDogRequirementVerification", "BlueDogReliability"))), type = "VerificationCaseDefinition"),
            properties = ("shortName", "name", "documentation"),
            columns = (Column(name = "Verifies", cell = { in row : SysML::VerificationCaseDefinition;
                RelatedElements(source = row, relationshipKind = "verification", direction = "outgoing", maxDepth = 1) })))
    }
    part def RequirementContext :> Document {
        attribute redefines title = "Requirement context and verification specifications";
        part intro : Paragraph { attribute redefines text = "Requirement statements are in the register and focused views. Qualification conditions below are normative definitions and test applicability; they are not optional rationale. Notes and rationale explain scope and decisions. Verification specifications describe planned evidence collection and return inconclusive until implemented with accepted evidence. No physical compliance is asserted."; }
        part conditions : Section {
            attribute redefines title = "Qualification conditions (normative)";
            part entries : Table { calc rows : Conditions; }
        }
        part rationale : Section {
            attribute redefines title = "Rationale";
            part entries : Table { calc rows : RationaleRows; }
        }
        part notes : Section {
            attribute redefines title = "Explanatory notes";
            part entries : Table { calc rows : Notes; }
        }
        part issues : Section {
            attribute redefines title = "Open issues";
            part entries : Table { calc rows : IssueRows; }
        }
        part verificationSpecifications : Section {
            attribute redefines title = "Verification specifications";
            part entries : Table { calc rows : VerificationSpecifications; }
        }
    }
}
