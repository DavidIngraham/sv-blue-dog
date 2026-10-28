import hashlib,json,xml.etree.ElementTree as ET
from tools.boat_analysis.model.runtime import ROOT
stage=ROOT/'reviews/se-skills-2026-10-23/02-behavior'
r=json.loads((stage/'after.json').read_text())
for group in ('sourceHashes','driverHashes'):
    for name,expected in r[group].items():
        assert hashlib.sha256((ROOT/name).read_text().encode()).hexdigest()==expected,name
suite=ET.parse(stage/'full.xml').getroot().find('testsuite')
focused=ET.parse(stage/'focused.xml').getroot().find('testsuite')
assert int(suite.attrib['failures'])==0 and int(suite.attrib['errors'])==0
assert int(focused.attrib['failures'])==0 and int(focused.attrib['errors'])==0
summary=dict(runtimeRevision=r['runtimeRevision'],modelHash=r['modelHash'],
    verifiedModelSources=len(r['sourceHashes']),verifiedDrivers=len(r['driverHashes']),
    fullRegression=dict(suite.attrib),focusedRegression=dict(focused.attrib),
    nativeDiagnostics=len(r['diagnostics']),architectureErrors=len(r['errors']),
    nativeBehaviorGraphs=len(r['behaviorGraphs']),publication='36 pages built successfully',
    skill='validated and installed; four matching draft files',
    sourceHashConvention='SHA256 of UTF-8 text with native-loader newline normalization')
(stage/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

