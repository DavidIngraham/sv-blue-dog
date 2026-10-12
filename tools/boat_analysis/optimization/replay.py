"""Refined operating, geometry, recovery and sensitivity replay of a search result."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import argparse,json
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
from tools.boat_analysis.model.vessel import CoupledModel
from tools.boat_analysis.model.operating import StructureKernel,RouteKernel,ConceptKernel
from tools.boat_analysis.geometry.hydro import free_pitch_equilibrium,DisplacementBody
from tools.boat_analysis.optimization.operating import solve_state, operating_margin_names
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import digest,validate


def operating_case(model,design,wind,up,tack,state,budget):
    constrained=solve_state(model,design,wind,up,budget,tack,resolution=16,initial_state=state,require_energy=True)
    constrained['energyConstraintsEnforced']=True
    constrained['energyConstraintScope']='Instantaneous peak power only; mission energy history assessed separately'
    if constrained['screenFeasible']:return constrained
    # Keep a balanced performance/energy diagnostic when the constrained attempt fails.
    seed=constrained['state'][3:] if constrained['equilibrated'] else state
    diagnostic=solve_state(model,design,wind,up,budget,tack,resolution=16,initial_state=seed,require_energy=False)
    diagnostic['energyConstraintsEnforced']=False
    diagnostic['energyConstrainedAttempt']={key:constrained[key] for key in ['equilibrated','screenFeasible','message']}
    diagnostic['energyConstrainedAttempt']['minimumEnergyMargin']=constrained['outputs']['peakMargin']
    return diagnostic


def verify(name,design,initial,scenarios,budget=35,route_profile='challenge'):
    if route_profile not in ('challenge','all-season'):raise ValueError('Unknown route profile')
    model=CoupledModel();model.parameters=np.array(scenarios['values'][name]);structure=StructureKernel();route=RouteKernel()
    x=np.array([design[n] for n in model.c['designNames']]);rows=[]
    env=[(w,u,t) for w in model.operation.contract['windSpeeds'] for u in [True,False] for t in [1,-1]]
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
    concept=ConceptKernel().evaluate(x,list(m.values()),g,max(west[5],trip[5]) if route_profile=='all-season' else west[5],max(r['outputs']['averagePower'] for r in rows))
    margins.update({n:concept[n] for n in ('voyageEnergyMargin','installationVolumeMargin')})
    recovery=[]
    # Complete curves for the nominal replay; additional evidence cases below.
    for trim in model.operation.contract['recoveryTrims']:
        bodies,m,g,_=model.configuration(x,np.deg2rad(trim),resolution=16)
        cg=[m['cgX'],m['cgY'],m['cgZ']]
        points=[]
        for heel in np.linspace(*model.operation.contract['recoveryHeels'][:2],int(model.operation.contract['recoveryHeels'][2])):
            try:points.append(free_pitch_equilibrium(model.hydro,bodies,cg,m['totalMass'],heel,density=model.parameters[31]))
            except ValueError as error:
                if not str(error).startswith(('No pitch equilibrium','Insufficient enclosed displacement')):raise
                points.append({'heel_deg':float(heel),'failure':str(error)})
        restoring=[p['righting_Nm']*np.sign(p['heel_deg']) for p in points if 'failure' not in p and 0<abs(p['heel_deg'])<180]
        recovery.append({'trim_deg':trim,'points':points,'failedEquilibria':sum('failure' in p for p in points),'minimumInteriorRestoring_Nm':min(restoring) if restoring else None})
    numerical=all(r['equilibrated'] for r in rows)
    operating=min(row['outputs'][n] for row in rows for n in operating_margin_names(model.operation.contract['outputNames']))
    result={'scenario':name,'parameters':dict(zip(model.c['parameterNames'],model.parameters)),'cases':rows,'structure':margins,'concept':concept,'route':trip.tolist(),'westerlyRoute':west.tolist(),'recovery':recovery,'numericallyBalanced':numerical,'minimumOperatingMargin':operating,'sampledStaticScreensPass':bool(numerical and operating>=-1e-4 and min(margins.values())>=-1e-4 and min(trip[:3])>=-1e-4 and min(west[:3])>=-1e-4 and all(r['failedEquilibria']==0 and r['minimumInteriorRestoring_Nm'] is not None and r['minimumInteriorRestoring_Nm']>0 for r in recovery)),'qualified':False}
    # Preserve the original strict two-direction field; expose the selected
    # profile separately so old evidence consumers cannot mistake its meaning.
    requires_east=structure.contract['challengeRequiresEastProgress' if route_profile=='challenge' else 'allSeasonRequiresEastProgress']
    common=numerical and operating>=-1e-4 and min(margins.values())>=-1e-4 and all(r['failedEquilibria']==0 and r['minimumInteriorRestoring_Nm'] is not None and r['minimumInteriorRestoring_Nm']>0 for r in recovery)
    result.update(routeProfile=route_profile,profileSampledStaticScreensPass=bool(common and min(west[:3])>=-1e-4 and (not requires_east or min(trip[:3])>=-1e-4)))
    print('REPLAY',name,result['sampledStaticScreensPass'],'struct',min(margins.items(),key=lambda a:a[1]),'route',trip,'operating',operating,flush=True)
    return result


def run(names,budget,workers=3):
    if workers<1:raise ValueError('workers must be positive')
    if len(names)!=len(set(names)):raise ValueError('Duplicate sensitivity scenarios')
    saved=input_record('coupled-sizing-search.json')
    scenarios=input_record('coupled-uncertainty-inputs.json')
    sources=['build/analysis/coupled-sizing-search.json','build/analysis/coupled-uncertainty-inputs.json','tools/boat_analysis/optimization/replay.py','tools/boat_analysis/optimization/operating.py','tools/boat_analysis/model/vessel.py','tools/boat_analysis/model/operating.py']
    hashes=source_hashes(sources)
    completed={}
    with ProcessPoolExecutor(max_workers=min(workers,len(names))) as pool:
        futures={pool.submit(verify,name,saved['design'],saved['stateRows'],scenarios,budget,saved.get('routeProfile','all-season')):name for name in names}
        for future in as_completed(futures):
            name=futures[future];completed[name]=future.result()
            validate(hashes)
            report={'sourceHashes':hashes,'design':saved['design'],'scenarios':[completed[n] for n in names if n in completed],'geometryResolution':16,'operatingSolveBudgetPerPhase':budget,'qualified':False,'scope':'Refined static replay and provisional engineering sensitivities, not measured uncertainty or physical qualification. Sealed bodies; no retained-water, structural failure, wave dynamics, broadside/stall or dynamic capsize validation. No sailing-induced pitch moment in the quasi-steady operating balance.'}
            output_path('coupled-sizing-replay.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--scenarios',nargs='+',default=['nominal','construction','aerodynamic','hydrodynamic','energy','combined']);p.add_argument('--budget',type=int,default=35);p.add_argument('--workers',type=int,default=3);a=p.parse_args();run(a.scenarios,a.budget,a.workers)
