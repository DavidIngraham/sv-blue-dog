import json
import numpy as np
from scripts.coupled_model import CoupledModel
from scripts.hydro_geometry import equilibrium
from scripts.hull_features import upright_hull_features
from scripts.native_design_kernel import ROOT
from scripts.native_hull_resistance import HullResistanceKernel
from scripts.study_open_sizing import digest
model=CoupledModel();kernel=HullResistanceKernel();rows=[]
for name,x in [('reference',model.c['referenceDesign']),('coarse_search',list(json.loads((ROOT/'docs/analysis/coupled-sizing-search.json').read_text())['design'].values()))]:
    bodies,m,_,_=model.configuration(x,0,resolution=16)
    h=equilibrium(model.hydro,bodies,[m['cgX'],m['cgY'],m['cgZ']],m['totalMass'],0,density=1000)
    body=next(b for b in bodies if b.name=='hull')
    f=upright_hull_features(body.tetrahedra,h['waterline_m'])
    native=model.hydro.moments(body.tetrahedra,h['waterline_m'])
    assert np.isclose(native[0],f[3],rtol=1e-9)
    result=kernel.evaluate(f,.4*(9.80665*f[0])**.5,require_domain=False)
    rows.append({'case':name,'hullFeatures':f.tolist(),'waterline_m':h['waterline_m'],'nativeCanoeVolume_m3':native[0],'screen':result,'outsideEnvelope':[k for k,v in list(result.items())[3:] if v < -1e-12]})
sources=['models/hull-resistance.sysml','scripts/native_hull_resistance.py','scripts/hull_features.py','scripts/audit_hull_resistance.py','scripts/coupled_model.py','scripts/coupled_geometry.py','scripts/hydro_geometry.py','docs/analysis/coupled-sizing-search.json','docs/analysis/coupled-mass-reference.json']
record={'sourceHashes':{name:digest(ROOT/name) for name in sources},'scope':'Upright static canoe-body geometry, mast trim zero and pitch fixed zero. Coefficient outputs outside the screening envelope are diagnostics only, not valid resistance predictions. Native clipped volume independently checks mesh feature extraction.','qualified':False,'cases':rows}
(ROOT/'docs/analysis/hull-resistance-domain.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'case':r['case'],'outsideEnvelope':r['outsideEnvelope']} for r in rows]))
