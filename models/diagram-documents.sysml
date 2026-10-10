package BlueDogDiagramDocuments {
    private import DocumentQueries::*;
    part def ArchitectureDiagram :> Document {
        attribute redefines title = "Boat definition and composition";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::architecture;
        }
    }
    part def ContextDiagram :> Document {
        attribute redefines title = "Mission context";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::context;
        }
    }
    part def DetailDiagram :> Document {
        attribute redefines title = "Detailed composition";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::detail;
        }
    }
    part def UseCasesDiagram :> Document {
        attribute redefines title = "Use cases and requirements";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogUseCaseViews::operations;
        }
    }
    calc def Statements1 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::transGorgeChallenge", "GorgeChallenge::courseCompletion", "GorgeChallenge::repeatedOperation", "GorgeChallenge::unassistedAttempt", "GorgeChallenge::sailingPropulsion", "GorgeChallenge::liveObservation", "GorgeChallenge::emergencyIntervention")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def TransGorgeChallengeRequirements :> Document {
        attribute redefines title = "C-000 TransGorgeChallenge relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements1; }
        part group1 : Section { attribute redefines title = "C-000 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::transGorgeChallenge1; } }
        part group2 : Section { attribute redefines title = "C-000 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::transGorgeChallenge2; } }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: C-001 CourseCompletion"; attribute redefines target = "requirements-c-001.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: C-002 RepeatedOperation"; attribute redefines target = "requirements-c-002.md"; } }
        part next2 : Paragraph { part link : Link { attribute redefines text = "Continue: C-003 UnassistedAttempt"; attribute redefines target = "requirements-c-003.md"; } }
        part next3 : Paragraph { part link : Link { attribute redefines text = "Continue: C-004 SailingPropulsion"; attribute redefines target = "requirements-c-004.md"; } }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: C-005 LiveObservation"; attribute redefines target = "requirements-c-005.md"; } }
        part next5 : Paragraph { part link : Link { attribute redefines text = "Continue: C-006 EmergencyIntervention"; attribute redefines target = "requirements-c-006.md"; } }
    }
    calc def Statements2 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::courseCompletion", "BlueDogRequirements::roundTrip")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def CourseCompletionRequirements :> Document {
        attribute redefines title = "C-001 CourseCompletion relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements2; }
        part group1 : Section { attribute redefines title = "C-001 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::courseCompletion1; } }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: M-001 RoundTrip"; attribute redefines target = "requirements-m-001.md"; } }
    }
    calc def Statements3 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::repeatedOperation")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis3 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::challengeEndurance", "BlueDogRequirements::energyDerivation1", "BlueDogRequirements::cruiseReliabilityDerivation5")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def RepeatedOperationRequirements :> Document {
        attribute redefines title = "C-002 RepeatedOperation relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements3; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis3; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: L-001 MissionReliability"; attribute redefines target = "requirements-l-001.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: E-200 SustainedEnergyFeasibility"; attribute redefines target = "requirements-e-200.md"; } }
        part next2 : Paragraph { part link : Link { attribute redefines text = "Continue: M-002 MultiDayEndurance"; attribute redefines target = "requirements-m-002.md"; } }
    }
    calc def Statements4 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::unassistedAttempt")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis4 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::challengeAutonomy", "BlueDogRequirements::auditDerivation4", "BlueDogRequirements::auditDerivation5")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def UnassistedAttemptRequirements :> Document {
        attribute redefines title = "C-003 UnassistedAttempt relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements4; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis4; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: C-102 CommandIntegrity"; attribute redefines target = "requirements-c-102.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: R-004 ChallengeMotorInhibition"; attribute redefines target = "requirements-r-004.md"; } }
        part next2 : Paragraph { part link : Link { attribute redefines text = "Continue: E-002 NavigationAndControl"; attribute redefines target = "requirements-e-002.md"; } }
    }
    calc def Statements5 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::sailingPropulsion")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis5 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::challengePropulsion", "BlueDogRequirements::auditDerivation3")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def SailingPropulsionRequirements :> Document {
        attribute redefines title = "C-004 SailingPropulsion relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements5; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis5; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: R-004 ChallengeMotorInhibition"; attribute redefines target = "requirements-r-004.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: M-001 RoundTrip"; attribute redefines target = "requirements-m-001.md"; } }
    }
    calc def Statements6 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::liveObservation", "BlueDogRequirements::communications")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def LiveObservationRequirements :> Document {
        attribute redefines title = "C-005 LiveObservation relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements6; }
        part group1 : Section { attribute redefines title = "C-005 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::liveObservation1; } }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: E-005 Communications"; attribute redefines target = "requirements-e-005.md"; } }
    }
    calc def Statements7 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("GorgeChallenge::emergencyIntervention")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis7 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::challengeOverride", "BlueDogRequirements::deriveSafeRecovery", "BlueDogRequirements::auditDerivation6")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def EmergencyInterventionRequirements :> Document {
        attribute redefines title = "C-006 EmergencyIntervention relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements7; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis7; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: C-102 CommandIntegrity"; attribute redefines target = "requirements-c-102.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: S-003 SafeRecovery"; attribute redefines target = "requirements-s-003.md"; } }
        part next2 : Paragraph { part link : Link { attribute redefines text = "Continue: E-005 Communications"; attribute redefines target = "requirements-e-005.md"; } }
    }
    calc def Statements8 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDog::Goals::hawaiiVoyage")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis8 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::hawaiiMultiDayEndurance", "BlueDogRequirements::hawaiiNavigationAndControl", "BlueDogRequirements::hawaiiCommunications", "BlueDogRequirements::hawaiiResetRecovery", "BlueDogRequirements::hawaiiMissionEvidence", "BlueDogRequirements::hawaiiEnvironment", "BlueDogRequirements::deriveOceanEnvironment", "BlueDogRequirements::auditDerivation7", "BlueDogRequirements::auditDerivation8", "BlueDogRequirements::auditDerivation9", "BlueDogRequirements::energyDerivation2", "BlueDogRequirements::cruiseReliabilityDerivation2", "BlueDogRequirements::cruiseReliabilityDerivation4")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def HawaiiVoyageRequirements :> Document {
        attribute redefines title = "H-001 HawaiiVoyage relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements8; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis8; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: L-001 MissionReliability"; attribute redefines target = "requirements-l-001.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: Q-001 CruisePerformance"; attribute redefines target = "requirements-q-001.md"; } }
        part next2 : Paragraph { part link : Link { attribute redefines text = "Continue: E-200 SustainedEnergyFeasibility"; attribute redefines target = "requirements-e-200.md"; } }
        part next3 : Paragraph { part link : Link { attribute redefines text = "Continue: P-003 Serviceability"; attribute redefines target = "requirements-p-003.md"; } }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: S-005 RegulatoryClassification"; attribute redefines target = "requirements-s-005.md"; } }
        part next5 : Paragraph { part link : Link { attribute redefines text = "Continue: S-002 OperatingBoundary"; attribute redefines target = "requirements-s-002.md"; } }
        part next6 : Paragraph { part link : Link { attribute redefines text = "Continue: N-020 OceanEnvironment"; attribute redefines target = "requirements-n-020.md"; } }
        part next7 : Paragraph { part link : Link { attribute redefines text = "Continue: N-001 EnvironmentalEnvelope"; attribute redefines target = "requirements-n-001.md"; } }
        part next8 : Paragraph { part link : Link { attribute redefines text = "Continue: E-007 MissionEvidence"; attribute redefines target = "requirements-e-007.md"; } }
        part next9 : Paragraph { part link : Link { attribute redefines text = "Continue: E-003 ResetRecovery"; attribute redefines target = "requirements-e-003.md"; } }
        part next10 : Paragraph { part link : Link { attribute redefines text = "Continue: E-005 Communications"; attribute redefines target = "requirements-e-005.md"; } }
        part next11 : Paragraph { part link : Link { attribute redefines text = "Continue: E-002 NavigationAndControl"; attribute redefines target = "requirements-e-002.md"; } }
        part next12 : Paragraph { part link : Link { attribute redefines text = "Continue: M-002 MultiDayEndurance"; attribute redefines target = "requirements-m-002.md"; } }
    }
    calc def Statements9 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::roundTrip")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis9 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::roundTripNavigation", "BlueDogRequirements::roundTripReset", "BlueDogRequirements::roundTripCommunications", "BlueDogRequirements::roundTripIngress", "BlueDogRequirements::roundTripEvidence", "BlueDogRequirements::deriveOperatingBoundary", "BlueDogRequirements::deriveRegulatoryClassification", "BlueDogRequirements::deriveEnvironmentalEnvelope", "BlueDogRequirements::deriveGorgeEnvironment", "BlueDogRequirements::cruiseReliabilityDerivation1", "BlueDogRequirements::cruiseReliabilityDerivation3")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def RoundTripRequirements :> Document {
        attribute redefines title = "M-001 RoundTrip relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements9; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis9; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: L-001 MissionReliability"; attribute redefines target = "requirements-l-001.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: Q-001 CruisePerformance"; attribute redefines target = "requirements-q-001.md"; } }
        part next2 : Paragraph { part link : Link { attribute redefines text = "Continue: N-010 GorgeEnvironment"; attribute redefines target = "requirements-n-010.md"; } }
        part next3 : Paragraph { part link : Link { attribute redefines text = "Continue: N-001 EnvironmentalEnvelope"; attribute redefines target = "requirements-n-001.md"; } }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: S-005 RegulatoryClassification"; attribute redefines target = "requirements-s-005.md"; } }
        part next5 : Paragraph { part link : Link { attribute redefines text = "Continue: S-002 OperatingBoundary"; attribute redefines target = "requirements-s-002.md"; } }
        part next6 : Paragraph { part link : Link { attribute redefines text = "Continue: E-007 MissionEvidence"; attribute redefines target = "requirements-e-007.md"; } }
        part next7 : Paragraph { part link : Link { attribute redefines text = "Continue: E-006 IngressResponse"; attribute redefines target = "requirements-e-006.md"; } }
        part next8 : Paragraph { part link : Link { attribute redefines text = "Continue: E-005 Communications"; attribute redefines target = "requirements-e-005.md"; } }
        part next9 : Paragraph { part link : Link { attribute redefines text = "Continue: E-003 ResetRecovery"; attribute redefines target = "requirements-e-003.md"; } }
        part next10 : Paragraph { part link : Link { attribute redefines text = "Continue: E-002 NavigationAndControl"; attribute redefines target = "requirements-e-002.md"; } }
    }
    calc def Statements10 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::multiDayEndurance", "BlueDogRequirements::sustainedReserveProtection", "BlueDogRequirements::peakSupplyCapability", "BlueDogRequirements::harvestCampaignCoverage", "BlueDogRequirements::energyEvidenceReadiness")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis10 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::enduranceEnergy", "BlueDogRequirements::enduranceLimpMode")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def MultiDayEnduranceRequirements :> Document {
        attribute redefines title = "M-002 MultiDayEndurance relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements10; }
        part group1 : Section { attribute redefines title = "M-002 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::multiDayEndurance1; } }
        part group2 : Section { attribute redefines title = "M-002 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::multiDayEndurance2; } }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis10; }
        }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: E-004 LowEnergyRecovery"; attribute redefines target = "requirements-e-004.md"; } }
        part next5 : Paragraph { part link : Link { attribute redefines text = "Continue: E-001 EnergyAwareness"; attribute redefines target = "requirements-e-001.md"; } }
    }
    calc def Statements11 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::energyAwareness", "BlueDogRequirements::energyEstimateCadence", "BlueDogRequirements::reserveEstimateCadence", "BlueDogRequirements::energyEstimateAccuracy", "BlueDogRequirements::conservativeEnergyEstimate")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis11 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::energyLimpMode")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def EnergyAwarenessRequirements :> Document {
        attribute redefines title = "E-001 EnergyAwareness relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements11; }
        part group1 : Section { attribute redefines title = "E-001 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::energyAwareness1; } }
        part group2 : Section { attribute redefines title = "E-001 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::energyAwareness2; } }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis11; }
        }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: E-004 LowEnergyRecovery"; attribute redefines target = "requirements-e-004.md"; } }
    }
    calc def Statements12 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::navigationAndControl", "BlueDogRequirements::navigationAvailability", "BlueDogRequirements::guidanceUpdateCadence", "BlueDogRequirements::sailCommandCadence", "BlueDogRequirements::steeringCommandCadence", "BlueDogRequirements::positionAccuracy", "BlueDogRequirements::headingAccuracy")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis12 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::deriveTrafficSafety")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def NavigationAndControlRequirements :> Document {
        attribute redefines title = "E-002 NavigationAndControl relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements12; }
        part group1 : Section { attribute redefines title = "E-002 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::navigationAndControl1; } }
        part group2 : Section { attribute redefines title = "E-002 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::navigationAndControl2; } }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis12; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: E-008 NavigationAvailability"; attribute redefines target = "requirements-e-008.md"; } }
        part next6 : Paragraph { part link : Link { attribute redefines text = "Continue: S-001 TrafficSafety"; attribute redefines target = "requirements-s-001.md"; } }
    }
    calc def Statements13 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::trafficSafety", "BlueDogRequirements::trafficTracking", "BlueDogRequirements::collisionAssessmentCadence", "BlueDogRequirements::avoidanceCommandDeadline", "BlueDogRequirements::trafficAwarenessFault")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis13 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::deriveNavigationConspicuity")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def TrafficSafetyRequirements :> Document {
        attribute redefines title = "S-001 TrafficSafety relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements13; }
        part group1 : Section { attribute redefines title = "S-001 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::trafficSafety1; } }
        part group2 : Section { attribute redefines title = "S-001 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::trafficSafety2; } }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis13; }
        }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: S-004 NavigationConspicuity"; attribute redefines target = "requirements-s-004.md"; } }
    }
    calc def Statements14 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::environmentalEnvelope", "BlueDogRequirements::airTemperature", "BlueDogRequirements::waterTemperature", "BlueDogRequirements::humidity", "BlueDogRequirements::visibility", "BlueDogRequirements::calmOperation", "BlueDogRequirements::envelopeTransition")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis14 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::deriveMarineDurability", "BlueDogRequirements::deriveStabilityAndFouling")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def EnvironmentalEnvelopeRequirements :> Document {
        attribute redefines title = "N-001 EnvironmentalEnvelope relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements14; }
        part group1 : Section { attribute redefines title = "N-001 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::environmentalEnvelope1; } }
        part group2 : Section { attribute redefines title = "N-001 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::environmentalEnvelope2; } }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis14; }
        }
        part next3 : Paragraph { part link : Link { attribute redefines text = "Continue: N-033 Visibility"; attribute redefines target = "requirements-n-033.md"; } }
        part next5 : Paragraph { part link : Link { attribute redefines text = "Continue: N-035 EnvelopeTransition"; attribute redefines target = "requirements-n-035.md"; } }
        part next6 : Paragraph { part link : Link { attribute redefines text = "Continue: N-003 StabilityAndFouling"; attribute redefines target = "requirements-n-003.md"; } }
        part next7 : Paragraph { part link : Link { attribute redefines text = "Continue: N-002 MarineDurability"; attribute redefines target = "requirements-n-002.md"; } }
    }
    calc def Statements15 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::safeRecovery", "BlueDogRequirements::abortLatchDeadline", "BlueDogRequirements::recoveryTelemetryCadence", "BlueDogRequirements::motorIsolationDeadline", "BlueDogRequirements::isolationRestartInhibition", "BlueDogRequirements::manualControlLossShutdown", "BlueDogRequirements::controlLossLocationContinuity", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::motorQualificationInvariant", "BlueDogRequirements::periodicLogCadence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis15 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::deriveRecoveryPropulsion")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def SafeRecoveryRequirements :> Document {
        attribute redefines title = "S-003 SafeRecovery relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements15; }
        part group1 : Section { attribute redefines title = "S-003 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::safeRecovery1; } }
        part group2 : Section { attribute redefines title = "S-003 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::safeRecovery2; } }
        part group3 : Section { attribute redefines title = "S-003 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::safeRecovery3; } }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis15; }
        }
        part next9 : Paragraph { part link : Link { attribute redefines text = "Continue: R-001 RecoveryPropulsion"; attribute redefines target = "requirements-r-001.md"; } }
    }
    calc def Statements16 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::recoveryPropulsion")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis16 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::deriveRecoveryEnergy", "BlueDogRequirements::motorWeedTolerance")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def RecoveryPropulsionRequirements :> Document {
        attribute redefines title = "R-001 RecoveryPropulsion relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements16; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis16; }
        }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: N-056 RecoveryPropulsorWeeds"; attribute redefines target = "requirements-n-056.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: R-002 RecoveryEnergy"; attribute redefines target = "requirements-r-002.md"; } }
    }
    calc def Statements17 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::communications", "BlueDogRequirements::telemetryDeliveryCadence", "BlueDogRequirements::outageAutonomy", "BlueDogRequirements::reconnectCurrentRecord", "BlueDogRequirements::backlogOrdering", "BlueDogRequirements::backlogCurrentPriority", "BlueDogRequirements::logRetention", "BlueDogRequirements::reconnectLogPreservation")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis17 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::deriveTelemetryEquipment", "BlueDogRequirements::deriveCommandIntegrity")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def CommunicationsRequirements :> Document {
        attribute redefines title = "E-005 Communications relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements17; }
        part group1 : Section { attribute redefines title = "E-005 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::communications1; } }
        part group2 : Section { attribute redefines title = "E-005 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::communications2; } }
        part group3 : Section { attribute redefines title = "E-005 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::communications3; } }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis17; }
        }
        part next7 : Paragraph { part link : Link { attribute redefines text = "Continue: C-102 CommandIntegrity"; attribute redefines target = "requirements-c-102.md"; } }
        part next8 : Paragraph { part link : Link { attribute redefines text = "Continue: C-101 TelemetryEquipment"; attribute redefines target = "requirements-c-101.md"; } }
    }
    calc def Statements18 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::gorgeEnvironment", "BlueDogRequirements::gorgeWind", "BlueDogRequirements::gorgeWaves", "BlueDogRequirements::gorgeCurrent", "BlueDogRequirements::gorgeSurvivalWind", "BlueDogRequirements::gorgeSurvivalWaves", "BlueDogRequirements::freshwaterExposure", "BlueDogRequirements::submergedWeedPassage", "BlueDogRequirements::weedSnagShedding")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def GorgeEnvironmentRequirements :> Document {
        attribute redefines title = "N-010 GorgeEnvironment relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements18; }
        part group1 : Section { attribute redefines title = "N-010 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::gorgeEnvironment1; } }
        part group2 : Section { attribute redefines title = "N-010 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::gorgeEnvironment2; } }
        part group3 : Section { attribute redefines title = "N-010 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::gorgeEnvironment3; } }
        part next6 : Paragraph { part link : Link { attribute redefines text = "Continue: N-053 SubmergedWeedPassage"; attribute redefines target = "requirements-n-053.md"; } }
        part next7 : Paragraph { part link : Link { attribute redefines text = "Continue: N-054 WeedSnagShedding"; attribute redefines target = "requirements-n-054.md"; } }
    }
    calc def Statements19 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::oceanEnvironment", "BlueDogRequirements::oceanWind", "BlueDogRequirements::oceanWaves", "BlueDogRequirements::oceanCurrent", "BlueDogRequirements::oceanSurvivalWind", "BlueDogRequirements::oceanSurvivalWaves", "BlueDogRequirements::saltwaterExposure")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def OceanEnvironmentRequirements :> Document {
        attribute redefines title = "N-020 OceanEnvironment relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements19; }
        part group1 : Section { attribute redefines title = "N-020 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::oceanEnvironment1; } }
        part group2 : Section { attribute redefines title = "N-020 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::oceanEnvironment2; } }
    }
    calc def Statements20 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::marineDurability", "BlueDogRequirements::freshwaterExposure", "BlueDogRequirements::saltwaterExposure", "BlueDogRequirements::enclosureSealing", "BlueDogRequirements::wetMechanicalIntegrity", "BlueDogRequirements::wetElectricalIntegrity", "BlueDogRequirements::solarHeating", "BlueDogRequirements::printedMaterialAging")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def MarineDurabilityRequirements :> Document {
        attribute redefines title = "N-002 MarineDurability relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements20; }
        part group1 : Section { attribute redefines title = "N-002 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::marineDurability1; } }
        part group2 : Section { attribute redefines title = "N-002 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::marineDurability2; } }
        part group3 : Section { attribute redefines title = "N-002 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::marineDurability3; } }
        part next3 : Paragraph { part link : Link { attribute redefines text = "Continue: N-044 WetMechanicalIntegrity"; attribute redefines target = "requirements-n-044.md"; } }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: N-045 WetElectricalIntegrity"; attribute redefines target = "requirements-n-045.md"; } }
        part next5 : Paragraph { part link : Link { attribute redefines text = "Continue: N-046 SolarHeating"; attribute redefines target = "requirements-n-046.md"; } }
    }
    calc def Statements21 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::stabilityAndFouling", "BlueDogRequirements::selfRighting", "BlueDogRequirements::capsizeControlRecovery", "BlueDogRequirements::submergedWeedPassage", "BlueDogRequirements::weedSnagShedding", "BlueDogRequirements::weedBlockageResponse", "BlueDogRequirements::recoveryPropulsorWeeds")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def StabilityAndFoulingRequirements :> Document {
        attribute redefines title = "N-003 StabilityAndFouling relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements21; }
        part group1 : Section { attribute redefines title = "N-003 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::stabilityAndFouling1; } }
        part group2 : Section { attribute redefines title = "N-003 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::stabilityAndFouling2; } }
        part next0 : Paragraph { part link : Link { attribute redefines text = "Continue: N-051 SelfRighting"; attribute redefines target = "requirements-n-051.md"; } }
        part next1 : Paragraph { part link : Link { attribute redefines text = "Continue: N-052 CapsizeControlRecovery"; attribute redefines target = "requirements-n-052.md"; } }
        part next2 : Paragraph { part link : Link { attribute redefines text = "Continue: N-053 SubmergedWeedPassage"; attribute redefines target = "requirements-n-053.md"; } }
        part next3 : Paragraph { part link : Link { attribute redefines text = "Continue: N-054 WeedSnagShedding"; attribute redefines target = "requirements-n-054.md"; } }
        part next4 : Paragraph { part link : Link { attribute redefines text = "Continue: N-055 WeedBlockageResponse"; attribute redefines target = "requirements-n-055.md"; } }
        part next5 : Paragraph { part link : Link { attribute redefines text = "Continue: N-056 RecoveryPropulsorWeeds"; attribute redefines target = "requirements-n-056.md"; } }
    }
    calc def Statements22 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::recoveryEnergy")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    calc def DesignBasis22 :> Query {
        Project(source = Named(qualifiedName = ("BlueDogRequirements::auditDerivation2", "BlueDogRequirements::energyDerivation11")), columns = (
            Column(name = "Dependent requirement", cell = { in row : KerML::Root::Dependency; row.client }),
            Column(name = "Design basis", cell = { in row : KerML::Root::Dependency; row.supplier }),
            Column(name = "Rationale", path = "rationale.text")))
    }
    part def RecoveryEnergyRequirements :> Document {
        attribute redefines title = "R-002 RecoveryEnergy relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements22; }
        part basis : Section { attribute redefines title = "Design decisions motivated by this requirement";
            part meaning : Paragraph { attribute redefines text = "Plain dependencies record design basis, not derivation or refinement. The native GeneralView renderer does not draw these dependencies; their actual endpoints and rationale are reported here."; }
            part entries : Table { calc rows : DesignBasis22; }
        }
    }
    calc def Statements23 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::resetRecovery", "BlueDogRequirements::restartDeadline", "BlueDogRequirements::missionStateRestoration", "BlueDogRequirements::gateProgressRestoration", "BlueDogRequirements::resetRestrictionPreservation", "BlueDogRequirements::qualificationRestoration", "BlueDogRequirements::logInterruptionDurability", "BlueDogRequirements::unknownQualificationFallback", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::freshRecoveryCommand", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def ResetRecoveryRequirements :> Document {
        attribute redefines title = "E-003 ResetRecovery relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements23; }
        part group1 : Section { attribute redefines title = "E-003 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::resetRecovery1; } }
        part group2 : Section { attribute redefines title = "E-003 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::resetRecovery2; } }
        part group3 : Section { attribute redefines title = "E-003 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::resetRecovery3; } }
        part group4 : Section { attribute redefines title = "E-003 relationships 4"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::resetRecovery4; } }
    }
    calc def Statements24 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::lowEnergyRecovery", "BlueDogRequirements::lowEnergyEntry", "BlueDogRequirements::lowEnergyPayloadInhibition", "BlueDogRequirements::lowEnergyNavigationContinuity", "BlueDogRequirements::lowEnergyCollisionContinuity", "BlueDogRequirements::lowEnergyExit", "BlueDogRequirements::payloadRestartPermission", "BlueDogRequirements::periodicLogCadence", "BlueDogRequirements::telemetryDeliveryCadence", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def LowEnergyRecoveryRequirements :> Document {
        attribute redefines title = "E-004 LowEnergyRecovery relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements24; }
        part group1 : Section { attribute redefines title = "E-004 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::lowEnergyRecovery1; } }
        part group2 : Section { attribute redefines title = "E-004 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::lowEnergyRecovery2; } }
        part group3 : Section { attribute redefines title = "E-004 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::lowEnergyRecovery3; } }
        part group4 : Section { attribute redefines title = "E-004 relationships 4"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::lowEnergyRecovery4; } }
    }
    calc def Statements25 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::ingressResponse", "BlueDogRequirements::ingressDetection", "BlueDogRequirements::ingressRecoveryRequest", "BlueDogRequirements::ingressFlotation", "BlueDogRequirements::ingressElectronicsProtection", "BlueDogRequirements::ingressPositionContinuity", "BlueDogRequirements::ingressEventDeadline", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def IngressResponseRequirements :> Document {
        attribute redefines title = "E-006 IngressResponse relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements25; }
        part group1 : Section { attribute redefines title = "E-006 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::ingressResponse1; } }
        part group2 : Section { attribute redefines title = "E-006 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::ingressResponse2; } }
        part group3 : Section { attribute redefines title = "E-006 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::ingressResponse3; } }
    }
    calc def Statements26 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::missionEvidence", "BlueDogRequirements::periodicLogCadence", "BlueDogRequirements::logRetention", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::logTimestampAccuracy", "BlueDogRequirements::invalidTimestampMarking", "BlueDogRequirements::logGapIndication", "BlueDogRequirements::logInterruptionDurability", "BlueDogRequirements::reconnectLogPreservation", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::unknownQualificationFallback")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def MissionEvidenceRequirements :> Document {
        attribute redefines title = "E-007 MissionEvidence relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements26; }
        part group1 : Section { attribute redefines title = "E-007 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionEvidence1; } }
        part group2 : Section { attribute redefines title = "E-007 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionEvidence2; } }
        part group3 : Section { attribute redefines title = "E-007 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionEvidence3; } }
        part group4 : Section { attribute redefines title = "E-007 relationships 4"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionEvidence4; } }
    }
    calc def Statements27 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::navigationAvailability", "BlueDogRequirements::navigationValidEpochs", "BlueDogRequirements::staleNavigationInvalidation", "BlueDogRequirements::navigationDegradedTransition", "BlueDogRequirements::staleNavigationUseInhibition", "BlueDogRequirements::criticalEventRecording")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def NavigationAvailabilityRequirements :> Document {
        attribute redefines title = "E-008 NavigationAvailability relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements27; }
        part group1 : Section { attribute redefines title = "E-008 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::navigationAvailability1; } }
        part group2 : Section { attribute redefines title = "E-008 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::navigationAvailability2; } }
    }
    calc def Statements28 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::transportability", "BlueDogRequirements::soloTransport", "BlueDogRequirements::liftMass", "BlueDogRequirements::setupDuration", "BlueDogRequirements::packDuration", "BlueDogRequirements::soloLaunch", "BlueDogRequirements::soloRetrieval")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def TransportabilityRequirements :> Document {
        attribute redefines title = "P-001 Transportability relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements28; }
        part group1 : Section { attribute redefines title = "P-001 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::transportability1; } }
        part group2 : Section { attribute redefines title = "P-001 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::transportability2; } }
    }
    calc def Statements29 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::serviceability", "BlueDogRequirements::replacementDuration", "BlueDogRequirements::nondestructiveService", "BlueDogRequirements::postServiceSealing", "BlueDogRequirements::postServiceActuation")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def ServiceabilityRequirements :> Document {
        attribute redefines title = "P-003 Serviceability relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements29; }
        part group1 : Section { attribute redefines title = "P-003 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::serviceability1; } }
        part group2 : Section { attribute redefines title = "P-003 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::serviceability2; } }
    }
    calc def Statements30 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::operatingBoundary", "BlueDogRequirements::boundaryEvaluationCadence", "BlueDogRequirements::boundaryAvoidanceDeadline", "BlueDogRequirements::boundaryAvoidanceRecording", "BlueDogRequirements::boundaryStartInhibition", "BlueDogRequirements::boundaryDegradedEvidence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def OperatingBoundaryRequirements :> Document {
        attribute redefines title = "S-002 OperatingBoundary relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements30; }
        part group1 : Section { attribute redefines title = "S-002 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::operatingBoundary1; } }
        part group2 : Section { attribute redefines title = "S-002 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::operatingBoundary2; } }
    }
    calc def Statements31 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::navigationConspicuity", "BlueDogRequirements::navigationLightPresentation", "BlueDogRequirements::navigationShapePresentation", "BlueDogRequirements::navigationSoundPresentation", "BlueDogRequirements::signalingModeDeadline", "BlueDogRequirements::signalingFaultRecording", "BlueDogRequirements::signalingFaultReporting")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def NavigationConspicuityRequirements :> Document {
        attribute redefines title = "S-004 NavigationConspicuity relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements31; }
        part group1 : Section { attribute redefines title = "S-004 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::navigationConspicuity1; } }
        part group2 : Section { attribute redefines title = "S-004 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::navigationConspicuity2; } }
    }
    calc def Statements32 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::regulatoryClassification", "BlueDogRequirements::deploymentComplianceRecord", "BlueDogRequirements::deploymentReleaseGate")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def RegulatoryClassificationRequirements :> Document {
        attribute redefines title = "S-005 RegulatoryClassification relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements32; }
        part group1 : Section { attribute redefines title = "S-005 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::regulatoryClassification1; } }
    }
    calc def Statements33 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::telemetryEquipment", "BlueDogRequirements::telemetryDisplayContent", "BlueDogRequirements::telemetryStaleIndication", "BlueDogRequirements::telemetryIdentityPreservation", "BlueDogRequirements::telemetryDuplicateSuppression")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def TelemetryEquipmentRequirements :> Document {
        attribute redefines title = "C-101 TelemetryEquipment relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements33; }
        part group1 : Section { attribute redefines title = "C-101 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::telemetryEquipment1; } }
        part group2 : Section { attribute redefines title = "C-101 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::telemetryEquipment2; } }
    }
    calc def Statements34 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::commandIntegrity", "BlueDogRequirements::unauthenticatedCommandRejection", "BlueDogRequirements::replayCommandRejection", "BlueDogRequirements::expiredCommandRejection", "BlueDogRequirements::acceptedCommandDeadline", "BlueDogRequirements::onboardAcknowledgmentDeadline", "BlueDogRequirements::acknowledgmentQueueing", "BlueDogRequirements::externalControlDisqualification", "BlueDogRequirements::criticalEventRecording", "BlueDogRequirements::qualificationPersistence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def CommandIntegrityRequirements :> Document {
        attribute redefines title = "C-102 CommandIntegrity relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements34; }
        part group1 : Section { attribute redefines title = "C-102 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::commandIntegrity1; } }
        part group2 : Section { attribute redefines title = "C-102 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::commandIntegrity2; } }
        part group3 : Section { attribute redefines title = "C-102 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::commandIntegrity3; } }
    }
    calc def Statements35 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::visibility", "BlueDogRequirements::visibilityNavigationCapability", "BlueDogRequirements::visibilityTrafficCapability", "BlueDogRequirements::restrictedVisibilityEntry", "BlueDogRequirements::restrictedVisibilityEvidence", "BlueDogRequirements::restrictedVisibilityCollisionAssessment")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def VisibilityRequirements :> Document {
        attribute redefines title = "N-033 Visibility relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements35; }
        part group1 : Section { attribute redefines title = "N-033 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::visibility1; } }
        part group2 : Section { attribute redefines title = "N-033 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::visibility2; } }
    }
    calc def Statements36 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::envelopeTransition", "BlueDogRequirements::survivalEntryDeadline", "BlueDogRequirements::survivalTransitionRecording", "BlueDogRequirements::sailingResumptionDeadline", "BlueDogRequirements::sailingResumptionInhibition", "BlueDogRequirements::resumptionBlockEvidence", "BlueDogRequirements::periodicLogCadence", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def EnvelopeTransitionRequirements :> Document {
        attribute redefines title = "N-035 EnvelopeTransition relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements36; }
        part group1 : Section { attribute redefines title = "N-035 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::envelopeTransition1; } }
        part group2 : Section { attribute redefines title = "N-035 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::envelopeTransition2; } }
        part group3 : Section { attribute redefines title = "N-035 relationships 3"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::envelopeTransition3; } }
    }
    calc def Statements37 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::wetMechanicalIntegrity", "BlueDogRequirements::wetMechanismTravel", "BlueDogRequirements::wetJointIntegrity")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def WetMechanicalIntegrityRequirements :> Document {
        attribute redefines title = "N-044 WetMechanicalIntegrity relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements37; }
        part group1 : Section { attribute redefines title = "N-044 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::wetMechanicalIntegrity1; } }
    }
    calc def Statements38 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::wetElectricalIntegrity", "BlueDogRequirements::wetConductorResistance", "BlueDogRequirements::wetInsulationResistance")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def WetElectricalIntegrityRequirements :> Document {
        attribute redefines title = "N-045 WetElectricalIntegrity relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements38; }
        part group1 : Section { attribute redefines title = "N-045 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::wetElectricalIntegrity1; } }
    }
    calc def Statements39 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::solarHeating", "BlueDogRequirements::hotSunElectronicsOperation", "BlueDogRequirements::hotSunBatteryTemperature", "BlueDogRequirements::batteryChargeTemperatureInhibition")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def SolarHeatingRequirements :> Document {
        attribute redefines title = "N-046 SolarHeating relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements39; }
        part group1 : Section { attribute redefines title = "N-046 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::solarHeating1; } }
    }
    calc def Statements40 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::selfRighting", "BlueDogRequirements::rightingDeadline", "BlueDogRequirements::capsizeRigRetention", "BlueDogRequirements::capsizeBallastRetention", "BlueDogRequirements::capsizeElectronicsSealing")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def SelfRightingRequirements :> Document {
        attribute redefines title = "N-051 SelfRighting relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements40; }
        part group1 : Section { attribute redefines title = "N-051 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::selfRighting1; } }
        part group2 : Section { attribute redefines title = "N-051 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::selfRighting2; } }
    }
    calc def Statements41 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::capsizeControlRecovery", "BlueDogRequirements::controlRecoveryDeadline", "BlueDogRequirements::capsizeGateProgressRetention", "BlueDogRequirements::capsizeQualificationRetention", "BlueDogRequirements::capsizeRestrictionRetention")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def CapsizeControlRecoveryRequirements :> Document {
        attribute redefines title = "N-052 CapsizeControlRecovery relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements41; }
        part group1 : Section { attribute redefines title = "N-052 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::capsizeControlRecovery1; } }
        part group2 : Section { attribute redefines title = "N-052 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::capsizeControlRecovery2; } }
    }
    calc def Statements42 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::submergedWeedPassage", "BlueDogRequirements::weedPassageSpeed", "BlueDogRequirements::weedPassageSteering")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def SubmergedWeedPassageRequirements :> Document {
        attribute redefines title = "N-053 SubmergedWeedPassage relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements42; }
        part group1 : Section { attribute redefines title = "N-053 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::submergedWeedPassage1; } }
    }
    calc def Statements43 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::weedSnagShedding", "BlueDogRequirements::weedSnagSpeedRecovery", "BlueDogRequirements::weedSnagSteeringRecovery")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def WeedSnagSheddingRequirements :> Document {
        attribute redefines title = "N-054 WeedSnagShedding relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements43; }
        part group1 : Section { attribute redefines title = "N-054 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::weedSnagShedding1; } }
    }
    calc def Statements44 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::weedBlockageResponse", "BlueDogRequirements::weedBlockageFault", "BlueDogRequirements::weedBlockageContingency", "BlueDogRequirements::weedBlockageLocation", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def WeedBlockageResponseRequirements :> Document {
        attribute redefines title = "N-055 WeedBlockageResponse relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements44; }
        part group1 : Section { attribute redefines title = "N-055 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::weedBlockageResponse1; } }
        part group2 : Section { attribute redefines title = "N-055 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::weedBlockageResponse2; } }
    }
    calc def Statements45 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::recoveryPropulsorWeeds", "BlueDogRequirements::poweredWeedSpeed", "BlueDogRequirements::poweredWeedCurrent", "BlueDogRequirements::poweredWeedTemperature", "BlueDogRequirements::lockedPropulsorShutdown", "BlueDogRequirements::motorQualificationInvariant")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def RecoveryPropulsorWeedsRequirements :> Document {
        attribute redefines title = "N-056 RecoveryPropulsorWeeds relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements45; }
        part group1 : Section { attribute redefines title = "N-056 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::recoveryPropulsorWeeds1; } }
        part group2 : Section { attribute redefines title = "N-056 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::recoveryPropulsorWeeds2; } }
    }
    calc def Statements46 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::challengeMotorInhibition", "BlueDogRequirements::motorQualificationInvariant", "BlueDogRequirements::freshRecoveryCommand", "BlueDogRequirements::qualificationPersistence", "BlueDogRequirements::criticalEventRecording")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def ChallengeMotorInhibitionRequirements :> Document {
        attribute redefines title = "R-004 ChallengeMotorInhibition relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements46; }
        part group1 : Section { attribute redefines title = "R-004 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::challengeMotorInhibition1; } }
        part group2 : Section { attribute redefines title = "R-004 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::challengeMotorInhibition2; } }
    }
    calc def Statements47 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::sustainedEnergyFeasibility", "BlueDogRequirements::sustainedReserveProtection", "BlueDogRequirements::repeatableCycleBalance", "BlueDogRequirements::peakSupplyCapability", "BlueDogRequirements::energyEvidenceReadiness")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def SustainedEnergyFeasibilityRequirements :> Document {
        attribute redefines title = "E-200 SustainedEnergyFeasibility relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements47; }
        part group1 : Section { attribute redefines title = "E-200 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::sustainedEnergyFeasibility1; } }
        part group2 : Section { attribute redefines title = "E-200 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::sustainedEnergyFeasibility2; } }
    }
    calc def Statements48 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::cruisePerformance", "BlueDogRequirements::legProgress", "BlueDogRequirements::passageDuration", "BlueDogRequirements::cruiseEvidence")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def CruisePerformanceRequirements :> Document {
        attribute redefines title = "Q-001 CruisePerformance relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements48; }
        part group1 : Section { attribute redefines title = "Q-001 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::cruisePerformance1; } }
    }
    calc def Statements49 :> Query {
        Project(source = RelatedElements(source = Named(qualifiedName = ("BlueDogRequirements::missionReliability", "BlueDogRequirements::missionSuccessProbability", "BlueDogRequirements::failureRateBudget", "BlueDogRequirements::reliabilityEvidence", "BlueDogRequirements::criticalFailureDisposition")), relationshipKind = "typing", direction = "outgoing", maxDepth = 1), properties = ("documentation"), columns = (Column(name = "Label", cell = { in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName })))
    }
    part def MissionReliabilityRequirements :> Document {
        attribute redefines title = "L-001 MissionReliability relationships";
        part navigation : Paragraph { part index : Link { attribute redefines text = "All requirement views"; attribute redefines target = "../requirements-views.md"; } }
        part context : Paragraph { part link : Link { attribute redefines text = "Conditions, rationale and verification"; attribute redefines target = "../requirements-context.md"; } }
        part statements : Definitions { attribute redefines term = "Label"; attribute redefines description = "documentation"; calc rows : Statements49; }
        part group1 : Section { attribute redefines title = "L-001 relationships 1"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionReliability1; } }
        part group2 : Section { attribute redefines title = "L-001 relationships 2"; part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogViews::missionReliability2; } }
    }
    part def MissionSemantics :> Document {
        attribute redefines title = "Challenge, vehicle and verification";
        part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogSemanticViews::MissionSemantics; }
    }
    part def EnergySemantics :> Document {
        attribute redefines title = "Energy acceptance, formalization and verification";
        part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogSemanticViews::EnergySemantics; }
    }
    part def CruiseSemantics :> Document {
        attribute redefines title = "Cruise acceptance and numerical refinement";
        part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogSemanticViews::CruiseSemantics; }
    }
    part def ReliabilitySemantics :> Document {
        attribute redefines title = "Reliability acceptance and numerical refinement";
        part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogSemanticViews::ReliabilitySemantics; }
    }
    part def ManufacturingSemantics :> Document {
        attribute redefines title = "Independent manufacturing constraint";
        part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogSemanticViews::ManufacturingSemantics; }
    }
    part def WeedSemantics :> Document {
        attribute redefines title = "Weed tolerance and design responsibility";
        part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogSemanticViews::WeedSemantics; }
    }
    part def SailingIntegrationDiagram :> Document {
        attribute redefines title = "Polar legs feed the cruise model";
        part diagram : Diagram { attribute redefines direction = "BT"; ref redefines source = BlueDogSemanticViews::SailingIntegration; }
    }
}
