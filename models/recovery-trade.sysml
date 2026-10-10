package RecoveryPropulsionTrade {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    doc /* Preliminary axial actuator-disk analysis. Example inputs are illustrative,
     * not measured Blue Dog hardware. Negative axial inflow, crosswind, ventilation,
     * cavitation, weed drag and propeller/hull interactions are outside this model.
     */

    part def Candidate :> BlueDog::Architecture::RecoveryPropulsion {
        attribute diskDiameter : LengthValue;
        attribute density : MassDensityValue;
        attribute axialInflow : SpeedValue;
        attribute requiredThrust : ForceValue;
        attribute overallEfficiency : Real;
        attribute essentialPower : PowerValue;
        attribute availableReserve : EnergyValue;
        attribute weedEvidenceAccepted : Boolean;
        attribute capsizeEvidenceAccepted : Boolean;
        attribute isolationEvidenceAccepted : Boolean;
        attribute thrustEvidenceAccepted : Boolean;
    }

    analysis def RecoverySizing {
        subject candidate : Candidate;
        objective sizingObjective {
            doc /* Assess whether the estimated R-002 recovery reserve fits the supplied battery reserve. This energy-only objective does not establish physical qualification or select an architecture. */
            require constraint { energyFits }
        }
        attribute thrustN : Real = candidate.requiredThrust / (1 [N]);
        attribute diameterM : Real = candidate.diskDiameter / (1 [m]);
        attribute rho : Real = candidate.density / (1 [kg/m^3]);
        attribute speed : Real = candidate.axialInflow / (1 [m/s]);
        attribute diskAreaM2 : Real = 3.141592653589793 * diameterM * diameterM / 4;
        attribute inducedSpeed : Real = (-speed + RealFunctions::sqrt(speed * speed + 2 * thrustN / (rho * diskAreaM2))) / 2;
        assert constraint validInputs {
            candidate.diskDiameter > 0 [m] and candidate.density > 0 [kg/m^3] and
            candidate.axialInflow >= 0 [m/s] and candidate.requiredThrust >= 0 [N] and
            candidate.overallEfficiency > 0 and candidate.overallEfficiency <= 1 and
            candidate.essentialPower > 0 [W] and candidate.availableReserve >= 0 [J]
        }
        out attribute idealPower : PowerValue = thrustN * (speed + inducedSpeed) * 1 [W];
        out attribute electricalPower : PowerValue = idealPower / candidate.overallEfficiency;
        return requiredReserve : EnergyValue = BlueDogRequirements::RecoveryReserveDemand(electricalPower, candidate.essentialPower);
        out attribute reserveMargin : EnergyValue = candidate.availableReserve - requiredReserve;
        out attribute energyFits : Boolean = reserveMargin >= 0 [J];
        out attribute qualificationEvidenceComplete : Boolean = candidate.weedEvidenceAccepted and candidate.capsizeEvidenceAccepted and candidate.isolationEvidenceAccepted and candidate.thrustEvidenceAccepted;
        out attribute modeledGatesMet : Boolean = energyFits and qualificationEvidenceComplete;
    }

    part waterExample : Candidate {
        doc /* Synthetic upstream example: 0.5 m/s ground speed against 1.5 m/s current. 5 N thrust is an assumed combined resistance, not a tow-test result. */
        attribute :>> diskDiameter default = 0.25 [m];
        attribute :>> density default = 1000 [kg/m^3];
        attribute :>> axialInflow default = 2 [m/s];
        attribute :>> requiredThrust default = 5 [N];
        attribute :>> overallEfficiency default = 0.5;
        attribute :>> essentialPower default = 10 [W];
        attribute :>> availableReserve default = 360000 [J];
        attribute :>> weedEvidenceAccepted default = false;
        attribute :>> capsizeEvidenceAccepted default = false;
        attribute :>> isolationEvidenceAccepted default = false;
        attribute :>> thrustEvidenceAccepted default = false;
    }
    part airExample : Candidate {
        doc /* Same assumed thrust and ground speed, with 5 m/s headwind: axial air inflow 5.5 m/s. Candidate drag and efficiency need independent measurements. */
        attribute :>> diskDiameter default = 0.25 [m];
        attribute :>> density default = 1.225 [kg/m^3];
        attribute :>> axialInflow default = 5.5 [m/s];
        attribute :>> requiredThrust default = 5 [N];
        attribute :>> overallEfficiency default = 0.5;
        attribute :>> essentialPower default = 10 [W];
        attribute :>> availableReserve default = 360000 [J];
        attribute :>> weedEvidenceAccepted default = false;
        attribute :>> capsizeEvidenceAccepted default = false;
        attribute :>> isolationEvidenceAccepted default = false;
        attribute :>> thrustEvidenceAccepted default = false;
    }
    dependency reserveCriterion from RecoverySizing to BlueDogRequirements::recoveryEnergy;
    dependency recoveryScenario from RecoverySizing to BlueDogRequirements::recoveryPropulsion;
    dependency weedGate from RecoverySizing to BlueDogRequirements::recoveryPropulsorWeeds;
    dependency capsizeGate from RecoverySizing to BlueDogRequirements::selfRighting;
    dependency controlRecoveryGate from RecoverySizing to BlueDogRequirements::capsizeControlRecovery;
    dependency isolationGate from RecoverySizing to BlueDogRequirements::motorIsolationDeadline;
    dependency isolationLatchGate from RecoverySizing to BlueDogRequirements::isolationRestartInhibition;
}
