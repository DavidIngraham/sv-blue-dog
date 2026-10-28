package SharedAcceptanceTests {
    private import SI::*;
    doc /* Test adapters expose observations as call inputs. Production requirements
     * own every constraint; each evaluation binds a fresh set of observations. */
    requirement def WetCouponStiffness :> BlueDog::Requirements::Structure::WetCouponStiffness {
        subject target;
        in attribute :>> creditedModulusPa;
        in attribute :>> qualifiedModulusPa;
        in attribute :>> evidenceAccepted;
    }
    requirement def WetCouponStrength :> BlueDog::Requirements::Structure::WetCouponStrength {
        subject target;
        in attribute :>> creditedAllowablePa;
        in attribute :>> qualifiedAllowablePa;
        in attribute :>> evidenceAccepted;
    }
    requirement def AppendageDeflection :> BlueDog::Requirements::Structure::AppendageDeflection {
        subject target;
        in attribute :>> fraction;
        in attribute :>> validatedMaximumFraction;
        in attribute :>> limitEvidenceAccepted;
    }
    requirement def HullDeflection :> BlueDog::Requirements::Structure::HullDeflection {
        subject target;
        in attribute :>> fraction;
        in attribute :>> validatedMaximumFraction;
        in attribute :>> limitEvidenceAccepted;
    }
    requirement def PanelDeflection :> BlueDog::Requirements::Structure::PanelDeflection {
        subject target;
        in attribute :>> fraction;
        in attribute :>> validatedMaximumFraction;
        in attribute :>> limitEvidenceAccepted;
    }
    requirement def PrintTileEnvelope :> BlueDog::Requirements::Structure::PrintTileEnvelope {
        subject target;
        in attribute :>> jobXM;
        in attribute :>> jobYM;
        in attribute :>> jobZM;
        in attribute :>> slicerEvidenceAccepted;
    }
    requirement def LaunchClearance :> BlueDog::Requirements::Structure::LaunchClearance {
        subject target;
        in attribute :>> availableDepthM;
        in attribute :>> immersedDepthM;
        in attribute :>> requiredClearanceM;
        in attribute :>> siteEvidenceAccepted;
    }
    requirement def ReserveBuoyancy :> BlueDog::Requirements::Structure::ReserveBuoyancy {
        subject target;
        in attribute :>> availableBuoyancyN;
        in attribute :>> loadedWeightN;
        in attribute :>> caseCoverageAccepted;
    }
    requirement def LoadedFreeboard :> BlueDog::Requirements::Structure::LoadedFreeboard {
        subject target;
        in attribute :>> minimumOpeningClearanceM;
        in attribute :>> caseCoverageAccepted;
    }
    requirement def BendingStrength :> BlueDog::Requirements::Structure::BendingStrength {
        subject target;
        in attribute :>> stressPa;
        in attribute :>> qualifiedAllowablePa;
        in attribute :>> evidenceAccepted;
    }
    requirement def PanelStrength :> BlueDog::Requirements::Structure::PanelStrength {
        subject target;
        in attribute :>> stressPa;
        in attribute :>> qualifiedAllowablePa;
        in attribute :>> evidenceAccepted;
    }
    requirement def PrintedMaterialAging :> BlueDog::Requirements::PrintedMaterialAging {
        subject target;
        in attribute :>> creditedLoadCapacityN;
        in attribute :>> qualifiedAgedCapacityN;
        in attribute :>> exposureEvidenceAccepted;
    }
    requirement def DesktopManufacture :> BlueDog::Requirements::DesktopManufacture {
        subject target;
        in attribute :>> jobX;
        in attribute :>> jobY;
        in attribute :>> jobZ;
    }
    requirement def RestartDeadline :> BlueDog::Requirements::RestartDeadline {
        subject target;
        in attribute :>> measuredRestartTime;
    }
    requirement def RecoveryEnergy :> BlueDog::Requirements::RecoveryEnergy {
        subject target;
        in attribute :>> motorPower;
        in attribute :>> essentialPower;
        in attribute :>> reserveEnergy;
        in attribute :>> poweredDuration;
        in attribute :>> essentialDuration;
        in attribute :>> uncertaintyFactor;
        in attribute :>> routeFeasible;
    }
    requirement def RightingDeadline :> BlueDog::Requirements::RightingDeadline {
        subject target;
        in attribute :>> measuredRightingTime;
    }
    requirement def ControlRecoveryDeadline :> BlueDog::Requirements::ControlRecoveryDeadline {
        subject target;
        in attribute :>> measuredControlRecoveryTime;
    }
    requirement def NavigationValidEpochs :> BlueDog::Requirements::NavigationValidEpochs {
        subject target;
        in attribute :>> validEpochs;
    }
    requirement def LaunchEnergyAdmission :> BlueDog::Requirements::LaunchEnergyAdmission {
        subject target;
        in attribute :>> conservativeStartEnergy;
        in attribute :>> protectedReserve;
        in attribute :>> estimateAge;
        in attribute :>> estimateValid;
        in attribute :>> reserveValid;
        in attribute :>> missionStartEnabled;
    }
    requirement def MotorQualificationInvariant :> BlueDog::Requirements::MotorQualificationInvariant {
        subject target;
        in attribute :>> qualificationStateKnown;
        in attribute :>> qualifying;
        in attribute :>> motorEnabled;
    }
    requirement def SustainedReserveProtection :> BlueDog::Requirements::SustainedReserveProtection {
        subject target;
        in attribute :>> samples;
        in attribute :>> reserve;
    }
    requirement def RepeatableCycleBalance :> BlueDog::Requirements::RepeatableCycleBalance {
        subject target;
        in attribute :>> initialEnergy;
        in attribute :>> finalEnergy;
    }
    requirement def PeakSupplyCapability :> BlueDog::Requirements::PeakSupplyCapability {
        subject target;
        in attribute :>> demands;
        in attribute :>> availablePower;
    }
    requirement def HarvestCampaignCoverage :> BlueDog::Requirements::HarvestCampaignCoverage {
        subject target;
        in attribute :>> duration;
        in attribute :>> dayCount;
        in attribute :>> enabledHours;
    }
    requirement def EnergyEvidenceReadiness :> BlueDog::Requirements::EnergyEvidenceReadiness {
        subject target;
        in attribute :>> accepted;
    }
}
