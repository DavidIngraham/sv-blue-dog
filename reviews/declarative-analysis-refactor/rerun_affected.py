"""Rerun modules invalidated by native-service OOM in fresh serial processes."""
import json
import os
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

root = Path('/home/david/repos/sv-blue-dog-declarative')
original = ET.parse(root/'.tools/refactor-full-tests.xml').getroot().find('testsuite')
files = sorted({case.attrib['classname'].replace('.', '/')+'.py'
    for case in original.findall('testcase')
    if case.find('failure') is not None or case.find('error') is not None})
files = [path for path in files if path != 'tests/test_inline_views.py']
environment = dict(os.environ, GOMEMLIMIT='3GiB', GOGC='50')
results = []
for index, filename in enumerate(files):
    label = f'affected-{index:02d}-'+Path(filename).stem
    log, junit = root/'.tools'/f'{label}.log', root/'.tools'/f'{label}.xml'
    with log.open('w') as stream:
        result = subprocess.run([str(root/'.venv/bin/python'), '-m', 'pytest', filename,
            '--durations=10', f'--junitxml={junit}'], cwd=root, env=environment,
            stdout=stream, stderr=subprocess.STDOUT)
    suite = ET.parse(junit).getroot().find('testsuite')
    row = dict(file=filename, exitCode=result.returncode, junit=str(junit.relative_to(root)),
               log=str(log.relative_to(root)), **{name: suite.attrib[name]
                   for name in ('tests','failures','errors','skipped','time')})
    results.append(row)
    (root/'.tools/affected-reruns.json').write_text(json.dumps(dict(
        method='Fresh serial pytest process per affected module',
        environment={'GOMEMLIMIT':'3GiB','GOGC':'50'}, files=results), indent=2)+'\n')
    print(json.dumps(row), flush=True)
print('Affected modules complete', flush=True)
