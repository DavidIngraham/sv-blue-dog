"""Replay prescribed wave motion against archived fixed-geometry operating points."""
import argparse
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import json
import numpy as np
from ..model.runtime import ROOT
from ..model.surface import SurfaceOperation,policy_inputs,NativeCalculation
from ..model.vessel import CoupledModel
from ..environment.motion import MotionResponse,contact_points
from ..environment.routing import build
from ..environment.trajectories import WeatherHistory
from ..evidence.records import source_hashes
from .campaign import traffic_scenarios
from .engine import Event,simulate
from .surface_campaign import save


def run(destination,count=4):
    archive=ROOT/'evidence/runs/2026-10-13-surface-environment'
    source=json.loads((archive/'operating-1.4.json').read_text())
    waves=json.loads((archive/'shear-waves.json').read_text())
    policy=policy_inputs();m=CoupledModel()
    provider=SurfaceOperation(m.operating_contract,m.polar,policy['wind'])
    design=[source['design'][n] for n in m.c['designNames']]
    response=MotionResponse(policy['motion'])
    d=source['design'];geometry=source['inputs']['surfaceEnvironment']['geometry']
    points=contact_points(d,geometry)
    study_height,study_period=policy['motionSea']
    phase_results=[]
    for row in source['cases']:
        captured=[]
        class Capture:
            def __call__(self,**inputs):
                args=tuple(inputs[n] for n in ('design','parameters','state','aero','mass','hydro'))
                captured.append(args)
                return provider.evaluate(*args)
        m.operation=Capture()
        m.at_state(design,row['state'],resolution=source['geometryResolution'],pitch_equilibrium=False)
        args=captured[0];baseline=provider.evaluate(*args)
        for name,direction,gains in [(name,direction,gains) for name,direction in [('head',np.pi),('beam',np.pi/2),('following',0.)] for gains in [(0,0),(1,0),(1,1)]]:
            response=MotionResponse([*gains,*policy['motion'][2:]])
            # Controlled 0.4m Hs, 3s period, no current transformation.
            # Equivalent diagnostic regular-wave height 2Hs, not a spectrum.
            k=(2*np.pi/study_period)**2/9.80665;speed=row['state'][3]
            train=[(study_height,k,np.sqrt(9.80665*k)-k*speed*np.cos(direction),direction)]
            outputs=[provider.evaluate(*args,motion=pose) for pose,_ in response.samples(train)]
            phase_results.append(dict(wind=row['state'][0],heading=row['state'][4],sea=name,
                responseGains=list(gains),baselineDriveN=baseline['drive'],meanDriveN=float(np.mean([r['drive'] for r in outputs])),
                minDriveN=min(r['drive'] for r in outputs),maxDriveN=max(r['drive'] for r in outputs),
                unsupportedPhaseCount=int(sum(min(r['surfaceIncidenceMargin'],r['surfaceHeightMargin'])<0 for r in outputs)),
                **response.clearance(train,geometry,points)))
    save(destination/'phase-loads.json',dict(policy=policy['motion'],significantHeightM=study_height,periodS=study_period,results=phase_results))
    course,water,groups,gates,route=build();missions=[]
    for old in waves['results'][:count]:
        inputs=deepcopy(waves['inputs']);inputs['surfaceEnvironment']['motionPolicy']=policy['motion'];inputs['surfaceEnvironment']['motionPoints']=points
        weather=WeatherHistory(inputs['weather'],inputs['time'][1],old['weatherSeed'])
        traffic=traffic_scenarios(inputs,route,water,groups,old['trafficSeed'])
        result=simulate(inputs,route,water,gates,weather=weather,traffic=traffic,events=[Event(6*3600,'communications_loss',2*3600)])
        missions.append(dict(index=old['index'],weatherSeed=old['weatherSeed'],trafficSeed=old['trafficSeed'],
            previousContactScreenSeconds=old['surface_summary']['contactScreenSeconds'],**asdict(result)))
        print(old['index'],result.outcome,result.cause,result.surface_summary['contactScreenSeconds'],flush=True)
        save(destination/'missions.json',dict(inputs=inputs,results=missions))
    paths=[p for p in (ROOT/'tools/boat_analysis').rglob('*.py') if '.venv' not in p.parts]
    paths += [archive/'operating-1.4.json',archive/'shear-waves.json']
    from ..evidence.records import input_path
    paths += [input_path('wing-polar-grid.json'),input_path('wing-geometry.json')]
    save(destination/'summary.json',dict(sourceHashes=source_hashes(paths),sourceArchive=str(archive.relative_to(ROOT)),
        physicalQualification=False,phaseCases=len(phase_results),missionCount=len(missions),
        scope='Prescribed heave/pitch/roll and point velocity change phase loads and relative clearance. Mission speed remains the archived quasi-steady polar plus wave resistance; phase loads are not a re-solved dynamic VPP.'))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'build/analysis/wave-motion')
    parser.add_argument('--count',type=int,default=4)
    args=parser.parse_args()
    if not 1<=args.count<=4:parser.error('count must be 1 to 4 archived seeds')
    run(args.output,args.count)
