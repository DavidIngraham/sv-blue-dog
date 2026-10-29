import importlib,json
from tools.boat_analysis.model.runtime import ROOT
definitions={'audit':'native_audit','architecture_audit':'native_architecture_audit','configuration_audit':'native_configuration_audit','credibility_audit':'native_credibility_audit','decision_audit':'native_decision_audit','safety_audit':'native_safety_audit','verification_audit':'native_verification_audit'}
results={}
for module,function in definitions.items():
    result=getattr(importlib.import_module('tools.boat_analysis.model.'+module),function)()
    assert not result.get('errors') and not result.get('diagnostics'),(module,result.get('errors'))
    results[module]=result
    print(module,result.get('summary'),flush=True)
(ROOT/'.tools/shared-after-audits.json').write_text(json.dumps(results,indent=2,default=str)+'\n')
