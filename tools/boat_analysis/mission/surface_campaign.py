"""Paired fixed-candidate wind-shear and wave sensitivity mission replay.

Run after `python -m tools.boat_analysis.cli prepare`. This does not resize the
boat or claim a new feasible sizing baseline. Run records retain unsupported
operating cases rather than silently using their unequilibrated velocities.
"""
import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from ..evidence.continuation import compatible_stages
from ..evidence.records import run_record,source_hashes,validate,input_path
from ..model.runtime import ROOT
from ..model.surface import SurfaceOperation,policy_inputs
from ..model.vessel import CoupledModel
from ..optimization.operating import solve_state
from ..environment.routing import build
from ..environment.trajectories import WeatherHistory
from .candidate import configure
from .campaign import traffic_scenarios
from .engine import Event,simulate

SCOPE=('Eight-strip neutral wind profile with bounded local finite-wing coefficients; '
       'fixed geometry, quasi-steady force balance and fixed-pitch hydrostatics. '
       'No lifting-line redistribution, viscous stall, dynamic recovery or seakeeping qualification.')


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def operating(stage,policy,budget,resolution,original_inputs):
    model=CoupledModel();original=model.operation
    surface=SurfaceOperation(model.operating_contract,model.polar,policy['wind'])
    design=[stage['design'][n] for n in model.c['designNames']]
    cases=[];uniform=[];uniform_cases=[]
    for index,(wind,up,tack) in enumerate((w,u,t) for w in model.operating_contract['windSpeeds'] for u in (True,False) for t in (1,-1)):
        state=stage['stateRows'][index]
        model.operation=original
        uniform.append(model.at_state(design,np.r_[wind,int(up),1,state],resolution=resolution,pitch_equilibrium=False))
        uniform_cases.append(solve_state(model,design,wind,up,budget,tack,resolution,state,pitch_equilibrium=False))
        model.operation=surface
        row=solve_state(model,design,wind,up,budget,tack,resolution,state,pitch_equilibrium=False)
        cases.append(row)
        print(f"{stage['lengthM']}m U10={wind} up={up} tack={tack} supported={row['screenFeasible']} VMG={row['outputs']['waterVMG']:.3f}",flush=True)
    outputs=[r['outputs'] for r in cases];states=[r['state'][3:] for r in cases]
    result=dict(design=design,rows=outputs,states=states,mass=stage['mass'],concept=stage['concept'])
    inputs=configure(original_inputs,SimpleNamespace(model=model,structure=original),result)
    inputs['performance'].update(validWinds=[all(c['screenFeasible'] for c in cases[i:i+4]) for i in range(0,len(cases),4)],scope=SCOPE)
    waterline=max(r['waterline_m'] for r in outputs);d=stage['design']
    inputs['surfaceEnvironment']=dict(seaPolicy=policy['sea'],winds=model.operating_contract['windSpeeds'],
        calmResistanceN=[float(np.mean([r['resistance'] for r in outputs[i:i+4]])) for i in range(0,len(outputs),4)],
        geometry=[d['length_m'],d['beam_m'],d['deck_height_m']-waterline,d['deck_height_m']-waterline,
                  waterline+d['bottom_depth_m']+min(d['keel_span_m'],d['rudder_span_m'])])
    uniform_result=dict(result,rows=[r['outputs'] for r in uniform_cases],states=[r['state'][3:] for r in uniform_cases])
    uniform_inputs=configure(original_inputs,SimpleNamespace(model=model,structure=original),uniform_result)
    uniform_inputs['performance']['validWinds']=[all(c['screenFeasible'] for c in uniform_cases[i:i+4]) for i in range(0,len(cases),4)]
    return dict(lengthM=stage['lengthM'],design=d,cases=cases,uniformCases=uniform_cases,uniformInputs=uniform_inputs,uniformAtArchivedStates=uniform,inputs=inputs,
                geometryResolution=resolution,physicalQualification=False,scope=SCOPE)


def run(count=4,budget=25,resolution=12,destination=None,reuse=False):
    destination=Path(destination or ROOT/'build/analysis/surface-campaign');destination.mkdir(parents=True,exist_ok=True)
    source_run=ROOT/'evidence/runs/2026-10-12-finite-passage'
    archived=run_record(source_run,'mission-candidate.json')
    stages=[s for s in compatible_stages(source_run) if s['feasible']]
    selected=[stages[-1],stages[0]]
    policy=policy_inputs()
    paths=[p for p in (ROOT/'tools/boat_analysis').rglob('*.py') if '.venv' not in p.parts]
    paths += [ROOT/'uv.lock',ROOT/'evidence/course/2026-10-11/chart-features.geojson',ROOT/'evidence/course/2026-10-11/chart-extraction.json']
    paths += [source_run/'mission-candidate.json',input_path('wing-polar-grid.json', purpose='reference'),input_path('wing-geometry.json', purpose='reference')]
    ancestor=source_run;seen=set()
    while ancestor not in seen and (ancestor/'sizing-continuation.json').exists():
        seen.add(ancestor)
        paths.extend([ancestor/'manifest.json',ancestor/'sizing-continuation.json'])
        ancestor=ROOT/'evidence/runs'/run_record(ancestor,'sizing-continuation.json').get('seedRun','')
    hashes=source_hashes(paths)
    configurations=[]
    for stage in selected:
        path=destination/f"operating-{stage['lengthM']:.1f}.json"
        if reuse and path.exists():
            record=json.loads(path.read_text());validate(record['sourceHashes'])
        else:
            record=operating(stage,policy,budget,resolution,archived['inputs'])
            record['sourceHashes']=hashes;save(path,record)
        configurations.append(record)
    course,water,groups,gates,route=build()
    seeds=[s.generate_state(2).tolist() for s in np.random.SeedSequence(archived['seed']).spawn(count)]
    # Paired current 1.4m replay: identical weather and traffic draws in all arms.
    baseline=deepcopy(configurations[0]['uniformInputs'])
    shear=deepcopy(configurations[0]['inputs']);shear.pop('surfaceEnvironment')
    waves=deepcopy(configurations[0]['inputs'])
    from ..environment.motion import contact_points
    motion=deepcopy(waves);motion['surfaceEnvironment']['motionPolicy']=policy['motion']
    motion['surfaceEnvironment']['motionPoints']=contact_points(configurations[0]['design'],motion['surfaceEnvironment']['geometry'])
    variants={'uniform-calm':baseline,'shear-calm':shear,'shear-waves':waves,'shear-wave-motion':motion}
    campaigns={}
    for name,inputs in variants.items():
        records=[]
        for index,(weather_seed,traffic_seed) in enumerate(seeds):
            weather=WeatherHistory(inputs['weather'],inputs['time'][1],weather_seed)
            traffic=traffic_scenarios(inputs,route,water,groups,traffic_seed)
            result=simulate(inputs,route,water,gates,weather=weather,traffic=traffic,
                            events=[Event(6*3600,'communications_loss',2*3600)])
            record=asdict(result);record.update(index=index,weatherSeed=weather_seed,trafficSeed=traffic_seed)
            records.append(record)
            print(name,index,result.outcome,result.cause,round(result.elapsed_seconds/3600,2),flush=True)
            save(destination/(name+'.json'),dict(sourceHashes=hashes,inputs=inputs,results=records,completed=len(records)==count))
        campaigns[name]=dict(outcomes=dict(Counter(r['outcome'] for r in records)),
            voyages=[{k:v for k,v in r.items() if k not in ('history','surface_summary')} for r in records],
            surface=[{k:v for k,v in r['surface_summary'].items() if k!='samples'} for r in records])
    validate(hashes)
    report=dict(sourceHashes=hashes,policy=policy,count=count,seed=archived['seed'],campaigns=campaigns,
                fixedCandidates=[r['lengthM'] for r in configurations],physicalQualification=False,
                scope='Paired synthetic sensitivity. Both uniform and sheared wind arms re-solve controls at fixed archived geometry. No size optimization or calibrated completion probability.')
    save(destination/'summary.json',report)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--count',type=int,default=4);p.add_argument('--budget',type=int,default=25)
    p.add_argument('--resolution',type=int,default=12);p.add_argument('--output',type=Path)
    p.add_argument('--reuse',action='store_true')
    a=p.parse_args()
    if a.count<1 or a.budget<1 or a.resolution<4:p.error('Positive count/budget and resolution >=4 required')
    run(a.count,a.budget,a.resolution,a.output,a.reuse)
