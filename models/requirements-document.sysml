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
    calc def ChallengeStatements :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "GorgeChallenge")), type = "RequirementDefinition"),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Rule", path = "name"), Column(name = "Statement", path = "documentation")))
    }
    part def ChallengeBrief :> Document {
        attribute redefines title = "Trans-Gorge challenge";
        part intro : Paragraph { attribute redefines text = "The challenge is defined independently of the vehicle in challenge.sysml. The statements below are generated from that model. Read the linked qualification conditions and open issues with these rules; a statement or model check is not proof of completion."; }
        part rules : Table { calc rows : ChallengeStatements; }
        part context : Paragraph { part link : Link { attribute redefines text = "Qualification conditions and open issues"; attribute redefines target = "requirements-context.md"; } }
        part derivation : Paragraph { part link : Link { attribute redefines text = "Challenge derivations"; attribute redefines target = "figures/requirements-c-000.md"; } }
        part process : Paragraph { part link : Link { attribute redefines text = "Design process and model sources"; attribute redefines target = "design-guide.md"; } }
    }
    part def RequirementsIndex :> Document {
        attribute redefines title = "Requirements views";
        part intro : Paragraph { attribute redefines text = "Follow a parent to its immediate derived requirements. Each diagram includes at most three children and places the parent above them. Shared requirements may appear under more than one parent. These views express derivation, not verification."; }
        part register : Paragraph { part link : Link { attribute redefines text = "Complete requirements register"; attribute redefines target = "requirements-register.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification"; attribute redefines target = "requirements-context.md"; } }
        part category0 : Section { attribute redefines title = "Mission and challenge";
            part entry1 : Paragraph { part link : Link { attribute redefines text = "C-000 trans gorge challenge"; attribute redefines target = "figures/requirements-c-000.md"; } }
            part entry2 : Paragraph { part link : Link { attribute redefines text = "C-001 course completion"; attribute redefines target = "figures/requirements-c-001.md"; } }
            part entry3 : Paragraph { part link : Link { attribute redefines text = "C-002 repeated operation"; attribute redefines target = "figures/requirements-c-002.md"; } }
            part entry4 : Paragraph { part link : Link { attribute redefines text = "C-003 unassisted attempt"; attribute redefines target = "figures/requirements-c-003.md"; } }
            part entry5 : Paragraph { part link : Link { attribute redefines text = "C-004 sailing propulsion"; attribute redefines target = "figures/requirements-c-004.md"; } }
            part entry6 : Paragraph { part link : Link { attribute redefines text = "C-005 live observation"; attribute redefines target = "figures/requirements-c-005.md"; } }
            part entry7 : Paragraph { part link : Link { attribute redefines text = "C-006 emergency intervention"; attribute redefines target = "figures/requirements-c-006.md"; } }
            part entry8 : Paragraph { part link : Link { attribute redefines text = "H-001 hawaii voyage"; attribute redefines target = "figures/requirements-h-001.md"; } }
            part entry9 : Paragraph { part link : Link { attribute redefines text = "M-001 round trip"; attribute redefines target = "figures/requirements-m-001.md"; } }
            part entry10 : Paragraph { part link : Link { attribute redefines text = "M-002 multi day endurance"; attribute redefines target = "figures/requirements-m-002.md"; } }
        }
        part category1 : Section { attribute redefines title = "Energy, autonomy and records";
            part entry11 : Paragraph { part link : Link { attribute redefines text = "E-001 energy awareness"; attribute redefines target = "figures/requirements-e-001.md"; } }
            part entry12 : Paragraph { part link : Link { attribute redefines text = "E-002 navigation and control"; attribute redefines target = "figures/requirements-e-002.md"; } }
            part entry13 : Paragraph { part link : Link { attribute redefines text = "E-005 communications"; attribute redefines target = "figures/requirements-e-005.md"; } }
            part entry14 : Paragraph { part link : Link { attribute redefines text = "E-003 reset recovery"; attribute redefines target = "figures/requirements-e-003.md"; } }
            part entry15 : Paragraph { part link : Link { attribute redefines text = "E-004 low energy recovery"; attribute redefines target = "figures/requirements-e-004.md"; } }
            part entry16 : Paragraph { part link : Link { attribute redefines text = "E-006 ingress response"; attribute redefines target = "figures/requirements-e-006.md"; } }
            part entry17 : Paragraph { part link : Link { attribute redefines text = "E-007 mission evidence"; attribute redefines target = "figures/requirements-e-007.md"; } }
            part entry18 : Paragraph { part link : Link { attribute redefines text = "E-008 navigation availability"; attribute redefines target = "figures/requirements-e-008.md"; } }
            part entry19 : Paragraph { part link : Link { attribute redefines text = "E-200 sustained energy feasibility"; attribute redefines target = "figures/requirements-e-200.md"; } }
        }
        part category2 : Section { attribute redefines title = "Environment and durability";
            part entry20 : Paragraph { part link : Link { attribute redefines text = "N-001 environmental envelope"; attribute redefines target = "figures/requirements-n-001.md"; } }
            part entry21 : Paragraph { part link : Link { attribute redefines text = "N-010 gorge environment"; attribute redefines target = "figures/requirements-n-010.md"; } }
            part entry22 : Paragraph { part link : Link { attribute redefines text = "N-020 ocean environment"; attribute redefines target = "figures/requirements-n-020.md"; } }
            part entry23 : Paragraph { part link : Link { attribute redefines text = "N-002 marine durability"; attribute redefines target = "figures/requirements-n-002.md"; } }
            part entry24 : Paragraph { part link : Link { attribute redefines text = "N-003 stability and fouling"; attribute redefines target = "figures/requirements-n-003.md"; } }
            part entry25 : Paragraph { part link : Link { attribute redefines text = "N-033 visibility"; attribute redefines target = "figures/requirements-n-033.md"; } }
            part entry26 : Paragraph { part link : Link { attribute redefines text = "N-035 envelope transition"; attribute redefines target = "figures/requirements-n-035.md"; } }
            part entry27 : Paragraph { part link : Link { attribute redefines text = "N-044 wet mechanical integrity"; attribute redefines target = "figures/requirements-n-044.md"; } }
            part entry28 : Paragraph { part link : Link { attribute redefines text = "N-045 wet electrical integrity"; attribute redefines target = "figures/requirements-n-045.md"; } }
            part entry29 : Paragraph { part link : Link { attribute redefines text = "N-046 solar heating"; attribute redefines target = "figures/requirements-n-046.md"; } }
            part entry30 : Paragraph { part link : Link { attribute redefines text = "N-051 self righting"; attribute redefines target = "figures/requirements-n-051.md"; } }
            part entry31 : Paragraph { part link : Link { attribute redefines text = "N-052 capsize control recovery"; attribute redefines target = "figures/requirements-n-052.md"; } }
            part entry32 : Paragraph { part link : Link { attribute redefines text = "N-053 submerged weed passage"; attribute redefines target = "figures/requirements-n-053.md"; } }
            part entry33 : Paragraph { part link : Link { attribute redefines text = "N-054 weed snag shedding"; attribute redefines target = "figures/requirements-n-054.md"; } }
            part entry34 : Paragraph { part link : Link { attribute redefines text = "N-055 weed blockage response"; attribute redefines target = "figures/requirements-n-055.md"; } }
            part entry35 : Paragraph { part link : Link { attribute redefines text = "N-056 recovery propulsor weeds"; attribute redefines target = "figures/requirements-n-056.md"; } }
        }
        part category3 : Section { attribute redefines title = "Practicality";
            part entry36 : Paragraph { part link : Link { attribute redefines text = "P-001 transportability"; attribute redefines target = "figures/requirements-p-001.md"; } }
            part entry37 : Paragraph { part link : Link { attribute redefines text = "P-003 serviceability"; attribute redefines target = "figures/requirements-p-003.md"; } }
        }
        part category4 : Section { attribute redefines title = "Safety and recovery";
            part entry38 : Paragraph { part link : Link { attribute redefines text = "S-001 traffic safety"; attribute redefines target = "figures/requirements-s-001.md"; } }
            part entry39 : Paragraph { part link : Link { attribute redefines text = "S-003 safe recovery"; attribute redefines target = "figures/requirements-s-003.md"; } }
            part entry40 : Paragraph { part link : Link { attribute redefines text = "R-001 recovery propulsion"; attribute redefines target = "figures/requirements-r-001.md"; } }
            part entry41 : Paragraph { part link : Link { attribute redefines text = "R-002 recovery energy"; attribute redefines target = "figures/requirements-r-002.md"; } }
            part entry42 : Paragraph { part link : Link { attribute redefines text = "S-002 operating boundary"; attribute redefines target = "figures/requirements-s-002.md"; } }
            part entry43 : Paragraph { part link : Link { attribute redefines text = "S-004 navigation conspicuity"; attribute redefines target = "figures/requirements-s-004.md"; } }
            part entry44 : Paragraph { part link : Link { attribute redefines text = "S-005 regulatory classification"; attribute redefines target = "figures/requirements-s-005.md"; } }
            part entry45 : Paragraph { part link : Link { attribute redefines text = "R-004 challenge motor inhibition"; attribute redefines target = "figures/requirements-r-004.md"; } }
        }
        part category5 : Section { attribute redefines title = "Communications equipment";
            part entry46 : Paragraph { part link : Link { attribute redefines text = "C-101 telemetry equipment"; attribute redefines target = "figures/requirements-c-101.md"; } }
            part entry47 : Paragraph { part link : Link { attribute redefines text = "C-102 command integrity"; attribute redefines target = "figures/requirements-c-102.md"; } }
        }
        part category6 : Section { attribute redefines title = "Cruise performance and reliability";
            part entry48 : Paragraph { part link : Link { attribute redefines text = "Q-001 cruise performance"; attribute redefines target = "figures/requirements-q-001.md"; } }
            part entry49 : Paragraph { part link : Link { attribute redefines text = "L-001 mission reliability"; attribute redefines target = "figures/requirements-l-001.md"; } }
        }
    }
}
