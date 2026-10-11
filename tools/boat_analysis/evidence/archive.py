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
    files = sorted(WORK.glob('*.json'))
    required = {'coupled-sizing-search.json', 'coupled-sizing-replay.json', 'coupled-recovery.json',
                'coupled-pitch-diagnostic.json', 'hull-resistance-domain.json', 'wing-convergence.json', 'wing-candidate-check.json'}
    if not required.issubset({p.name for p in files}):
        raise ValueError('Incomplete run: ' + str(required - {p.name for p in files}))
    replay = json.loads((WORK / 'coupled-sizing-replay.json').read_text(encoding='utf-8'))
    scenarios = [case['scenario'] for case in replay['scenarios']]
    if len(scenarios) != 6 or set(scenarios) != {'nominal', 'construction', 'aerodynamic', 'hydrodynamic', 'energy', 'combined'}:
        raise ValueError('Replay has not completed all six scenarios')
    search = json.loads((WORK / 'coupled-sizing-search.json').read_text(encoding='utf-8'))
    if search.get('resumed') and digest(WORK / 'optimizer-start.json') != search['resumeCheckpointSha256']:
        raise ValueError('The original resumed checkpoint must be retained as optimizer-start.json')
    with tempfile.TemporaryDirectory() as temporary:
        staged = Path(temporary)
        entries = {}
        for path in files:
            shutil.copyfile(path, staged / path.name)
            entries[path.name] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        manifest = {'sourceRevision': revision, 'files': entries, 'qualified': False,
                    'scope': 'Conservative primary sizing and six-scenario replay; provisional aerodynamic assumptions, not measured confidence bounds.'}
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
