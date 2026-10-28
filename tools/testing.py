"""Run the configured regression inventory with a fresh native service per module."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = tomllib.loads((ROOT/'pyproject.toml').read_text())
    modules = []
    for name in config['tool']['pytest']['ini_options']['testpaths']:
        path = ROOT/name
        modules.extend(sorted(path.rglob('test_*.py')) if path.is_dir() else [path])
    if not modules or len(modules) != len(set(modules)):
        raise ValueError('Expected a nonempty, unique regression module inventory')
    output = ROOT/'build/test-results'
    output.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ)
    environment.setdefault('GOMEMLIMIT', '3GiB')
    environment.setdefault('GOGC', '50')
    results = []
    for module in modules:
        name = str(module.relative_to(ROOT))
        slug = name.removesuffix('.py').replace('/', '__')
        log_path = output/(slug+'.log')
        print('START '+name, flush=True)
        started = time.monotonic()
        with log_path.open('w') as log:
            try:
                result = subprocess.run([sys.executable, '-m', 'pytest', name, '-q',
                    '--durations=30', '--junitxml='+str(output/(slug+'.xml'))],
                    cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT,
                    timeout=1800)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
                log.write('\nModule exceeded the 1800 second execution limit.\n')
        row = dict(module=name, exitCode=code, seconds=round(time.monotonic()-started, 2))
        results.append(row)
        (output/'results.json').write_text(json.dumps(results, indent=2)+'\n')
        print(json.dumps(row), flush=True)
        if code:
            print('\n'.join(log_path.read_text().splitlines()[-80:]), flush=True)
    print('COMPLETE '+str(len(results)), flush=True)
    return int(any(row['exitCode'] for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
