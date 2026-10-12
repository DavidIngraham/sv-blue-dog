"""Fixed-design sensitivity and sealed-wing recovery diagnostics for a candidate."""
import argparse
import json
from pathlib import Path
import numpy as np
from .search import Problem
from ..model.runtime import ROOT
from ..evidence.records import validate,source_hashes
from ..geometry.hydro import free_pitch_equilibrium


def assess(candidate,destination=None):
    candidate=Path(candidate).resolve();record=json.loads(candidate.read_text());validate(record['sourceHashes'])
    hashes={**record['sourceHashes'],**source_hashes([candidate.relative_to(ROOT).as_posix(),'tools/boat_analysis/optimization/credibility.py'])}
    p=Problem();z=np.array(record['smallestFeasibleZ']);r=p.evaluate(z)
    if not p.feasible(z):raise ValueError('Candidate fails current nominal screens')
    sensitivities=[]
    nominal=p.structure.contract['conceptPolicy']
    for index,name in enumerate(['durationMultiplier','delayHours','batteryInstalledWhM3','equipmentInstalledKgM3','usableHullVolumeFraction']):
        for value in p.structure.contract['conceptSensitivity'][name]:
            policy=list(nominal);policy[index]=value
            _,m,g,_=p.model.configuration(r['design'],0,resolution=12)
            result=p.concept.evaluate(r['design'],list(m.values()),g,r['westerlyRoute'][5],max(row['averagePower'] for row in r['rows']),policy)
            sensitivities.append(dict(parameter=name,value=value,**result))
    aspect=[]
    original=p.structure.contract['structure'][10]
    _,m,g,_=p.model.configuration(r['design'],0,resolution=12)
    loads=[max(row[n] for row in r['rows']) for n in ['wingResultant','keelResultant','rudderResultant']]
    for ratio in p.structure.contract['conceptSensitivity']['minimumUnderwaterAspectRatio']:
        p.structure.contract['structure'][10]=ratio
        margins=p.structure.evaluate(r['design'],p.model.parameters,list(m.values()),g,loads,0.)
        aspect.append(dict(minimumAspectRatio=ratio,keel=margins['keelAspectMargin'],rudder=margins['rudderAspectMargin']))
    p.structure.contract['structure'][10]=original
    # Reuse the model's declared construction sensitivity at fixed geometry.
    from ..evidence.records import input_record
    uncertainty=input_record('coupled-uncertainty-inputs.json')
    hashes.update(source_hashes(['build/analysis/coupled-uncertainty-inputs.json']))
    parameters=np.array(uncertainty['values']['construction'])
    bodies,construction_mass,construction_geometry,_=p.model.configuration(r['design'],0,resolution=12)
    construction=p.structure.evaluate(r['design'],parameters,list(construction_mass.values()),construction_geometry,loads,0.)
    # Only material stiffness/strength margins are interpreted here; mass and
    # changed sailing equilibria require a fully re-solved uncertainty replay.
    material={n:v for n,v in construction.items() if 'Stress' in n or 'Deflection' in n}
    bounds=[dict(parameter=name,value=float(r['design'][i]),lower=float(p.lo[i]),upper=float(p.hi[i]))
            for i,name in enumerate(p.model.c['designNames']) if min(z[i],1-z[i])<1e-4]
    recovery=[]
    for trim in p.structure.contract['recoveryTrims']:
        bodies,m,_,_=p.model.configuration(r['design'],np.deg2rad(trim),resolution=16)
        for heel in p.structure.contract['conceptSensitivity']['recoveryProbeHeels']:
            try:
                state=free_pitch_equilibrium(p.model.hydro,bodies,[m['cgX'],m['cgY'],m['cgZ']],m['totalMass'],heel,density=p.model.parameters[31])
                recovery.append(dict(trimDeg=trim,**state))
            except ValueError as error:
                recovery.append(dict(trimDeg=trim,heel_deg=heel,error=str(error)))
        print('Recovery trim',trim,'complete',flush=True)
    validate(hashes)
    result=dict(sourceHashes=hashes,qualified=False,concept=r['concept'],sensitivity=sensitivities,aspectSensitivity=aspect,constructionMaterialMargins=material,nearSearchBounds=bounds,sealedRecovery=recovery,
                scope='Fixed-design one-at-a-time allocation sensitivity and sparse free-pitch static recovery. No reoptimization, dynamic recovery or physical qualification.')
    destination=Path(destination or ROOT/'build/analysis/concept-credibility.json');destination.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('candidate',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();assess(args.candidate,args.output)
