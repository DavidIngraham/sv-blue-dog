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
| avoidTraffic | Avoid collision. | trafficSafety |

## Architecture satisfaction allocations

| name | Design element |
| --- | --- |
| roundTrip | missionManager |
| multiDayEndurance | energy |
| energyAwareness | powerManagement |
| navigationAndControl | control |
| resetRecovery | recoveryController |
| lowEnergyRecovery | powerManagement |
| communications | communications |
| ingressResponse | ingressMonitor |
| missionEvidence | recording |
| transportability | handling |
| desktopManufacture | printedHull |
| serviceability | enclosure |
| trafficSafety | collisionAvoidance, traffic |
| operatingBoundary | boundarySupervisor |
| safeRecovery | recoveryController |
| navigationConspicuity | signaling |
| regulatoryClassification |  |
| environmentalEnvelope | missionManager |
| marineDurability | enclosure |
| stabilityAndFouling | keelAndBallast |
| recoveryPropulsion | motorSystem |
| recoveryEnergy | powerManagement |
| telemetryEquipment | telemetryRadio, monitoringStation |
| commandIntegrity | commandGateway |
