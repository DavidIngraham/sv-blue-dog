package BlueDogWingActuator {
    private import ScalarValues::*;
    doc /* Output-shaft torque and speed drive electrical consumption. Efficiency
     * and idle/no-load losses are measured or bounded inputs, not free design
     * improvements. A self-locking candidate may be studied with holding motor
     * power zero, but that assumption is distinct from verified holding behavior.
     * The external search must retain power-loss trim and capsize checks. */
    calc def MastTorque {
        in densityKgM3 : Real;
        in apparentWindMS : Real;
        in sailAreaM2 : Real;
        in chordM : Real;
        in momentCoefficientAtMast : Real;
        in bearingFrictionNm : Real;
        return torqueNm : Real;
        0.5*densityKgM3*apparentWindMS*apparentWindMS*sailAreaM2*chordM*RealFunctions::abs(momentCoefficientAtMast)+bearingFrictionNm
    }
    calc def DrivePower {
        doc /* Preconditions: efficiencies in (0,1], nonnegative powers and duty
         * fractions; moving plus holding fraction at most one. The external
         * sizing adapter must reject inputs outside these domains. */
        in shaftTorqueNm : Real;
        in shaftSpeedRadS : Real;
        in motorEfficiency : Real;
        in gearboxEfficiency : Real;
        in motorNoLoadW : Real;
        in controllerW : Real;
        in motorHoldingW : Real;
        in moveFraction : Real;
        in holdingFraction : Real;
        attribute movingW : Real = controllerW+motorNoLoadW+RealFunctions::abs(shaftTorqueNm*shaftSpeedRadS)/(motorEfficiency*gearboxEfficiency);
        attribute holdingW : Real = controllerW+motorHoldingW;
        return powersW : Real [3] ordered nonunique;
        (moveFraction*movingW+holdingFraction*holdingW+(1-moveFraction-holdingFraction)*controllerW,
         NumericalFunctions::max(movingW,holdingW),movingW)
    }
    calc def DailyEnergy {
        in averagePowerW : Real;
        in durationHours : Real;
        return energyWh : Real;
        averagePowerW*durationHours
    }
    analysis accountingExample {
        doc /* Arithmetic check, not component specifications or mission evidence.
         * 1 Nm at 0.2 rad/s; 80% motor, 40% gearbox; 1 W no-load,
         * 0.1 W controller; 2% moving, 98% holding. */
        out attribute locked : Real [3] ordered nonunique = DrivePower(1,0.2,0.8,0.4,1,0.1,0,0.02,0.98);
        out attribute poweredHold : Real [3] ordered nonunique = DrivePower(1,0.2,0.8,0.4,1,0.1,2,0.02,0.98);
        out attribute lockedWhPerDay : Real = DailyEnergy(locked#(1),24);
        out attribute poweredHoldWhPerDay : Real = DailyEnergy(poweredHold#(1),24);
    }
    dependency sustainedEnergy from DrivePower to BlueDogRequirements::sustainedEnergyFeasibility;
    dependency lockedTrimRecovery from DrivePower to BlueDogRequirements::capsizeControlRecovery;
    dependency loadSizing from MastTorque to BlueDogStructure::structuralIntegrity;
}
