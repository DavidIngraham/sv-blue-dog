"""Verify the task did not change the original pending source tree."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path('/home/david/repos/sv-blue-dog-declarative')
baseline = json.loads((root/'.tools/baseline-source.json').read_text())
source = Path(baseline['source'])
def git(*args):
    return subprocess.check_output(['git', '-C', str(source), *args]).decode()
changed = []
for name, expected in baseline['sourceHashes'].items():
    path = source/name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        changed.append(name)
status = git('status', '--porcelain=v1', '-z').split('\0')
report = dict(original=str(source), originalHead=git('rev-parse','HEAD').strip(),
    originalBranch=git('branch','--show-current').strip(),
    checkedFiles=len(baseline['sourceHashes']), changedFiles=changed,
    sourceStatusUnchanged=status == baseline['sourceStatus'],
    sourceHeadUnchanged=git('rev-parse','HEAD').strip() == baseline['sourceHead'])
assert not changed and report['sourceStatusUnchanged'] and report['sourceHeadUnchanged'], report
(root/'reviews/declarative-analysis-refactor/original-preservation.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
