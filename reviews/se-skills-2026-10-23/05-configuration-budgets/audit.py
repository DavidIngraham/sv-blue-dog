from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.configuration_audit import native_configuration_audit
import hashlib,json
stage=ROOT/'reviews/se-skills-2026-10-23/05-configuration-budgets'
r=native_configuration_audit()
r['driverHashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in
    (ROOT/'tests/test_configuration_budgets.py',ROOT/'tests/test_named_configuration.py')}
(stage/'after.json').write_text(json.dumps(r,default=str,indent=2)+'\n')
print(r['summary'],r['review'],r['errors'])
