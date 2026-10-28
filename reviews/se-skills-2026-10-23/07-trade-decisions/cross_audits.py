"""Read-only integrated audits of the final model using existing native facilities."""
import json
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.audit import native_audit
from tools.boat_analysis.model.architecture_audit import native_architecture_audit
from tools.boat_analysis.model.verification_audit import native_verification_audit
from tools.boat_analysis.model.safety_audit import native_safety_audit
from tools.boat_analysis.model.configuration_audit import native_configuration_audit
from tools.boat_analysis.model.credibility_audit import native_credibility_audit
stage=ROOT/'reviews/se-skills-2026-10-23/07-trade-decisions'
for name,fn in [('requirements',native_audit),('architecture',native_architecture_audit),('verification',native_verification_audit),('safety',native_safety_audit),('configuration',native_configuration_audit),('credibility',native_credibility_audit)]:
    r=fn();(stage/(name+'.json')).write_text(json.dumps(r,default=str,indent=2)+'\n')
    assert not r['errors'] and not r.get('diagnostics',[]),name
    print(name,r.get('summary','Native audit passed; detailed review in JSON'),flush=True)
