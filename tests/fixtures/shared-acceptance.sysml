package SharedAcceptanceTests {
    private import SI::*;
    doc /* Test adapters expose observations as call inputs. Production requirements
     * own every constraint; each evaluation binds a fresh set of observations. */
    requirement def WetCouponStiffness :> BlueDogStructure::WetCouponStiffness {
        subject target;
        in attribute :>> creditedModulusPa;
        in attribute :>> qualifiedModulusPa;
        in attribute :>> evidenceAccepted;
    }
    requirement def WetCouponStrength :> BlueDogStructure::WetCouponStrength {
        subject target;
        in attribute :>> creditedAllowablePa;
        in attribute :>> qualifiedAllowablePa;
        in attribute :>> evidenceAccepted;
    }
    requirement def AppendageDeflection :> BlueDogStructure::AppendageDeflection {
        subject target;
        in attribute :>> fraction;
        in attribute :>> validatedMaximumFraction;
        in attribute :>> limitEvidenceAccepted;
    }
    requirement def HullDeflection :> BlueDogStructure::HullDeflection {
        subject target;
        in attribute :>> fraction;
        in attribute :>> validatedMaximumFraction;
        in attribute :>> limitEvidenceAccepted;
    }
    requirement def PanelDeflection :> BlueDogStructure::PanelDeflection {
        subject target;
        in attribute :>> fraction;
        in attribute :>> validatedMaximumFraction;
        in attribute :>> limitEvidenceAccepted;
    }
    requirement def PrintTileEnvelope :> BlueDogStructure::PrintTileEnvelope {
        subject target;
        in attribute :>> jobXM;
        in attribute :>> jobYM;
        in attribute :>> jobZM;
        in attribute :>> slicerEvidenceAccepted;
    }
    requirement def LaunchClearance :> BlueDogStructure::LaunchClearance {
        subject target;
        in attribute :>> availableDepthM;
        in attribute :>> immersedDepthM;
        in attribute :>> requiredClearanceM;
        in attribute :>> siteEvidenceAccepted;
    }
    requirement def ReserveBuoyancy :> BlueDogStructure::ReserveBuoyancy {
        subject target;
        in attribute :>> availableBuoyancyN;
        in attribute :>> loadedWeightN;
        in attribute :>> caseCoverageAccepted;
    }
    requirement def LoadedFreeboard :> BlueDogStructure::LoadedFreeboard {
        subject target;
        in attribute :>> minimumOpeningClearanceM;
        in attribute :>> caseCoverageAccepted;
    }
    requirement def BendingStrength :> BlueDogStructure::BendingStrength {
        subject target;
        in attribute :>> stressPa;
        in attribute :>> qualifiedAllowablePa;
        in attribute :>> evidenceAccepted;
    }
    requirement def PanelStrength :> BlueDogStructure::PanelStrength {
        subject target;
        in attribute :>> stressPa;
        in attribute :>> qualifiedAllowablePa;
        in attribute :>> evidenceAccepted;
    }
    requirement def PrintedMaterialAging :> BlueDogRequirements::PrintedMaterialAging {
        subject target;
        in attribute :>> creditedLoadCapacityN;
        in attribute :>> qualifiedAgedCapacityN;
        in attribute :>> exposureEvidenceAccepted;
    }
    requirement def DesktopManufacture :> BlueDogRequirements::DesktopManufacture {
        subject target;
        in attribute :>> jobX;
        in attribute :>> jobY;
        in attribute :>> jobZ;
    }
    requirement def RestartDeadline :> BlueDogRequirements::RestartDeadline {
        subject target;
        in attribute :>> measuredRestartTime;
    }
    requirement def RecoveryEnergy :> BlueDogRequirements::RecoveryEnergy {
        subject target;
        in attribute :>> motorPower;
        in attribute :>> essentialPower;
        in attribute :>> reserveEnergy;
        in attribute :>> poweredDuration;
        in attribute :>> essentialDuration;
        in attribute :>> uncertaintyFactor;
        in attribute :>> routeFeasible;
    }
    requirement def RightingDeadline :> BlueDogRequirements::RightingDeadline {
        subject target;
        in attribute :>> measuredRightingTime;
    }
    requirement def ControlRecoveryDeadline :> BlueDogRequirements::ControlRecoveryDeadline {
        subject target;
        in attribute :>> measuredControlRecoveryTime;
    }
    requirement def NavigationValidEpochs :> BlueDogRequirements::NavigationValidEpochs {
        subject target;
        in attribute :>> validEpochs;
    }
    requirement def LaunchEnergyAdmission :> BlueDogRequirements::LaunchEnergyAdmission {
        subject target;
        in attribute :>> conservativeStartEnergy;
        in attribute :>> protectedReserve;
        in attribute :>> estimateAge;
        in attribute :>> estimateValid;
        in attribute :>> reserveValid;
        in attribute :>> missionStartEnabled;
    }
    requirement def MotorQualificationInvariant :> BlueDogRequirements::MotorQualificationInvariant {
        subject target;
        in attribute :>> qualificationStateKnown;
        in attribute :>> qualifying;
        in attribute :>> motorEnabled;
    }
    requirement def SustainedReserveProtection :> BlueDogRequirements::SustainedReserveProtection {
        subject target;
        in attribute :>> samples;
        in attribute :>> reserve;
    }
    requirement def RepeatableCycleBalance :> BlueDogRequirements::RepeatableCycleBalance {
        subject target;
        in attribute :>> initialEnergy;
        in attribute :>> finalEnergy;
    }
    requirement def PeakSupplyCapability :> BlueDogRequirements::PeakSupplyCapability {
        subject target;
        in attribute :>> demands;
        in attribute :>> availablePower;
    }
    requirement def HarvestCampaignCoverage :> BlueDogRequirements::HarvestCampaignCoverage {
        subject target;
        in attribute :>> duration;
        in attribute :>> dayCount;
        in attribute :>> enabledHours;
    }
    requirement def EnergyEvidenceReadiness :> BlueDogRequirements::EnergyEvidenceReadiness {
        subject target;
        in attribute :>> accepted;
    }
}
