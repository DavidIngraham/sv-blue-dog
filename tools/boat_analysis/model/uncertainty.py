"""Export explicit native sensitivity scenarios, with their evidence limitation."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import json
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.runtime import MODELS, analysis_values
from tools.boat_analysis.evidence.records import digest

def prepare():
    extra=[ROOT/'models'/n for n in ['blue-dog.sysml','blue-dog.sysml','blue-dog.sysml']]
    values=analysis_values('BlueDog::Analyses::Sizing::Uncertainty::Inputs', models=MODELS+tuple(extra))
    r={'sourceHashes':source_hashes([__file__]),'values':values,'evidence':'Provisional engineering sensitivities; not measured uncertainty distributions.'}
    output_path('coupled-uncertainty-inputs.json').write_text(json.dumps(r,indent=2)+'\n')

if __name__=='__main__':prepare()
