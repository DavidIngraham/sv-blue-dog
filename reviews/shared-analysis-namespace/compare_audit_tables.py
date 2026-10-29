import json,re
from pathlib import Path
root=Path.cwd()
b=json.loads((root/'reviews/shared-analysis-namespace/baseline-audits.json').read_text())
a=json.loads((root/'.tools/shared-after-audits.json').read_text())
mapping=json.loads((root/'reviews/shared-analysis-namespace/namespace-map.json').read_text())['packages']
pattern=re.compile(r'(?<![A-Za-z0-9_:])('+'|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
def mapped(v):
    if isinstance(v,str):return pattern.sub(lambda m:mapping[m.group()],v)
    if isinstance(v,list):
        values=[mapped(x) for x in v]
        if values and all(isinstance(x,dict) for x in values):
            values=sorted(values,key=lambda x:json.dumps(x,sort_keys=True))
        return values
    if isinstance(v,dict):return {mapped(k):mapped(x) for k,x in v.items()}
    return v
for k,v in a.items():
    print(k, {key:(len(value) if isinstance(value,(list,dict)) else str(value)[:70]) for key,value in v.items()})
diffs=[]
def compare(before,after,path):
    if isinstance(before,dict) and isinstance(after,dict):
        for key in before.keys()|after.keys():
            if key in {'sourceHashes','auditSources','modelHash','auditModelHash','baselineSource','sourceRevision','configurationSourceHashes','sourceTreeModified'}:continue
            compare(before.get(key),after.get(key),path+'.'+key)
    elif isinstance(before,list) and isinstance(after,list):
        if len(before)!=len(after):diffs.append(dict(path=path,beforeLength=len(before),afterLength=len(after)))
        else:
            for i,(bv,av) in enumerate(zip(before,after)):compare(bv,av,path+f'[{i}]')
    elif before!=after:diffs.append(dict(path=path,before=before,after=after))
compare(mapped(b),mapped(a),'audit')
(root/'.tools/shared-audit-table-differences.json').write_text(json.dumps(diffs,indent=2)+'\n')
print('Differences',len(diffs));print(json.dumps(diffs[:12],indent=2))

assert not diffs, "Native audit table content changed after identity normalization"
