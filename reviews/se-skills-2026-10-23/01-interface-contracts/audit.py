"""Record native interface inventory and source provenance for stage one."""
from dataclasses import asdict
import json
from pathlib import Path
from tools.boat_analysis.model.runtime import load_model
from tools.boat_analysis.model.architecture_audit import native_architecture_audit

m=load_model()
report=native_architecture_audit()
report['interfaceInventory']={}
for scope in ('BlueDogLogicalArchitecture','BlueDogPhysicalArchitecture','BlueDogMethod'):
    rows=m.query(scope=[scope],select=['owner'],where={'@type':'PrimitiveConstraint',
        'operator':'=','property':'@type','value':['ItemDefinition','PortDefinition','FlowUsage']})
    report['interfaceInventory'][scope]=[dict(id=r.id,type=r.type,owner=r.get('owner'),
        attributes=[asdict(a) for a in m.find(r.id).attribute_facts()] if r.type=='ItemDefinition' else []) for r in rows]
report['interfacePredicateChecks']='See focused.xml: synthetic time/context/authority tests; no physical qualification.'
Path('reviews/se-skills-2026-10-23/01-interface-contracts/after.json').write_text(json.dumps(report,default=str,indent=2)+'\n')
print(json.dumps(dict(diagnostics=report['diagnostics'],errors=report['errors'],
    inventory={k:len(v) for k,v in report['interfaceInventory'].items()}),indent=2))
