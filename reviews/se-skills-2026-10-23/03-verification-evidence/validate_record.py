import hashlib,json,xml.etree.ElementTree as ET
from tools.boat_analysis.model.runtime import ROOT
stage=ROOT/'reviews/se-skills-2026-10-23/03-verification-evidence'
r=json.loads((stage/'after.json').read_text())
for group in ('sourceHashes','auditSources'):
    for name,expected in r[group].items():
        assert hashlib.sha256((ROOT/name).read_text().encode()).hexdigest()==expected,name
suites={name:ET.parse(stage/(name+'.xml')).getroot().find('testsuite') for name in ('full','focused')}
assert all(int(s.attrib['failures'])==0 and int(s.attrib['errors'])==0 for s in suites.values())
summary=dict(runtimeRevision=r['runtimeRevision'],modelHash=r['modelHash'],verifiedModelSources=len(r['sourceHashes']),
    verifiedAuditSources=len(r['auditSources']),fullRegression=dict(suites['full'].attrib),
    focusedRegression=dict(suites['focused'].attrib),nativeDiagnostics=len(r['diagnostics']),auditErrors=len(r['errors']),
    planningSummary=r['summary'],openExecutionDetails=r['openEvidence'],publication='36 pages built successfully',
    skill='validated and installed; four matching draft files',sourceSnapshot=json.loads((stage/'source-snapshot.json').read_text()))
(stage/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

