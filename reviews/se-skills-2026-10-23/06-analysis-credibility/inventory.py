import json
from tools.boat_analysis.model.runtime import ROOT,load_model
m=load_model();roots=sorted({c.id for r in m.roots for c in r.children()})
a=m.query(scope=roots,select=['owner','type'],where={'@type':'PrimitiveConstraint','property':'@type','operator':'=','value':['AnalysisCaseDefinition','AnalysisCaseUsage']})
r=[dict(id=x.id,properties=x.properties) for x in a]
(ROOT/'reviews/se-skills-2026-10-23/06-analysis-credibility/before.json').write_text(json.dumps(r,default=str,indent=2)+'\n')
for x in r:print(x['id'])
