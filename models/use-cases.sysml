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
        actor traffic : OtherVessel;
        objective 'M-001 Gorge mission' :> roundTrip;
    }
    use case sailOcean {
        doc /* Sail to Hawaii. */
        subject boat : Boat;
        actor operator : Operator;
        actor traffic : OtherVessel;
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
        actor traffic : OtherVessel;
        objective 'S-003 Safe recovery' :> safeRecovery;
    }
    use case maintain {
        doc /* Manufacture and service. */
        subject boat : Boat;
        actor operator : Operator;
        objective 'P-003 Serviceability' :> serviceability;
    }
    use case avoidTraffic {
        doc /* Detect AIS and non-AIS traffic, assess collision risk, maneuver, and monitor separation without depending on operator intervention or cooperation by the other vessel. */
        subject boat : Boat;
        actor operator : Operator;
        actor traffic : OtherVessel;
        objective 'S-001 Traffic safety' :> trafficSafety;
    }
    use case presentNavigationSignals {
        doc /* Present mode-appropriate navigation signals to other vessels during sailing, powered recovery and stationary operation. */
        subject boat : Boat;
        actor traffic : OtherVessel;
        objective 'S-004 Navigation conspicuity' :> navigationConspicuity;
    }
}
package BlueDogUseCaseViews {
    private import StandardViewDefinitions::*;
    view operations : GeneralView {
        expose BlueDogUseCases::*;
        filter @SysML::UseCaseUsage;
    }
}
