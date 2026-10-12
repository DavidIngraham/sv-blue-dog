package GorgeChallenge {
    doc /* Independent trans-gorge autonomous sailing challenge.
     * Inspired by the structure of the Microtransat rules:
     * https://microtransat.org/content.php?p=rules&top=rules
     * This is a separate project challenge, not a Microtransat entry or endorsement.
     * No vessel architecture, hull size, or communications technology is prescribed.
     * The Gorge is the proving ground for a longer-term voyage toward Hawaii.
     * Marker-referenced virtual gates are defined in TransGorgeCourse.
     * There is no completion deadline. The vehicle defines candidate environmental qualification profiles; no dam passage is permitted.
     */
    private import RequirementDerivation::*;
    requirement def <'C-000'> TransGorgeChallenge {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall complete the Trans-Gorge challenge under C-001 and C-003 through C-009. */
        metadata rationale : ModelingMetadata::Rationale { text = "One The Dalles–Bonneville–The Dalles circuit defines the finite challenge. Repeated circuits are a separate future endurance objective."; }
    }
    requirement transGorgeChallenge : TransGorgeChallenge;
    requirement def <'C-001'> CourseCompletion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall cross the configured The Dalles departure, Bonneville turnaround and The Dalles finish gates in order during one attempt. */
        comment conditions /* TransGorgeCourse defines nominal marker references and directed finite gate segments. Completion has no elapsed-time deadline. Position history must demonstrate crossings; touching a gate line alone does not count. */
        metadata issue : ModelingMetadata::Issue { text = "The marker-based gate proposal remains subject to the course safety review before launch; route corridor and current notice exclusions must accompany the accepted configuration."; }
    }
    requirement def <'C-002'> RepeatedOperation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* After its first circuit, the vessel should repeat The Dalles–Bonneville–The Dalles autonomously for as long as practical. */
        comment notes /* Future endurance objective, excluded from finite challenge acceptance. */
        metadata issue : ModelingMetadata::Issue { text = "No fixed objective endurance duration has been selected."; }
    }
    requirement def <'C-003'> UnassistedAttempt {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* A qualifying attempt shall complete the round trip without operator intervention. */
        comment conditions /* Passive live monitoring is permitted. Remote emergency abort or manual control disqualifies the attempt as unassisted. */
        comment restartConditions /* After intervention, a new qualifying attempt begins only with a new downstream crossing of the departure gate. Previous partial progress does not transfer. */
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
    requirement def <'C-007'> NavigationRules {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall comply with applicable navigation rules throughout the attempt. */
        comment conditions /* Evaluate the actual encounter and visibility conditions, including lookout, collision-risk assessment, avoidance action, safe speed, overtaking, sailing encounters and narrow-channel obligations. A safety action takes precedence over preserving attempt qualification. */
        metadata rationale : ModelingMetadata::Rationale { text = "USCG Navigation Rules: https://www.navcen.uscg.gov/navigation-rules-amalgamated . Detailed encounter cases and quantitative acceptance allocations belong to the vehicle analysis, not the independent challenge. Small size and sail propulsion do not exempt the vessel from collision avoidance or channel non-impediment."; }
    }
    requirement def <'C-008'> RestrictedWaters {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall remain outside waters prohibited to the attempt configuration. */
        comment conditions /* Include dam restricted areas, lock approaches excluded by the challenge, and applicable temporary safety/security zones or closures. Use the chart and notice set applicable to the attempt. */
        metadata rationale : ModelingMetadata::Rationale { text = "33 CFR 207.718 defines site-specific dam restrictions and lock-approach authority: https://www.ecfr.gov/current/title-33/chapter-II/part-207/section-207.718 . The course stays between the dams and requires no lock passage. Do not replace mapped restrictions with an invented universal stand-off radius."; }
    }
    requirement def <'C-009'> TrafficCoexistence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        doc /* The vessel shall complete the course without collision with other waterway users. */
        comment conditions /* The operating context includes commercial tows, passenger vessels, fishing craft, recreational powerboats, sailing vessels and people in the water. Channel non-impediment and encounter conduct remain independently required by C-007. The vehicle analysis defines representative and adverse traffic scenarios and assesses maneuver feasibility. */
        metadata rationale : ModelingMetadata::Rationale { text = "The course is shared water, not a closed test range. Typical traffic and uncertainty in other users' behavior are part of mission validation; AIS absence is not evidence of clear water. Numeric separation allocations must be justified by encounter geometry and vessel performance."; }
    }
    requirement navigationRules : NavigationRules;
    requirement restrictedWaters : RestrictedWaters;
    requirement trafficCoexistence : TrafficCoexistence;
    #derivation connection challengeNavigationRules {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "C-000 includes this obligation independently of course progress or elapsed time."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> navigationRules;
    }
    #derivation connection challengeRestrictedWaters {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "C-000 includes this obligation independently of course progress or elapsed time."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> restrictedWaters;
    }
    #derivation connection challengeTrafficCoexistence {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "C-000 includes this obligation independently of course progress or elapsed time."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> trafficCoexistence;
    }
    #derivation connection challengeRuleCourseCompletion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule is explicitly included in C-000; C-002 retains its objective-only status."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> courseCompletion;
    }
    dependency futureEnduranceBasis from repeatedOperation to courseCompletion;
    #derivation connection challengeRuleUnassistedAttempt {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule is explicitly included in C-000; C-002 retains its objective-only status."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> unassistedAttempt;
    }
    #derivation connection challengeRuleSailingPropulsion {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule is explicitly included in C-000; C-002 retains its objective-only status."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> sailingPropulsion;
    }
    #derivation connection challengeRuleLiveObservation {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule is explicitly included in C-000; C-002 retains its objective-only status."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> liveObservation;
    }
    #derivation connection challengeRuleEmergencyIntervention {
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata rationale : ModelingMetadata::Rationale { text = "This rule is explicitly included in C-000; C-002 retains its objective-only status."; }
        end #original source ::> transGorgeChallenge;
        end #derive target ::> emergencyIntervention;
    }
}
