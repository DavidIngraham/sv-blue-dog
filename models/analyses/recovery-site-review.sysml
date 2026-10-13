package BlueDogRecoverySiteReview {
    private import ScalarValues::*;
    doc /* Desktop shortlist for shore-recovery assessment. Public land access does
     * not establish a navigable approach, suitable casualty landing or permission
     * for unattended operations. No coordinates are admitted to the route planner. */
    part def Candidate {
        attribute site : String;
        attribute source : String;
        attribute evidence : String;
        attribute outstanding : String;
        attribute acceptedForRouting : Boolean = false;
    }
    part bingen : Candidate {
        attribute :>> site = "Bingen boat ramp and harbor";
        attribute :>> source = "https://www.portofklickitat.com/boat-launch-parks";
        attribute :>> evidence = "Port-operated ramp and harbor connect to the Columbia; same facility as the unscored launch/retrieval base.";
        attribute :>> outstanding = "Survey entrance and final capture; assess weeds, depth and current. Port rules prohibit overnight parking, so overnight retrieval logistics need a separate plan.";
    }
    part stevenson : Candidate {
        attribute :>> site = "Stevenson Cascade Avenue boat launch";
        attribute :>> source = "https://www.portofskamania.org/boat-launch-and-docks";
        attribute :>> evidence = "Port identifies a public launch at the east end of Cascade Avenue, near the western end of the course.";
        attribute :>> outstanding = "Assess approach, exposure, ramps versus rock shoreline, competing launch traffic and casualty capture.";
    }
    part springCreek : Candidate {
        attribute :>> site = "Spring Creek Hatchery State Park";
        attribute :>> source = "https://parks.wa.gov/find-parks/state-parks/spring-creek-hatchery-state-park";
        attribute :>> evidence = "State park on the Columbia provides a candidate north-bank access location for field assessment.";
        attribute :>> outstanding = "Confirm access hours, appropriate retrieval frontage, rocks, current, park conditions and wind-sport conflicts; not a sheltered-harbor assumption.";
    }
    part viento : Candidate {
        attribute :>> site = "Viento State Park";
        attribute :>> source = "https://stateparks.oregon.gov/index.cfm?do=park.profile&parkId=123";
        attribute :>> evidence = "Official park map identifies river access, making it a candidate south-bank retrieval location.";
        attribute :>> outstanding = "Assess accessible carry path, rocky landing and exposure. Cross-river traffic and current may make it inferior to a farther same-bank location.";
    }
    metadata rationale : ModelingMetadata::Rationale { text = "Assess more than the two endpoints so recovery distance can vary with position and remaining authority. These source-backed candidates narrow the field survey; none is yet a safe harbor or an approved numerical destination. Source review date: 2026-10-12."; }
    dependency reserveAssessment from bingen to GorgeChallenge::courseRecoveryReserve;
    dependency westernRecovery from stevenson to GorgeChallenge::autonomousShoreRecovery;
    dependency intermediateRecovery from springCreek to GorgeChallenge::autonomousShoreRecovery;
    dependency oppositeBankRecovery from viento to GorgeChallenge::autonomousShoreRecovery;
}
