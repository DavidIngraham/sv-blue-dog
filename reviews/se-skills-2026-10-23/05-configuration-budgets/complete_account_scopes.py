from tools.boat_analysis.model.runtime import ROOT,model_files,connection
p=ROOT/'models/configurations/management.sysml';q=ROOT/'tools/publishing/reference.sysml'
t=p.read_text();qt=q.read_text()
t=t.replace('        attribute massAllocation : MassValue [0..1];','        attribute massAllocation : MassValue [0..1];\n        attribute massEstimate : MassValue [0..1];')
t=t.replace('            massAllocation->ControlFunctions::forAll { in v : MassValue; v >= 0 [kg] } and',
    '            massAllocation->ControlFunctions::forAll { in v : MassValue; v >= 0 [kg] } and\n            massEstimate->ControlFunctions::forAll { in v : MassValue; v >= 0 [kg] } and')
addition='''        part wholeVesselMass : ResourceScope subsets scopes {
            attribute :>> requiredQuantitiesPresent = SequenceFunctions::size(massEstimate) == 1;
            attribute :>> label = "Whole-vessel mass estimate, not supplied in this register";
            attribute :>> quantityKind = "Total vessel mass estimate; distinct from component allowances";
            attribute :>> boundary = "Complete loaded vessel: structure, rig, appendages, batteries, equipment, attachment and support/finish contributions. Fixed equipment is one contribution; do not add it again after a complete native mass rollup.";
            attribute :>> mode = "Same loaded IC-01 geometry, equipment and carried-fluid configuration as the associated performance/handling/recovery study";
            attribute :>> ownerRole = "System integration/mass";
            attribute :>> basis = "A new identified coupled/native MassProperties execution is needed to populate this register. Historical IC-01 or reference-design estimates keep their own recorded source/configuration; none is silently substituted here.";
            attribute :>> closureEvidenceNeeded = "Current coupled/native mass/CG result with exact source/geometry inputs, complete installation reconciliation and weighed-article evidence for physical claims; compare with the applicable handling criterion";
        }
        part mainStorage : ResourceScope subsets scopes {
            attribute :>> requiredQuantitiesPresent = SequenceFunctions::size(nameplateEnergy) == 1 and SequenceFunctions::size(departureEnergy) == 1;
            attribute :>> label = "Main sailing storage account";
            attribute :>> quantityKind = "Nameplate and allocated departure stored energy; successive states";
            attribute :>> boundary = "One main bank; nameplate, usable and departure states are not additive. Sailing withdrawal/losses/self-discharge and its protected reserve belong to the same finite-passage screen. Independent recovery storage is separate; no cross-bank transfer is credited.";
            attribute :>> mode = "Finite-Gorge passage/holds with current sizing usable/departure fractions; no solar credit in the IC-01 integration hypothesis";
            attribute :>> ownerRole = "Power/energy integration";
            attribute :>> basis = "BlueDogIC01.design.battery_Wh and BlueDogOperatingEnvironment.Inputs usable_fraction/initial_fraction; existing allocations, not measured storage capability";
            attribute :>> nameplateEnergy = BlueDogIC01::design.battery_Wh * 3600 [J];
            attribute :>> departureEnergy = nameplateEnergy * BlueDogOperatingEnvironment::Inputs.usable_fraction * BlueDogOperatingEnvironment::Inputs.initial_fraction;
            attribute :>> closureEvidenceNeeded = "Installed bank usable capacity, initial energy and temperature/end-of-service basis; complete withdrawal/reserve history and measured voltage/current/peak capability, coupled passage and casualty assessment";
        }
'''
assert t.count('        part fixedEquipment : ResourceScope subsets scopes {')==1
t=t.replace('        part fixedEquipment : ResourceScope subsets scopes {',addition+'        part fixedEquipment : ResourceScope subsets scopes {')
t=t.replace('    dependency massBasis from ic01::fixedEquipment',
    '    dependency wholeMassBasis from ic01::wholeVesselMass to BlueDogCoupledSizing::MassProperties;\n    dependency mainStorageBasis from ic01::mainStorage to BlueDogIC01::design::battery_Wh;\n    dependency massBasis from ic01::fixedEquipment')
old='Column(name = "Command latency", path = "commandLatency"), Column(name = "Maneuver duration", path = "maneuverDuration")))'
new='Column(name = "Command latency", path = "commandLatency"), Column(name = "Maneuver duration", path = "maneuverDuration"),\n            Column(name = "Whole-vessel mass estimate", path = "massEstimate")))'
assert qt.count(old)==1
qt=qt.replace(old,new)
s=tuple((str(f),t if f==p else f.read_text()) for f in model_files())
m=connection().parse_sources((*s,(str(q),qt)),strict=True)
print(m.run_analysis('BlueDogConfigurationManagement::AccountingReview',subject='BlueDogConfigurationManagement::ic01').outputs)
for n in ('nameplateEnergy','departureEnergy'):
    print(n,m.eval('BlueDogConfigurationManagement::ic01.mainStorage.'+n+' / (3600 [J])',context_symbol_id='BlueDogConfigurationManagement'))
p.write_text(t.rstrip()+'\n');q.write_text(qt.rstrip()+'\n')
