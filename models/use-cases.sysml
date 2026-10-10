package BlueDogUseCases {
    private import BlueDog::Architecture::*;
    private import BlueDogRequirements::*;
    use case prepare {
        doc /* Prepare and launch. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'P-001 Transportability' :> transportability;
    }
    use case sailGorge {
        doc /* Complete Gorge challenge. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'M-001 Gorge mission' :> roundTrip;
    }
    use case sailOcean {
        doc /* Sail to Hawaii. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'H-001 Hawaii voyage' :> BlueDog::Goals::hawaiiVoyage;
    }
    use case monitor {
        doc /* Monitor live and reconnect. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'C-101 Telemetry' :> telemetryEquipment;
    }
    use case recover {
        doc /* Abort and recover. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'S-003 Safe recovery' :> safeRecovery;
    }
    use case maintain {
        doc /* Manufacture and service. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'P-003 Serviceability' :> serviceability;
    }
    use case avoidTraffic {
        doc /* Avoid collision. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'S-001 Traffic safety' :> trafficSafety;
    }
}
package BlueDogUseCaseViews {
    private import StandardViewDefinitions::*;
    view operations : GeneralView {
        expose BlueDogUseCases::*;
        filter @SysML::UseCaseUsage;
    }
}
