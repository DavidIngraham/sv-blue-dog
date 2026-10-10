package BlueDogCoupledUncertainty {
    private import ScalarValues::*;
    doc /* Explicit engineering sensitivity brackets, not calibrated probability
     * distributions or qualified tolerances. They expose dependence on missing
     * material/actuator/polar/environment evidence; they do not replace it. */
    analysis Inputs {
        out attribute nominal : Real [38] ordered nonunique = BlueDogCoupledSizing::Inputs.parameterValues;
        out attribute construction : Real [38] ordered nonunique = (1..38)->ControlFunctions::collect { in i : Integer; if i == 1 ? 1.2 else if i == 13 ? 120 else if i == 14 ? 0.7 else if i == 21 ? 0.225 else if i == 23 ? 3 else BlueDogCoupledSizing::Inputs.parameterValues#(i) };
        out attribute aerodynamic : Real [38] ordered nonunique = (1..38)->ControlFunctions::collect { in i : Integer; if i == 15 ? 0.04 else if i == 16 ? 0.9 else if i == 17 ? 0.7 else if i == 18 ? 1.4 else BlueDogCoupledSizing::Inputs.parameterValues#(i) };
        out attribute energy : Real [38] ordered nonunique = (1..38)->ControlFunctions::collect { in i : Integer; if i == 2 ? 0.25 else if i == 3 ? 0.7 else if i == 5 ? 0.15 else if i == 7 ? 0.05 else if i == 8 ? 0.95 else if i == 10 ? 0.1 else if i == 11 ? 5.5 else if i == 12 ? 0.45 else BlueDogCoupledSizing::Inputs.parameterValues#(i) };
        out attribute combined : Real [38] ordered nonunique = (1..38)->ControlFunctions::collect { in i : Integer; if i == 1 ? 1.2 else if i == 13 ? 120 else if i == 14 ? 0.7 else if i == 21 ? 0.225 else if i == 23 ? 3 else if i == 15 ? 0.04 else if i == 16 ? 0.9 else if i == 17 ? 0.7 else if i == 18 ? 1.4 else if i == 2 ? 0.25 else if i == 3 ? 0.7 else if i == 5 ? 0.15 else if i == 7 ? 0.05 else if i == 8 ? 0.95 else if i == 10 ? 0.1 else if i == 11 ? 5.5 else if i == 12 ? 0.45 else BlueDogCoupledSizing::Inputs.parameterValues#(i) };
        out attribute nominalRoute : Real [6] ordered nonunique = (0.95,0.5,1,100000,72,0.5);
        out attribute adverseRoute : Real [6] ordered nonunique = (0.90,0.75,1.25,100000,72,0.5);
    }
    dependency materialEvidence from Inputs to BlueDogStructure::structuralIntegrity;
    dependency energyEvidence from Inputs to BlueDogRequirements::sustainedEnergyFeasibility;
    dependency routeEvidence from Inputs to BlueDogRequirements::cruiseEvidence;
}
