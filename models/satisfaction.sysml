package BlueDogSatisfaction {
    private import BlueDogRequirements::*;
    private import BlueDog::Architecture::missionContext;
    doc /* Design satisfaction allocations, not verification evidence. Physical
     * implementation, quantitative acceptance, and verification remain open.
     * Regulatory classification is a project process obligation, not assigned
     * to a component as though hardware alone could establish authorization.
     */
    satisfy BlueDogRequirements::transportability by missionContext.boat.hullAndRig.handling;
    satisfy BlueDogRequirements::desktopManufacture by missionContext.boat.hullAndRig.printedHull;
    satisfy BlueDogRequirements::serviceability by missionContext.boat.hullAndRig.enclosure;
    satisfy BlueDogRequirements::trafficSafety by missionContext.boat.control.collisionAvoidance;
    satisfy BlueDogRequirements::operatingBoundary by missionContext.boat.control.boundarySupervisor;
    satisfy BlueDogRequirements::safeRecovery by missionContext.boat.recovery.recoveryController;
    satisfy BlueDogRequirements::navigationConspicuity by missionContext.boat.signaling;
    satisfy BlueDogRequirements::environmentalEnvelope by missionContext.boat.control.missionManager;
    satisfy BlueDogRequirements::marineDurability by missionContext.boat.hullAndRig.enclosure;
    satisfy BlueDogRequirements::stabilityAndFouling by missionContext.boat.hullAndRig.keelAndBallast;
    satisfy BlueDogRequirements::recoveryPropulsion by missionContext.boat.recovery.motorSystem;
    satisfy BlueDogRequirements::recoveryEnergy by missionContext.boat.energy.powerManagement;
    satisfy BlueDogRequirements::telemetryEquipment by missionContext.boat.communications.telemetryRadio;
    satisfy BlueDogRequirements::commandIntegrity by missionContext.boat.communications.commandGateway;
    satisfy BlueDogRequirements::roundTrip by missionContext.boat.control.missionManager;
    satisfy BlueDogRequirements::multiDayEndurance by missionContext.boat.energy;
    satisfy BlueDogRequirements::energyAwareness by missionContext.boat.energy.powerManagement;
    satisfy BlueDogRequirements::navigationAndControl by missionContext.boat.control;
    satisfy BlueDogRequirements::resetRecovery by missionContext.boat.recovery.recoveryController;
    satisfy BlueDogRequirements::lowEnergyRecovery by missionContext.boat.energy.powerManagement;
    satisfy BlueDogRequirements::communications by missionContext.boat.communications;
    satisfy BlueDogRequirements::ingressResponse by missionContext.boat.recovery.ingressMonitor;
    satisfy BlueDogRequirements::missionEvidence by missionContext.boat.recording;
    satisfy BlueDogRequirements::trafficSafety by missionContext.boat.navigation.traffic;
    satisfy BlueDogRequirements::telemetryEquipment by missionContext.shoreSupport.monitoringStation;
}
