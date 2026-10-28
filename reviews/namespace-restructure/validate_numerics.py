import json
import re
from pathlib import Path
import numpy as np
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.studies.runner import run_study
from tools.boat_analysis.mission.demonstration import run
from tools.boat_analysis.optimization.search import Problem

plan=json.loads((ROOT/'reviews/namespace-restructure/namespace-map.json').read_text())['packages']
pattern=re.compile(r'(?<![A-Za-z0-9_:])('+'|'.join(re.escape(k) for k in sorted(plan,key=len,reverse=True))+r')(?=::|$)')
def mapped(v):
    if isinstance(v,str):return pattern.sub(lambda m:plan[m.group()],v)
    if isinstance(v,list):return [mapped(x) for x in v]
    if isinstance(v,dict):return {mapped(k):mapped(x) for k,x in v.items()}
    return v
reports={name:run_study(ROOT/'examples/studies'/name) for name in ('recovery.yaml','sail-trade.yaml','recovery-scenarios.yaml')}
demo=run()
p=Problem(); z=p.initial(); values=p.evaluate(z)
result=dict(studies={name:report['nativeOutputs'] for name,report in reports.items()},
    demonstration={name:demo[name] for name in ('configuration','configurationId','configurationInputs','nativeOutputs','behaviorTraces')},
    search=dict(constraintNames=p.constraint_names,rows=values['rows'],designFields=p.design_count,stateFields=p.state_count,cases=p.case_count))
(ROOT/'.tools/namespace-after-numerics.json').write_text(json.dumps(result,indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else x.item(),allow_nan=False)+'\n')
before=mapped(json.loads((ROOT/'reviews/namespace-restructure/baseline-numerics.json').read_text()))
assert result==before, 'Study, demonstration or search contract differs'
base=np.load(ROOT/'reviews/namespace-restructure/baseline-search.npz')
after=dict(lo=p.lo,hi=p.hi,span=p.span,initial=z,**{name:np.asarray(values[name]) for name in ('eq','ineq','design','states','route','westerlyRoute','righting')})
errors={}
for name,current in after.items():
    np.testing.assert_allclose(current,base[name],rtol=1e-13,atol=1e-12,err_msg=name)
    errors[name]=float(np.max(np.abs(current-base[name]))) if current.size else 0.0
report=dict(studyRuns=sum(len(r['nativeOutputs']) for r in reports.values()),constraints=len(p.constraint_names),exactReports=True,maximumAbsoluteErrors=errors,rtol=1e-13,atol=1e-12)
(ROOT/'.tools/namespace-numerical-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
