"""Verify review artifact coverage and provenance, not engineering judgments."""
import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
ROOT = HERE.parents[2]
snapshot = json.loads((HERE / 'native-review.json').read_text())

def check(condition, detail):
    if not condition: raise ValueError(detail)

def read_csv(name):
    with (REVIEW / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def native(name):
    t = snapshot['tables'][name]
    return [{'element': r['element']['id'], **dict(zip(t['columns'], r['cells']))} for r in t['rows']]

current_revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
check(current_revision == snapshot['baseline'], 'Baseline revision changed')
changed = [p for p, digest in snapshot['sources'].items()
           if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != digest]
check(not changed, ('Audited source changed', changed))
check(not snapshot['diagnostics'] and not snapshot['queryDiagnostics'], 'Native diagnostics present')

requirements = read_csv('requirement-review.csv')
check(len(requirements) == len(native('Requirements')) == 251, 'Requirement coverage mismatch')
check({r['element'] for r in requirements} == {r['element'] for r in native('Requirements')}, 'Missing requirement row')
check(len({r['id'] for r in requirements}) == len(requirements), 'Duplicate requirement ID')
for row in requirements:
    path, line = row['location'].rsplit(':', 1)
    check("requirement def <'" + row['id'] + "'>" in (ROOT / path).read_text().splitlines()[int(line)-1], ('Source location', row['element']))
    check(row['wording_review'] and row['source_review'] and row['acceptance_feasibility'] and row['proposed_action'], ('Incomplete review row', row['element']))

derivations = read_csv('derivation-review.csv')
native_derivations = {r['element']: r for r in native('Derivations')}
check({r['element'] for r in native('AllDerivations')} == set(native_derivations), 'Derivations outside reviewed package inventory')
check(len(derivations) == len(native_derivations) == 238, 'Derivation count')
check({r['relationship'] for r in derivations} == set(native_derivations), 'Missing derivation disposition')
for row in derivations:
    expected = native_derivations[row['relationship']]
    check([row['original']] == [v['id'] for v in expected['Original']], ('Original endpoint', row['relationship']))
    check([row['derived']] == [v['id'] for v in expected['Derived']], ('Derived endpoint', row['relationship']))
    check(row['reason'] and row['status'] and row['proposed_action'], ('Incomplete derivation review', row['relationship']))
check(Counter(r['status'] for r in derivations) == {'pass with stated scope': 67, 'fail implication': 119, 'unresolved meaning': 52}, 'Report disposition totals changed')

dependencies = read_csv('dependency-review.csv')
check(len(dependencies) == len(native('AllDependencies')) == 422, 'Dependency count')
check({r['relationship'] for r in dependencies} == {r['element'] for r in native('AllDependencies')}, 'Missing dependency')
check({r['relationship'] for r in dependencies if r['kind'] == 'refinement'} == {r['element'] for r in native('AllRefinements')}, 'Refinement classification')
for row in dependencies:
    check(row['client'] and row['supplier'] and row['scope'], ('Missing endpoint review', row['relationship']))

allocations = read_csv('allocation-review.csv')
expected_allocations = [(r['element'], v['id']) for r in native('AllAllocationSources') for v in r['Targets']]
check(Counter((r['source'], r['target']) for r in allocations) == Counter(expected_allocations), 'Allocation coverage')
check(len(allocations) == 55, 'Allocation total')
verification = read_csv('verification-review.csv')
check(len(verification) == 94 and {r['case'] for r in verification} == {r['element'] for r in native('AllVerification')}, 'Verification definition coverage')
check(len(native('Basis')) == 109 and len(native('BasisTargets')) == 109, 'Basis coverage')
check(len(snapshot['otherRequirementDefinitions']) == 2, 'Analysis-contract scope changed')

checklist = (REVIEW / 'checklist-review.md').read_text()
expected_checks = {f'{prefix}{i:02}' for prefix, count in [('Q',12),('H',9),('R',8),('V',6)] for i in range(1,count+1)}
check(set(re.findall(r'^\| ([QHRV]\d{2}) ', checklist, re.M)) == expected_checks, 'Checklist coverage')
report = (REVIEW / 'audit.md').read_text()
check(set(re.findall(r'^### (F\d{2}) ', report, re.M)) == {f'F{i:02}' for i in range(1,9)}, 'Finding coverage')
check({f'U{i:02}' for i in range(1,7)} <= set(re.findall(r'\bU\d{2}\b', report)), 'Open decisions missing')
missing_links = []
for page in REVIEW.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', page.read_text()):
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path: continue
        destination = (page.parent / unquote(url.path)).resolve()
        if destination == (HERE / 'validation.json').resolve(): continue  # Written after all checks below.
        if not destination.exists(): missing_links.append((page.name, target))
check(not missing_links, ('Broken review links', missing_links))

xml = ET.parse(HERE / 'criterion-regressions.xml')
suites = list(xml.getroot().iter('testsuite'))
tests = sum(int(s.get('tests',0)) for s in suites)
failed = sum(int(s.get('failures',0)) + int(s.get('errors',0)) for s in suites)
skipped = sum(int(s.get('skipped',0)) for s in suites)
check((tests,failed,skipped) == (93,0,0), ('Criterion regression record', tests,failed,skipped))

record = {'status': 'passed', 'baseline': current_revision, 'model_sources_unchanged': True,
          'native_model_diagnostics': 0, 'native_query_diagnostics': 0,
          'requirement_rows': len(requirements), 'derivation_rows': len(derivations),
          'dependency_rows': len(dependencies), 'refinements': 19, 'allocation_pairs': len(allocations),
          'verification_cases': len(verification), 'checklist_checks': len(expected_checks),
          'criterion_regressions': {'passed': tests, 'failed': failed, 'skipped': skipped},
          'scope': 'Artifact completeness, exact native inventory/endpoints, source integrity, links and recorded regressions. Engineering judgment is documented in the report and ledgers.',
          'test_source_hashes': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
              ['tests/test_executable_requirements.py','tests/test_structural_acceptance.py','tests/fixtures/shared-acceptance.sysml']}}
record['artifacts'] = {p.relative_to(REVIEW).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted(REVIEW.rglob('*')) if p.is_file() and p.name != 'validation.json' and '__pycache__' not in p.parts}
(HERE / 'validation.json').write_text(json.dumps(record, indent=2) + '\n')
check((HERE / 'validation.json').is_file(), 'Validation record was not saved')
print('Audit artifacts verified:', len(requirements), 'requirements,', len(derivations), 'derivations,', tests, 'passing criterion regressions.')
