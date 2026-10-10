package BlueDogEnergy {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
    doc /* Battery-bus energy accounting with piecewise-constant bounded loads and
     * harvested power. All calculations execute natively. Interval averaging must
     * resolve outages/load bursts that matter to storage minima; peak demand is
     * checked separately without credit for intermittent harvesting. No controller,
     * weather forecast, electrochemical model or vessel qualification is implied.
     */

    part def ElectricalLoad {
        attribute label : String;
        attribute activePower : PowerValue;
        attribute idlePower : PowerValue;
        attribute activeFraction : Real;
        attribute conversionEfficiency : Real;
        attribute uncertaintyFactor : Real;
        attribute averagePower : PowerValue =
            (idlePower + (activePower - idlePower) * activeFraction) * uncertaintyFactor / conversionEfficiency;
        attribute peakPower : PowerValue = activePower * uncertaintyFactor / conversionEfficiency;
        attribute valid : Boolean = activePower >= idlePower and idlePower >= 0 [W] and
            activeFraction >= 0 and activeFraction <= 1 and
            conversionEfficiency > 0 and conversionEfficiency <= 1 and uncertaintyFactor >= 1;
    }
    part def LoadBudget {
        part loads : ElectricalLoad [1..*] ordered;
        attribute averagePower : PowerValue = NumericalFunctions::sum(loads.averagePower);
        attribute peakPower : PowerValue = NumericalFunctions::sum(loads.peakPower);
        attribute valid : Boolean = SequenceFunctions::size(loads) > 0 and
            loads->ControlFunctions::forAll { in load : ElectricalLoad; load.valid };
    }
    part def Battery {
        attribute nominalEnergy : EnergyValue;
        attribute usableFraction : Real;
        attribute capacity : EnergyValue = nominalEnergy * usableFraction;
        attribute chargeEfficiency : Real;
        attribute dischargeEfficiency : Real;
        attribute maxChargePower : PowerValue;
        attribute selfDischargePower : PowerValue;
        attribute maxDischargePower : PowerValue;
        attribute valid : Boolean = nominalEnergy > 0 [J] and usableFraction > 0 and usableFraction <= 1 and
            chargeEfficiency > 0 and chargeEfficiency <= 1 and
            dischargeEfficiency > 0 and dischargeEfficiency <= 1 and
            maxChargePower >= 0 [W] and maxDischargePower > 0 [W] and selfDischargePower >= 0 [W];
    }
    part def Interval {
        ref part budget : LoadBudget;
        attribute duration : TimeValue;
        attribute harvestEnabled : Boolean;
        attribute rawHarvestPower : PowerValue;
        attribute harvestEfficiency : Real;
        attribute busHarvestPower : PowerValue = if harvestEnabled ? rawHarvestPower * harvestEfficiency else 0 [W];
        attribute netBusPower : PowerValue = busHarvestPower - budget.averagePower;
        attribute valid : Boolean = duration > 0 [s] and rawHarvestPower >= 0 [W] and
            harvestEfficiency > 0 and harvestEfficiency <= 1 and budget.valid;
    }
    part def Scenario {
        part battery : Battery;
        part intervals : Interval [1..*];
        ref part timeline : Interval [1..*] ordered;
        attribute initialEnergy : EnergyValue;
        attribute recoveryMotorPower : PowerValue;
        attribute recoveryEssentialPower : PowerValue;
        attribute reserve : EnergyValue = BlueDogRequirements::RecoveryReserveDemand(recoveryMotorPower, recoveryEssentialPower);
        attribute dayCount : Integer;
        attribute evidenceAccepted : Boolean;
        doc /* evidenceAccepted requires the evidence checklist in sustained-operations.md.
         * No default: numerical feasibility and measurement acceptance are distinct.
         * Inputs refer to the same installed configuration. Recovery powers are
         * battery-energy withdrawal rates (include discharge/conversion losses).
         */
    }
    calc def StorageRate {
        in interval : Interval;
        in battery : Battery;
        return rate : PowerValue;
        if interval.netBusPower >= 0 [W] ?
            NumericalFunctions::min(interval.netBusPower * battery.chargeEfficiency / (1 [W]), battery.maxChargePower / (1 [W])) * 1 [W] - battery.selfDischargePower
        else interval.netBusPower / battery.dischargeEfficiency - battery.selfDischargePower
    }
    calc def EnergyAt {
        in scenario : Scenario;
        in index : Integer;
        return energy : EnergyValue;
        if index == 0 ? scenario.initialEnergy else
            NumericalFunctions::min(scenario.battery.capacity / (1 [J]),
                (EnergyAt(scenario, index - 1) + StorageRate(scenario.timeline#(index), scenario.battery) * scenario.timeline#(index).duration) / (1 [J])) * 1 [J]
    }
    calc def TimeAt {
        in scenario : Scenario;
        in index : Integer;
        return time : TimeValue;
        if index == 0 ? 0 [s] else TimeAt(scenario, index - 1) + scenario.timeline#(index).duration
    }
    calc def HarvestTimeInDay {
        in scenario : Scenario;
        in day : Integer;
        return enabledTime : TimeValue;
        NumericalFunctions::sum((1..SequenceFunctions::size(scenario.timeline))->ControlFunctions::collect {
            in i : Integer;
            if scenario.timeline#(i).harvestEnabled ?
                NumericalFunctions::max(0, NumericalFunctions::min(TimeAt(scenario, i) / (1 [s]), day * 86400) -
                    NumericalFunctions::max(TimeAt(scenario, i - 1) / (1 [s]), (day - 1) * 86400)) * 1 [s]
            else 0 [s]
        })
    }
    analysis def BudgetRollup {
        subject budget : LoadBudget;
        assert constraint validInputs { budget.valid }
        out attribute labels : String [*] ordered nonunique = budget.loads.label;
        out attribute averageContributions : PowerValue [*] ordered nonunique = budget.loads.averagePower;
        out attribute peakContributions : PowerValue [*] ordered nonunique = budget.loads.peakPower;
        out attribute coincidentPeak : PowerValue = budget.peakPower;
        return averageDemand : PowerValue = budget.averagePower;
    }
    analysis def SustainedOperation {
        subject scenario : Scenario;
        attribute count : Integer = SequenceFunctions::size(scenario.timeline);
        out attribute inputsValid : Boolean =
            count > 0 and scenario.dayCount > 0 and scenario.battery.valid and
            scenario.initialEnergy > 0 [J] and scenario.initialEnergy <= scenario.battery.capacity and
            scenario.recoveryMotorPower > 0 [W] and scenario.recoveryEssentialPower > 0 [W] and
            scenario.timeline->ControlFunctions::forAll { in interval : Interval; interval.valid };
        assert constraint validInputs { inputsValid }
        out attribute campaignDuration : TimeValue = TimeAt(scenario, count);
        out attribute usableCapacity : EnergyValue = scenario.battery.capacity;
        out attribute protectedReserve : EnergyValue = scenario.reserve;
        out attribute boundaryTimes : TimeValue [*] ordered nonunique = (0..count)->ControlFunctions::collect { in i : Integer; TimeAt(scenario, i) };
        out attribute energyHistory : EnergyValue [*] ordered nonunique = (0..count)->ControlFunctions::collect { in i : Integer; EnergyAt(scenario, i) };
        out attribute storageRates : PowerValue [*] ordered nonunique = scenario.timeline->ControlFunctions::collect { in interval : Interval; StorageRate(interval, scenario.battery) };
        out attribute reserveMargins : EnergyValue [*] ordered nonunique = energyHistory->ControlFunctions::collect { in e : EnergyValue; e - scenario.reserve };
        out attribute harvestHoursPerDay : Real [*] ordered nonunique = (1..scenario.dayCount)->ControlFunctions::collect { in d : Integer; HarvestTimeInDay(scenario, d) / (3600 [s]) };
        out attribute consumedEnergy : EnergyValue = NumericalFunctions::sum(scenario.timeline->ControlFunctions::collect {
            in interval : Interval; interval.budget.averagePower * interval.duration });
        out attribute harvestedBusEnergy : EnergyValue = NumericalFunctions::sum(scenario.timeline->ControlFunctions::collect {
            in interval : Interval; interval.busHarvestPower * interval.duration });
        out attribute finalStoredEnergy : EnergyValue = EnergyAt(scenario, count);
        out attribute reserveProtected : Boolean = BlueDogRequirements::SustainedReserveProtectionCriterion(energyHistory, scenario.reserve);
        out attribute repeatableBalance : Boolean = BlueDogRequirements::RepeatableCycleBalanceCriterion(scenario.initialEnergy, finalStoredEnergy);
        out attribute peakSupported : Boolean = BlueDogRequirements::PeakSupplyCapabilityCriterion(
            scenario.timeline->ControlFunctions::collect { in interval : Interval; interval.budget.peakPower / scenario.battery.dischargeEfficiency + scenario.battery.selfDischargePower },
            scenario.battery.maxDischargePower);
        out attribute campaignCovered : Boolean = BlueDogRequirements::HarvestCampaignCoverageCriterion(campaignDuration, scenario.dayCount, harvestHoursPerDay);
        return modeledEnergyFeasible : Boolean = inputsValid and reserveProtected and repeatableBalance and peakSupported and campaignCovered;
        out attribute evidenceReady : Boolean = BlueDogRequirements::EnergyEvidenceReadinessCriterion(scenario.evidenceAccepted);
        out attribute energyCaseSupported : Boolean = modeledEnergyFeasible and evidenceReady;
        objective feasibility {
            doc /* Conditional numerical feasibility only; evidenceReady is separately reported. */
            require constraint { modeledEnergyFeasible }
        }
    }
    dependency sustainedReserveProtectionTrace from SustainedOperation to BlueDogRequirements::sustainedReserveProtection;
    dependency repeatableCycleBalanceTrace from SustainedOperation to BlueDogRequirements::repeatableCycleBalance;
    dependency peakSupplyCapabilityTrace from SustainedOperation to BlueDogRequirements::peakSupplyCapability;
    dependency harvestCampaignCoverageTrace from SustainedOperation to BlueDogRequirements::harvestCampaignCoverage;
    dependency energyEvidenceReadinessTrace from SustainedOperation to BlueDogRequirements::energyEvidenceReadiness;

    verification def SustainedEnergyVerification {
        doc /* Energy-case verification only. Synthetic or unaccepted evidence is
         * inconclusive even when the numerical analysis passes. This does not verify
         * navigation, sailing performance, weather availability or indefinite life.
         */
        subject scenario : Scenario;
        analysis calculation : SustainedOperation { subject = scenario; }
        objective energyAcceptance {
            verify BlueDogRequirements::sustainedEnergyFeasibility;
            require constraint { calculation.energyCaseSupported }
        }
        return verdict : VerificationCases::VerdictKind =
            if not calculation.evidenceReady ? VerificationCases::VerdictKind::inconclusive
            else VerificationCases::PassIf(calculation.modeledEnergyFeasible);
    }
}
