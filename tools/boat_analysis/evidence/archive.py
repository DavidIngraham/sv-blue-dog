"""Freeze a completed analysis workspace, validating its source and input provenance."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from .records import ROOT, WORK, digest, verify_run_sources


def archive(name, revision):
    if not name or Path(name).name != name or name in ('.', '..'):
        raise ValueError('Expected a run directory name')
    destination = ROOT / 'evidence/runs' / name
    if destination.exists():
        raise ValueError('Archived runs are immutable: ' + str(destination))
    revision = subprocess.check_output(['git', 'rev-parse', revision], cwd=ROOT, text=True).strip()
    required = {'coupled-sizing-search.json', 'coupled-sizing-replay.json', 'coupled-recovery.json',
                'coupled-pitch-diagnostic.json', 'hull-resistance-domain.json'}
    # Archive the completed study and its transitive workspace inputs, not unrelated
    # mission runs or stale outputs left by a previous study.
    selected = set(required)
    pending = list(required)
    while pending:
        name = pending.pop()
        record = json.loads((WORK / name).read_text(encoding='utf-8'))
        for field in ('sourceHashes', 'driverHashes'):
            for dependency in record.get(field, {}):
                if dependency.startswith('build/analysis/'):
                    child = Path(dependency).name
                    if child not in selected:
                        selected.add(child)
                        pending.append(child)
    files = [WORK / name for name in sorted(selected)]
    replay = json.loads((WORK / 'coupled-sizing-replay.json').read_text(encoding='utf-8'))
    scenarios = [case['scenario'] for case in replay['scenarios']]
    if len(scenarios) != 6 or set(scenarios) != {'nominal', 'construction', 'aerodynamic', 'hydrodynamic', 'energy', 'combined'}:
        raise ValueError('Replay has not completed all six scenarios')
    search = json.loads((WORK / 'coupled-sizing-search.json').read_text(encoding='utf-8'))
    if search.get('resumed') and digest(WORK / 'optimizer-start.json') != search['resumeCheckpointSha256']:
        raise ValueError('The original resumed checkpoint must be retained as optimizer-start.json')
    if search.get('resumed'):
        files.append(WORK / 'optimizer-start.json')
    with tempfile.TemporaryDirectory(dir=WORK) as temporary:
        staged = Path(temporary)
        entries = {}
        for path in files:
            shutil.copyfile(path, staged / path.name)
            entries[path.name] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        manifest = {'sourceRevision': revision, 'files': entries, 'qualified': False,
                    'routeProfile': search.get('routeProfile', 'all-season'),
                    'requiresEastProgress': search.get('requiresEastProgress', True),
                    'energyConstraintScope': search.get('energyConstraintScope', 'See source model'),
                    'scope': 'Finite Gorge sizing and six-scenario replay; provisional aerodynamic assumptions, not measured confidence bounds.'}
        (staged / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        verify_run_sources(staged)
        shutil.copytree(staged, destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    print(archive(args.name, args.revision))
