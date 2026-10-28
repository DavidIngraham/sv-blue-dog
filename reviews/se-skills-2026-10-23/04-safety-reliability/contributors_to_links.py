import ast
from tools.boat_analysis.model.runtime import ROOT,connection,model_files
script=ROOT/'reviews/se-skills-2026-10-23/04-safety-reliability/apply.py'
tree=ast.parse(script.read_text())
hazards=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
    and any(isinstance(t,ast.Name) and t.id=='hazards' for t in n.targets))
p=ROOT/'models/analyses/safety.sysml'
text=p.read_text()
old='        ref part contributors : FailureAnalysis::ReviewRow [1..*];\n'
assert text.count(old)==1
text=text.replace(old,'')
links=[]
for row in hazards:
    name=row[0];contributors=row[7]
    if name in ('collisionExposure','boundaryLoss'):
        contributors=(*contributors[:-1],'commandContextFault',contributors[-1])
    old='            ref part :>> contributors = ('+', '.join('BlueDogDFMEA::starter.'+c for c in contributors)+');\n'
    assert text.count(old)==1,name
    text=text.replace(old,'')
    for index,target in enumerate(contributors):
        links.append(f'''    dependency {name}Contributor{index+1} from gorge::{name} to BlueDogDFMEA::starter::{target} {{
        metadata rationale : ModelingMetadata::Rationale {{ text = "Possible contributing mechanism in this hazard's stated modes; supporting basis, not an inevitable mishap or numerical probability."; }}
    }}''')
text=text.rstrip()[:-1]+'\n'+'\n'.join(links)+'\n}\n'
sources=tuple((str(path),text if path==p else path.read_text()) for path in model_files())
connection().parse_sources(sources,strict=True)
p.write_text(text)
print('Native contributor basis uses resolved supporting dependencies; no duplicated tuple-reference registry.')
