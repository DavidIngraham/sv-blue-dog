"""Solve coupled operating states before releasing vessel design variables."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import argparse,json,time
import numpy as np
from scipy.optimize import least_squares,minimize
from tools.boat_analysis.model.vessel import CoupledModel
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import digest


def operating_margin_names(contract, require_energy=True):
    """Static screens; finite storage/reserve feasibility belongs to the voyage.

    The instantaneous peak capability remains mandatory in normal solves.
    Daily cycle balance and a fixed overnight interval are not Gorge criteria.
    """
    return contract['staticMarginOutputs'] + ([contract['peakMarginOutput']] if require_energy else []) + contract['resistanceMarginOutputs']


def solve_state(model,design,wind,up,budget=70,tack=1,resolution=4,initial_state=None,require_energy=True,pitch_equilibrium=True):
    contract=model.operating_contract
    lo=np.array(contract['stateLower'],dtype=float)
    hi=np.array(contract['stateUpper'],dtype=float)
    if not up: lo[1],hi[1]=contract['leewardHeading']
    width=hi-lo;last=None;calls=0;t=time.time()
    eq=contract['equilibriumOutputs'];margins=operating_margin_names(contract,require_energy)
    def physical_state(z):
        operating=lo+z*width
        operating[1:]*=tack
        return np.r_[wind,int(up),1,operating]
    def evaluate(z):
        nonlocal last,calls
        if last is None or not np.array_equal(z,last[0]):
            state=physical_state(z)
            last=(np.array(z,copy=True),model.at_state(design,state,resolution=resolution,pitch_equilibrium=pitch_equilibrium));calls+=1
            if calls%100==0:print(f'wind {wind}, up {up}: {calls} calls, {time.time()-t:.1f}s',flush=True)
        return last[1]
    def equality(z):return np.array([evaluate(z)[n] for n in eq])
    def inequality(z):return np.array([evaluate(z)[n] for n in margins])
    guess=np.array([2,50 if up else 130,4,1,-2,15],dtype=float)
    if initial_state is not None:
        guess=np.array(initial_state[-6:],dtype=float);guess[1:]*=tack
    initial=np.clip((guess-lo)/width,1e-8,1-1e-8)
    phase=least_squares(lambda z:np.r_[equality(z),np.minimum(inequality(z),0)],initial,bounds=(0,1),diff_step=1e-4,max_nfev=budget,ftol=1e-8,xtol=1e-8,gtol=1e-8)
    result=minimize(lambda z:-evaluate(z)['waterVMG'],phase.x,method='SLSQP',bounds=[(0,1)]*6,constraints=[{'type':'eq','fun':equality},{'type':'ineq','fun':inequality}],options={'maxiter':budget,'ftol':1e-8,'eps':1e-5})
    candidates=[phase.x,result.x]
    feasible=[z for z in candidates if np.abs(equality(z)).max()<1e-4 and inequality(z).min()>-1e-4]
    selected=max(feasible,key=lambda z:evaluate(z)['waterVMG']) if feasible else min(candidates,key=lambda z:np.linalg.norm(np.r_[equality(z),np.minimum(inequality(z),0)]))
    output=evaluate(selected)
    return {'wind_m_s':wind,'windward':up,'tack':tack,'state':physical_state(selected).tolist(),'outputs':output,'equilibrated':bool(np.abs(equality(selected)).max()<1e-4),'screenFeasible':bool(np.abs(equality(selected)).max()<1e-4 and inequality(selected).min()>-1e-4),'message':str(result.message),'calls':calls,'elapsed_s':time.time()-t}


def run(budget):
    model=CoupledModel();design=model.c['referenceDesign'];rows=[]
    for wind,up,tack in [(w,u,t) for w in model.operating_contract['windSpeeds'] for u in [True,False] for t in [1,-1]]:
        row=solve_state(model,design,wind,up,budget,tack);rows.append(row)
        print('RESULT',wind,up,row['screenFeasible'],row['outputs']['waterVMG'],flush=True)
        (ROOT/'.tools/coupled-fixed-checkpoint.json').write_text(json.dumps(rows,indent=2)+'\n')
    sources=['tools/boat_analysis/geometry/laminate.py','tools/boat_analysis/geometry/hull.py','models/libraries/analysis.sysml','models/blue-dog.sysml','uv.lock','models/blue-dog.sysml','models/blue-dog.sysml','models/blue-dog.sysml','tools/boat_analysis/model/vessel.py','tools/boat_analysis/optimization/operating.py','packages/sysml-python/sysml_python/execution.py','tools/boat_analysis/geometry/vessel.py','tools/boat_analysis/aerodynamics/polar.py','build/analysis/wing-polar-grid.json']
    report={'sourceHashes':source_hashes(sources),'design':dict(zip(model.c['designNames'],design)),'parameters':dict(zip(model.c['parameterNames'],model.parameters)),'cases':rows,'qualified':False,'scope':'Fixed-design operating solve only, not size optimization. Attached-flow inviscid response plus provisional profile drag, lift cap and discrepancy factors. Hydrostatic heave and pitch equilibrium, approximate upright force projections. No sailing-induced pitch balance, wave dynamics, separated-flow polar or dynamic capsize verification.'}
    output_path('coupled-fixed-design.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--budget',type=int,default=70);run(p.parse_args().budget)
