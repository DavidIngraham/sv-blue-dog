from tools.boat_analysis.model.runtime import ROOT,model_files,connection
p=ROOT/'models/configurations/management.sysml'
t=p.read_text()
t=t.replace('attribute configurationReconciled : Boolean = identityReady and reconciled;',
    '''attribute plannedReferencesApplicable : Boolean = design == BlueDogIC01::design and assembly == BlueDogPhysicalArchitecture::ic01;
        attribute configurationReconciled : Boolean = plannedReferencesApplicable and identityReady and reconciled;''')
t=t.replace('        attribute ready : Boolean = coverageReviewed and measurementsAccepted and accountingReconciled and',
    '''        attribute contextIdentified : Boolean = label != "" and quantityKind != "" and boundary != "" and
            mode != "" and ownerRole != "" and basis != "" and closureEvidenceNeeded != "";
        attribute quantitiesValid : Boolean =
            massAllocation->ControlFunctions::forAll { in v : MassValue; v >= 0 [kg] } and
            averagePowerAllocation->ControlFunctions::forAll { in v : PowerValue; v >= 0 [W] } and
            peakPowerBound->ControlFunctions::forAll { in v : PowerValue; v >= 0 [W] } and
            nameplateEnergy->ControlFunctions::forAll { in v : EnergyValue; v >= 0 [J] } and
            departureEnergy->ControlFunctions::forAll { in v : EnergyValue; v >= 0 [J] } and
            acquisitionLatency->ControlFunctions::forAll { in v : TimeValue; v >= 0 [s] } and
            assessmentLatency->ControlFunctions::forAll { in v : TimeValue; v >= 0 [s] } and
            commandLatency->ControlFunctions::forAll { in v : TimeValue; v >= 0 [s] } and
            maneuverDuration->ControlFunctions::forAll { in v : TimeValue; v >= 0 [s] };
        attribute ready : Boolean = contextIdentified and quantitiesValid and coverageReviewed and measurementsAccepted and accountingReconciled and''')
s=tuple((str(f),t if f==p else f.read_text()) for f in model_files())
m=connection().parse_sources(s,strict=True)
print(m.run_analysis('BlueDogConfigurationManagement::AccountingReview',subject='BlueDogConfigurationManagement::ic01').outputs)
p.write_text(t)
