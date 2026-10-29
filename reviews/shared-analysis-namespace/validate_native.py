import hashlib,json
from tools.boat_analysis.model.runtime import ROOT,load_model,model_files
plan=json.loads((ROOT/'reviews/shared-analysis-namespace/namespace-map.json').read_text())
baseline=json.loads((ROOT/'reviews/shared-analysis-namespace/baseline.json').read_text())
mapping=plan['packages']
def mapped(v):
    if isinstance(v,str):
        for old in sorted(mapping,key=len,reverse=True):
            if v==old or v.startswith(old+'::'):return mapping[old]+v[len(old):]
        return v
    if isinstance(v,list):return [mapped(x) for x in v]
    if isinstance(v,dict):return {k:mapped(x) for k,x in v.items()}
    return v
model=load_model();rows=model.query(select=['owner','type','general'])
actual={r.id:dict(id=r.id,kind=r.type,properties=r.properties) for r in rows};missing=[];changed=[]
for row in baseline['elements']:
    expected=mapped(row)
    if row['kind']=='Package' and row['id'] in mapping:expected['properties']['owner']=expected['id'].rpartition('::')[0]
    found=actual.get(expected['id'])
    if found is None:missing.append(expected)
    elif found!=expected:changed.append(dict(before=expected,after=found))
added=set(actual)-{mapped(r)['id'] for r in baseline['elements']}
packages=[r for r in rows if r.type=='Package'];roots={r.id for r in packages if not r.get('owner')}
retained={lib['id']:lib['path'] for lib in baseline['libraries'] if lib['id'] in plan['retained']}
retained_hashes={key:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for key,name in retained.items()}
assert all(retained_hashes[key]==baseline['sourceHashes'][retained[key]] for key in retained)
report=dict(beforeElements=len(baseline['elements']),afterElements=len(rows),missing=missing,changed=changed,added=sorted(added),
    topLevelPackages=sorted(roots),allPackages=len(packages),sourceFiles=len(model_files()),retainedLibraryHashes=retained_hashes)
(ROOT/'.tools/shared-native-comparison.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
assert not missing and not changed and added==set(plan['addedPackages'])
assert roots==set(plan['intendedRoots']) and len(packages)==115 and len(model_files())==7
print(json.dumps({k:v for k,v in report.items() if k not in ('retainedLibraryHashes',)},indent=2))
