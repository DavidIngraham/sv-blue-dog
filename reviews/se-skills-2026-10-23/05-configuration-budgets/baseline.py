from tools.boat_analysis.model.runtime import ROOT,model_files,connection
from tools.boat_analysis.model.install import REVISION
import hashlib,json
sources=tuple((str(p),p.read_text()) for p in model_files())
m=connection().parse_sources(sources,strict=True)
r=dict(runtimeRevision=REVISION,modelHash=m.hash,
    sourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in model_files()},
    integration=m.run_analysis('BlueDogIntegratedCandidate::Inputs').outputs,
    interpretation='IC-01 allocations; archived 440Wh and synthetic load examples remain distinct; no installed-article identity or complete measured equipment ledger.')
(ROOT/'reviews/se-skills-2026-10-23/05-configuration-budgets/before.json').write_text(json.dumps(r,default=str,indent=2)+'\n')
print(r['modelHash'],r['integration']['identifier'])
