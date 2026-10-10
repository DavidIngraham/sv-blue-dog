"""Export explicit native sensitivity scenarios, with their evidence limitation."""
import json
from .native_design_kernel import ROOT
from .render_requirements import MODELS,native
from .prepare_design_search import native_value
from .study_open_sizing import digest

def prepare():
    extra=[ROOT/'models'/n for n in ['structure.sysml','coupled-sizing.sysml','coupled-uncertainty.sysml']]
    audit=json.loads(native('-analysis','BlueDogCoupledUncertainty::Inputs','-json',models=MODELS+tuple(extra)))
    if audit['status']!='holds':raise ValueError('Sensitivity export failed')
    r={'sourceHashes':{p.relative_to(ROOT).as_posix():digest(p) for p in extra},'values':{v['name']:native_value(v['value']) for v in audit['checks'][0]['values']},'evidence':'Provisional engineering sensitivities; not measured uncertainty distributions.'}
    (ROOT/'docs/analysis/coupled-uncertainty-inputs.json').write_text(json.dumps(r,indent=2)+'\n')

if __name__=='__main__':prepare()
