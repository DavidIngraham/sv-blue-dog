"""Check stage source fingerprints and serial regression records before closing it."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from tools.boat_analysis.model.runtime import ROOT
stage=ROOT/'reviews/se-skills-2026-10-23'/sys.argv[1]
r=json.loads((stage/'after.json').read_text())
verified={}
for group in ('sourceHashes','auditSources','driverHashes'):
    for name,expected in r.get(group,{}).items():
        assert hashlib.sha256((ROOT/name).read_text().encode()).hexdigest()==expected,name
    verified[group]=len(r.get(group,{}))
suites={name:ET.parse(stage/(name+'.xml')).getroot().find('testsuite') for name in ('full','focused')}
assert all(int(s.attrib['failures'])==0 and int(s.attrib['errors'])==0 for s in suites.values())
assert not r['errors'] and not r['diagnostics']
summary=dict(runtimeRevision=r['runtimeRevision'],modelHash=r['modelHash'],verifiedSources=verified,
    fullRegression=dict(suites['full'].attrib),focusedRegression=dict(suites['focused'].attrib),
    nativeDiagnostics=len(r['diagnostics']),auditErrors=len(r['errors']),
    publication='See publication.log: serial build completed',
    skill='Validated and installed; see skill-installation.json and skill-review.md',
    sourceSnapshot=json.loads((stage/'source-snapshot.json').read_text()))
(stage/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
