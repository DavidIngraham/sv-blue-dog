"""Bounded full-course encounter and casualty continuations; virtual evidence only."""
from collections import Counter
from dataclasses import asdict
import json
import numpy as np
from .encounter_study import scenario,targets,compact
from .engine import simulate,mission_inputs,Event
from .perception import Observations,SensorEnvelope
from .recovery import RecoveryPlanner,RecoverySite,RecoveryCapability,execute_drift,execute_recovery
from tools.boat_analysis.model.runtime import ROOT,load_model,analysis_values
from tools.boat_analysis.evidence.records import source_hashes,validate,output_path


def expanded(result):
    return dict(**compact(result),consequences=result.consequence_summary,timing=result.timing_trace,
                completedCourse=result.cause=='ordered_gates_without_intervention',
                physicalTerminal=result.consequence_summary.get('termination') in ('shore_contact','drift_collision','recovery_collision') or result.cause in ('traffic_collision','weed_contact'))


def run():
    p=analysis_values('BlueDogEncounterFeasibility::Inputs');m=load_model()
    budget=analysis_values('BlueDogCandidateEnergy::Reconciliation');base=mission_inputs()
    base['energy'][:4]=[p['usableBatteryWh'],budget['departureWh'],budget['reserveWh'],budget['averageBusW']]
    base['continueAfterAbort']=True;base['commandLatencySeconds']=p['commandLatencyS']
    missions=[]
    for stack in (0,1):
        envelope=SensorEnvelope(p['craftRange'][stack],p['lowRange'][stack],p['weedRange'][stack],p['cooperativeRange'],p['samplePeriodS'],p['latency'][stack],p['missProbability'],p['positionErrorM'],p['trackExpiryS'],p['nightFactor'][stack])
        for control in p['controllerSweepS']:
            for night in (False,True):
                for actor in targets():
                    args=scenario(base,p['continuationHorizonS']);args[0]['controlPeriodSeconds']=control;args[0]['energy'][3]+=p['additionalBusW'][stack]
                    r=simulate(*args,traffic=[actor],observations=Observations(envelope,int(p['trialSeeds'][0]),night=night,dropouts=[(40,60)]))
                    missions.append(dict(stack=p['stacks'][stack],controlPeriodS=control,night=night,target=actor.name,**expanded(r)))
    casualties=[];args=scenario(base,p['continuationHorizonS'])
    planner=RecoveryPlanner(args[2],[RecoverySite('synthetic approach',(80.,300.),'not surveyed','straight water approach')],RecoveryCapability(*p['recoveryCapability']))
    for kind in ('sensing_loss','steering_loss','power_loss','capsize'):
        r=simulate(*args,events=[Event(0,kind)],recovery_planner=planner)
        casualties.append(dict(case=kind,**expanded(r)))
    # Failed powered attempts must expose their remaining drift trajectory too.
    for name,energy,flow in [('energy_depleted',2.01,(0.,0.)),('adverse_current',100.,(0.,-3.))]:
        r=execute_recovery(planner,(80.,0.),0.,energy,lambda p,t:flow,dt=1,horizon_seconds=p['continuationHorizonS'])
        d=execute_drift(args[2],r.position,r.seconds,r.energy_wh,lambda p,t:flow,dt=1,horizon_seconds=p['continuationHorizonS']-r.seconds,essential_w=planner.capability.essential_w)
        casualties.append(dict(case=name,recovery=asdict(r),consequences=asdict(d)))
    refinement=[]
    for dt in p['refinementStepS']:
        args=scenario(base,p['continuationHorizonS']);args[0]['time'][0]=dt;args[0]['controlPeriodSeconds']=1
        r=simulate(*args,events=[Event(0,'steering_loss')])
        refinement.append(dict(dt=dt,**expanded(r)))
    timing=[]
    for control in p['controllerSweepS']:
        for latency in p['latency'][:2]:
            distance=m.calc('BlueDogEncounterFeasibility::RequiredRange',arguments=[18,p['acquisition'],control+latency,p['commandLatencyS'],15,p['contingency'],30,p['error']]).value
            verdict=m.verify_requirement('BlueDogEncounterFeasibility::TimingCriterion',named_arguments={'assessmentPeriodS':control,'commandLatencyS':p['commandLatencyS']})
            timing.append(dict(assessmentPeriodS=control,sensorLatencyS=latency,requiredFastCraftM=float(distance),declaredScheduleCriterionHolds=verdict.holds))
    paths=[x.relative_to(ROOT).as_posix() for folder in ['tools/boat_analysis/mission','tools/boat_analysis/environment'] for x in (ROOT/folder).glob('*.py')]
    paths+=['tools/boat_analysis/model/runtime.py','tools/boat_analysis/evidence/records.py','uv.lock']
    hashes=source_hashes(paths);validate(hashes)
    report=dict(sourceHashes=hashes,inputs=p,missionInputs=base,missions=missions,casualties=casualties,refinement=refinement,timingEnvelope=timing,
        outcomeCounts=dict(Counter(r['cause'] for r in missions)),evidenceType='virtual',physicalQualification=False,measuredInstallations=[],
        scope='Synthetic corridor, conceptual polar, two hypothetical stacks, seed 17, day/night, 30/1 s assessment, 2 s command delivery, 15 s maneuver; 3600 s bounded continuation. Course completion and physical terminal events are explicit; all other trajectories remain censored. Current-only casualty drift excludes windage, wave and capsize dynamics. No installed measurements, sensor selection, coupled resizing or physical qualification.')
    output_path('encounter-continuation.json').write_text(json.dumps(report,indent=2,allow_nan=False,default=lambda x:x.item() if isinstance(x,np.generic) else (_ for _ in ()).throw(TypeError(type(x).__name__)))+'\n')
    print(json.dumps(dict(missions=len(missions),outcomes=report['outcomeCounts'],courseCompleted=sum(r['completedCourse'] for r in missions),physicalTerminal=sum(r['physicalTerminal'] for r in missions),timing=timing,casualties=[dict(case=c['case'],termination=c['consequences'].get('termination')) for c in casualties]),indent=2))
    return report

if __name__=='__main__':run()
