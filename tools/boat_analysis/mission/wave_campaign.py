"""Fixed-geometry coupled wave-averaged sailing and paired mission replay."""
import argparse
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
from ..hydrodynamics.response import ResponseTable
from ..hydrodynamics.bem import policy_inputs
from ..model.runtime import ROOT
from ..model.surface import SurfaceOperation,policy_inputs as surface_policy
from ..model.wave_performance import WaveAveragedOperation
from ..model.vessel import CoupledModel
from ..optimization.operating import solve_state
from ..evidence.records import source_hashes,validate,input_path
from ..environment.routing import build
from ..environment.trajectories import WeatherHistory
from .campaign import traffic_scenarios
from .engine import Event,simulate
from .surface_campaign import save


def mesh_check(coarse,refined):
    rows=[]
    for row in coarse.record['rows']:
        args=(row['period'],row['speed'],np.deg2rad(row['direction']))
        low=coarse.solve(*args)[0];high=refined.solve(*args)[0]
        error=float(np.linalg.norm(low-high)/max(np.linalg.norm(high),1e-8))
        rows.append(dict(period=row['period'],speed=row['speed'],direction=row['direction'],relativeResponseError=error))
    return dict(maximumRelativeResponseError=max(r['relativeResponseError'] for r in rows),cases=rows)


def run(destination,budget=8):
    p=policy_inputs();surface=surface_policy();archive=ROOT/'evidence/runs/2026-10-13-surface-environment'
    saved=json.loads((archive/'operating-1.4.json').read_text());oldmissions=json.loads((archive/'shear-waves.json').read_text())
    coarse=ResponseTable(json.loads((destination/'bem.json').read_text()))
    response=ResponseTable(json.loads((destination/'bem-refined.json').read_text()))
    mesh=mesh_check(coarse,response);response.compare_mesh(coarse);save(destination/'mesh-check.json',mesh)
    print('Mesh error',mesh['maximumRelativeResponseError'],flush=True)
    model=CoupledModel();original=model.operation;design=[saved['design'][n] for n in model.c['designNames']]
    period=p['periods'][1];height=p['settings'][1];baseline=[];nodes=[];cases=[]
    paths=[f for f in (ROOT/'tools/boat_analysis').rglob('*.py') if '.venv' not in f.parts]
    paths += [destination.resolve()/'bem.json',destination.resolve()/'bem-refined.json',ROOT/'uv.lock',archive/'operating-1.4.json',archive/'shear-waves.json',input_path('wing-polar-grid.json'),input_path('wing-geometry.json')]
    hashes=source_hashes(paths)
    model.operation=SurfaceOperation(model.operating_contract,model.polar,surface['wind'])
    for row in saved['cases']:
        current=model.at_state(design,row['state'],resolution=12,pitch_equilibrium=False)
        if max(abs(current[n]) for n in model.operating_contract['outputNames'][:4])>1e-4:
            raise ValueError('Archived calm state no longer equilibrates')
        baseline.append(dict(row,outputs=current))
    for direction in p['directions']:
        for wind in model.operating_contract['windSpeeds']:
            calm=[r for r in baseline if r['wind_m_s']==wind]
            for wave_height in (0.,height):
                rows=[]
                for old in calm:
                    if wave_height==0:rows.append(old);continue
                    model.operation=WaveAveragedOperation(model.operating_contract,model.polar,surface['wind'],response,height,period,np.deg2rad(direction),resistance_coefficient=surface['sea'][2])
                    solved=solve_state(model,design,wind,old['windward'],budget,old['tack'],12,old['state'],pitch_equilibrium=False)
                    # Independently double phase resolution at the selected state.
                    provider=model.operation;provider.phases*=2
                    fine=model.at_state(design,solved['state'],resolution=12,pitch_equilibrium=False)
                    provider.phases//=2
                    error=max(abs(fine[n]-solved['outputs'][n])/max(abs(fine[n]),1.) for n in ('drive','resistance','heeling','averagePower'))
                    refined_equilibrium=max(abs(fine[n]) for n in model.operating_contract['outputNames'][:4])
                    solved.update(waveHeightM=height,wavePeriodS=period,waveWindAngleDeg=direction,
                        phaseRelativeError=float(error),refinedBalanceResidual=float(refined_equilibrium),
                        numericalSupport=bool(solved['screenFeasible'] and error<=p['settings'][9] and refined_equilibrium<=1e-3 and fine['waveCoverageMargin']>=0 and fine['profileFailures']==0 and fine['incidenceFailures']==0))
                    rows.append(solved);cases.append(solved)
                    print('Sailing',direction,wind,old['windward'],old['tack'],solved['numericalSupport'],solved['outputs']['waterVMG'],flush=True)
                    save(destination/'operating.json',dict(sourceHashes=hashes,solverBudget=budget,design=saved['design'],baseline=baseline,cases=cases,complete=False))
                points=[[0.,0.]]
                for row in rows:
                    state=row['state'];angle=np.deg2rad(state[4]+state[6]);points.append([state[3]*np.cos(angle),state[3]*np.sin(angle)])
                nodes.append(dict(wind=wind,height=wave_height,period=period,direction=direction,velocities=points,
                    powerW=max(r['outputs']['averagePower'] for r in rows),supported=all(r.get('numericalSupport',r['screenFeasible']) for r in rows)))
    table=dict(nodes=nodes,scope='Fixed 1.4 m cycle-averaged regular-wave sailing; averaged-tack envelope, bounded interpolation, linear response, no physical qualification.')
    save(destination/'performance.json',dict(sourceHashes=hashes,**table))
    save(destination/'operating.json',dict(sourceHashes=hashes,solverBudget=budget,design=saved['design'],baseline=baseline,cases=cases,complete=True))
    course,water,groups,gates,route=build();voyages=[]
    for old in oldmissions['results']:
        inputs=deepcopy(oldmissions['inputs']);inputs['wavePerformance']=table;inputs['performance']['scope']=table['scope']
        weather=WeatherHistory(inputs['weather'],inputs['time'][1],old['weatherSeed'])
        traffic=traffic_scenarios(inputs,route,water,groups,old['trafficSeed'])
        result=simulate(inputs,route,water,gates,weather=weather,traffic=traffic,events=[Event(6*3600,'communications_loss',2*3600)])
        voyages.append(dict(index=old['index'],weatherSeed=old['weatherSeed'],trafficSeed=old['trafficSeed'],**asdict(result)))
        print('Mission',old['index'],result.cause,result.elapsed_seconds,flush=True)
    validate(hashes)
    save(destination/'missions.json',dict(sourceHashes=hashes,inputs=inputs,results=voyages))
    save(destination/'summary.json',dict(sourceHashes=hashes,policy=p,solverBudget=budget,mesh=mesh,
        supportedCases=sum(r['numericalSupport'] for r in cases),totalCases=len(cases),
        supportedWaveNodes=sum(n['supported'] for n in nodes if n['height']>0),
        physicalQualification=False,missionCauses=[r['cause'] for r in voyages]))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'build/analysis/wave-performance');parser.add_argument('--budget',type=int,default=8)
    args=parser.parse_args();run(args.output,args.budget)
