"""Project a recorded continuation campaign into reviewable SysML evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from .records import ROOT, WORK, run_record, verify_run_sources, validate, source_hashes
from .projection import SECTIONS, projection_path, projection_package, check_projection, write_projection


def recover_target():
    """Finish an interrupted campaign only when its retained target passes afresh."""
    import numpy as np
    from ..optimization.search import Problem
    path = WORK/'sizing-continuation.json'
    record = json.loads(path.read_text())
    if record.get('completed'):
        raise ValueError('Campaign is already completed')
    validate(record['sourceHashes'])
    checkpoint = ROOT/'.tools/continuation-progress.json'
    saved = json.loads(checkpoint.read_text())
    if saved.get('bestFeasibleZ') is None:
        raise ValueError('No retained feasible point')
    p = Problem()
    z = np.array(saved['bestFeasibleZ'])
    length = float((p.lo+z*p.span)[0])
    if abs(length-record['targetM']) > 1e-9 or not p.feasible(z):
        raise ValueError('Retained point does not pass at the exact target length')
    r = p.evaluate(z)
    shutil.copyfile(path,WORK/'continuation-before-recovery.json')
    shutil.copyfile(checkpoint,WORK/'continuation-retained-checkpoint.json')
    record['attempts'].append(dict(lengthM=length,feasible=True,
        merit=float(np.linalg.norm(p.residual(z))),
        maxEquilibriumResidual=float(np.abs(r['eq']).max()),minimumMargin=float(r['ineq'].min()),
        worstConstraints=sorted(zip(p.constraint_names,map(float,r['ineq'])),key=lambda x:x[1])[:12],
        normalizedDesignAndStates=z.tolist(),design=dict(zip(p.model.c['designNames'],r['design'])),
        mass=r['mass'],westerlyRoute=r['westerlyRoute'].tolist(),
        history=[dict(method='retained checkpoint revalidation',
                      message='Stopped further restoration after the checkpoint had already retained a feasible target; all coarse checks recomputed in a fresh Problem.')]))
    record.update(completed=True,targetReached=True,smallestFeasibleLengthM=length,
                  smallestFeasibleZ=z.tolist(),completionMethod='retained checkpoint revalidation',
                  evaluationsAtCheckpoint=saved['calls'])
    record['sourceHashes'].update(source_hashes([
        'tools/boat_analysis/evidence/continuation.py',
        'build/analysis/continuation-before-recovery.json',
        'build/analysis/continuation-retained-checkpoint.json']))
    path.write_text(json.dumps(record,indent=2)+'\n')
    return record


def archive(name, revision, extras=(), snapshot=False):
    destination = ROOT/'evidence/runs'/name
    if not name or '/' in name or '\\' in name or name in ('.','..') or destination.exists():
        raise ValueError('Expected a new immutable run name')
    record = json.loads((WORK/'sizing-continuation.json').read_text())
    if not record['completed'] and not snapshot:
        raise ValueError('Continuation is still running')
    revision = subprocess.check_output(['git','rev-parse',revision],cwd=ROOT,text=True).strip()
    if any('/' in name or '\\' in name or name in ('.','..') for name in extras):
        raise ValueError('Expected workspace record filenames')
    pending = ['sizing-continuation.json', *extras]
    selected = set()
    while pending:
        filename = pending.pop()
        if filename in selected:
            continue
        selected.add(filename)
        data = json.loads((WORK/filename).read_text())
        pending += [path.split('/')[-1] for field in ('sourceHashes','driverHashes')
                    for path in data.get(field,{}) if path.startswith('build/analysis/')]
    with tempfile.TemporaryDirectory(dir=WORK) as temporary:
        from pathlib import Path
        staged = Path(temporary)
        files = {}
        for filename in sorted(selected):
            shutil.copyfile(WORK/filename,staged/filename)
            files[filename] = {'sha256':hashlib.sha256((staged/filename).read_bytes()).hexdigest()}
        (staged/'manifest.json').write_text(json.dumps(dict(sourceRevision=revision,files=files,
            qualified=False,completed=record['completed'],scope=('Interrupted exploration snapshot; unfinished trials are unresolved. ' if not record['completed'] else '')+record['scope']),indent=2)+'\n')
        verify_run_sources(staged)
        shutil.copytree(staged,destination)
    return destination


def compatible_stages(directory, seen=None):
    """Collect resumed stages only while the complete source model is identical."""
    directory=Path(directory)
    seen=set() if seen is None else seen
    if directory in seen:raise ValueError('Cyclic sizing seed history')
    seen.add(directory)
    record=run_record(directory,'sizing-continuation.json');stages=[]
    parent=ROOT/'evidence/runs'/record.get('seedRun','')
    if (parent/'sizing-continuation.json').exists():
        previous=run_record(parent,'sizing-continuation.json')
        models=lambda r:{k:v for k,v in r['sourceHashes'].items() if k.startswith('models/')}
        if models(record)==models(previous):stages.extend(compatible_stages(parent,seen))
    if record.get('seedRestoration'):stages.append(record['seedRestoration'])
    stages.extend(record['attempts'])
    return stages


def model_source(directory, package="BlueDog::Evidence::SizingContinuation"):
    package = projection_package(package)
    directory=Path(directory)
    record = run_record(directory, 'sizing-continuation.json')
    stages = record['attempts'] if package == 'BlueDog::Evidence::SizingContinuation' else compatible_stages(directory)
    lines = ['// Generated by tools.boat_analysis.evidence.continuation.',
             f"package {package.rsplit('::',1)[-1]} {{", '    private import ScalarValues::*;',
             '    doc /* Coarse fixed-length feasibility only; no refined replay or physical qualification.',
             '     * Hull length does not bound the full vessel footprint. Appendage geometry/model applicability,',
             '     * chronological voyage energy and free-pitch dynamic recovery require further assessment. */',
             '    part summary {',
             f'        attribute targetM : Real = {record["targetM"]};',
             f'        attribute smallestFeasibleM : Real = {record["smallestFeasibleLengthM"]};',
             f'        attribute targetReached : Boolean = {str(record.get("targetReached",False)).lower()};',
             '        attribute qualified : Boolean = false;', '    }']
    if package != 'BlueDog::Evidence::SizingContinuation':
        lines += [f'    attribute evidenceManifest : String = "evidence/runs/{directory.name}/manifest.json";']
        names=', '.join(json.dumps(f'{package}::stage{i}') for i in range(len(stages)))
        lines += [f'    attribute stageNames : String [*] ordered nonunique = ({names});']
    for i, attempt in enumerate(stages):
        lines += [f'    part stage{i} {{',
                  f'        attribute lengthM : Real = {attempt["lengthM"]};',
                  f'        attribute feasible : Boolean = {str(attempt["feasible"]).lower()};',
                  f'        attribute maximumResidual : Real = {attempt["maxEquilibriumResidual"]};',
                  f'        attribute minimumMargin : Real = {attempt["minimumMargin"]};',
                  '    }']
        if 'concept' in attempt:
            lines.pop()
            for name,value in [('massKg',attempt['mass']['totalMass']),('batteryWh',attempt['design']['battery_Wh']),('sweptLengthM',attempt['envelope']['sweptLengthM'])]:
                lines += [f'        attribute {name} : Real = {value};']
            lines += ['    }']
    chosen = next((a for a in reversed(stages) if a['feasible']), None)
    if chosen:
        lines += ['    part candidate : MarineDesign::Design {']
        lines += [f'        attribute :>> {k} = {v};' for k,v in chosen['design'].items()]
        lines += ['    }',
                  '    dependency basis from candidate to BlueDog::Decisions::Design::sizingBaseline;']
        if 'mass' in chosen:
            lines += ['    part assessment {',
                      f'        attribute massKg : Real = {chosen["mass"]["totalMass"]};',
                      f'        attribute westerlyHours : Real = {chosen["westerlyRoute"][-1]};',
                      '        attribute rudderChordM : Real = candidate.rudder_m2 / candidate.rudder_span_m;',
                      '        attribute rudderAspectRatio : Real = candidate.rudder_span_m * candidate.rudder_span_m / candidate.rudder_m2;',
                      '        attribute neutralHullRudderLengthM : Real = NumericalFunctions::max(candidate.length_m/2, -candidate.rudder_arm_fraction*candidate.length_m + rudderChordM/2) + NumericalFunctions::max(candidate.length_m/2, candidate.rudder_arm_fraction*candidate.length_m + rudderChordM/2);',
                      '        attribute qualified : Boolean = false;', '    }']
    if chosen and 'concept' in chosen:
        lines += ['    part passage {']
        for name,value in chosen['concept'].items():
            lines += [f'        attribute {name} : Real = {value};']
        lines += ['    }','    dependency energyBasis from passage to BlueDog::Analyses::Sizing::Credibility::passagePolicy;']
    if package != 'BlueDog::Evidence::SizingContinuation' and (directory/'concept-credibility.json').exists():
        review=run_record(directory,'concept-credibility.json')
        points=review['sealedRecovery']
        values={'recoverySamples':len(points),'missingPitchRoots':sum('error' in p for p in points),
                'unstablePitchSamples':sum(not p.get('pitch_stable',False) for p in points if 'error' not in p),
                'adverseRollSamples':sum(p.get('righting_Nm',0)*p.get('heel_deg',0)<=0 for p in points if 'error' not in p),
                'constructionWorstDeflectionMargin':min(v for k,v in review['constructionMaterialMargins'].items() if 'Deflection' in k)}
        lines += ['    part validation {']+[f'        attribute {k} : Real = {v};' for k,v in values.items()]+['    }',
                  '    dependency recoveryBasis from validation to BlueDog::Requirements::selfRighting;']
    if package != 'BlueDog::Evidence::SizingContinuation' and (directory/'mission-candidate.json').exists():
        mission=run_record(directory,'mission-candidate.json');results=mission['results']
        values={'scenarios':len(results),'virtualCompletions':sum(r['outcome']=='qualified_completion' for r in results),
                'coverageStops':sum(r['cause']=='performance_model_outside_coverage' for r in results),
                'minimumStoredWh':min(r['minimum_energy_wh'] for r in results),
                'protectedReserveWh':mission['inputs']['energy'][2]}
        lines += ['    part mission {']+[f'        attribute {k} : Real = {v};' for k,v in values.items()]+['    }',
                  '    dependency missionBasis from mission to BlueDog::Analyses::MissionSimulation::MissionOutcome;']
    lines += ['}']
    return '\n'.join(lines)+'\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--archive', action='store_true')
    parser.add_argument('--revision')
    parser.add_argument('--snapshot',action='store_true')
    parser.add_argument('--extra',action='append',default=[])
    parser.add_argument('--package',default='BlueDog::Evidence::SizingContinuation')
    parser.add_argument('--output', help='Legacy model projection path redirects to its canonical section; an output outside models exports a standalone leaf package')
    parser.add_argument('--recover-target', action='store_true')
    args = parser.parse_args()
    if args.recover_target:
        recover_target()
        raise SystemExit(0)
    if args.archive:
        if not args.revision:
            parser.error('--archive requires --revision')
        archive(args.run,args.revision,args.extra,args.snapshot)
        if args.snapshot:raise SystemExit(0)
    args.package = projection_package(args.package)
    content = model_source(ROOT/'evidence/runs'/args.run,args.package)
    section = next((key for key, package in SECTIONS.items() if package == args.package), None)
    destination = (ROOT/args.output).resolve() if args.output else projection_path()
    legacy = {ROOT/'models/evidence/sizing-continuation.sysml': 'sizing-continuation',
              ROOT/'models/evidence/finite-passage-sizing.sysml': 'finite-passage-sizing'}
    if destination == projection_path() and section not in ('sizing-continuation', 'finite-passage-sizing'):
        parser.error('--package must identify a declared continuation projection for the canonical model')
    if destination in legacy and legacy[destination] != section:
        parser.error('--output projection identity disagrees with --package')
    try:
        if destination == projection_path() or destination in legacy:
            if args.check:
                check_projection(section, content)
            else:
                write_projection(section, content)
        else:
            if destination.is_relative_to(ROOT/'models'):
                parser.error('Active project projections belong in models/blue-dog.sysml; standalone exports must be outside models')
            if args.check:
                if destination.read_text() != content:
                    raise ValueError('Stale standalone continuation evidence export: '+str(destination))
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content, encoding='utf-8')
    except ValueError as error:
        raise SystemExit(str(error)) from error
