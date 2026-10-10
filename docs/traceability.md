# Use-case and architecture traceability

Use-case objectives subset the referenced requirements. Satisfy relationships express intended design allocations, not verified compliance; criteria and evidence remain open.

## Use-case objectives

| name | documentation | Requirement |
| --- | --- | --- |
| prepare | Prepare and launch. | transportability |
| sailGorge | Complete Gorge challenge. | roundTrip |
| sailOcean | Sail to Hawaii. | hawaiiVoyage |
| monitor | Monitor live and reconnect. | telemetryEquipment |
| recover | Abort and recover. | safeRecovery |
| maintain | Manufacture and service. | serviceability |
| avoidTraffic | Detect AIS and non-AIS traffic, assess collision risk, maneuver, and monitor separation without depending on operator intervention or cooperation by the other vessel. | trafficSafety |
| presentNavigationSignals | Present mode-appropriate navigation signals to other vessels during sailing, powered recovery and stationary operation. | navigationConspicuity |

## Architecture satisfaction allocations

| name | Design element |
| --- | --- |
| roundTrip | boat |
| multiDayEndurance | boat |
| energyAwareness | powerManagement |
| navigationAndControl | boat |
| resetRecovery | boat |
| lowEnergyRecovery | boat |
| communications | boat |
| ingressResponse | boat |
| missionEvidence | boat |
| transportability | handling |
| desktopManufacture | printedHull |
| serviceability | enclosure |
| trafficSafety | boat |
| operatingBoundary | boundarySupervisor |
| safeRecovery | boat |
| navigationConspicuity | signaling |
| regulatoryClassification |  |
| environmentalEnvelope | boat |
| marineDurability | boat |
| stabilityAndFouling | boat |
| recoveryPropulsion | boat |
| recoveryEnergy | boat |
| telemetryEquipment | monitoringStation |
| commandIntegrity | commandGateway |
| gorgeEnvironment | boat |
| oceanEnvironment | boat |
| gorgeWind | boat |
| gorgeWaves | boat |
| gorgeCurrent | boat |
| gorgeSurvivalWind | boat |
| gorgeSurvivalWaves | boat |
| oceanWind | boat |
| oceanWaves | boat |
| oceanCurrent | boat |
| oceanSurvivalWind | boat |
| oceanSurvivalWaves | boat |
| airTemperature | boat |
| waterTemperature | boat |
| humidity | boat |
| visibility | boat |
| calmOperation | boat |
| envelopeTransition | boat |
| freshwaterExposure | boat |
| saltwaterExposure | boat |
| enclosureSealing | enclosure |
| wetMechanicalIntegrity | hullAndRig |
| wetElectricalIntegrity | communications |
| solarHeating | powerManagement |
| printedMaterialAging | printedHull |
| selfRighting | boat |
| capsizeControlRecovery | boat |
| submergedWeedPassage | boat |
| weedSnagShedding | boat |
| weedBlockageResponse | boat |
| recoveryPropulsorWeeds | boat |
| navigationAvailability | navigation |
| launchEnergyAdmission | powerManagement |
| challengeMotorInhibition | recoveryController |
