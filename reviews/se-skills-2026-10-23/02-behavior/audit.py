import json,hashlib
from pathlib import Path
from tools.boat_analysis.model.architecture_audit import native_architecture_audit
from tools.boat_analysis.model.runtime import load_model,ROOT
m=load_model()
r=native_architecture_audit()
r['behaviorGraphs']={name:json.loads(m.export_graphs(name).content) for name in (
    'BlueDogMethod::Scenarios::AbortAndRecover','BlueDogMethod::Scenarios::NormalSailing',
    'BlueDogMethod::Scenarios::TrafficEncounter','BlueDogMethod::Scenarios::NavigationUpdate',
    'BlueDogBehaviorContracts::SailingActuationGate','BlueDogBehaviorContracts::RecoveryActuationGate',
    'BlueDogBehaviorContracts::RestoreQualification','BlueDogBehaviorContracts::AssessObservationUsability')}
r['driverHashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in (
    ROOT/'tools/boat_analysis/mission/logic.py',ROOT/'tests/test_behavior_contracts.py')}
Path('reviews/se-skills-2026-10-23/02-behavior/after.json').write_text(json.dumps(r,default=str,indent=2)+'\n')
assert not r['diagnostics'] and not r['errors'],(r['diagnostics'],r['errors'])
print(json.dumps(dict(summary=r['summary'],graphs=len(r['behaviorGraphs']),diagnostics=r['diagnostics'],errors=r['errors']),indent=2))
