package BlueDogWindDocuments {
    private import DocumentQueries::*;
    calc def Configurations :> Query {
        Project(source = Named(qualifiedName = ("BlueDogWindEquipment::testbed", "BlueDogWindEquipment::challenge")), columns = (
            Column(name = "Configuration", path = "name"),
            Column(name = "Sensor", path = "product"),
            Column(name = "Interface", path = "dataInterface"),
            Column(name = "Installed mass kg", path = "installedMassKg"),
            Column(name = "Vessel bus W", path = "busPowerW"),
            Column(name = "Internal battery hours (supplier)", path = "internalBatteryRuntimeHours")))
    }
    part def WindEquipment :> Document {
        attribute redefines title = "Wind-sensing configurations";
        part configurations : Table { calc rows : Configurations; }
    }
}

package BlueDogDocuments {
    private import DocumentQueries::*;
    calc def ModelElements :> Query {
        Descendants(source = Named(qualifiedName = ("GorgeChallenge", "BlueDog::Goals", "BlueDogRequirements")))
    }
    calc def Requirements :> Query {
        Project(source = WhereType(source = ModelElements(), type = "RequirementDefinition"),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name"), Column(name = "Status", path = "workStatus.status"), Column(name = "Statement", path = "documentation")))
    }
    calc def DeferredRequirements :> Query {
        Project(source = WhereMetadata(source = WhereType(source = ModelElements(), type = "RequirementDefinition"), 'metadata' = "BlueDogMissionScope::Applicability"),
            columns = (Column(name = "ID", path = "shortName"), Column(name = "Requirement", path = "name")))
    }
    part def FutureMissionRequirements :> Document {
        attribute redefines title = "Deferred mission requirements";
        part entries : Table { calc rows : DeferredRequirements; }
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
            part link : Link { attribute redefines text = "Qualification conditions, rationale, open issues and verification specifications"; attribute redefines target = "methods/modeling.md"; }
        }
        part intro : Paragraph {
            attribute redefines text = "Generated natively by OpenSysML from the project models. Status describes work on the model element, not verification. Derivations express required acceptance outcomes under their stated conditions, not evidence that a vessel satisfies them. Design-basis dependencies and refinements are reported separately.";
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
        part intro : Paragraph { attribute redefines text = "The challenge is defined independently of the vehicle in missions/transgorge.sysml. The statements below are generated from that model. Read the linked qualification conditions and open issues with these rules; a statement or model check is not proof of completion."; }
        part rules : Table { calc rows : ChallengeStatements; }
        part context : Paragraph { part link : Link { attribute redefines text = "Qualification conditions and open issues"; attribute redefines target = "methods/modeling.md"; } }
        part derivation : Paragraph { part link : Link { attribute redefines text = "Challenge derivations"; attribute redefines target = "requirements/requirements-c-000.md"; } }
        part process : Paragraph { part link : Link { attribute redefines text = "Design process and model sources"; attribute redefines target = "index.md"; } }
    }


    calc def RefinementDependencies :> Query {
        WhereMetadata(source = WhereType(source = ModelElements(), type = "Dependency"), 'metadata' = "ModelingMetadata::Refinement")
    }
    calc def RefinementLinks :> Query {
        Project(source = RefinementDependencies(), columns = (
            Column(name = "Refining element", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Refined element", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    calc def DesignBasisLinks :> Query {
        Project(source = Except(source = WhereType(source = ModelElements(), type = "Dependency"), exclude = RefinementDependencies()), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def RelationshipRegister :> Document {
        attribute redefines title = "Refinements and design-basis dependencies";
        part meaning : Paragraph { attribute redefines text = "Refinement points from a more precise representation to the element it clarifies. Plain dependency points from a dependent design obligation to its basis; it makes no satisfaction implication. These are model relationships, not completed evidence."; }
        part refinements : Section { attribute redefines title = "Refinement"; part entries : Table { calc rows : RefinementLinks; } }
        part designBasis : Section { attribute redefines title = "Plain dependency"; part entries : Table { calc rows : DesignBasisLinks; } }
    }
}

package BlueDogEvidenceDocuments {
    private import DocumentQueries::*;
    calc def Cases :> Query {
        Named(qualifiedName = ("BlueDogCurrentSizing::nominal", "BlueDogCurrentSizing::construction", "BlueDogCurrentSizing::aerodynamic", "BlueDogCurrentSizing::hydrodynamic", "BlueDogCurrentSizing::energy", "BlueDogCurrentSizing::combined"))
    }
    calc def Outcomes :> Query {
        Project(source = Cases(), columns = (
            Column(name = "Scenario", path = "label"),
            Column(name = "Sailing, structure and route", path = "operatingScreensPass"),
            Column(name = "Lowest replay margins", path = "limitingScreens"),
            Column(name = "Sampled roll positive", path = "sampledRollPositive"),
            Column(name = "Unstable pitch samples", path = "pitchUnstableSamples"),
            Column(name = "Peak-power diagnostic cases", path = "diagnosticControlCases"),
            Column(name = "Evidence accepted", path = "evidenceAccepted")))
    }
    calc def Dimensions :> Query {
        Project(source = Named(qualifiedName = "BlueDogCurrentSizing::candidate"), columns = (
            Column(name = "Length (m)", path = "length_m"),
            Column(name = "Beam (m)", path = "beam_m"),
            Column(name = "Wing area (m2)", path = "sail_m2"),
            Column(name = "Ballast (kg)", path = "ballast_kg"),
            Column(name = "Battery (Wh)", path = "battery_Wh")))
    }
    calc def Search :> Query {
        Project(source = Named(qualifiedName = "BlueDogCurrentSizing::searchAssessment"), columns = (
            Column(name = "Search status", path = "solverStatus"),
            Column(name = "Coarse feasible", path = "coarseFeasible"),
            Column(name = "Mass (kg)", path = "massKg"),
            Column(name = "Max equilibrium residual", path = "maximumResidual"),
            Column(name = "Minimum screen margin", path = "minimumMargin"),
            Column(name = "Qualified", path = "qualified")))
    }
    calc def Passage :> Query {
        Project(source = Cases(), columns = (Column(name = "Scenario", path = "label"),
            Column(name = "Westerly round trip (h, conditional)", path = "westerlyTimeLabel"),
            Column(name = "Easterly round trip (h, conditional)", path = "easterlyTimeLabel"),
            Column(name = "Mass (kg)", path = "massKg")))
    }
    calc def LimitingScreens :> Query {
        Project(source = Named(qualifiedName = ("BlueDogCurrentSizing::searchConstraint0", "BlueDogCurrentSizing::searchConstraint1", "BlueDogCurrentSizing::searchConstraint2", "BlueDogCurrentSizing::searchConstraint3", "BlueDogCurrentSizing::searchConstraint4", "BlueDogCurrentSizing::searchConstraint5")), columns = (
            Column(name = "Lowest search screens", path = "label"), Column(name = "Normalized margin", path = "margin")))
    }
    calc def ActiveBounds :> Query {
        Project(source = Named(qualifiedName = "BlueDogCurrentSizing::searchAssessment"), columns = (
            Column(name = "Active design brackets (not frozen variables)", path = "activeBounds")))
    }
    calc def Convergence :> Query {
        Project(source = Named(qualifiedName = ("BlueDogCurrentSizing::convergence0", "BlueDogCurrentSizing::convergence1", "BlueDogCurrentSizing::convergence2", "BlueDogCurrentSizing::convergence3", "BlueDogCurrentSizing::convergence4", "BlueDogCurrentSizing::convergence5")), columns = (
            Column(name = "Numerical increment", path = "label"),
            Column(name = "Max change CL", path = "CLtot"),
            Column(name = "Max change CDi", path = "CDi"),
            Column(name = "Max change CMy", path = "CMytot"),
            Column(name = "Screen passes", path = "passesScreen")))
    }
    part def AerodynamicChecks :> Document {
        attribute redefines title = "Representative numerical sensitivity";
        part checks : Table { calc rows : Convergence; }
        part coarse : Table { calc rows : CoarseGrid; }
    }
    calc def CoarseGrid :> Query {
        Project(source = Named(qualifiedName = ("BlueDogCurrentSizing::coarseGrid0", "BlueDogCurrentSizing::coarseGrid1", "BlueDogCurrentSizing::coarseGrid2")), columns = (
            Column(name = "Coarse grid versus finest case", path = "label"),
            Column(name = "Max change CL", path = "CLtot"),
            Column(name = "Max change CDi", path = "CDi"),
            Column(name = "Max change CMy", path = "CMytot")))
    }
    calc def Ingress :> Query {
        Project(source = Named(qualifiedName = ("BlueDogCurrentSizing::ingress0", "BlueDogCurrentSizing::ingress1", "BlueDogCurrentSizing::ingress2", "BlueDogCurrentSizing::ingress3", "BlueDogCurrentSizing::ingress4", "BlueDogCurrentSizing::ingress5")), columns = (
            Column(name = "Wing state and water density", path = "label"),
            Column(name = "Min sampled restoring (Nm)", path = "minimumRestoringNm"),
            Column(name = "Missing pitch roots", path = "missingPitchRoots"),
            Column(name = "Unstable pitch samples", path = "unstablePitchSamples"),
            Column(name = "Retained water (kg)", path = "retainedWaterKg")))
    }
    part def Recovery :> Document {
        attribute redefines title = "Current static ingress sensitivity";
        part cases : Table { calc rows : Ingress; }
    }
    part def CandidateBrief :> Document {
        attribute redefines title = "The trial geometry";
        part candidate : Table { calc rows : Dimensions; }
    }
    part def Summary :> Document {
        attribute redefines title = "Conservative sizing and refined replay";
        part search : Table { calc rows : Search; }
        part candidate : Table { calc rows : Dimensions; }
        part passage : Table { calc rows : Passage; }
        part cases : Table { calc rows : Outcomes; }
        part limiting : Table { calc rows : LimitingScreens; }
        part bounds : Table { calc rows : ActiveBounds; }
    }
}

package BlueDogSailTradeDocuments {
    private import DocumentQueries::*;
    calc def Candidates :> Query { Named(qualifiedName = ("BlueDogSailTrade::tailWing", "BlueDogSailTrade::camberedWing", "BlueDogSailTrade::softSail")) }
    calc def Concepts :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Definition", path = "concept"))) }
    calc def Durability :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Durability and reliability", path = "durability"), Column(name = "Energy", path = "energy"))) }
    calc def Recovery :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Sailing performance", path = "sailing"), Column(name = "Recovery geometry", path = "recovery"))) }
    calc def Manufacturing :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Construction", path = "manufacturing"), Column(name = "Next evidence", path = "nextEvidence"))) }
    calc def Results :> Query { Project(source = Named(qualifiedName = ("BlueDogSailTrade::tailAssessment", "BlueDogSailTrade::camberAssessment", "BlueDogSailTrade::softAssessment")), columns = (Column(name = "Candidate", path = "candidateName"), Column(name = "Development decision", path = "developmentDecision"), Column(name = "Requirement verdict", path = "requirementVerdict"))) }
    calc def Traces :> Query { Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogSailTrade")), type = "Dependency"), columns = (Column(name = "Analysis element", cell = { in row : KerML::Root::Dependency; row.client }), Column(name = "Requirement / architecture", cell = { in row : KerML::Root::Dependency; row.supplier }))) }
    part def Report :> Document {
        attribute redefines title = "Sail architecture trade study";
        part scope : Paragraph { attribute redefines text = "Preliminary qualitative development selection. All physical requirement gates remain unknown. No numeric reliability rates or arbitrary weighted scores are assigned. Neither rigid concept is mission-qualified; the soft sail is deprioritized, not proven noncompliant. Sources and decision rationale are linked in BlueDogSourceEvidence and BlueDogDesignDecisions."; }
        part decision : Section { attribute redefines title = "Native analysis conclusion"; part rows : Table { calc rows : Results; } }
        part concepts : Section { attribute redefines title = "Candidate definitions"; part rows : Table { calc rows : Concepts; } }
        part durability : Section { attribute redefines title = "Durability and energy"; part rows : Table { calc rows : Durability; } }
        part recovery : Section { attribute redefines title = "Performance and capsize"; part rows : Table { calc rows : Recovery; } }
        part construction : Section { attribute redefines title = "Manufacturing and evidence"; part rows : Table { calc rows : Manufacturing; } }
        part trace : Section { attribute redefines title = "Requirement and architecture links"; part rows : Table { calc rows : Traces; } }
    }
    part def Conclusion :> Document {
        attribute redefines title = "Current trade disposition";
        part decision : Table { calc rows : Results; }
    }
}

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
        part intro : Paragraph { attribute redefines text = "Initial hypotheses for the logical architecture. Detection and prevention actions are proposed, not implemented controls. Risks are unassessed; no probabilities or RPNs are assigned. Scope completeness and every disposition remain open. Read reliability.md for the exposure model."; }
        part functions : Section { attribute redefines title = "Functions and failure modes"; part rows : Table { calc rows : Functions; } }
        part guide : Paragraph { part link : Link { attribute redefines text = "Cruise and reliability analysis guide"; attribute redefines target = "reliability.md"; } }
        part effects : Section { attribute redefines title = "Causes and effects"; part rows : Table { calc rows : Effects; } }
        part actions : Section { attribute redefines title = "Detection, actions and evidence"; part rows : Table { calc rows : Actions; } }
        part dispositions : Section { attribute redefines title = "Disposition and evidence"; part rows : Table { calc rows : Dispositions; } }
        part traces : Section { attribute redefines title = "Architecture and requirement links"; part rows : Table { calc rows : Traces; } }
    }
}

package BlueDogWeatherDocuments {
    private import DocumentQueries::*;
    calc def Cases :> Query {
        Named(qualifiedName = ("BlueDogWindObservations::KDLS_warm", "BlueDogWindObservations::KDLS_winter", "BlueDogWindObservations::KTTD_warm", "BlueDogWindObservations::KTTD_winter"))
    }
    calc def Counts :> Query {
        Project(source = Cases(), columns = (
            Column(name = "Station", path = "station"), Column(name = "Season", path = "season"),
            Column(name = "Calendar hours", path = "expectedHours"),
            Column(name = "West", path = "westHours"), Column(name = "East", path = "eastHours"),
            Column(name = "Light", path = "lightHours"), Column(name = "Other", path = "otherHours"),
            Column(name = "Unknown / absent", path = "unknownHours")))
    }
    calc def Windows :> Query {
        Project(source = Cases(), columns = (
            Column(name = "Station", path = "station"), Column(name = "Season", path = "season"),
            Column(name = "Complete windows", path = "selectedWindows"),
            Column(name = "East encounters", path = "windowsWithEast"),
            Column(name = "Incomplete windows", path = "incompleteWindows"),
            Column(name = "Missing-data lower %", path = "encounterLowerPercent"),
            Column(name = "Missing-data upper %", path = "encounterUpperPercent"),
            Column(name = "Status", path = "eastEncounterLabel")))
    }
    part def Observations :> Document {
        attribute redefines title = "Gorge station observations: 2015–2024";
        part counts : Section { attribute redefines title = "Hourly bins"; part rows : Table { calc rows : Counts; } }
        part windows : Section { attribute redefines title = "72-hour window probe, not mission probability"; part rows : Table { calc rows : Windows; } }
    }
}

package BlueDogContinuationDocuments {
    private import DocumentQueries::*;
    calc def Stages :> Query {
        Project(source = Named(qualifiedName = ("BlueDogSizingContinuation::stage0", "BlueDogSizingContinuation::stage1", "BlueDogSizingContinuation::stage2", "BlueDogSizingContinuation::stage3", "BlueDogSizingContinuation::stage4")), columns = (
            Column(name = "Hull length (m)", path = "lengthM"),
            Column(name = "Coarse feasible", path = "feasible"),
            Column(name = "Max equilibrium residual", path = "maximumResidual"),
            Column(name = "Lowest margin", path = "minimumMargin")))
    }
    calc def Dimensions :> Query {
        Project(source = Named(qualifiedName = "BlueDogSizingContinuation::candidate"), columns = (
            Column(name = "Length (m)", path = "length_m"),
            Column(name = "Beam (m)", path = "beam_m"),
            Column(name = "Wing area (m2)", path = "sail_m2"),
            Column(name = "Ballast (kg)", path = "ballast_kg"),
            Column(name = "Battery (Wh)", path = "battery_Wh")))
    }
    calc def Assessment :> Query {
        Project(source = Named(qualifiedName = "BlueDogSizingContinuation::assessment"), columns = (
            Column(name = "Mass (kg)", path = "massKg"),
            Column(name = "Coarse westerly time (h)", path = "westerlyHours"),
            Column(name = "Rudder chord (m)", path = "rudderChordM"),
            Column(name = "Rudder aspect ratio", path = "rudderAspectRatio"),
            Column(name = "Hull + neutral rudder extent (m)", path = "neutralHullRudderLengthM"),
            Column(name = "Qualified", path = "qualified")))
    }
    part def Summary :> Document {
        attribute redefines title = "Continuation toward 1.2 m";
        part stages : Table { calc rows : Stages; }
        part dimensions : Table { calc rows : Dimensions; }
        part assessment : Table { calc rows : Assessment; }
    }
}

package BlueDogFinitePassageDocuments {
    private import DocumentQueries::*;
    calc def Stages :> Query {
        Project(source = Named(qualifiedName = ("BlueDogFinitePassageSizing::stage0", "BlueDogFinitePassageSizing::stage1", "BlueDogFinitePassageSizing::stage2", "BlueDogFinitePassageSizing::stage3")), columns = (
            Column(name = "Hull length (m)", path = "lengthM"),
            Column(name = "Mass (kg)", path = "massKg"),
            Column(name = "Battery (Wh)", path = "batteryWh"),
            Column(name = "Swept length (m)", path = "sweptLengthM"),
            Column(name = "Nominal coarse pass", path = "feasible")))
    }
    part def Summary :> Document {
        attribute redefines title = "Finite-passage sizing stages";
        part stages : Table { calc rows : Stages; }
    }
}

package BlueDogSRRDocuments {
    private import DocumentQueries::*;
    calc def EnvironmentProposalRows :> Query {
        Project(source = Named(qualifiedName = ("BlueDogEnvironmentReview::proposed")), columns = (
            Column(name = "Wind upper m/s", path = "operationalWindUpperMps"),
            Column(name = "Gust upper m/s", path = "operationalGustUpperMps"),
            Column(name = "Significant wave height m", path = "operationalWaveHeightM"),
            Column(name = "Peak periods s", path = "operationalPeriodSeconds"),
            Column(name = "Current sensitivity m/s", path = "currentSensitivityUpperMps")))
    }
    part def EnvironmentProposal :> Document {
        attribute redefines title = "Environmental allocations proposed for review";
        part allocations : Table { calc rows : EnvironmentProposalRows; }
    }
}

package BlueDogRecoverySiteDocuments {
    private import DocumentQueries::*;
    calc def Candidates :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRecoverySiteReview::bingen", "BlueDogRecoverySiteReview::stevenson", "BlueDogRecoverySiteReview::springCreek", "BlueDogRecoverySiteReview::viento", "BlueDogRecoverySiteReview::homeValley", "BlueDogRecoverySiteReview::drano")), columns = (
            Column(name = "Candidate", path = "site"),
            Column(name = "Access evidence", path = "evidence"),
            Column(name = "Before routing", path = "outstanding"),
            Column(name = "Desktop decision", path = "desktopDisposition"),
            Column(name = "Accepted", path = "acceptedForRouting")))
    }
    part def Shortlist :> Document {
        attribute redefines title = "Recovery-site assessment shortlist";
        part candidates : Table { calc rows : Candidates; }
    }
}

package BlueDogSRRFrontierDocuments {
    private import DocumentQueries::*;
    calc def Alternatives :> Query {
        Project(source = Named(qualifiedName = ("BlueDogSRRFrontier::point0", "BlueDogSRRFrontier::point1", "BlueDogSRRFrontier::point2", "BlueDogSRRFrontier::point3", "BlueDogSRRFrontier::point4", "BlueDogSRRFrontier::point5")), columns = (
            Column(name = "Length cap (m)", path = "capM"),
            Column(name = "Objective", path = "optimizationObjective"),
            Column(name = "Coarse feasible", path = "feasible"),
            Column(name = "Mass (kg)", path = "massKg"),
            Column(name = "Conditional passage (h)", path = "conditionalPassageHours"),
            Column(name = "Overall length (m)", path = "overallLengthM")))
    }
    part def Summary :> Document {
        attribute redefines title = "Bounded local sizing alternatives";
        part alternatives : Table { calc rows : Alternatives; }
    }
    calc def Replay :> Query {
        Project(source = Named(qualifiedName = "BlueDogSRRFrontier::retainedSeedReplay"), columns = (
            Column(name = "Mass (kg)", path = "massKg"),
            Column(name = "Westerly passage (h)", path = "westerlyHours"),
            Column(name = "Voyage energy margin", path = "voyageEnergyMargin"),
            Column(name = "Refined screens pass", path = "profileScreensPass"),
            Column(name = "Qualified", path = "qualified")))
    }
    part def SeedReplay :> Document {
        attribute redefines title = "Refined replay of the retained seed";
        part replay : Table { calc rows : Replay; }
    }
}

package BlueDogSRRReadinessDocuments {
    private import DocumentQueries::*;
    calc def EncounterRows :> Query {
        Project(source = Named(qualifiedName = "BlueDogEncounterReview::criteria"), columns = (
            Column(name = "Acquisition range m", path = "rangeAllocationM"),
            Column(name = "Acquisition s", path = "acquisitionSeconds"),
            Column(name = "Assessment s", path = "assessmentSeconds"),
            Column(name = "Command s", path = "commandSeconds"),
            Column(name = "Maneuver s", path = "maneuverSeconds"),
            Column(name = "Contingency s", path = "reserveSeconds")))
    }
    part def Encounters :> Document {
        attribute redefines title = "Traffic performance design allocation";
        part budget : Table { calc rows : EncounterRows; }
    }
    calc def SiteDecisionRows :> Query {
        Project(source = Named(qualifiedName = "BlueDogRecoverySiteReview::selection"), columns = (
            Column(name = "Endpoints", path = "primarySites"),
            Column(name = "Intermediate coverage", path = "intermediateSites"),
            Column(name = "Coverage acceptance", path = "coverageDecision")))
    }
    part def SiteDecision :> Document {
        attribute redefines title = "Recovery architecture decision";
        part selection : Table { calc rows : SiteDecisionRows; }
    }
}

package BlueDogSRRCurrentDocuments {
    private import DocumentQueries::*;
    calc def CandidateRows :> Query {
        Project(source = Named(qualifiedName = "BlueDogSRRCurrent::candidate"), columns = (
            Column(name = "Battery Wh", path = "batteryWh"),
            Column(name = "Mass kg", path = "massKg"),
            Column(name = "Passage h", path = "westerlyPassageHours"),
            Column(name = "Energy headroom Wh", path = "energyHeadroomWh"),
            Column(name = "Refined static screens pass", path = "staticScreensPass"),
            Column(name = "Physically qualified", path = "physicallyQualified")))
    }
    part def Summary :> Document {
        attribute redefines title = "Current SRR sizing candidate";
        part result : Table { calc rows : CandidateRows; }
    }
}
