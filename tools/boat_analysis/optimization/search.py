"""Shared free-design feasibility and minimum-length search.

The search uses coarse geometry and fixed-pitch hydrostatic screens for cost.
A candidate is not accepted as verified until finer, free-pitch replay succeeds.
"""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import argparse,json,time
from types import SimpleNamespace
import numpy as np
from scipy.optimize import least_squares,minimize
from tools.boat_analysis.model.vessel import CoupledModel
from tools.boat_analysis.model.operating import StructureKernel,RouteKernel
from tools.boat_analysis.geometry.hydro import equilibrium
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import digest,validate
from tools.boat_analysis.optimization.operating import operating_margin_names

class Problem:
    def __init__(self,resolution=12,route_profile='challenge'):
        if route_profile not in ('challenge','all-season'):raise ValueError('Unknown route profile')
        self.route_profile=route_profile
        self.resolution=resolution
        # Numerical allowance for coarse fixed-pitch versus refined free-pitch VMG.
        self.model=CoupledModel();self.structure=StructureKernel();self.route=RouteKernel();c=self.structure.contract
        self.progress_reserve_m_s=c['progressSearchReserve']
        self.require_east=c['challengeRequiresEastProgress' if route_profile=='challenge' else 'allSeasonRequiresEastProgress']
        self.lo=np.r_[c['designLower'],np.tile(c['stateLower'],8)]
        self.hi=np.r_[c['designUpper'],np.tile(c['stateUpper'],8)]
        self.env=[(w,u,t) for w in c['windSpeeds'] for u in [True,False] for t in [1,-1]]
        for i,(_,up,_) in enumerate(self.env):
            if not up:self.lo[29+6*i+1],self.hi[29+6*i+1]=c['leewardHeading']
        self.span=self.hi-self.lo
        axes=self.model.polar.axes
        physical_knots={5:axes[0],6:axes[1],**{29+6*i+2:axes[2] for i in range(8)}}
        self.breakpoints={i:(values-self.lo[i])/self.span[i] for i,values in physical_knots.items()}
        self.last=None;self.calls=0;self.start=time.time();self.best=None;self.best_feasible=None;self.derivatives=None;self.design_cache=None
    def design_data(self,x):
        if self.design_cache is not None and np.array_equal(x,self.design_cache[0]):return self.design_cache[1]
        k=self.model
        bodies,m,g,_=k.configuration(x,0,resolution=self.resolution)
        reference_mass=m.copy()
        cg=[m['cgX'],m['cgY'],m['cgZ']]
        upright=equilibrium(k.hydro,bodies,cg,m['totalMass'],0,density=k.parameters[31])
        righting=[]
        for trim in np.deg2rad(self.structure.contract['coarseTrims']):
            bodies,m,_,_=k.configuration(x,trim,resolution=self.resolution)
            cg=[m['cgX'],m['cgY'],m['cgZ']]
            for heel in self.structure.contract['coarseHeels']:
                h=equilibrium(k.hydro,bodies,cg,m['totalMass'],heel,density=k.parameters[31])
                righting.append(h['righting_Nm']*np.sign(heel)/(m['totalMass']*k.parameters[34]*.1))
        result=(reference_mass,g,upright,righting)
        self.design_cache=(np.array(x,copy=True),result)
        return result
    def evaluate(self,z):
        try:return self._evaluate(z)
        except ValueError as error:
            geometric=('Insufficient enclosed displacement','Waterline must cut','f(a) and f(b) must have different signs')
            if self.last is None or not any(str(error).startswith(text) for text in geometric):raise
            # Invalid trial geometry is infeasible, never a resistance extrapolation.
            previous=self.last[1]
            return {'eq':np.full_like(previous['eq'],1000.),'ineq':np.full_like(previous['ineq'],-1000.),'invalidGeometry':str(error)}
    def _evaluate(self,z):
        if self.last is not None and np.array_equal(z,self.last[0]):return self.last[1]
        physical=self.lo+z*self.span;x=physical[:29];states=physical[29:].reshape(8,6).copy()
        for state,(_,_,tack) in zip(states,self.env):state[1:]*=tack
        k=self.model;rows=[]
        for state,(wind,up,_) in zip(states,self.env):rows.append(k.at_state(x,np.r_[wind,int(up),1,state],resolution=self.resolution,pitch_equilibrium=False))
        reference_mass,g,upright,righting=self.design_data(x)
        loads=[max(row[name] for row in rows) for name in ['wingResultant','keelResultant','rudderResultant']]
        margins=self.structure.evaluate(x,k.parameters,list(reference_mass.values()),g,loads,upright['waterline_m'])
        route=self.route.evaluate([r['waterVMG'] for r in rows],states.ravel())
        west=self.route.evaluate([r['waterVMG'] for r in rows],states.ravel(),wind_from='west')
        names=k.operation.contract['outputNames'];eq=np.array([[r[n] for n in names[:4]] for r in rows]).ravel()
        static_names=operating_margin_names(names)[:12]
        operating=np.array([[r[n] for n in static_names] for r in rows])
        ineq=operating.ravel()
        route_reserve=np.array([1.,1.,0.])*self.progress_reserve_m_s/self.route.contract['routeParameters'][5]
        route_screens=[('westerly',west)]+([('easterly',route)] if self.require_east else [])
        ineq=np.r_[ineq,(np.array([[r[n] for n in names[47:]] for r in rows])-np.array(k.operation.contract['resistanceDomainReserve'])).ravel(),list(margins.values()),np.concatenate([r[:3]-route_reserve for _,r in route_screens]),righting]
        self.constraint_names=([f'case {i}: {n}' for i in range(8) for n in static_names]
            +[f'case {i}: {n} (search reserve)' for i in range(8) for n in names[47:]]
            +list(margins)+[f'{direction} {n}' for direction,_ in route_screens for n in ['downstream progress','upstream progress','duration']]
            +[f'righting trim {trim:g}, heel {heel:g}' for trim in self.structure.contract['coarseTrims'] for heel in self.structure.contract['coarseHeels']])
        result={'eq':eq,'ineq':ineq,'design':x,'states':states,'rows':rows,'structure':margins,'route':route,'westerlyRoute':west,'righting':righting,'mass':reference_mass}
        self.calls+=1
        merit=float(np.linalg.norm(np.r_[eq,np.minimum(ineq,0)]))
        if self.best is None or merit<self.best[0]:self.best=(merit,np.array(z,copy=True))
        if np.abs(eq).max()<1e-4 and ineq.min()>-1e-4 and (self.best_feasible is None or x[0]<self.best_feasible[0]):self.best_feasible=(float(x[0]),np.array(z,copy=True))
        if self.calls%40==0:
            print(f'{self.calls} calls, {time.time()-self.start:.0f}s, merit {merit:.5f}, best {self.best[0]:.5f}, L {x[0]:.3f}, min margin {ineq.min():.4f}',flush=True)
            (ROOT/'.tools/coupled-search-progress.json').write_text(json.dumps({'calls':self.calls,'bestMerit':self.best[0],'bestZ':self.best[1].tolist(),'currentZ':np.asarray(z).tolist(),'bestFeasibleZ':None if self.best_feasible is None else self.best_feasible[1].tolist()})+'\n')
        self.last=(np.array(z,copy=True),result);return result
    def jacobians(self,z):
        if self.derivatives is not None and np.array_equal(z,self.derivatives[0]):return self.derivatives[1:]
        base=self.evaluate(z);eq=np.empty((len(base['eq']),len(z)));ineq=np.empty((len(base['ineq']),len(z)))
        for i in range(len(z)):
            step=1e-5 if z[i]<=1-1e-5 else -1e-5
            knots=getattr(self,'breakpoints',{}).get(i,np.array([]))
            if step>0 and np.any((knots>z[i]+1e-12)&(knots<z[i]+step)):step=-step
            elif step<0 and np.any((knots<z[i]-1e-12)&(knots>z[i]+step)):step=-step
            trial=np.array(z,copy=True);trial[i]+=step;r=self.evaluate(trial)
            eq[:,i]=(r['eq']-base['eq'])/step;ineq[:,i]=(r['ineq']-base['ineq'])/step
        self.derivatives=(np.array(z,copy=True),eq,ineq)
        return eq,ineq
    def residual(self,z):
        r=self.evaluate(z);return np.r_[r['eq'],np.minimum(r['ineq'],0)]
    def residual_jacobian(self,z):
        r=self.evaluate(z);eq,ineq=self.jacobians(z)
        return np.vstack([eq,ineq*(r['ineq']<0)[:,None]])
    def initial(self):
        saved=input_record('coupled-fixed-design.json')
        x=np.array([saved['design'].get(n,self.model.c['referenceDesign'][i]) for i,n in enumerate(self.model.c['designNames'])]);states=[]
        for row in saved['cases']:
            state=np.array(row['state'][3:]);state[1:]*=row['tack'];states.extend(state)
        if len(states)!=48:raise ValueError('Both-tack reference solve required')
        # Initial guesses only; all dimensions remain free in the solve.
        x[5]=3.;x[7]=1.2;x[23]=.6
        return np.clip((np.r_[x,states]-self.lo)/self.span,1e-5,1-1e-5)
    def feasible(self,z,tolerance=1e-4):
        r=self.evaluate(z);return bool(np.abs(r['eq']).max()<tolerance and r['ineq'].min()>-tolerance)


def run(budget,resume=False,resolution=12,route_profile='challenge'):
    p=Problem(resolution,route_profile);initial=p.initial()
    checkpoint_hash=None
    if resume:
        checkpoint=ROOT/'.tools/coupled-search-progress.json'
        checkpoint_hash=digest(checkpoint)
        initial=np.array(json.loads(checkpoint.read_text())['bestZ'])
        if initial.shape!=p.lo.shape or np.any(initial<0) or np.any(initial>1):raise ValueError('Incompatible numerical checkpoint')
    seed=initial.copy()
    # Geometrically consistent starting guess only; length remains free.
    physical=p.lo+initial*p.span
    _,_,geometry,_=p.model.configuration(physical[:29],0,resolution=resolution)
    needed=physical[17]/(p.model.parameters[37]*geometry[51])
    if needed>1.001:
        physical[0]=min(p.hi[0],physical[0]*needed*1.02)
        initial=(physical-p.lo)/p.span
    sources=['tools/boat_analysis/geometry/laminate.py','uv.lock','tools/boat_analysis/optimization/search.py','tools/boat_analysis/optimization/operating.py','tools/boat_analysis/model/vessel.py','tools/boat_analysis/model/mass.py','tools/boat_analysis/model/operating.py','tools/boat_analysis/model/hydrostatics.py','tools/boat_analysis/geometry/hydro.py','tools/boat_analysis/geometry/vessel.py','tools/boat_analysis/geometry/hull.py','tools/boat_analysis/aerodynamics/polar.py','build/analysis/wing-polar-grid.json','build/analysis/wing-geometry.json']
    hashes={**p.model.mass.contract['sourceHashes'],**p.model.operation.contract['sourceHashes'],**source_hashes(sources),'models/analyses/recovery.sysml':digest(ROOT/'models/analyses/recovery.sysml')}

    if np.abs(p.evaluate(initial)['eq']).max()>1e-4:
        from tools.boat_analysis.optimization.operating import solve_state
        current=p.evaluate(initial);states=[]
        for state,(wind,up,tack) in zip(current['states'],p.env):
            row=solve_state(p.model,current['design'],wind,up,budget=20,tack=tack,resolution=resolution,initial_state=state,pitch_equilibrium=False)
            signed=np.array(row['state'][3:]);signed[1:]*=tack;states.extend(signed)
        balanced=(np.r_[current['design'],states]-p.lo)/p.span
        if np.linalg.norm(p.residual(balanced))<np.linalg.norm(p.residual(initial)):initial=balanced
    def stop_when_feasible(intermediate_result):
        if p.feasible(intermediate_result.x):raise StopIteration
    feasibility_initial=initial.copy()
    phase=SimpleNamespace(x=initial,message='Saved initial guess passes freshly evaluated feasibility screens') if p.feasible(initial) else least_squares(p.residual,initial,jac=p.residual_jacobian,bounds=(0,1),diff_step=1e-4,max_nfev=budget,callback=stop_when_feasible,ftol=1e-7,xtol=1e-7,gtol=1e-7)
    best=phase.x if np.linalg.norm(p.residual(phase.x))<=p.best[0]+1e-8 else p.best[1]
    constraints=[{'type':'eq','fun':lambda z:p.evaluate(z)['eq'],'jac':lambda z:p.jacobians(z)[0]},{'type':'ineq','fun':lambda z:p.evaluate(z)['ineq']+1e-8,'jac':lambda z:p.jacobians(z)[1]}]
    feasibility_sqp_message=None
    if not p.feasible(best):
        anchor=np.array(best,copy=True)
        feasibility_sqp=minimize(lambda z:.5*np.sum((z-anchor)**2),anchor,method='SLSQP',jac=lambda z:z-anchor,bounds=[(0,1)]*len(anchor),constraints=constraints,options={'maxiter':budget,'ftol':1e-8})
        feasibility_sqp_message=str(feasibility_sqp.message)
        if p.feasible(feasibility_sqp.x):best=feasibility_sqp.x
    message='Feasibility phase did not satisfy all screens';last_attempt=None;repair_message=None
    if p.feasible(best):
        result=minimize(lambda z:p.lo[0]+z[0]*p.span[0],best,method='SLSQP',jac=lambda z:np.r_[p.span[0],np.zeros(len(z)-1)],bounds=[(0,1)]*len(best),constraints=constraints,options={'maxiter':budget,'eps':1e-5,'ftol':1e-4})
        message=str(result.message)
        trial=p.evaluate(result.x)
        last_attempt={'normalizedDesignAndStates':result.x.tolist(),'maxEquilibriumResidual':float(np.abs(trial['eq']).max()),'minimumMargin':float(trial['ineq'].min()),'worstConstraints':sorted(zip(p.constraint_names,map(float,trial['ineq'])),key=lambda item:item[1])[:12]}
        if p.feasible(result.x):best=result.x
        else:
            # Restore feasibility near the shorter trial; no design variable is frozen.
            repair=least_squares(p.residual,np.clip(result.x,0,1),jac=p.residual_jacobian,bounds=(0,1),diff_step=1e-4,max_nfev=budget,callback=stop_when_feasible,ftol=1e-7,xtol=1e-7,gtol=1e-7)
            repair_message=str(repair.message)
            if p.feasible(repair.x):best=repair.x
    if p.best_feasible is not None:best=p.best_feasible[1]
    elif p.best is not None:best=p.best[1]
    r=p.evaluate(best)
    validate(hashes)

    report={'sourceHashes':hashes,'geometryResolution':resolution,'progressSearchReserve_m_s':p.progress_reserve_m_s,'budgetPerPhase':budget,'optimizerFtol':1e-4,'energyConstraintScope':'Instantaneous peak power only; finite storage/reserve requires chronological mission replay','resistanceDomainReserve':p.model.operation.contract['resistanceDomainReserve'],'designBounds':dict(zip(p.model.c['designNames'],zip(p.lo[:29].tolist(),p.hi[:29].tolist()))),'design':dict(zip(p.model.c['designNames'],r['design'])),'stateRows':r['states'].tolist(),'operating':r['rows'],'structure':r['structure'],'route':r['route'].tolist(),'westerlyRoute':r['westerlyRoute'].tolist(),'rightingScreen':r['righting'],'mass':r['mass'],'maxEquilibriumResidual':float(np.abs(r['eq']).max()),'minimumMargin':float(r['ineq'].min()),'coarseFeasible':p.feasible(best),'optimizerMessage':message,'feasibilityRestorationMessage':repair_message,'lastOptimizerAttempt':last_attempt,'worstConstraints':sorted(zip(p.constraint_names,map(float,r['ineq'])),key=lambda item:item[1])[:12],'feasibilitySqpMessage':feasibility_sqp_message,'feasibilityMessage':str(phase.message),'calls':p.calls,'elapsed_s':time.time()-p.start,'normalizedDesignAndStates':best.tolist(),'qualified':False,'scope':'Delft upright untrimmed bare-hull regression with explicit coordinate screens; free hull-fullness exponent. Fixed-pitch screening search at the recorded geometry resolution; pending refined free-pitch and uncertainty replay. VSPAERO attached-flow only; independent provisional drag and lift caps. No claim of mission qualification or global optimum.'}
    report.update(routeProfile=p.route_profile,requiresEastProgress=p.require_east,
                  probabilityWeighting='No calibrated mission distribution; separate native probability sensitivity, never averaged hard safety constraints.',
                  resumed=resume,resumeCheckpointSha256=checkpoint_hash,
                  seedNormalizedDesignAndStates=seed.tolist(),
                  feasibilityInitialNormalizedDesignAndStates=feasibility_initial.tolist())
    output_path('coupled-sizing-search.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print('FINISHED',report['coarseFeasible'],report['design']['length_m'],report['minimumMargin'],flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--budget',type=int,default=40);parser.add_argument('--resume',action='store_true');parser.add_argument('--resolution',type=int,default=12);parser.add_argument('--route-profile',choices=['challenge','all-season'],default='challenge');args=parser.parse_args();run(args.budget,args.resume,args.resolution,args.route_profile)
