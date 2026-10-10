"""Shared free-design feasibility and minimum-length search.

The search uses coarse geometry and fixed-pitch hydrostatic screens for cost.
A candidate is not accepted as verified until finer, free-pitch replay succeeds.
"""
import argparse,json,time
import numpy as np
from scipy.optimize import least_squares,minimize
from .coupled_model import CoupledModel
from .native_coupled_operation import StructureKernel,RouteKernel
from .hydro_geometry import equilibrium
from .native_design_kernel import ROOT
from .study_open_sizing import digest

class Problem:
    def __init__(self):
        self.model=CoupledModel();self.structure=StructureKernel();self.route=RouteKernel();c=self.structure.contract
        self.lo=np.r_[c['designLower'],np.tile([.2,20,-12,-12,-25,-40],8)]
        self.hi=np.r_[c['designUpper'],np.tile([5,88,16,12,25,40],8)]
        self.env=[(w,u,t) for w in [5.,8.] for u in [True,False] for t in [1,-1]]
        for i,(_,up,_) in enumerate(self.env):
            if not up:self.lo[28+6*i+1]=95;self.hi[28+6*i+1]=175
        self.span=self.hi-self.lo;self.last=None;self.calls=0;self.start=time.time();self.best=None
    def evaluate(self,z):
        if self.last is not None and np.array_equal(z,self.last[0]):return self.last[1]
        physical=self.lo+z*self.span;x=physical[:28];states=physical[28:].reshape(8,6).copy()
        for state,(_,_,tack) in zip(states,self.env):state[1:]*=tack
        k=self.model;rows=[]
        for state,(wind,up,_) in zip(states,self.env):rows.append(k.at_state(x,np.r_[wind,int(up),1,state],pitch_equilibrium=False))
        bodies,m,g,_=k.configuration(x,0)
        loads=[max(row[name] for row in rows) for name in ['wingResultant','keelResultant','rudderResultant']]
        cg=[m['cgX'],m['cgY'],m['cgZ']]
        upright=equilibrium(k.hydro,bodies,cg,m['totalMass'],0,density=k.parameters[31])
        margins=self.structure.evaluate(x,k.parameters,list(m.values()),g,loads,upright['waterline_m'])
        route=self.route.evaluate([r['waterVMG'] for r in rows],states.ravel())
        righting=[]
        for trim in [0.,np.pi/2]:
            bodies,m,_,_=k.configuration(x,trim)
            cg=[m['cgX'],m['cgY'],m['cgZ']]
            for heel in [-175.,-150.,-90.,-15.,15.,90.,150.,175.]:
                h=equilibrium(k.hydro,bodies,cg,m['totalMass'],heel,density=k.parameters[31])
                righting.append(h['righting_Nm']*np.sign(heel)/(m['totalMass']*k.parameters[34]*.1))
        names=k.operation.contract['outputNames'];eq=np.array([[r[n] for n in names[:4]] for r in rows]).ravel()
        ineq=np.r_[[[r[n] for n in names[4:18]] for r in rows]].ravel()
        ineq=np.r_[ineq,list(margins.values()),route[:3],righting]
        result={'eq':eq,'ineq':ineq,'design':x,'states':states,'rows':rows,'structure':margins,'route':route,'righting':righting,'mass':m}
        self.calls+=1
        merit=float(np.linalg.norm(np.r_[eq,np.minimum(ineq,0)]))
        if self.best is None or merit<self.best[0]:self.best=(merit,np.array(z,copy=True))
        if self.calls%40==0:
            print(f'{self.calls} calls, {time.time()-self.start:.0f}s, merit {merit:.5f}, best {self.best[0]:.5f}, L {x[0]:.3f}, min margin {ineq.min():.4f}',flush=True)
            (ROOT/'.tools/coupled-search-progress.json').write_text(json.dumps({'calls':self.calls,'bestMerit':self.best[0],'bestZ':self.best[1].tolist()})+'\n')
        self.last=(np.array(z,copy=True),result);return result
    def residual(self,z):
        r=self.evaluate(z);return np.r_[r['eq'],np.minimum(r['ineq'],0)]
    def initial(self):
        saved=json.loads((ROOT/'docs/analysis/coupled-fixed-design.json').read_text())
        x=np.array([saved['design'][n] for n in self.model.c['designNames']]);states=[]
        for row in saved['cases']:
            state=np.array(row['state'][3:]);state[1:]*=row['tack'];states.extend(state)
        if len(states)!=48:raise ValueError('Both-tack reference solve required')
        # Initial guesses only; all dimensions remain free in the solve.
        x[5]=3.;x[7]=1.2;x[23]=.6
        return np.clip((np.r_[x,states]-self.lo)/self.span,1e-5,1-1e-5)
    def feasible(self,z,tolerance=1e-4):
        r=self.evaluate(z);return bool(np.abs(r['eq']).max()<tolerance and r['ineq'].min()>-tolerance)


def run(budget):
    p=Problem();initial=p.initial()
    phase=least_squares(p.residual,initial,bounds=(0,1),diff_step=1e-4,max_nfev=budget,ftol=1e-7,xtol=1e-7,gtol=1e-7)
    best=phase.x if np.linalg.norm(p.residual(phase.x))<=p.best[0]+1e-8 else p.best[1]
    message='Feasibility phase did not satisfy all screens'
    if p.feasible(best):
        result=minimize(lambda z:p.lo[0]+z[0]*p.span[0],best,method='SLSQP',bounds=[(0,1)]*len(best),constraints=[{'type':'eq','fun':lambda z:p.evaluate(z)['eq']},{'type':'ineq','fun':lambda z:p.evaluate(z)['ineq']}],options={'maxiter':budget,'eps':1e-5,'ftol':1e-7})
        message=str(result.message)
        if p.feasible(result.x):best=result.x
    r=p.evaluate(best)
    sources=['models/coupled-sizing.sysml','models/coupled-operation.sysml','models/wing-actuator.sysml','models/hydrostatics.sysml','scripts/coupled_model.py','scripts/optimize_coupled.py','scripts/native_coupled.py','scripts/native_coupled_operation.py','scripts/coupled_geometry.py','scripts/wing_polar.py','docs/analysis/wing-polar-grid.json']
    report={'sourceHashes':{n:digest(ROOT/n) for n in sources},'design':dict(zip(p.model.c['designNames'],r['design'])),'stateRows':r['states'].tolist(),'operating':r['rows'],'structure':r['structure'],'route':r['route'].tolist(),'rightingScreen':r['righting'],'mass':r['mass'],'maxEquilibriumResidual':float(np.abs(r['eq']).max()),'minimumMargin':float(r['ineq'].min()),'coarseFeasible':p.feasible(best),'optimizerMessage':message,'feasibilityMessage':str(phase.message),'calls':p.calls,'elapsed_s':time.time()-p.start,'normalizedDesignAndStates':best.tolist(),'qualified':False,'scope':'Coarse fixed-pitch screening search; pending refined free-pitch and uncertainty replay. VSPAERO attached-flow only; independent provisional drag and lift caps. No claim of mission qualification or global optimum.'}
    (ROOT/'docs/analysis/coupled-sizing-search.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print('FINISHED',report['coarseFeasible'],report['design']['length_m'],report['minimumMargin'],flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--budget',type=int,default=40);run(parser.parse_args().budget)
