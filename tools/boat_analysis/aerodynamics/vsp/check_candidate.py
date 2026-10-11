"""Direct VSPAERO check of grid interpolation at the current sizing candidate."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import json,sys
import numpy as np
from tools.boat_analysis.aerodynamics.vsp.polar_grid import run_case
from tools.boat_analysis.aerodynamics.vsp.vsp_runtime import ROOT
sys.path.insert(0,str(ROOT))
from tools.boat_analysis.aerodynamics.polar import WingPolar
from tools.boat_analysis.evidence.records import digest,validate


def run():
    saved=input_record('coupled-sizing-search.json')
    d=saved['design'];polar=WingPolar();cases=[]
    sources=['build/analysis/coupled-sizing-search.json','build/analysis/wing-polar-grid.json','tools/boat_analysis/aerodynamics/vsp/check_candidate.py','tools/boat_analysis/aerodynamics/vsp/polar_grid.py','tools/boat_analysis/aerodynamics/vsp/reference_vsp.py','tools/boat_analysis/aerodynamics/vsp/vsp_runtime.py','tools/boat_analysis/aerodynamics/polar.py']
    hashes=source_hashes(sources)
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
    output_path('wing-candidate-check.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':run()
