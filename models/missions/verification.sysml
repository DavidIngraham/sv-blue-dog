package GorgeChallengeVerification {
    doc /* Planned qualification cases, not completed evidence. Virtual regression checks and physical demonstrations are separate evidence streams. */
    verification def OverallLengthVerification {
        doc /* Inspect and measure the maximum fore-and-aft extent through all normal rig, steering and equipment configurations. Apply the executable lengthLimit constraint with recorded measurement uncertainty; confirm no unmeasured projection extends beyond the reported envelope. */
        objective acceptance { verify GorgeChallenge::overallLength; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def TrafficNonInterferenceVerification {
        doc /* Review applicable navigation obligations, then exercise AIS and non-AIS crossing, overtaking, head-on and constrained-water encounters. Use BlueDogClassDetection reviewed class-specific or conservative plausible-class envelopes, target extents, observation and response timing, clearance, consequence and reliability/confidence criteria. Independently observe closest hull approach and other-vessel impediment. No current class allocation is accepted. Coarse mission truth tracks do not verify sensing or waive collision/nonimpediment obligations.*/
        objective acceptance { verify GorgeChallenge::trafficNonInterference; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def SafetyCapabilityAbortVerification {
        doc /* Inject loss of required safety functions, including visibility-driven loss and common-cause faults. Confirm qualification terminates when the function is unavailable; demonstrate continued qualification only when an accepted backup maintains that function. */
        objective acceptance { verify GorgeChallenge::safetyCapabilityAbort; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def AutonomousShoreRecoveryVerification {
        doc /* From declared course locations and casualty states, remove communications and trigger safety abort. Record recovery initiation, chosen accessible destination, transit and final approach. Assess impaired-sensing collision exposure and consequences independently; a successful transit alone does not accept that residual risk. */
        objective acceptance { verify GorgeChallenge::autonomousShoreRecovery; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def AbortAlertVerification {
        doc /* Trigger abort with available and unavailable links. Observe immediate transmission attempts with a link, durable queueing without a link and delivery after reconnection. Timing implementation tolerance must be declared before qualification. */
        objective acceptance { verify GorgeChallenge::abortAlert; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def NoLitteringVerification {
        doc /* Review and demonstrate the linked flotation, major-component retention and capsize recovery cases using the same casualty configuration. Account for every major component at retrieval. */
        objective acceptance { verify GorgeChallenge::noLittering; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def CasualtyFlotationVerification {
        doc /* Execute the approved flooding and capsize exposure cases with maximum mission load. Observe flotation throughout the course-derived recovery duration. A short static float test cannot substantiate a longer recovery exposure. */
        objective acceptance { verify GorgeChallenge::casualtyFlotation; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def MajorComponentRetentionVerification {
        doc /* Inspect rig, ballast and battery retention before and after the same flooding and capsize cases used for flotation. Record attachments and any released debris. */
        objective acceptance { verify GorgeChallenge::majorComponentRetention; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def CapsizeRecoveryVerification {
        doc /* Release the vessel in the declared capsize orientations with communications disabled and execute shore recovery under the approved current, wind and wave profile. Observe arrival at a retrievable location; remaining inverted is allowed. Motor use must disqualify the attempt. */
        objective acceptance { verify GorgeChallenge::capsizeRecovery; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def UnattachedPassageVerification {
        doc /* Review timestamped passage records and inject grounding, anchoring, shore attachment and refuge entry. Each ends qualification; safe afloat waiting does not. Missing evidence prevents an affirmative qualification verdict. */
        objective acceptance { verify GorgeChallenge::unattachedPassage; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def OutageAutonomyVerification {
        doc /* Interrupt communications during healthy passage and verify continued autonomous operation, retained observations and backlog delivery. Separately inject a safety failure during the outage to ensure loss of contact does not inhibit recovery. */
        objective acceptance { verify GorgeChallenge::communicationOutageAutonomy; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def ForecastAdmissionVerification {
        doc /* Exercise forecast-conditioned launch scenarios covering full passage, waiting and recovery exposure. Reject missing or insufficient forecast coverage. Evaluate the frozen Monte Carlo ensemble and explicit edge cases without treating sample completion fraction as calibrated real-world probability. */
        objective acceptance { verify GorgeChallenge::forecastAdmission; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def WeatherOutageContinuationVerification {
        doc /* Interrupt weather access with applicable and expired forecasts; independently vary onboard safety capability. Confirm continuation requires both applicable forecast information and preserved safety capability. */
        objective acceptance { verify GorgeChallenge::weatherOutageContinuation; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def CourseRecoveryReserveVerification {
        doc /* Evaluate route-dependent reserve along the course using installed load evidence, adverse currents, route feasibility and uncertainty. An inaccessible shore, infeasible route or missing input cannot establish a protected reserve. */
        objective acceptance { verify GorgeChallenge::courseRecoveryReserve; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def ReserveAbortVerification {
        doc /* Inject declining energy and increasing recovery demand along the route. Confirm recovery begins with sufficient reserve for the decision delay, transition and transit rather than only after reserve exhaustion. */
        objective acceptance { verify GorgeChallenge::reserveAbort; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def NightOperationVerification {
        doc /* Exercise the declared navigation, traffic, communications and recovery scenarios in darkness. Confirm nightfall alone does not terminate qualification. Simulation cannot close optical sensing or navigation-light physical evidence. */
        objective acceptance { verify GorgeChallenge::nightOperation; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def AbortPersistenceVerification {
        doc /* After abort, test reboot, contact restoration, refuge departure and operator relocation. Qualification remains ended until the new attempt departure-gate condition is met; partial progress is not carried forward. */
        objective acceptance { verify GorgeChallenge::abortPersistence; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def RecoveryConspicuityVerification {
        doc /* Inspect and test recovery indications against the deployment-specific navigation-signal matrix in the approved visibility conditions, including the casualty states for which recovery is claimed. */
        objective acceptance { verify GorgeChallenge::recoveryConspicuity; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
}
