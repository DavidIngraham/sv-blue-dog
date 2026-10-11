"""Export explicit native sensitivity scenarios, with their evidence limitation."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import json
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.runtime import MODELS,native
from tools.boat_analysis.model.runtime import native_value
from tools.boat_analysis.evidence.records import digest

def prepare():
    extra=[ROOT/'models'/n for n in ['vehicle/structure.sysml','analyses/sizing/inputs.sysml','analyses/sizing/uncertainty.sysml']]
    audit=json.loads(native('-analysis','BlueDogCoupledUncertainty::Inputs','-json',models=MODELS+tuple(extra)))
    if audit['status']!='holds':raise ValueError('Sensitivity export failed')
    r={'sourceHashes':{p.relative_to(ROOT).as_posix():digest(p) for p in extra},'values':{v['name']:native_value(v['value']) for v in audit['checks'][0]['values']},'evidence':'Provisional engineering sensitivities; not measured uncertainty distributions.'}
    output_path('coupled-uncertainty-inputs.json').write_text(json.dumps(r,indent=2)+'\n')

if __name__=='__main__':prepare()
