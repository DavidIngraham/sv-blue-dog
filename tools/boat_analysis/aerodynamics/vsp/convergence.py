"""Cross-check mesh and wake sensitivity at representative restricted-domain cases."""
import json
import numpy as np
from tools.boat_analysis.aerodynamics.vsp.polar_grid import run_case
from tools.boat_analysis.model.runtime import ROOT, analysis_values
from tools.boat_analysis.evidence.records import source_hashes,output_path


def run():
    c=analysis_values('BlueDogAerodynamicPolicy::convergenceInputs')
    hashes=source_hashes(['tools/boat_analysis/aerodynamics/vsp/convergence.py','tools/boat_analysis/aerodynamics/vsp/polar_grid.py','tools/boat_analysis/aerodynamics/vsp/reference_vsp.py','tools/boat_analysis/aerodynamics/vsp/vsp_runtime.py','build/analysis/wing-geometry.json'])
    rows=[]
    for reverse,beta in [(False,0),(True,0),(False,20)]:
        configurations=[(c['meshes'][0],w) for w in c['wakeIterations']]+[(m,c['wakeIterations'][-1]) for m in c['meshes'][1:]]
        for mesh,wake in configurations:
            row=run_case(c['aspect'],c['camber'],mesh,reverse,wake_iterations=wake,alpha_start=-4,alpha_end=8,alpha_count=4,beta=beta)
            rows.append(row);print('CONVERGENCE',reverse,beta,mesh,wake,flush=True)
    comparisons=[]
    keys=['CLtot','CDi','CMytot']
    for reverse,beta in [(False,0),(True,0),(False,20)]:
        selected=[r for r in rows if r['reverseChord']==reverse and r['beta_deg']==beta]
        for label,i,j in [('wake',1,2),('mesh',3,4)]:
            difference=[float(np.max(np.abs(np.array(selected[i]['values'][k])-selected[j]['values'][k]))) for k in keys]
            comparisons.append({'reverseChord':reverse,'beta_deg':beta,'comparison':label,'maxAbsoluteDifference':dict(zip(keys,difference)),'passesScreen':bool(np.all(np.array(difference)<=c['absoluteTolerance']))})
    output_path('wing-convergence.json').write_text(json.dumps({'sourceHashes':hashes,'settings':c,'cases':rows,'comparisons':comparisons,'validated':False,'scope':'Representative numerical checks, not complete design-space convergence or physical validation.'},indent=2)+'\n')

if __name__=='__main__':run()
