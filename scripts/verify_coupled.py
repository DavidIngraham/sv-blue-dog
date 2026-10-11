"""Refined operating, geometry, recovery and sensitivity replay of a search result."""
import argparse,json
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
from .coupled_model import CoupledModel
from .native_coupled_operation import StructureKernel,RouteKernel
from .hydro_geometry import free_pitch_equilibrium,DisplacementBody
from .study_coupled import solve_state
from .native_design_kernel import ROOT
from .study_open_sizing import digest,validate


def operating_case(model,design,wind,up,tack,state,budget):
    constrained=solve_state(model,design,wind,up,budget,tack,resolution=16,initial_state=state,require_energy=True)
    constrained['energyConstraintsEnforced']=True
    if constrained['screenFeasible']:return constrained
    # Keep a balanced performance/energy diagnostic when the constrained attempt fails.
    seed=constrained['state'][3:] if constrained['equilibrated'] else state
    diagnostic=solve_state(model,design,wind,up,budget,tack,resolution=16,initial_state=seed,require_energy=False)
    diagnostic['energyConstraintsEnforced']=False
    diagnostic['energyConstrainedAttempt']={key:constrained[key] for key in ['equilibrated','screenFeasible','message']}
    diagnostic['energyConstrainedAttempt']['minimumEnergyMargin']=min(constrained['outputs'][n] for n in ['cycleMargin','reserveMarginScaled','peakMargin'])
    return diagnostic


def verify(name,design,initial,scenarios,budget=35):
    model=CoupledModel();model.parameters=np.array(scenarios['values'][name]);structure=StructureKernel();route=RouteKernel()
    x=np.array([design[n] for n in model.c['designNames']]);rows=[]
    env=[(w,u,t) for w in [5.,8.] for u in [True,False] for t in [1,-1]]
    for state,(wind,up,tack) in zip(initial,env):
        rows.append(operating_case(model,x,wind,up,tack,state,budget))
    bodies,m,g,_=model.configuration(x,0,resolution=16)
    cg=[m['cgX'],m['cgY'],m['cgZ']]
    upright=free_pitch_equilibrium(model.hydro,bodies,cg,m['totalMass'],0,density=model.parameters[31])
    loads=[max(row['outputs'][n] for row in rows) for n in ['wingResultant','keelResultant','rudderResultant']]
    margins=structure.evaluate(x,model.parameters,list(m.values()),g,loads,upright['waterline_m'])
    policy=scenarios['values']['adverseRoute' if name=='combined' else 'nominalRoute']
    trip=route.evaluate([r['outputs']['waterVMG'] for r in rows],np.array([r['state'][3:] for r in rows]).ravel(),policy)
    west=route.evaluate([r['outputs']['waterVMG'] for r in rows],np.array([r['state'][3:] for r in rows]).ravel(),policy,wind_from='west')
    recovery=[]
    # Complete curves for the nominal replay; additional evidence cases below.
    for trim in [0,90,180,270]:
        bodies,m,g,_=model.configuration(x,np.deg2rad(trim),resolution=16)
        cg=[m['cgX'],m['cgY'],m['cgZ']]
        points=[]
        for heel in np.linspace(-180,180,49):
            try:points.append(free_pitch_equilibrium(model.hydro,bodies,cg,m['totalMass'],heel,density=model.parameters[31]))
            except ValueError as error:
                if not str(error).startswith(('No pitch equilibrium','Insufficient enclosed displacement')):raise
                points.append({'heel_deg':float(heel),'failure':str(error)})
        restoring=[p['righting_Nm']*np.sign(p['heel_deg']) for p in points if 'failure' not in p and 0<abs(p['heel_deg'])<180]
        recovery.append({'trim_deg':trim,'points':points,'failedEquilibria':sum('failure' in p for p in points),'minimumInteriorRestoring_Nm':min(restoring) if restoring else None})
    numerical=all(r['equilibrated'] for r in rows)
    operating=min(row['outputs'][n] for row in rows for n in model.operation.contract['outputNames'][4:18]+model.operation.contract['outputNames'][47:])
    result={'scenario':name,'parameters':dict(zip(model.c['parameterNames'],model.parameters)),'cases':rows,'structure':margins,'route':trip.tolist(),'westerlyRoute':west.tolist(),'recovery':recovery,'numericallyBalanced':numerical,'minimumOperatingMargin':operating,'sampledStaticScreensPass':bool(numerical and operating>=-1e-4 and min(margins.values())>=-1e-4 and min(trip[:3])>=-1e-4 and min(west[:3])>=-1e-4 and all(r['failedEquilibria']==0 and r['minimumInteriorRestoring_Nm'] is not None and r['minimumInteriorRestoring_Nm']>0 for r in recovery)),'qualified':False}
    print('REPLAY',name,result['sampledStaticScreensPass'],'struct',min(margins.items(),key=lambda a:a[1]),'route',trip,'operating',operating,flush=True)
    return result


def run(names,budget,workers=3):
    if workers<1:raise ValueError('workers must be positive')
    if len(names)!=len(set(names)):raise ValueError('Duplicate sensitivity scenarios')
    source=ROOT/'docs/analysis/coupled-sizing-search.json';saved=json.loads(source.read_text());validate(saved['sourceHashes'])
    scenarios=json.loads((ROOT/'docs/analysis/coupled-uncertainty-inputs.json').read_text());validate(scenarios['sourceHashes'])
    sources=['docs/analysis/coupled-sizing-search.json','docs/analysis/coupled-uncertainty-inputs.json','scripts/verify_coupled.py','scripts/study_coupled.py','scripts/coupled_model.py','scripts/native_coupled_operation.py']
    hashes={n:digest(ROOT/n) for n in sources}
    completed={}
    with ProcessPoolExecutor(max_workers=min(workers,len(names))) as pool:
        futures={pool.submit(verify,name,saved['design'],saved['stateRows'],scenarios,budget):name for name in names}
        for future in as_completed(futures):
            name=futures[future];completed[name]=future.result()
            validate(hashes)
            report={'sourceHashes':hashes,'design':saved['design'],'scenarios':[completed[n] for n in names if n in completed],'geometryResolution':16,'operatingSolveBudgetPerPhase':budget,'qualified':False,'scope':'Refined static replay and provisional engineering sensitivities, not measured uncertainty or physical qualification. Sealed bodies; no retained-water, structural failure, wave dynamics, broadside/stall or dynamic capsize validation. No sailing-induced pitch moment in the quasi-steady operating balance.'}
            (ROOT/'docs/analysis/coupled-sizing-replay.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--scenarios',nargs='+',default=['nominal','construction','aerodynamic','hydrodynamic','energy','combined']);p.add_argument('--budget',type=int,default=35);p.add_argument('--workers',type=int,default=3);a=p.parse_args();run(a.scenarios,a.budget,a.workers)
