package GorgeChallenge {
    doc /* Independent trans-gorge autonomous sailing challenge.
     * Inspired by the structure of the Microtransat rules:
     * https://microtransat.org/content.php?p=rules&top=rules
     * This is a separate project challenge, not a Microtransat entry or endorsement.
     * No vessel architecture, hull size, or communications technology is prescribed.
     * The Gorge is the proving ground for a longer-term voyage toward Hawaii.
     * Exact gates, corridor, time limit, environmental envelope, evidence requirements,
     * and restart/recovery procedure remain open; no dam passage is assumed.
     */
    requirement def <'C-001'> CourseCompletion {
        doc /* CONFIRMED INTENT: Threshold: Complete a journey from The Dalles
         * to Bonneville and back to The Dalles. Exact start/finish and turnaround
         * gates, permitted corridor, and crossing evidence remain to be agreed.
         */
    }
    requirement def <'C-002'> RepeatedOperation {
        doc /* CONFIRMED INTENT: Objective beyond the first completed round trip:
         * repeat The Dalles-Bonneville-The Dalles autonomously for as long as
         * practical. No fixed objective endurance duration has been selected.
         */
    }
    requirement def <'C-003'> UnassistedAttempt {
        doc /* CONFIRMED INTENT: A qualifying attempt shall complete the round trip
         * without operator intervention. Passive live monitoring is permitted.
         * Any use of remote emergency abort or manual control disqualifies the
         * attempt as unassisted. Restart criteria remain to be agreed.
         */
    }
    requirement def <'C-004'> SailingPropulsion {
        doc /* CONFIRMED INTENT: A qualifying challenge attempt shall use sailing
         * propulsion without auxiliary motor propulsion. Auxiliary motor use is
         * allowed during development tests, which do not count as challenge attempts.
         * Motor use during an attempt prevents it from qualifying.
         * An auxiliary motor may remain installed for vessel recovery.
         * Recovery propulsion is permitted outside the qualifying attempt; use
         * during an attempt ends that attempt without qualification.
         * The restriction concerns propulsion, not electrical power for onboard systems.
         */
    }
    requirement def <'C-005'> LiveObservation {
        doc /* CONFIRMED INTENT: Live monitoring shall be available to the operator.
         * Monitoring-link loss shall not interrupt autonomous mission execution.
         * Telemetry shall be retained onboard and transmitted when contact returns.
         * Coverage, update rate, retained data, and outage retention duration are open.
         */
    }
    requirement def <'C-006'> EmergencyIntervention {
        doc /* CONFIRMED INTENT: Provide remote emergency abort or manual control
         * when a command link is available. Use disqualifies the attempt as unassisted.
         * Emergency abort behavior and the subsequent recovery procedure are open.
         */
    }
    requirement courseCompletion : CourseCompletion;
    requirement repeatedOperation : RepeatedOperation;
    requirement unassistedAttempt : UnassistedAttempt;
    requirement sailingPropulsion : SailingPropulsion;
    requirement liveObservation : LiveObservation;
    requirement emergencyIntervention : EmergencyIntervention;
}
