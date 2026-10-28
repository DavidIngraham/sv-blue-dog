"""Preserve hash-verified model/audit inputs for stages 1-3.

Earlier model sources are reconstructed from this goal's recorded, reversible
edits and accepted only when every recorded fingerprint matches. Archives are
model/audit source snapshots, not a complete runtime or physical-evidence bundle.
"""
import ast,hashlib,json,zipfile
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT
BASE=ROOT/'reviews/se-skills-2026-10-23'

def digest(data):return hashlib.sha256(data).hexdigest()
def record(stage):return json.loads((BASE/stage/'after.json').read_text())

names=('01-interface-contracts','02-behavior','03-verification-evidence')
records={s:record(s) for s in names}
current={p:p.read_text() for p in (ROOT/'models').rglob('*.sysml')}
second={name:current[ROOT/name] for name in records[names[1]]['sourceHashes']}
# Stage 3 inserted only planned-method lines into these four existing models.
for name in ('models/vehicle/verification.sysml','models/missions/verification.sysml',
             'models/analyses/energy.sysml','models/analyses/reliability.sysml'):
    second[name]=''.join(line for line in second[name].splitlines(keepends=True)
        if not ('metadata planned' in line and 'VerificationCases::VerificationMethod {' in line))
first={name:second[name] for name in records[names[0]]['sourceHashes']}
method='models/vehicle/method.sysml'
required_tree=ast.parse((BASE/'02-behavior/require_inputs.py').read_text())
for node in ast.walk(required_tree):
    if isinstance(node,ast.For) and isinstance(node.target,ast.Tuple) and \
       [n.id for n in node.target.elts if isinstance(n,ast.Name)]==['old','new']:
        for old,new in reversed(ast.literal_eval(node.iter)):
            first[method]=first[method].replace(new,old)
apply_tree=ast.parse((BASE/'02-behavior/apply.py').read_text())
pairs=[tuple(ast.literal_eval(arg) for arg in node.args) for node in ast.walk(apply_tree)
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='replace']
for old,new in reversed(pairs):
    assert first[method].count(new)==1,new[:100]
    first[method]=first[method].replace(new,old,1)
third={name:current[ROOT/name] for name in records[names[2]]['sourceHashes']}
reference=(ROOT/'tools/publishing/reference.sysml').read_text()
old_reference=reference.split('package BlueDogVerificationDocuments {',1)[0].rstrip()

for stage,model_sources in zip(names,(first,second,third)):
    r=records[stage]
    files={}
    manifest=dict(stage=stage,runtimeRevision=r['runtimeRevision'],recordedModelHash=r['modelHash'],
        reconstructedFromVerifiedEdits=stage!=names[2],originalRoot=str(ROOT),files={},
        scope='Exact model/audit sources and recorded drivers where available; not a complete execution environment or physical evidence bundle.')
    for name,text in model_sources.items():
        content=text.encode()
        assert digest(content)==r['sourceHashes'][name],(stage,name)
        files[name]=content;manifest['files'][name]=dict(sha256=digest(content),hashMode='native-text')
    for group in ('auditSources','driverHashes'):
        for name,expected in r.get(group,{}).items():
            p=ROOT/name
            # Architecture audits recorded raw bytes; verification audit/driver hashes use native text.
            raw_mode=group=='auditSources' and stage!=names[2]
            candidates=[p.read_bytes()] if raw_mode else [p.read_text().encode()]
            if name=='tools/publishing/reference.sysml' and stage!=names[2]:
                candidates += [(old_reference+'\n'*n).replace('\n',newline).encode()
                    for n in range(1,5) for newline in ('\n','\r\n')]
            content=next((data for data in candidates if digest(data)==expected),None)
            assert content is not None,(stage,group,name)
            files[name]=content;manifest['files'][name]=dict(sha256=expected,hashMode='bytes' if raw_mode else 'native-text')
    archive=BASE/stage/'source-snapshot.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,content in sorted(files.items()):z.writestr(name,content)
        z.writestr('snapshot-manifest.json',json.dumps(manifest,indent=2)+'\n')
    with zipfile.ZipFile(archive) as z:
        for name,info in manifest['files'].items():assert digest(z.read(name))==info['sha256']
    (BASE/stage/'source-snapshot.json').write_text(json.dumps(dict(archive=archive.name,
        sha256=digest(archive.read_bytes()),modelSources=len(model_sources),totalSources=len(files),
        reconstructedFromVerifiedEdits=manifest['reconstructedFromVerifiedEdits'],scope=manifest['scope']),indent=2)+'\n')
    print(stage,len(model_sources),'model sources verified; snapshot',archive.stat().st_size,'bytes')
