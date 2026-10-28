import importlib,json
from tools.boat_analysis.model.runtime import ROOT
definitions={'audit':'native_audit','architecture_audit':'native_architecture_audit',
 'configuration_audit':'native_configuration_audit','credibility_audit':'native_credibility_audit',
 'decision_audit':'native_decision_audit','safety_audit':'native_safety_audit','verification_audit':'native_verification_audit'}
before=json.loads((ROOT/'reviews/namespace-restructure/baseline-audits.json').read_text())
results={}; summary=[]
for module,function in definitions.items():
    result=getattr(importlib.import_module('tools.boat_analysis.model.'+module),function)()
    results[module]=result
    row=dict(audit=module,before=before[module].get('summary'),after=result.get('summary'),errors=result.get('errors',[]))
    summary.append(row)
    print(json.dumps(row,default=str),flush=True)
    (ROOT/'.tools/namespace-after-audits.json').write_text(json.dumps(results,indent=2,default=str)+'\n')
    assert not row['errors'],row
    assert row['before']==row['after'],row
(ROOT/'.tools/namespace-audit-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
