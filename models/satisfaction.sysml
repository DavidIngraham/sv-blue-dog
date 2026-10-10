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
    satisfy BlueDogRequirements::environmentalEnvelope by missionContext.boat;
    satisfy BlueDogRequirements::marineDurability by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::stabilityAndFouling by missionContext.boat;
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
    satisfy BlueDogRequirements::gorgeEnvironment by missionContext.boat;
    satisfy BlueDogRequirements::oceanEnvironment by missionContext.boat;
    satisfy BlueDogRequirements::gorgeWind by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::gorgeWaves by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::gorgeCurrent by missionContext.boat.control;
    satisfy BlueDogRequirements::gorgeSurvivalWind by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::gorgeSurvivalWaves by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::oceanWind by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::oceanWaves by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::oceanCurrent by missionContext.boat.control;
    satisfy BlueDogRequirements::oceanSurvivalWind by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::oceanSurvivalWaves by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::airTemperature by missionContext.boat;
    satisfy BlueDogRequirements::waterTemperature by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::humidity by missionContext.boat.hullAndRig.enclosure;
    satisfy BlueDogRequirements::visibility by missionContext.boat.navigation.traffic;
    satisfy BlueDogRequirements::calmOperation by missionContext.boat.control;
    satisfy BlueDogRequirements::envelopeTransition by missionContext.boat.control.missionManager;
    satisfy BlueDogRequirements::freshwaterExposure by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::saltwaterExposure by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::enclosureSealing by missionContext.boat.hullAndRig.enclosure;
    satisfy BlueDogRequirements::wetMechanicalIntegrity by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::wetElectricalIntegrity by missionContext.boat.communications;
    satisfy BlueDogRequirements::solarHeating by missionContext.boat.energy.powerManagement;
    satisfy BlueDogRequirements::printedMaterialAging by missionContext.boat.hullAndRig.printedHull;
    satisfy BlueDogRequirements::selfRighting by missionContext.boat.hullAndRig.keelAndBallast;
    satisfy BlueDogRequirements::capsizeControlRecovery by missionContext.boat.recovery.recoveryController;
    satisfy BlueDogRequirements::submergedWeedPassage by missionContext.boat.hullAndRig;
    satisfy BlueDogRequirements::weedSnagShedding by missionContext.boat.actuation;
    satisfy BlueDogRequirements::weedBlockageResponse by missionContext.boat.control;
    satisfy BlueDogRequirements::recoveryPropulsorWeeds by missionContext.boat.recovery.motorSystem;
}
