package GorgeChallenge {
    doc /* Independent trans-gorge autonomous sailing challenge.
     * Inspired by the structure of the Microtransat rules:
     * https://microtransat.org/content.php?p=rules&top=rules
     * This is a separate project challenge, not a Microtransat entry or endorsement.
     * No vessel architecture, hull size, or communications technology is prescribed.
     * The Gorge is the proving ground for a longer-term voyage toward Hawaii.
     * Exact gates, corridor, time limit, route-specific acceptance evidence,
     * and formal attempt restart procedure remain open; the vehicle defines candidate environmental qualification profiles; no dam passage is assumed.
     */
    private import RequirementDerivation::*;
    requirement def <'C-000'> TransGorgeChallenge {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall complete the Trans-Gorge challenge under C-001 through C-006. */
        metadata rationale : ModelingMetadata::Rationale { text = "The first The Dalles–Bonneville–The Dalles circuit is the threshold; repeated circuits are the endurance objective."; }
    }
    requirement transGorgeChallenge : TransGorgeChallenge;
    requirement def <'C-001'> CourseCompletion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall complete a journey from The Dalles to Bonneville and back to The Dalles. */
        metadata issue : ModelingMetadata::Issue { text = "Start/finish and turnaround gates, permitted corridor and crossing evidence remain to be agreed."; }
    }
    requirement def <'C-002'> RepeatedOperation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After its first circuit, the vessel should repeat The Dalles–Bonneville–The Dalles autonomously for as long as practical. */
        comment notes /* This is an endurance objective, not a finite-duration pass/fail claim. */
        metadata issue : ModelingMetadata::Issue { text = "No fixed objective endurance duration has been selected."; }
    }
    requirement def <'C-003'> UnassistedAttempt {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A qualifying attempt shall complete the round trip without operator intervention. */
        comment conditions /* Passive live monitoring is permitted. Remote emergency abort or manual control disqualifies the attempt as unassisted. */
        metadata issue : ModelingMetadata::Issue { text = "Restart criteria remain to be agreed."; }
    }
    requirement def <'C-004'> SailingPropulsion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A qualifying attempt shall use sailing propulsion without auxiliary motor propulsion. */
        comment conditions /* An auxiliary motor may remain installed. Motor use is permitted during separate development tests and vessel recovery; use during an attempt ends its qualification. */
        comment notes /* The restriction concerns propulsion, not onboard electrical power. */
    }
    requirement def <'C-005'> LiveObservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall provide live monitoring with autonomous operation and retained telemetry across communication outages. */
        comment conditions /* Monitoring-link loss shall not interrupt autonomous mission execution. Retained telemetry shall be transmitted after contact returns. */
        metadata issue : ModelingMetadata::Issue { text = "Challenge-level coverage, update rate and outage-retention criteria remain to be agreed; vehicle design targets do not amend the challenge automatically."; }
    }
    requirement def <'C-006'> EmergencyIntervention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall permit remote emergency abort or manual control when a command link is available. */
        comment conditions /* Use disqualifies the attempt as unassisted. */
        metadata issue : ModelingMetadata::Issue { text = "Challenge-level abort and recovery procedures remain to be agreed."; }
    }
    requirement courseCompletion : CourseCompletion;
    requirement repeatedOperation : RepeatedOperation;
    requirement unassistedAttempt : UnassistedAttempt;
    requirement sailingPropulsion : SailingPropulsion;
    requirement liveObservation : LiveObservation;
    requirement emergencyIntervention : EmergencyIntervention;
    #derivation connection challengeRuleCourseCompletion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule refines the overall Trans-Gorge challenge."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> courseCompletion;
    }
    #derivation connection challengeRuleRepeatedOperation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule refines the overall Trans-Gorge challenge."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> repeatedOperation;
    }
    #derivation connection challengeRuleUnassistedAttempt {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule refines the overall Trans-Gorge challenge."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> unassistedAttempt;
    }
    #derivation connection challengeRuleSailingPropulsion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule refines the overall Trans-Gorge challenge."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> sailingPropulsion;
    }
    #derivation connection challengeRuleLiveObservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule refines the overall Trans-Gorge challenge."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> liveObservation;
    }
    #derivation connection challengeRuleEmergencyIntervention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule refines the overall Trans-Gorge challenge."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> emergencyIntervention;
    }
}
