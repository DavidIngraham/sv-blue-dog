# One-time authoring record. Not idempotent; do not rerun against the changed model.
"""Attach open value-specific closure plans to native-discovered allocations."""
from pathlib import Path
exec(Path(__file__).with_name('apply_model.py').read_text().split("REQ = 'models/vehicle/requirements.sysml'")[0])
BASIS='models/vehicle/requirement-basis.sysml'
audit=json.loads((HERE.parent/'requirements-audit-2026-10-22/evidence/native-review.json').read_text())
basis={r['element']['id']:r['cells'][1][0]['id'].rsplit('::',1)[-1] for r in audit['tables']['Basis']['rows']}
export=json.loads((ROOT/'.tools/basis-export.json').read_text())
requirements=list(csv.DictReader((HERE.parent/'requirements-audit-2026-10-22/requirement-review.csv').open()))
byid={r['element'].replace('::','__'):r for r in requirements}
notation=''
records=[]
for meta in export:
    if basis.get(meta['qualifiedName']) != 'performanceAllocation': continue
    r=byid[meta['annotatedElement'][0]['@id']]
    rid=r['id'];name=r['element'].rsplit('::',1)[-1]
    if rid.startswith('P-'):
        action='Measure timed handling tasks, carried loads and setup interfaces with one adult and permitted aids; compare the selected limit with repeatability, fatigue and launch/retrieval conditions.'
    elif name.startswith('Wind'):
        action='Correlate the installed wind observation with a traceable reference across the declared flow/heel/trim matrix; reconcile local apparent-wind errors and the 10 m true-wind admission estimate before accepting the limit.'
    elif rid.startswith('N-'):
        action='Establish representative site/casualty exposure and configuration-specific functional recovery; compare the selected boundary or response limit with measured failure margins and interacting exposures.'
    elif rid.startswith('S-'):
        action='Use installed observations and achieved maneuvers in representative and adverse encounters or emergency-control faults; compare the selected latency with complete response and safety margins.'
    elif rid.startswith('C-'):
        action='Measure end-to-end telemetry or command handling under delays, reconnects and invalid/replayed input; compare the selected timing with operator interpretation and persistent qualification behavior.'
    elif any(w in name for w in ['Log','Timestamp','Recording']):
        action='Interrupt power, reset and communications at the recording boundaries; measure lost history, timestamp uncertainty and replay behavior against the selected bound.'
    elif any(w in name for w in ['Energy','Reserve','Conservative']):
        action='Correlate installed energy estimates and reserve timing with calibrated withdrawal and temperature/aging evidence; compare the selected bound with route-dependent recovery margin.'
    else:
        action='Measure installed command/observation refresh and fault-transition latency at the declared interface; compare the selected bound with achieved control response and interacting-fault safety margins.'
    values={
      'source': f"Retained baseline {rid}; {meta['qualifiedName']} records its provisional allocation. No accepted originating value-selection trade is recorded.",
      'applicability': f"{rid} retains its own normative conditions and mission applicability: {r['applicability']}.",
      'valueJustification': f"Open: justify the actual limit in {rid} {name}; mission motivation alone does not select that value.",
      'marginBasis': f"Open: record measurement uncertainty, variability and margin for {rid}; no extra numerical margin is allocated by this decision record.",
      'evidenceNeeded': r['verification_links']+'; accepted configuration-specific measurements and the value-selection argument remain required.',
      'owner': 'Project owner; supporting assessment responsibility follows the named verification case.',
      'closureAction': f"Before release of {rid}: "+action+' Record the retained or revised value, alternatives, evidence references, assumptions and acceptance disposition.',
    }
    notation+=f'metadata decision{name} : AllocationDecision about {r["element"]} {{\n'
    notation+=''.join(f'        {k} = {json.dumps(v)};\n' for k,v in values.items())
    notation+='        accepted = false;\n    }\n    '
    records.append(dict(requirement=rid,element=r['element'],**values,accepted=False))
assert len(records)==77,len(records)
for name,selection in [('AirTemperatureVerification','two hours at each stabilized air-temperature endpoint'),('WaterTemperatureVerification','two hours at each stabilized water-temperature endpoint'),('HumidityVerification','three powered 24-hour condensation cycles')]:
    notation+=f'''metadata procedure{name} : AllocationDecision about BlueDogRequirementVerification::{name} {{
        source = "Planned procedure uses {selection}; this is a test-design choice, not another product requirement.";
        applicability = "Installed configuration and the associated environmental qualification conditions.";
        valueJustification = "Open: justify exposure duration and cycle count using thermal time constants, moisture transport, failure mechanisms and course/campaign representativeness.";
        marginBasis = "Open: record instrumentation uncertainty and duration/coverage margin.";
        evidenceNeeded = "Correlated temperature/moisture histories, stabilization evidence and review of cumulative and combined exposures.";
        owner = "Project owner, environmental assessment";
        closureAction = "Before accepting this procedure, establish representative exposure and coverage or revise the procedure; retain the associated product limits and inconclusive verdict until evidence is accepted.";
        accepted = false;
    }}
    '''
append(BASIS,'BlueDogRequirementBasis',notation,'Record 77 value-specific allocation closure plans and three environmental procedure justifications')
(HERE/'allocation-closure-plans.json').write_text(json.dumps(records,indent=2)+'\n')

text='''package BlueDogRequirementDecisions {
    private import ScalarValues::*;
    part def OpenDecision {
        attribute question : String;
        attribute evidenceNeeded : String;
        attribute owner : String = "Project owner";
        attribute accepted : Boolean = false;
    }
'''
decisions=[
('trafficAcceptance','Accept class-specific observation, response, clearance and reliability/confidence criteria and the deployment applicability matrix.','Installed class-specific observations and achieved responses; configuration-specific rule review and recorded authority.',['BlueDogRequirements::trafficSafety','BlueDogRequirements::regulatoryClassification','GorgeChallenge::navigationRuleApplicability']),
('recoveryAcceptance','Establish independent course-wide recovery and physical retrieval.','Surveyed accessible shores, final capture/retention, casualty propulsion, onboard observations/control and protected power under no-contact faults.',['BlueDogRequirements::recoveryPropulsion','BlueDogRequirements::recoveryEnergy','GorgeChallenge::capsizeRecovery']),
('structuralQualification','Accept actual structural loads and installed functional limits.','Wet and aged production materials/joints, impact/fatigue/buckling and combined environmental load evidence.',['BlueDogStructure::structuralIntegrity']),
('installedControlEvidence','Connect supplied observations and commands to installed sensing and achieved motion.','Correlated apparent and 10 m true wind, navigation/traffic observations, maneuver response and interacting faults.',['BlueDogRequirements::windObservation','BlueDogRequirements::navigationAndControl']),
('integrationCoverage','Establish an integrated acceptance argument beyond sampled predicates and supplied Booleans.','Compatible configuration-specific whole-route, safety, energy, structural and casualty evidence with justified coverage and exclusions.',['BlueDogRequirements::missionReliability','BlueDogRequirements::cruisePerformance']),
('futureMissionAcceptance','Select independently scoped future voyage targets and acceptance.','Hawaii route, weather, ocean exposure, sustained energy, communications, maintenance and recovery decisions.',['BlueDogMissionScope::future']),
]
for i,(name,question,evidence,targets) in enumerate(decisions,1):
    text+=f'''    part <'U0{i}'> {name} : OpenDecision {{
        attribute :>> question = {json.dumps(question)};
        attribute :>> evidenceNeeded = {json.dumps(evidence)};
    }}
'''
    for j,target in enumerate(targets):text+=f'    dependency {name}Basis{j+1} from {name} to {target};\n'
text+='}\n'
p=ROOT/'models/vehicle/requirement-decisions.sysml'
assert not p.exists()
sources=tuple((str(f),f.read_text()) for f in model_files())+((str(p),text),)
connection().parse_sources(sources,strict=True)
p.write_text(text)
print('Record six unresolved engineering decisions without accepting missing evidence',flush=True)
