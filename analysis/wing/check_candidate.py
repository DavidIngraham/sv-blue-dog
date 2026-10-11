"""Direct VSPAERO check of grid interpolation at the current sizing candidate."""
import json,sys
import numpy as np
from polar_grid import run_case
from vsp_runtime import ROOT
sys.path.insert(0,str(ROOT))
from scripts.wing_polar import WingPolar
from scripts.study_open_sizing import digest,validate


def run():
    saved=json.loads((ROOT/'docs/analysis/coupled-sizing-search.json').read_text());validate(saved['sourceHashes'])
    d=saved['design'];polar=WingPolar();cases=[]
    sources=['docs/analysis/coupled-sizing-search.json','docs/analysis/wing-polar-grid.json','analysis/wing/check_candidate.py','analysis/wing/polar_grid.py','analysis/wing/reference_vsp.py','analysis/wing/vsp_runtime.py','scripts/wing_polar.py']
    hashes={n:digest(ROOT/n) for n in sources}
    for reverse in [False,True]:
        r=run_case(d['sail_AR'],d['camber_scale'],reverse=reverse)
        alpha=np.array(r['values']['Alpha'])
        # Compare positive-camber geometries before the sailing sign transform.
        predicted=polar.interpolators[reverse](np.array([[d['sail_AR'],d['camber_scale'],a] for a in alpha]))
        direct=np.array([r['values'][n] for n in ['CLtot','CDi','CMytot']]).T
        r['interpolated']=dict(zip(['CLtot','CDi','CMytot'],predicted.T.tolist()))
        r['maxAbsoluteInterpolationError']=dict(zip(['CLtot','CDi','CMytot'],np.max(np.abs(direct-predicted),axis=0).tolist()))
        cases.append(r)
        print('CANDIDATE',reverse,r['maxAbsoluteInterpolationError'],flush=True)
    validate(hashes)
    report={'sourceHashes':hashes,'design':d,'validated':False,'cases':cases,'scope':'Direct inviscid VSPAERO comparison at candidate aspect ratio and camber, mesh 24. Reference section thickness remains fixed as in the interpolation grid. This checks interpolation, not viscous drag, stall, broadside response, aerodynamic thickness sensitivity or physical sailing performance.'}
    (ROOT/'docs/analysis/wing-candidate-check.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':run()
