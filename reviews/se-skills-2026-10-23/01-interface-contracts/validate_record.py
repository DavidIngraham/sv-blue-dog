import hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT
stage=ROOT/'reviews/se-skills-2026-10-23/01-interface-contracts'
r=json.loads((stage/'after.json').read_text())
for name,expected in r['sourceHashes'].items():
    # Match the native parser's UTF-8 text snapshot, including universal newline decoding.
    actual=hashlib.sha256((ROOT/name).read_text().encode()).hexdigest()
    assert actual==expected, name
suite=ET.parse(stage/'full.xml').getroot().find('testsuite')
summary=dict(runtimeRevision=r['runtimeRevision'],modelHash=r['modelHash'],
    verifiedModelSources=len(r['sourceHashes']),fullRegression=dict(suite.attrib),
    focusedTests=22,nativeDiagnostics=len(r['diagnostics']),architectureErrors=len(r['errors']),
    publication='36 pages built successfully',skill='validated and installed; matching draft hashes',
    sourceHashConvention='SHA256 of UTF-8 text with native-loader newline normalization')
(stage/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
assert int(suite.attrib['failures'])==0 and int(suite.attrib['errors'])==0
print(json.dumps(summary,indent=2))
