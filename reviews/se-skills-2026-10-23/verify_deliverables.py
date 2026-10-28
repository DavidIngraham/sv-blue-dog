"""Verify installed skill copies and immutable completed-stage archives without comparing old models to the current tree."""
import hashlib,json,re,zipfile
from tools.boat_analysis.model.runtime import ROOT
base=ROOT/'reviews/se-skills-2026-10-23'
installed=__import__('pathlib').Path('/mnt/c/Users/davin/.codex/skills')
results=[]
for stage in sorted(base.iterdir()):
    skill=stage/'skill/SKILL.md'
    if not skill.exists():continue
    name=re.search(r'^name: (.+)$',skill.read_text(),re.M)[1]
    copies=[]
    for source in sorted((stage/'skill').rglob('*')):
        if not source.is_file():continue
        relative=source.relative_to(stage/'skill')
        destination=installed/name/relative
        assert source.read_bytes()==destination.read_bytes(),str(destination)
        copies.append(str(relative))
    row=dict(stage=stage.name,skill=name,installedMatchingFiles=copies)
    snapshot=stage/'source-snapshot.json'
    if snapshot.exists():
        info=json.loads(snapshot.read_text());archive=stage/info['archive']
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==info['sha256'],str(archive)
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None,str(archive)
            manifest=json.loads(z.read('source-manifest.json' if 'source-manifest.json' in z.namelist() else 'snapshot-manifest.json'))
            hashes=manifest.get('sha256') or {p:v['sha256'] for p,v in manifest['files'].items()}
            for path,expected in hashes.items():
                content=z.read(path)
                mode=manifest.get('files',{}).get(path,{}).get('hashMode','native-text')
                if mode=='native-text':content=content.replace(b'\r\n',b'\n')
                assert hashlib.sha256(content).hexdigest()==expected,path
        row['verifiedArchivedSources']=len(hashes)
        row['archiveSha256']=info['sha256']
    else:row['stageSnapshot']='Not yet closed'
    results.append(row)
(base/'deliverable-integrity.json').write_text(json.dumps(results,indent=2)+'\n')
for row in results:print(row['stage'],row['skill'],len(row['installedMatchingFiles']),row.get('verifiedArchivedSources','pending'))
