"""Reviewed method selections, keyed to native verification definitions.

These are planned assessment methods, not executed or accepted evidence.
Procedural conditions remain authoritative in each existing case/requirement.
"""
VEHICLE={
    'test': '''ResetRecoveryVerification CommunicationsVerification IngressResponseVerification
        EmergencyControlVerification MarineDurabilityVerification TelemetryEquipmentVerification
        CommandIntegrityVerification GorgeWindVerification GorgeWavesVerification GorgeCurrentVerification
        GorgeSurvivalWavesVerification OceanWindVerification OceanWavesVerification OceanCurrentVerification
        OceanSurvivalWavesVerification AirTemperatureVerification WaterTemperatureVerification HumidityVerification
        CalmOperationVerification EnvelopeTransitionVerification WetMechanicalIntegrityVerification
        WetElectricalIntegrityVerification SolarHeatingVerification SelfRightingVerification
        CapsizeControlRecoveryVerification SubmergedWeedPassageVerification WeedSnagSheddingVerification
        WeedBlockageResponseVerification RecoveryPropulsorWeedsVerification NavigationAvailabilityVerification
        LaunchEnergyAdmissionVerification ChallengeMotorInhibitionVerification''',
    'test analyze': '''RoundTripVerification MultiDayEnduranceVerification EnergyAwarenessVerification
        NavigationAndControlVerification LowEnergyRecoveryVerification TrafficSafetyVerification
        OperatingBoundaryVerification EnvironmentalEnvelopeVerification RecoveryPropulsionVerification
        RecoveryEnergyVerification VisibilityVerification PrintedMaterialAgingVerification WindObservationVerification
        StructuralMaterialEvidence FunctionalDeformationEvidence StructuralLoadEvidence FlotationEvidence
        LaunchSiteEvidence CapsizeResilienceVerification MissionCapabilityVerification PeakSupplyCapabilityVerification
        VegetationResilienceVerification''',
    'test inspect': '''MissionEvidenceVerification TransportabilityVerification ServiceabilityVerification
        NavigationConspicuityVerification''',
    'inspect analyze': '''DesktopManufactureVerification EnergyEvidenceReadinessVerification
        FailureDispositionVerification StructuralPrintEnvelope ReliabilityEvidenceVerification''',
    'inspect': 'RegulatoryClassificationVerification ConstructionArchitectureVerification',
    'analyze': 'SustainedReserveProtectionVerification MissionPerformanceAssessmentVerification',
}
MISSION={
    'test': '''SafetyCapabilityAbortVerification AbortAlertVerification CasualtyFlotationVerification
        CapsizeRecoveryVerification OutageAutonomyVerification WeatherOutageContinuationVerification
        NightOperationVerification AbortPersistenceVerification ObservationAndInterventionVerification''',
    'test analyze': '''AutonomousShoreRecoveryVerification UnattachedPassageVerification ForecastAdmissionVerification
        CourseRecoveryReserveVerification ReserveAbortVerification WindSportEncounterVerification
        LocationTrafficAdmissionVerification InlandLookoutAndAvoidanceVerification InlandEncounterConductVerification
        InlandChannelAndVisibilityVerification PassageQualificationVerification''',
    'test inspect': 'MajorComponentRetentionVerification RecoveryConspicuityVerification InlandSignalsVerification',
    'inspect analyze': 'NoLitteringVerification InlandApplicabilityVerification',
    'inspect test analyze': '''OverallLengthVerification NavigationRulesEntryAndAdjudicationVerification
        RestrictedWatersVerification''',
}

def selections():
    result={}
    for package,groups in [('BlueDogRequirementVerification',VEHICLE),('GorgeChallengeVerification',MISSION)]:
        for methods,names in groups.items():
            for name in names.split():
                identifier=package+'::'+name
                assert identifier not in result,identifier
                result[identifier]=tuple(methods.split())
    return result
