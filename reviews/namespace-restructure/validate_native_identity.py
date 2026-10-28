import json
from collections import Counter
from tools.boat_analysis.model.runtime import ROOT, load_model
model=load_model()
before=json.loads((ROOT/'reviews/namespace-restructure/baseline.json').read_text())
plan=json.loads((ROOT/'reviews/namespace-restructure/namespace-map.json').read_text())
mapping=plan['packages']
def mapped(value):
    if isinstance(value,str):
        for old in sorted(mapping,key=len,reverse=True):
            if value==old or value.startswith(old+'::'):return mapping[old]+value[len(old):]
        return value
    if isinstance(value,list):return [mapped(item) for item in value]
    if isinstance(value,dict):return {key:mapped(item) for key,item in value.items()}
    return value

rows=model.query(select=['owner','type','general'])
after={row.id:dict(id=row.id,kind=row.type,properties=row.properties) for row in rows}
missing=[];changed=[]
for row in before['elements']:
    expected=mapped(row)
    # Owner of a moved package is precisely the new containing namespace.
    if row['kind']=='Package':
        owner=expected['id'].rpartition('::')[0]
        if owner:expected['properties']['owner']=owner
        else:expected['properties'].pop('owner',None)
    actual=after.get(expected['id'])
    if actual is None:missing.append(expected)
    elif actual!=expected:changed.append(dict(before=expected,after=actual))
report=dict(baselineElements=len(before['elements']),afterElements=len(rows),missing=missing,changed=changed,
    beforePackageCount=len(before['packages']),
    afterPackages=[dict(id=row.id,owner=row.get('owner')) for row in model.query(select=['owner'],where={
        '@type':'PrimitiveConstraint','operator':'=','property':'@type','value':['Package']})])
(ROOT/'.tools/namespace-semantic-comparison.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print(json.dumps(dict(baselineElements=report['baselineElements'],afterElements=len(rows),missing=len(missing),changed=len(changed),
    missingKinds=dict(Counter(row['kind'] for row in missing)),changedKinds=dict(Counter(row['before']['kind'] for row in changed))),indent=2))

assert not missing and not changed, "Native declaration identity or ownership changed"
expected_added={'BlueDog::'+name for name in ('Behavior','Analyses','Decisions','Verification','Evidence','Configurations::Examples')}
added=set(after)-{mapped(row)['id'] for row in before['elements']}
assert added==expected_added, ('Unexpected added native elements',added)
