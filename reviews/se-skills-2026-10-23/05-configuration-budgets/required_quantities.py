from tools.boat_analysis.model.runtime import ROOT,model_files,connection
p=ROOT/'models/configurations/management.sysml'
t=p.read_text()
t=t.replace('        attribute ready : Boolean = contextIdentified and quantitiesValid and coverageReviewed',
    '        attribute requiredQuantitiesPresent : Boolean default = false;\n        attribute ready : Boolean = contextIdentified and requiredQuantitiesPresent and quantitiesValid and coverageReviewed')
markers={
'fixedEquipment':'SequenceFunctions::size(massAllocation) == 1',
'sailingElectronics':'SequenceFunctions::size(averagePowerAllocation) == 1 and SequenceFunctions::size(peakPowerBound) == 1',
'recoveryEssentials':'SequenceFunctions::size(averagePowerAllocation) == 1 and SequenceFunctions::size(peakPowerBound) == 1',
'recoveryStorage':'SequenceFunctions::size(nameplateEnergy) == 1 and SequenceFunctions::size(departureEnergy) == 1',
'responseTiming':'SequenceFunctions::size(acquisitionLatency) == 1 and SequenceFunctions::size(assessmentLatency) == 1 and SequenceFunctions::size(commandLatency) == 1 and SequenceFunctions::size(maneuverDuration) == 1'}
for name,value in markers.items():
    old='        part '+name+' : ResourceScope subsets scopes {\n'
    assert t.count(old)==1
    t=t.replace(old,old+'            attribute :>> requiredQuantitiesPresent = '+value+';\n')
m=connection().parse_sources(tuple((str(f),t if f==p else f.read_text()) for f in model_files()),strict=True)
print(m.run_analysis('BlueDogConfigurationManagement::AccountingReview',subject='BlueDogConfigurationManagement::ic01').outputs)
p.write_text(t)
