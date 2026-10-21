"""Fresh coupled sizing of the allocated integrated candidate."""
import json
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import numpy as np
from ..model.runtime import ROOT,analysis_values
from ..model.vessel import CoupledModel
from ..evidence.records import input_record,output_path,source_hashes,validate,digest,run_record
from ..optimization.replay import verify
from .engine import mission_inputs
from .candidate import configure


def save(name,record):
    output_path(name).write_text(json.dumps(record,indent=2,allow_nan=False,default=lambda x:x.item() if isinstance(x,np.generic) else (_ for _ in ()).throw(TypeError(type(x).__name__)))+'\n')


def named_configuration():
    """The complete design is a native named configuration, never archive overlays."""
    values=analysis_values('BlueDogIntegratedCandidate::Inputs')
    design=dict(zip(values['designNames'],values['designValues'],strict=True))
    if len(design)!=len(values['designNames']):
        raise ValueError('Named configuration has duplicate design properties')
    return values,design


def sizing(budget=35,warm_start=None):
    p,design=named_configuration()
    source=ROOT/'evidence/runs/2026-10-13-srr-readiness/srr-readiness.json'
    prior=run_record(source.parent,source.name)  # Initial operating guesses only; archive bytes are checked.
    scenarios=deepcopy(input_record('coupled-uncertainty-inputs.json'));model=CoupledModel()
    for name,value in zip(p['parameterNames'],p['parameterValues']):
        scenarios['values']['nominal'][model.c['parameterNames'].index(name)]=value
    initial=[case['state'][3:] for case in prior['refinedReplay']['cases']]
    seed_source=dict(path=source.relative_to(ROOT).as_posix(),sha256=digest(source),scope='Initial operating guesses only; complete design comes from BlueDogIC01::design')
    if warm_start:
        seed_path=Path(warm_start);seed=json.loads(seed_path.read_text())
        initial=[c['state'][3:] for c in seed['replay']['cases']]
        seed_source=dict(path=str(seed_path),sha256=digest(seed_path),scope='Initial guesses only; every state freshly solved')
    model.parameters=np.array(scenarios['values']['nominal'])
    physical=[design[n] for n in model.c['designNames']]
    geometry_check=model.at_state(physical,[model.operating_contract['windSpeeds'][0],1,1,*initial[0]],resolution=16)
    unsupported={k:v for k,v in geometry_check.items() if k.startswith('delftDomain') and int(k.removeprefix('delftDomain'))>=6 and v < -1e-4}
    if unsupported:
        raise ValueError(f'Candidate hull outside resistance geometry domain: {unsupported}')
    hashes=source_hashes(['tools/boat_analysis/mission/integrated_sizing.py','tools/boat_analysis/mission/candidate.py','tools/boat_analysis/mission/engine.py','tools/boat_analysis/optimization/replay.py','tools/boat_analysis/optimization/operating.py','tools/boat_analysis/model/vessel.py',source.relative_to(ROOT).as_posix(),'build/analysis/coupled-uncertainty-inputs.json','build/analysis/wing-polar-grid.json','build/analysis/wing-geometry.json'])
    replay=verify('nominal',design,initial,scenarios,budget,'challenge',workers=4)
    model.parameters=np.array(scenarios['values']['nominal'])
    _,mass,_,_=model.configuration(physical,0,resolution=16)
    inputs=configure(mission_inputs(),SimpleNamespace(model=model,context=model.operating_contract),dict(design=physical,rows=[c['outputs'] for c in replay['cases']],states=[c['state'][3:] for c in replay['cases']],mass=mass,concept=replay['concept']))
    inputs['performance']['validWinds']=[all(c['screenFeasible'] for c in replay['cases'][i:i+4]) for i in range(0,8,4)]
    for key in ('controlPeriodSeconds','commandLatencySeconds','planningHorizonSeconds','minimumSailingSpeedMps','depowerPenaltyM','crossTrackWeight','maneuverPenaltyM','recoveryStandbyW'):
        inputs[key]=p[key]
    inputs.update(captureGateCenters=True,progressGuidance=True,independentRecovery=p['independentRecoveryAssumed'],recoveryBatteryWh=p['recoveryDepartureWh'])
    inputs['time'][4]=p['maneuverSeconds'];inputs['energy'][5]=0.
    record=dict(identifier=p['identifier'],configuration='BlueDogIC01::design',inputs=inputs,allocation=p,design=design,mass=mass,replay=replay,physicalQualification=False,
                initialStates=initial,initialStateSource=seed_source,operatingSolveBudgetPerPhase=budget,sourceHashes=hashes)
    validate(hashes);save('integrated-sizing.json',record)
    print(json.dumps(dict(massKg=mass['totalMass'],staticPass=replay['profileSampledStaticScreensPass'],structure=replay['structure'],hours=replay['westerlyRoute'][5]),indent=2),flush=True)
    return record
