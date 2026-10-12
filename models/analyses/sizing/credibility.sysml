package BlueDogConceptCredibility {
    private import ScalarValues::*;
    part policy {
        attribute minimumUnderwaterAspectRatio : Real = 2;
        attribute rudderStockChordFraction : Real = 0.5;
        attribute rudderLoadChordFraction : Real = 0.25;
        doc /* The geometry rotates about mid-chord. Use the attached-flow
         * symmetric-section quarter-chord force location for the provisional
         * torque arm, rather than an independent 2-percent balance credit.
         * https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/aerodynamic-center/
         * Measured hinge moments and stalled/reversed-flow loads remain open. */
        attribute appendageClearanceM : Real = 0.02;
        doc /* Provisional screening allocations, not universal hydrodynamic limits.
         * AR >= 2 excludes squat foils from the simple finite-wing correction;
         * it does not validate that correction at AR=2. Both keel and rudder
         * need section/finite-span evidence before design acceptance.
         * 20 mm is a provisional rigid-geometry separation, not a deflection
         * or debris allowance. The current architecture has no aft outrigger:
         * rudder stock must be at or forward of the transom. A bracket concept
         * must explicitly add its structure, mass and loads before relaxing this.
         * Theory context: https://ntrs.nasa.gov/citations/19930085047 .
         * That source motivates a domain screen; it does not prescribe AR=2. */
    }
    dependency steeringScope from policy to BlueDogRequirements::navigationAndControl;
    dependency handlingScope from policy to BlueDogRequirements::transportability;
    dependency structureScope from policy to BlueDogStructure::structuralIntegrity;
    comment remainingAcceptanceGaps /* Geometry screening is necessary but insufficient.
     * Candidate voyage energy (including reserve and weather delays), component
     * volume/installation space, real foil polars and stall/ventilation,
     * rudder stock/bearings and joints, fatigue/slamming, dynamic recovery and
     * packaging of 250 mm printed segments remain acceptance work.
     * Do not promote coarseFeasible to a credible or mission-qualified design.
     * Report hull length separately from the complete operating envelope;
     * no user-approved whole-vessel length limit has been allocated yet. */
}
