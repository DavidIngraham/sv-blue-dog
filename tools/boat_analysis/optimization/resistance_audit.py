from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes
import json
import numpy as np
from tools.boat_analysis.model.vessel import CoupledModel
from tools.boat_analysis.geometry.hydro import equilibrium
from tools.boat_analysis.geometry.hull import upright_hull_features
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.resistance import evaluate
from tools.boat_analysis.evidence.records import digest
def run():
    model=CoupledModel();rows=[]
    for name,x in [('reference',model.c['referenceDesign']),('coarse_search',[input_record('coupled-sizing-search.json')['design'][n] for n in model.c['designNames']])]:
        bodies,m,_,_=model.configuration(x,0,resolution=16)
        h=equilibrium(model.hydro,bodies,[m['cgX'],m['cgY'],m['cgZ']],m['totalMass'],0,density=1000)
        body=next(b for b in bodies if b.name=='hull')
        f=upright_hull_features(body.tetrahedra,h['waterline_m'])
        native=model.hydro.moments(body.tetrahedra,h['waterline_m'])
        assert np.isclose(native[0],f[3],rtol=1e-9)
        result=evaluate(f,.4*(9.80665*f[0])**.5,require_domain=False)
        rows.append({'case':name,'hullFeatures':f.tolist(),'waterline_m':h['waterline_m'],'nativeCanoeVolume_m3':native[0],'screen':result.to_mapping(),'outsideEnvelope':[k for k,v in list(result.items())[3:] if v < -1e-12]})
    sources=['models/libraries/marine/hull-resistance.sysml','tools/boat_analysis/model/resistance.py','tools/boat_analysis/geometry/hull.py','tools/boat_analysis/optimization/resistance_audit.py','tools/boat_analysis/model/vessel.py','tools/boat_analysis/geometry/vessel.py','tools/boat_analysis/geometry/hydro.py','build/analysis/coupled-sizing-search.json','build/analysis/coupled-mass-reference.json']
    record={'sourceHashes':source_hashes(sources),'scope':'Upright static canoe-body geometry, mast trim zero and pitch fixed zero. Coefficient outputs outside the screening envelope are diagnostics only, not valid resistance predictions. Native clipped volume independently checks mesh feature extraction.','qualified':False,'cases':rows}
    output_path('hull-resistance-domain.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{'case':r['case'],'outsideEnvelope':r['outsideEnvelope']} for r in rows]))

if __name__ == "__main__":
    run()
