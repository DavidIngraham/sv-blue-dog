"""Validate the completed implementation record without changing model inputs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from tools.boat_analysis.model.audit import native_audit
from tools.boat_analysis.model.install import REVISION
HERE=Path(__file__).resolve().parent

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

snapshot=json.loads((HERE/'native-review.json').read_text())
for name,expected in snapshot['sources'].items():
    assert digest(ROOT/name)==expected, f'Changed input: {name}'
original=HERE.parents[1]/'requirements-audit-2026-10-22'
historical=json.loads((original/'evidence/validation.json').read_text())
for name,expected in historical['artifacts'].items():
    assert digest(original/name)==expected, f'Changed historical artifact: {name}'
for name,expected in historical['test_source_hashes'].items():
    assert digest(ROOT/name)==expected, f'Changed original criterion regression: {name}'
suite=ET.parse(HERE/'full-tests.xml').getroot().find('testsuite')
assert suite is not None
assert int(suite.get('errors'))==int(suite.get('failures'))==0
criterion_cases=[case for case in suite.findall('testcase') if case.get('classname') in
    {'tests.test_executable_requirements','tests.test_structural_acceptance'}]
assert len(criterion_cases)==93
assert all(case.find('skipped') is None for case in criterion_cases)
build=json.loads((HERE/'build-result.json').read_text())
assert build['returncode']==0
site=json.loads((ROOT/'build/site/build.json').read_text())
assert (ROOT/'build/site/index.html').is_file()
coverage=native_audit()
assert not coverage['errors'] and not coverage['diagnostics']
assert coverage['summary']['requirements']==257
assert coverage['summary']['currentWithObjectives']==coverage['summary']['current']==245
assert coverage['summary']['currentRequirements']==243
assert coverage['summary']['currentStudyObjectives']==2
assert coverage['summary']['future']==12
(HERE/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
changed=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
changed+=['models/vehicle/requirement-decisions.sysml','tests/test_requirement_quality.py','tests/fixtures/requirement-quality.sysml']
result=dict(status='passed',runtimeRevision=REVISION,
    sourceRevision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    sourceTreeModified=coverage['sourceTreeModified'],nativeModelDiagnostics=0,nativeQueryDiagnostics=0,
    nativeSourceHashesChecked=len(snapshot['sources']),historicalArtifactHashesChecked=len(historical['artifacts']),
    fullSuite=dict(tests=int(suite.get('tests')),passed=int(suite.get('tests'))-int(suite.get('skipped')),failures=0,errors=0,skipped=int(suite.get('skipped')),seconds=float(suite.get('time'))),
    criterionRegressions=len(criterion_cases),coverage=coverage['summary'],
    publishing=dict(pages=len(site['pages']),views=site['viewCount'],**build),
    sourceHashes={name:digest(ROOT/name) for name in sorted(set(changed))},
    scope='Native model, software regressions and publication consistency. This does not accept physical qualification or unresolved engineering decisions.')
(HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
report=HERE.parent/'implementation.md'
s=report.read_text().replace('Full regression suite: pending final run.',f"Full regression suite: {int(suite.get('tests'))-int(suite.get('skipped'))} passed, {suite.get('skipped')} skipped, {suite.get('failures')} failures, {suite.get('errors')} errors; includes all 93 executable-requirement/structural-acceptance regressions. [JUnit results](evidence/full-tests.xml).")
s=s.replace('Publishing build: pending final run.',f"Publishing build passed: {len(site['pages'])} pages and {site['viewCount']} native views/reports. [Validation record](evidence/validation.json).")
report.write_text(s)
print(json.dumps({k:result[k] for k in ['status','fullSuite','criterionRegressions','coverage','publishing']},indent=2))
