"""Reproduce the SRR desktop basis and replay the retained design on current inputs."""
import argparse
import json
import subprocess
import numpy as np
from .records import source_hashes, validate, output_path
from ..model.runtime import ROOT, native, native_value
from ..environment.routing import build, rounding_paths


def run(budget=10, battery_wh=None, beam_m=None):
    source=ROOT/'evidence/runs/2026-10-13-srr-frontier/srr-candidate-replay.json'
    paths=[p.relative_to(ROOT).as_posix() for p in (ROOT/'tools/boat_analysis').rglob('*.py')]
    paths += [source.relative_to(ROOT).as_posix(),'evidence/course/2026-10-11/chart-features.geojson',
              'build/analysis/coupled-uncertainty-inputs.json','build/analysis/wing-polar-grid.json',
              'build/analysis/wing-geometry.json','uv.lock']
    hashes=source_hashes(paths)
    report={'sourceHashes':hashes,'sourceRevision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'physicalQualification':False,'srrApproved':False,'analyses':{}}
    for name in ('BlueDogEnvironmentReview::FetchSensitivity','BlueDogEncounterReview::Acquisition','BlueDogRecoveryRisk::Sensitivity'):
        result=json.loads(native('-analysis',name,'-json'))
        if result['status']!='holds':raise ValueError(name+' did not evaluate')
        report['analyses'][name]={v['name']:native_value(v['value']) for v in result['checks'][0]['values']}
    course,water,groups,gates,route=build()
    paths=rounding_paths(water,gates,route,course['routing'][4])
    report['course']={'circuitM':sum(p.length for p in paths),'gateClear':all(water.covers(g) for g in gates.values()),
        'pathsClear':all(water.covers(p) for p in paths),'selectedSpan':course['bridgeSpanIdentifier'],
        'bothLegsUseSelectedSpan':all(p.intersects(groups['SELECTED_BRIDGE_SPAN']) for p in (paths[0],paths[-1])),
        'avoidUnassessedSpans':all(not p.intersects(groups['BRIDGE_EXCLUSIONS']) for p in paths)}
    print('Desktop basis evaluated',flush=True)
    from ..optimization.search import Problem
    from ..optimization.replay import verify
    from .records import input_record
    old=json.loads(source.read_text())
    problem=Problem()
    z=np.array(old['normalizedDesignAndStates'])
    if battery_wh is not None:
        index=problem.model.c['designNames'].index('battery_Wh')
        z[index]=(battery_wh-problem.lo[index])/problem.span[index]
        if not 0 <= z[index] <= 1:raise ValueError('Battery capacity outside modeled bounds')
    if beam_m is not None:
        index=problem.model.c['designNames'].index('beam_m')
        z[index]=(beam_m-problem.lo[index])/problem.span[index]
        if not 0 <= z[index] <= 1:raise ValueError('Hull beam outside modeled bounds')
    coarse=problem.evaluate(z)
    report['coarseReplay']={'feasible':bool(problem.feasible(z)),'minimumMargin':float(min(coarse['ineq'])),
        'maxResidual':float(max(abs(coarse['eq']))),'massKg':float(coarse['mass']['totalMass']),
        'conditionalPassageHours':float(coarse['westerlyRoute'][5]),'concept':coarse['concept']}
    print('Coarse retained-design replay complete',flush=True)
    physical=problem.lo+z*problem.span
    design=dict(zip(problem.model.c['designNames'],physical[:29]))
    states=physical[29:].reshape(8,6).copy()
    for state,(_,_,tack) in zip(states,problem.env):state[1:]*=tack
    report['design']=design
    report['batteryCapacityOverrideWh']=battery_wh
    report['beamOverrideM']=beam_m
    report['refinedReplay']=verify('nominal',design,states,input_record('coupled-uncertainty-inputs.json'),budget,'challenge')
    report['scope']='Current-requirement replay of the retained geometry with the recorded battery capacity and hull beam, not a new optimization or physical verification. Traffic and recovery sensitivities are hypotheses, not measured probabilities. Site selection is desktop evidence; no operational recovery destination is released.'
    validate(hashes)
    output_path('srr-readiness.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--budget',type=int,default=10)
    parser.add_argument('--battery-wh',type=float,help='Replay a changed battery capacity including mass, packaging and operating equilibrium')
    parser.add_argument('--beam-m',type=float,help='Replay revised hull beam with displacement and structural effects')
    args=parser.parse_args()
    if args.budget<1:parser.error('Positive replay budget required')
    run(args.budget,args.battery_wh,args.beam_m)
