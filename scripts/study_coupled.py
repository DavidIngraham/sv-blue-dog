"""Solve coupled operating states before releasing vessel design variables."""
import argparse,json,time
import numpy as np
from scipy.optimize import least_squares,minimize
from .coupled_model import CoupledModel
from .native_design_kernel import ROOT
from .study_open_sizing import digest


def solve_state(model,design,wind,up,budget=70,tack=1,resolution=4,initial_state=None,require_energy=True):
    lo=np.array([.2,20 if up else 95,-12,-12,-25,-40.])
    hi=np.array([5.,88 if up else 175,16,12,25,40.])
    width=hi-lo;last=None;calls=0;t=time.time()
    names=model.operation.contract['outputNames'];eq=names[:4];margins=names[4:18 if require_energy else 15]
    def physical_state(z):
        operating=lo+z*width
        operating[1:]*=tack
        return np.r_[wind,int(up),1,operating]
    def evaluate(z):
        nonlocal last,calls
        if last is None or not np.array_equal(z,last[0]):
            state=physical_state(z)
            last=(np.array(z,copy=True),model.at_state(design,state,resolution=resolution));calls+=1
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
    for wind,up,tack in [(w,u,t) for w in [5.,8.] for u in [True,False] for t in [1,-1]]:
        row=solve_state(model,design,wind,up,budget,tack);rows.append(row)
        print('RESULT',wind,up,row['screenFeasible'],row['outputs']['waterVMG'],flush=True)
        (ROOT/'.tools/coupled-fixed-checkpoint.json').write_text(json.dumps(rows,indent=2)+'\n')
    sources=['models/coupled-sizing.sysml','models/coupled-operation.sysml','models/wing-actuator.sysml','scripts/coupled_model.py','scripts/study_coupled.py','scripts/native_coupled.py','scripts/native_coupled_operation.py','scripts/coupled_geometry.py','scripts/wing_polar.py','docs/analysis/wing-polar-grid.json']
    report={'sourceHashes':{n:digest(ROOT/n) for n in sources},'design':dict(zip(model.c['designNames'],design)),'parameters':dict(zip(model.c['parameterNames'],model.parameters)),'cases':rows,'qualified':False,'scope':'Fixed-design operating solve only, not size optimization. Attached-flow inviscid response plus provisional profile drag, lift cap and discrepancy factors. Hydrostatic heave and pitch equilibrium, approximate upright force projections. No sailing-induced pitch balance, wave dynamics, separated-flow polar or dynamic capsize verification.'}
    (ROOT/'docs/analysis/coupled-fixed-design.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--budget',type=int,default=70);run(p.parse_args().budget)
