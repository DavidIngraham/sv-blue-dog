"""Paired navigation-policy replay of frozen IC-01 scenarios; no resizing."""
import argparse
from copy import deepcopy
from dataclasses import replace
from collections import Counter
import json
from shapely.geometry import LineString
from ..model.runtime import ROOT
from ..evidence.records import run_record, source_hashes, validate, verify_run_sources
from .integrated import local_case, envelope
from .integrated_sizing import save
from .engine import simulate, Event
from .perception import Observations
from .traffic import Traffic
from .recovery import RecoveryPlanner, RecoverySite, RecoveryCapability
from .navigation import NavigationAssessment

ARCHIVE=ROOT/'evidence/runs/2026-10-15-integrated-candidate'
CONTEXT=dict(inlandProfile='yes',ownKind='sailing',ownExceptionalStatus='no',
    restrictedVisibility='no',channelContext='no',crossingChannel='no',proceedingAlongChannel='no',
    specialRiverRulesApply='no',unmodeledSpecialCircumstances='no')
ASSESSED_CONTEXT=dict(CONTEXT,lookoutAdequate='yes',safeSpeedSupported='yes')
ASSESSED_FACTS=dict(kind='power',inSight='yes',exceptionalStatus='no',underway='yes',
    observationsAdequate='yes',confinedToChannel='no',navigatingChannel='no',
    otherActionAppropriate='no',giveWayAloneSufficient='yes',
    source='Explicit sensitivity assumptions, including night visual identification and Rule 17 assessments; not inferred from scripted future motion')


def cases(record):
    for group in ('missions','casualties','refinement','negativeControls'):
        for index,row in enumerate(record[group]):
            yield group,index,row


def execute(record, group, index, row, mode):
    sizing=record['sizing'];p=sizing['allocation'];inputs=sizing['inputs']
    # Observation parameters frozen from the archived report/model allocation.
    p=dict(p,cooperativeRange=1500.,samplePeriodS=1.,missProbability=.1,positionErrorM=5.,trackExpiryS=10.,error=record['primaryClearanceAllowanceM'])
    args=list(local_case(inputs,p['horizonS'],row['stepSeconds']))
    args[0]['retainCurrentHeadingCandidate']=True
    args[0]['piecewiseTrafficForecast']=True
    case=row['case'];seed=row['seed'];night=row['night'];events=[]
    if 'windMps' in row:args[0]['weather'][:3]=[270,row['windMps'],.4]
    actors={'non-AIS crossing':Traffic('non-AIS crossing',LineString([(-200,-300),(-200,300)]),150,5,6,2,20),
            'low target':Traffic('low target',LineString([(-240,0),(-239,0)]),0,0,2,1,20,stationary_seconds=p['horizonS'],target_kind='low'),
            'weed patch':Traffic('weed patch',LineString([(-240,0),(-239,0)]),0,0,12,25,0,stationary_seconds=p['horizonS'],target_kind='weed')}
    actors['timed crossing']=replace(actors['non-AIS crossing'],name='timed crossing',start_seconds=280)
    actor=actors.get(case)
    if group=='casualties':
        end=case.startswith('end-exposure ');kind=case.removeprefix('end-exposure ')
        events=[Event(0 if end else 30,kind)]
        if end:args[0]['recoveryBatteryWh']=record['recoveryCoverage']['remainingWh']
    if case=='shared power failure':
        events=[Event(30,'power_loss')];args[0]['independentRecovery']=False
    if case=='empty recovery bank':
        events=[Event(0,'power_loss')];args[0]['recoveryBatteryWh']=0.
    if case=='short-range weed sensing':actor=actors['weed patch']
    if mode=='assessed' and actor is not None and actor.target_kind=='craft':
        actor=replace(actor,navigation_facts=ASSESSED_FACTS)
    planner=RecoveryPlanner(args[2],[RecoverySite('east recovery approach',(100,280),'hypothetical access; survey required','synthetic corridor'),
        RecoverySite('west recovery approach',(-700,280),'hypothetical access; survey required','synthetic corridor')],RecoveryCapability(*p['recoveryCapability']))
    navigation=None if mode=='baseline' else NavigationAssessment(assessed_context=ASSESSED_CONTEXT if mode=='assessed' else CONTEXT,label=mode)
    initial_main=args[0]['energy'][1];initial_recovery=args[0]['recoveryBatteryWh']
    result=simulate(*args,traffic=[] if actor is None else [actor],events=events,recovery_planner=planner,
        observations=Observations(envelope(p,.1 if case=='short-range weed sensing' else 1.),seed,night=night,
                                  clearance_allowance_m=p['error'],observe_navigation_facts=mode=='assessed'),
        recovery_observations=Observations(envelope(p),seed+1000,night=night),navigation=navigation,save_every=30)
    end=result.energy_summary
    output=dict(group=group,index=index,case=case,seed=seed,night=night,stepSeconds=row['stepSeconds'],mode=mode,
        outcome=result.outcome,cause=result.cause,elapsedSeconds=result.elapsed_seconds,distanceM=result.distance_m,
        mainUsedWh=initial_main-end['mainStoredWh'],recoveryUsedWh=initial_recovery-end['recoveryStoredWh'],
        minimumMainWh=result.minimum_energy_wh,clearanceViolated=bool(result.consequence_summary.get('truthClearanceViolated',False) or result.consequence_summary.get('clearance_violated',False)),
        collision=result.cause in ('traffic_collision','weed_contact') or bool(result.consequence_summary.get('collision',False)),
        recoveryOutcome=result.recovery_summary.get('outcome'),navigation=result.navigation_summary,
        history=result.history,crossings=result.crossings,events=result.events)
    print(mode,group,index,case,result.outcome,result.cause,round(result.elapsed_seconds,2),flush=True)
    return output


def main(modes=('baseline','unassessed','assessed'),limit=None):
    verify_run_sources(ARCHIVE)
    source=run_record(ARCHIVE,'integrated-mission.json')
    sources=[x.relative_to(ROOT).as_posix() for x in (ROOT/'tools/boat_analysis/mission').glob('*.py')]
    hashes=source_hashes([*sources,(ARCHIVE/'integrated-mission.json').relative_to(ROOT).as_posix()])
    rows=[]
    for group,index,row in list(cases(source))[:limit]:
        for mode in modes:rows.append(execute(source,group,index,row,mode))
    if limit is None:
        for index,(seed,night) in enumerate((s,n) for s in (17,29) for n in (False,True)):
            row=dict(case='timed crossing',seed=seed,night=night,stepSeconds=1)
            for mode in modes:rows.append(execute(source,'supplemental',index,row,mode))
    paired=[]
    for group,index,old in list(cases(source))[:limit]:
        selected={r['mode']:r for r in rows if r['group']==group and r['index']==index}
        baseline=selected.get('baseline')
        if baseline is None:continue
        for mode,row in selected.items():
            if mode=='baseline':continue
            paired.append(dict(group=group,index=index,case=row['case'],seed=row['seed'],night=row['night'],mode=mode,
                baselineOutcome=baseline['outcome'],outcome=row['outcome'],baselineCause=baseline['cause'],cause=row['cause'],
                deltaElapsedSeconds=row['elapsedSeconds']-baseline['elapsedSeconds'],
                deltaMainWh=row['mainUsedWh']-baseline['mainUsedWh'],deltaRecoveryWh=row['recoveryUsedWh']-baseline['recoveryUsedWh'],
                changedSelections=row['navigation'].get('changedSelections',0)))
    for baseline in [r for r in rows if r['group']=='supplemental' and r['mode']=='baseline']:
        for row in rows:
            if row['group']!='supplemental' or row['index']!=baseline['index'] or row['mode']=='baseline':continue
            paired.append(dict(group='supplemental',index=row['index'],case=row['case'],seed=row['seed'],night=row['night'],mode=row['mode'],
                baselineOutcome=baseline['outcome'],outcome=row['outcome'],baselineCause=baseline['cause'],cause=row['cause'],
                deltaElapsedSeconds=row['elapsedSeconds']-baseline['elapsedSeconds'],deltaMainWh=row['mainUsedWh']-baseline['mainUsedWh'],
                deltaRecoveryWh=row['recoveryUsedWh']-baseline['recoveryUsedWh'],changedSelections=row['navigation'].get('changedSelections',0)))
    summary={mode:dict(outcomes=dict(Counter(r['outcome'] for r in rows if r['mode']==mode)),
        nominalOutcomes=dict(Counter(r['outcome'] for r in rows if r['mode']==mode and r['group']=='missions')),
        supplementalOutcomes=dict(Counter(r['outcome'] for r in rows if r['mode']==mode and r['group']=='supplemental')),
        clearanceViolations=sum(r['clearanceViolated'] for r in rows if r['mode']==mode),
        collisions=sum(r['collision'] for r in rows if r['mode']==mode),
        changedSelections=sum(r['navigation'].get('changedSelections',0) for r in rows if r['mode']==mode)) for mode in modes}
    baseline_checks=[]
    for group,index,old in list(cases(source))[:limit]:
        row=next((r for r in rows if r['mode']=='baseline' and r['group']==group and r['index']==index),None)
        if row:baseline_checks.append(dict(group=group,index=index,sameOutcome=row['outcome']==old['outcome'],sameCause=row['cause']==old['cause'],deltaElapsedSeconds=row['elapsedSeconds']-old['elapsed_seconds'],deltaMinimumWh=row['minimumMainWh']-old['minimum_energy_wh']))
    report=dict(identifier='IC-01 navigation integration comparison',frozenSizingSource=str((ARCHIVE/'integrated-mission.json').relative_to(ROOT)),
        resized=False,physicalQualification=False,completeComplianceEstablished=False,
        hypotheses=dict(context=CONTEXT,assessedContext=ASSESSED_CONTEXT,assessedCraftFacts=ASSESSED_FACTS),
        scope=['Same 29 archived local scenarios and frozen candidate inputs, three policy modes; not the full Gorge route.',
               'Supplemental timed crossing shifts only target appearance from 150 to 280 seconds; two seeds and day/night, explicitly separate from the archived 29-case comparison.',
               'All three modes share the retained-heading candidate and piecewise latency/drift forecast, with archived-baseline differences recorded separately. Baseline geometric guidance; unassessed refuses unresolved applicable duties; assessed adds explicit hypothetical craft identification and response judgments only.',
               'Low target remains unclassified in both rule modes; weeds retain geometric avoidance.',
               'Averaged-tack course is used as a bow-heading proxy for bearing; this needs resolved rig/heading validation.',
               'No lights, signals, sensing hardware or power increment is invented. Rule 19, equipment, multi-vessel negotiation and powered recovery rule control remain unassessed.',
               'Elapsed time includes recovery after abort. Reduced time/energy from an earlier abort is not improved mission efficiency.',
               'Forecast uses delivered constant-velocity observations, the same finite planning horizon and same hypothetical point-mass maneuver model.'],
        summary=summary,paired=paired,baselineArchiveChecks=baseline_checks,runs=rows,sourceHashes=hashes)
    validate(hashes)
    save('navigation-integration.json',report)
    print(json.dumps(summary,indent=2),flush=True)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int)
    parser.add_argument('--modes',nargs='+',choices=['baseline','unassessed','assessed'],default=['baseline','unassessed','assessed'])
    args=parser.parse_args();main(tuple(args.modes),args.limit)
