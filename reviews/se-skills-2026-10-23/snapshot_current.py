"""Preserve exact current inputs after a successful per-stage audit; never reconstruct or relabel them."""
import hashlib,json,zipfile,sys
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT
stage=ROOT/'reviews/se-skills-2026-10-23'/sys.argv[1]
r=json.loads((stage/'after.json').read_text())
entries={**r['sourceHashes'],**r['auditSources'],**r.get('driverHashes',{})}
for p in sorted((stage/'skill').rglob('*')):
    if p.is_file():entries[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_text().encode()).hexdigest()
for name,expected in entries.items():
    assert hashlib.sha256((ROOT/name).read_text().encode()).hexdigest()==expected,name
archive=stage/'source-snapshot.zip'
assert not archive.exists(),'Immutable stage snapshot already exists'
manifest=dict(runtimeRevision=r['runtimeRevision'],modelHash=r['modelHash'],originalRoot=str(ROOT),
    encoding='UTF-8, universal-newline-normalized source text',sha256=entries,
    scope='Exact model/audit/skill sources; not a complete execution environment or physical evidence bundle.')
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for name in entries:z.writestr(name,(ROOT/name).read_text())
    z.writestr('source-manifest.json',json.dumps(manifest,indent=2)+'\n')
summary=dict(archive=archive.name,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
    modelSources=len(r['sourceHashes']),totalSources=len(entries),reconstructedFromVerifiedEdits=False,scope=manifest['scope'])
(stage/'source-snapshot.json').write_text(json.dumps(summary,indent=2)+'\n')
print(summary)

