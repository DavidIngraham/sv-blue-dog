from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.decision_audit import native_decision_audit
import hashlib,json
stage=ROOT/'reviews/se-skills-2026-10-23/07-trade-decisions'
r=native_decision_audit()
r['driverHashes']={name:hashlib.sha256((ROOT/name).read_text().encode()).hexdigest() for name in
    ('tests/test_decision_management.py','tests/test_sail_trade.py')}
(stage/'after.json').write_text(json.dumps(r,default=str,indent=2)+'\n')
print(r['summary'],r['errors'])
