import hashlib,json
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT,load_model,model_files,connection
review=ROOT/'reviews/standalone-gorge-challenge';base=json.loads((review/'baseline.json').read_text());plan=json.loads((review/'namespace-map.json').read_text());mapping=plan['packages']
def mapped(v):
    if isinstance(v,str):
        for old in sorted(mapping,key=len,reverse=True):
            if v==old or v.startswith(old+'::'):return mapping[old]+v[len(old):]
        return v
    if isinstance(v,list):return [mapped(x) for x in v]
    if isinstance(v,dict):return {k:mapped(x) for k,x in v.items()}
    return v
model=load_model();rows=model.query(select=['owner','type','general']);actual={r.id:dict(id=r.id,kind=r.type,properties=r.properties) for r in rows};changed=[];missing=[];ids={}
for old in base['elements']:
    expected=mapped(old)
    if old['id']=='BlueDog::Mission::Challenge':expected['properties'].pop('owner',None)
    if old['id']=='BlueDog::Mission::Challenge::LiveObservation::issue':expected['properties']['owner']='BlueDog::Requirements::Communications'
    if expected['id']!=old['id']:ids[old['id']]=expected['id']
    if expected['id'] not in actual:missing.append(expected['id'])
    elif actual[expected['id']]!=expected:changed.append(dict(expected=expected,actual=actual[expected['id']]))
added=set(actual)-{mapped(r)['id'] for r in base['elements']}
roots={r.id for r in rows if r.type=='Package' and not r.get('owner')};packages=sum(r.type=='Package' for r in rows)
assert not missing and not changed and not added and roots==set(plan['intendedRoots'])
assert len(rows)==14933 and packages==115 and len(model_files())==8
for name,sha in base['sourceHashes'].items():
    if name!='models/blue-dog.sysml':assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
path=ROOT/'models/gorge-challenge.sysml';standalone=connection().parse_sources(((str(path),path.read_text()),),strict=True)
assert standalone.get('GorgeChallenge::transGorgeChallenge') is not None and standalone.get('BlueDog') is None
assert 'BlueDog' not in path.read_text()
before_challenge=json.loads((review/'challenge-baseline.json').read_text())
definitions=model.query(scope=['GorgeChallenge'],select=['documentation','shortName'],where={'@type':'PrimitiveConstraint','operator':'=','property':'@type','value':['RequirementDefinition']})
after_definitions={r.id:r.properties for r in definitions}
for row in before_challenge:
    if row['kind']=='RequirementDefinition':
        expected=mapped(row['id'])
        assert row['properties'].get('documentation')==after_definitions[expected].get('documentation'),expected
        assert row['properties'].get('shortName')==after_definitions[expected].get('shortName'),expected
report=dict(elementsBefore=len(base['elements']),elementsAfter=len(rows),packages=packages,roots=sorted(roots),sources=len(model_files()),missing=missing,changed=changed,added=sorted(added),movedIds=len(ids),standaloneStrictParse=True,normativeRequirementStatementsUnchanged=True,requirementDefinitions=len(definitions),sharedLibraryHashesPreserved=True,sourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in model_files()})
(review/'element-id-map.json').write_text(json.dumps(ids,indent=2)+'\n');(ROOT/'.tools/gorge-native-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
