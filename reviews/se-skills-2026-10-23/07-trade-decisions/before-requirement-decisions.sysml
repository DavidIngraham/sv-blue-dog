package BlueDogRequirementDecisions {
    private import ScalarValues::*;
    part def OpenDecision {
        attribute question : String;
        attribute evidenceNeeded : String;
        attribute owner : String = "Project owner";
        attribute accepted : Boolean = false;
    }
    part <'U01'> trafficAcceptance : OpenDecision {
        attribute :>> question = "Accept class-specific observation, response, clearance and reliability/confidence criteria and the deployment applicability matrix.";
        attribute :>> evidenceNeeded = "Installed class-specific observations and achieved responses; configuration-specific rule review and recorded authority.";
    }
    dependency trafficAcceptanceBasis1 from trafficAcceptance to BlueDogRequirements::trafficSafety;
    dependency trafficAcceptanceBasis2 from trafficAcceptance to BlueDogRequirements::regulatoryClassification;
    dependency trafficAcceptanceBasis3 from trafficAcceptance to GorgeChallenge::navigationRuleApplicability;
    part <'U02'> recoveryAcceptance : OpenDecision {
        attribute :>> question = "Establish independent course-wide recovery and physical retrieval.";
        attribute :>> evidenceNeeded = "Surveyed accessible shores, final capture/retention, casualty propulsion, onboard observations/control and protected power under no-contact faults.";
    }
    dependency recoveryAcceptanceBasis1 from recoveryAcceptance to BlueDogRequirements::recoveryPropulsion;
    dependency recoveryAcceptanceBasis2 from recoveryAcceptance to BlueDogRequirements::recoveryEnergy;
    dependency recoveryAcceptanceBasis3 from recoveryAcceptance to GorgeChallenge::capsizeRecovery;
    part <'U03'> structuralQualification : OpenDecision {
        attribute :>> question = "Accept actual structural loads and installed functional limits.";
        attribute :>> evidenceNeeded = "Wet and aged production materials/joints, impact/fatigue/buckling and combined environmental load evidence.";
    }
    dependency structuralQualificationBasis1 from structuralQualification to BlueDogStructure::structuralIntegrity;
    part <'U04'> installedControlEvidence : OpenDecision {
        attribute :>> question = "Connect supplied observations and commands to installed sensing and achieved motion.";
        attribute :>> evidenceNeeded = "Correlated apparent and 10 m true wind, navigation/traffic observations, maneuver response and interacting faults.";
    }
    dependency installedControlEvidenceBasis1 from installedControlEvidence to BlueDogRequirements::windObservation;
    dependency installedControlEvidenceBasis2 from installedControlEvidence to BlueDogRequirements::navigationAndControl;
    part <'U05'> integrationCoverage : OpenDecision {
        attribute :>> question = "Establish an integrated acceptance argument beyond sampled predicates and supplied Booleans.";
        attribute :>> evidenceNeeded = "Compatible configuration-specific whole-route, safety, energy, structural and casualty evidence with justified coverage and exclusions.";
    }
    dependency integrationCoverageBasis1 from integrationCoverage to BlueDogRequirements::missionReliability;
    dependency integrationCoverageBasis2 from integrationCoverage to BlueDogRequirements::cruisePerformance;
    part <'U06'> futureMissionAcceptance : OpenDecision {
        attribute :>> question = "Select independently scoped future voyage targets and acceptance.";
        attribute :>> evidenceNeeded = "Hawaii route, weather, ocean exposure, sustained energy, communications, maintenance and recovery decisions.";
    }
    dependency futureMissionAcceptanceBasis1 from futureMissionAcceptance to BlueDogMissionScope::future;
}
