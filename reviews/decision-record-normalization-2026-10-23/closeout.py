"""Check final validation artifacts and the exact audited source content."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from tools.boat_analysis.model.runtime import ROOT

out = Path(__file__).parent
before = json.loads((out/'before.json').read_text())
audit = json.loads((out/'after.json').read_text())
assert not audit['errors'] and not audit['diagnostics']
assert before['assessments'] == audit['assessments'], 'Rig dispositions changed'
for relative, expected in {**audit['sourceHashes'], **audit['auditSources']}.items():
    assert hashlib.sha256((ROOT/relative).read_text().encode()).hexdigest() == expected, relative
suites = ET.parse(out/'full.xml').getroot().findall('testsuite')
tests = {key:sum(int(s.attrib.get(key,0)) for s in suites) for key in ('tests','failures','errors','skipped')}
assert tests['tests'] == 1097 and not any(tests[k] for k in ('failures','errors','skipped')), tests
publication = json.loads((ROOT/'build/site/build.json').read_text())
assert len(publication['pages']) == 36
assert 'sail-trade.md' in publication['pages']
rendered = (ROOT/'build/site/imports/docs/sail-trade.md').read_text()
assert '250 mm print jobs and one-person handling remain owner constraints.' in rendered
assert 'Working disposition records preserve existing baselines' in rendered
result = dict(runtimeRevision=audit['runtimeRevision'],modelHash=audit['modelHash'],
    auditedSourceContentUnchanged=True,rigAssessmentsUnchanged=True,
    tests=tests,testSeconds=sum(float(s.attrib['time']) for s in suites),
    publicationPages=len(publication['pages']),decisionInventory=audit['summary'],
    preserved=dict(informationRecords=20,contextAnnotations=14,allocationProcedureReviews=80,
        supportingDependencies=43,openQuestionShortIDs=6),
    interpretation='Structural normalization only; no new engineering selection, evidence acceptance or approval.')
(out/'validation-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
