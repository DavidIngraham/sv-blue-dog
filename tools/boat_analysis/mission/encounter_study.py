"""Paired observation/energy and casualty hypotheses, not hardware selection."""
import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
from shapely.geometry import LineString, box
from tools.boat_analysis.model.runtime import ROOT, load_model, analysis_values
from tools.boat_analysis.evidence.records import source_hashes, validate, output_path
from .engine import simulate, mission_inputs, Event
from .perception import Observations, SensorEnvelope
from .traffic import Traffic
from .recovery import RecoveryPlanner, RecoverySite, RecoveryCapability


def scenario(inputs, horizon):
    inputs = deepcopy(inputs)
    inputs['time'][0] = 1.
    inputs['time'][1] = horizon/3600
    inputs['gateNames'] = ['eastGate','westGate','westGate','eastGate']
    inputs['gateDirections'] = [-1,-1,1,1]
    inputs['energy'][5] = 0.  # No solar credit in bounded comparison.
    return inputs, LineString([(0,0),(-1000,0)]), box(-1500,-500,500,500), {
        'eastGate':LineString([(0,100),(0,-100)]),
        'westGate':LineString([(-1000,100),(-1000,-100)])}


def targets():
    return [
        Traffic('oncoming equipped tow',LineString([(-400,0),(500,0)]),0,3.5,180,24,50,ais_equipped=True),
        Traffic('fast crossing non-AIS craft',LineString([(-80,-900),(-80,900)]),0,15,30,3,30),
        Traffic('low-profile drifting target',LineString([(-80,0),(-79,0)]),0,0,2,1,20,stationary_seconds=3600,target_kind='low'),
        Traffic('weed patch across local corridor',LineString([(-80,0),(-79,0)]),0,0,20,160,0,stationary_seconds=3600,target_kind='weed'),
        Traffic('reversing craft',LineString([(-100,-150),(-100,150),(-100,-150)]),0,5,8,3,20),
    ]


def compact(result):
    return dict(outcome=result.outcome,cause=result.cause,seconds=result.elapsed_seconds,
                minimumEnergyWh=result.minimum_energy_wh,recovery=result.recovery_summary,
                observations={k:v for k,v in result.observation_summary.items() if k!='trace'},
                observationTrace=result.observation_summary.get('trace',[]),
                logicTrace=result.logic_trace,history=result.history)


def run():
    paths=[p.relative_to(ROOT).as_posix() for folder in ['tools/boat_analysis/mission','tools/boat_analysis/environment'] for p in (ROOT/folder).glob('*.py')]
    paths += ['tools/boat_analysis/model/runtime.py','tools/boat_analysis/model/install.py','tools/boat_analysis/evidence/records.py','uv.lock']
    hashes=source_hashes(paths)
    model=load_model(); p=analysis_values('BlueDogEncounterFeasibility::Inputs')
    base=mission_inputs(); budget=analysis_values('BlueDogCandidateEnergy::Reconciliation')
    base['energy'][:4]=[p['usableBatteryWh'],budget['departureWh'],budget['reserveWh'],budget['averageBusW']]
    ranges=[]
    for target,speed,separation in zip(p['targets'],p['speeds'],p['separations']):
        for maneuver in p['maneuverSweep']:
            for processing in p['processingSweep']:
                value=model.calc('BlueDogEncounterFeasibility::RequiredRange',arguments=[speed+p['ownSpeed'],p['acquisition'],processing,p['command'],maneuver,p['contingency'],separation,p['error']]).value
                ranges.append(dict(target=target,maneuverS=maneuver,processingS=processing,requiredM=float(value),withinAllocation=float(value)<=p['rangeAllocation']))
    stacks=[]; records=[]
    for i,name in enumerate(p['stacks']):
        extra=p['additionalBusW'][i]
        remaining=float(model.calc('BlueDogEncounterFeasibility::EnergyScreen',arguments=[extra]).value)
        envelope=SensorEnvelope(p['craftRange'][i],p['lowRange'][i],p['weedRange'][i],p['cooperativeRange'],p['samplePeriodS'],p['latency'][i],p['missProbability'],p['positionErrorM'],p['trackExpiryS'],p['nightFactor'][i])
        stacks.append(dict(name=name,envelope=asdict(envelope),additionalBusW=extra,remainingHeadroomWh=remaining,energyScreenPass=remaining>=0,hardwareSelected=False))
        for night in (False,True):
            for seed in p['trialSeeds']:
                for actor in targets():
                    args=scenario(base,p['trialHorizonS']);args[0]['energy'][3]+=extra
                    provider=Observations(envelope,int(seed),night=night,dropouts=[(40,60)])
                    result=simulate(*args,traffic=[actor],observations=provider,save_every=10)
                    records.append(dict(stack=name,night=night,seed=int(seed),target=actor.name,**compact(result)))
    # Same geometry and control with a truth baseline; no stochastic perception.
    baselines=[]
    for actor in targets():
        baselines.append(dict(target=actor.name,**compact(simulate(*scenario(base,p['trialHorizonS']),traffic=[actor]))))
    args=scenario(base,p['trialHorizonS']);args[0]['time'][1]=1.
    water=args[2];site=RecoverySite('synthetic lateral approach',(80.,300.),'hypothesis only; not a surveyed site','synthetic straight water approach')
    capability=RecoveryCapability(*p['recoveryCapability'])
    planner=RecoveryPlanner(water,[site],capability)
    casualties=[]
    for kind in ['sensing_loss','steering_loss','power_loss','capsize']:
        blockers=[Traffic('unseen craft on recovery path',LineString([(80,150),(81,150)]),0,0,20,30,0,stationary_seconds=3600)] if kind=='sensing_loss' else []
        result=simulate(*deepcopy(args),events=[Event(0,kind)],traffic=blockers,recovery_planner=planner)
        casualties.append(dict(case=kind,**compact(result)))
    from .recovery import execute_recovery
    for name,energy,flow in [('energy_depleted',2.01,(0.,0.)),('adverse_current',100.,(0.,-3.))]:
        result=execute_recovery(planner,(80.,0.),0.,energy,lambda point,t:flow)
        casualties.append(dict(case=name,**asdict(result)))
    target_truth=[dict(name=a.name,track=list(a.track.coords),startSeconds=a.start_seconds,speedMps=a.speed_mps,lengthM=a.length_m,beamM=a.beam_m,clearanceM=a.clearance_m,stationarySeconds=a.stationary_seconds,kind=a.target_kind,aisEquipped=a.ais_equipped) for a in targets()]
    report=dict(targetTruth=target_truth,sourceHashes=hashes,inputs=p,missionInputs=base,rangeSweep=ranges,stacks=stacks,missions=records,
                perfectBaselines=baselines,casualties=casualties,
                outcomeCounts=dict(Counter(r['cause'] for r in records)),evidenceType='virtual',physicalQualification=False,
                scope='Synthetic local corridor, conceptual polar, retained-candidate energy only; 120 s encounters with 30 s controller and 15 s maneuver. Not a full Gorge replay, correlated sensor benchmark, reoptimization, statistical reliability estimate or recovery-site approval. No credited hydrophone range uplift; forward-sonar hypothesis affects weeds only. Scenario horizon means censoring, not success.')
    validate(hashes)
    output_path('encounter-feasibility.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(rangeCases=len(ranges),missionCases=len(records),outcomes=report['outcomeCounts'],stacks=stacks,casualties=[dict(case=c['case'],outcome=c.get('recovery',{}).get('outcome',c['outcome'])) for c in casualties]),indent=2))
    return report


if __name__=='__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    run()
