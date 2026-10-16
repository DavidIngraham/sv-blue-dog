"""Replay one allocated candidate through sensing, guidance, energy and recovery."""
import argparse
from copy import deepcopy
from dataclasses import asdict
from shapely.geometry import LineString,box
from ..model.runtime import ROOT,load_model,analysis_values
from ..evidence.records import input_record,source_hashes,validate
from .engine import simulate,Event
from .perception import Observations,SensorEnvelope
from .recovery import RecoveryPlanner,RecoverySite,RecoveryCapability
from .traffic import Traffic
from .integrated_sizing import sizing,save
from .integrated_acceptance import assess


def local_case(inputs,horizon,step=1):
    inputs=deepcopy(inputs);inputs['time'][:2]=[step,horizon/3600]
    inputs['gateNames']=['east','west','west','east'];inputs['gateDirections']=[-1,-1,1,1]
    inputs['gateApproachM']=40
    return inputs,LineString([(0,0),(-600,0)]),box(-1000,-350,400,350),dict(east=LineString([(0,150),(0,-150)]),west=LineString([(-600,150),(-600,-150)]))


def envelope(p,range_factor=1):
    return SensorEnvelope(p['sensorRangeM']*range_factor,p['sensorRangeM']*range_factor,p['weedRangeM']*range_factor,p['cooperativeRange'],p['samplePeriodS'],p['sensorLatencyS'],p['missProbability'],p['positionErrorM'],p['trackExpiryS'],1.)


def scenarios(record):
    validate(record['sourceHashes'])
    hashes=source_hashes(['build/analysis/integrated-sizing.json',*[x.relative_to(ROOT).as_posix() for x in (ROOT/'tools/boat_analysis/mission').glob('*.py')]])
    p={**analysis_values('BlueDogEncounterFeasibility::Inputs'),**record['allocation']};inputs=record['inputs'];args=local_case(inputs,p['horizonS'])
    planner=RecoveryPlanner(args[2],[RecoverySite('east recovery approach',(100,280),'hypothetical access; survey required','synthetic corridor'),RecoverySite('west recovery approach',(-700,280),'hypothetical access; survey required','synthetic corridor')],RecoveryCapability(*p['recoveryCapability']))
    actors=[None,Traffic('non-AIS crossing',LineString([(-200,-300),(-200,300)]),150,5,6,2,20),Traffic('low target',LineString([(-240,0),(-239,0)]),0,0,2,1,20,stationary_seconds=p['horizonS'],target_kind='low'),Traffic('weed patch',LineString([(-240,0),(-239,0)]),0,0,12,25,0,stationary_seconds=p['horizonS'],target_kind='weed')]
    def run(case,*,seed=17,night=False,actor=None,events=(),overrides=None,step=1,range_factor=1,weather=None):
        case_args=list(local_case(inputs,p['horizonS'],step))
        if overrides:case_args[0].update(overrides)
        if weather:case_args[0]['weather'][:3]=weather
        result=simulate(*case_args,traffic=[] if actor is None else [actor],events=events,recovery_planner=planner,
                        observations=Observations(envelope(p,range_factor),int(seed),night=night,clearance_allowance_m=p['error']),
                        recovery_observations=Observations(envelope(p),int(seed)+1000,night=night),save_every=30)
        row=dict(case=case,seed=int(seed),night=night,stepSeconds=step,**asdict(result))
        print(case,seed,night,result.outcome,result.cause,result.elapsed_seconds,flush=True)
        return row
    rows=[run('clear' if actor is None else actor.name,seed=seed,night=night,actor=actor)
          for seed in p['seeds'] for night in (False,True) for actor in actors]
    for wind in inputs['performance']['winds']:
        rows.append(run('clear',weather=[270,wind,.4]));rows[-1]['windMps']=wind
    casualties=[run(kind,events=[Event(30,kind)]) for kind in ('sensing_loss','steering_loss','power_loss','capsize')]
    exposure=record['replay']['concept']['passageHours']
    bank=load_model().calc('BlueDogIntegratedCandidate::RecoveryBankAfterExposure',arguments=[exposure]).value
    coverage=[]
    for inverted in (False,True):
        for x in (40,-300,-640):
            for y in (-150,0,150):
                plan=planner.plan((x,y),(-.4,0),inverted)
                coverage.append(dict(position=[x,y],inverted=inverted,reserveWh=None if plan is None else float(plan.reserve_wh),destination=None if plan is None else plan.site.name,passCheck=bool(plan is not None and bank>=plan.reserve_wh)))
    casualties.extend(run('end-exposure '+kind,events=[Event(0,kind)],overrides={'recoveryBatteryWh':max(0.,bank)}) for kind in ('power_loss','capsize'))
    refined=[run('clear',step=.5),run('weed patch',actor=actors[-1],step=.5)]
    negatives=[run('shared power failure',events=[Event(30,'power_loss')],overrides={'independentRecovery':False}),
               run('empty recovery bank',events=[Event(0,'power_loss')],overrides={'recoveryBatteryWh':0}),
               run('short-range weed sensing',actor=actors[-1],range_factor=.1)]
    report=dict(identifier=p['identifier'],sizing=record,missions=rows,casualties=casualties,refinement=refined,negativeControls=negatives,primaryClearanceAllowanceM=p['error'],
                recoveryCoverage=dict(exposureHours=exposure,remainingWh=bank,currentMps=[-.4,0],samples=coverage,passed=all(c['passCheck'] for c in coverage),scope='Sampled positions in the synthetic gate corridor; not continuous or Gorge coverage'),
                physicalQualification=False,
                assumptions=[
                    'Allocated 750 m craft/low-target and 40 m weed acquisition by day/night, 1 s latency, 10 percent independent misses, 5 m position error and 8 W additional bus demand are simultaneous hypotheses, not measured equipment performance.',
                    'Separate recovery power, thrust, control and observations survive the injected primary-path fault; common environmental damage remains unqualified.',
                    'Primary guidance adds the native 10 m relative-position allowance as a recovery-handoff buffer. Backup routes use delivered tracks and retain the current destination when its predicted route remains clear; otherwise they select an available alternative. Recovery uses point-mass current compensation, not measured finite-turn dynamics.',
                    'Recovery approaches, upright/inverted authority and retention are hypotheses; approach arrival is not physical capture. Primary sailing load shuts down on abort.',
                    'Averaged-tack performance omits resolved tacks and wave dynamics. Static nominal passage energy and local chronological replay have distinct scopes.',
                    'Equipment uses lumped mass and installation volume; measured placement, cable losses, surge, startup and thermal behavior remain unresolved.',
                    'The main pack retains its legacy reserve in addition to the independent recovery bank; no reserve transfer or solar harvest is credited.',
                    'Recovery motor and essential powers are battery-side allocations; primary sailing bus demand applies its separate discharge efficiency. End-exposure cases initialize only the independent bank after standby, not a synthetic full-course voyage history.'
                ],physicalEvidenceNeeds=[
                    'Installed sensing, target truth, latency, mass, sustained/peak power and thermal measurements across target and lighting classes.',
                    'Measured sailing polars, swept maneuvers and command response in representative current and waves.',
                    'Primary fault isolation, backup startup/observations, upright/inverted thrust and power, and usable battery capacity.',
                    'Surveyed approaches, shore capture/retention, weighed assemblies, structural coupons and flotation/righting trials.'
                ],sourceHashes=hashes)
    report['acceptance']=assess(report)
    validate(hashes);save('integrated-mission.json',report)
    print(report['acceptance'],flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['sizing','missions','all'],default='all')
    parser.add_argument('--budget',type=int,default=35)
    parser.add_argument('--warm-start',help='Prior sizing JSON used only for initial operating guesses')
    a=parser.parse_args()
    record=sizing(a.budget,a.warm_start) if a.phase!='missions' else input_record('integrated-sizing.json')
    if a.phase!='sizing':scenarios(record)
