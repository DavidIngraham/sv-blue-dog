from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.safety_audit import native_safety_audit
import hashlib,json
stage=ROOT/'reviews/se-skills-2026-10-23/04-safety-reliability'
r=native_safety_audit()
r['driverHashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in
    (ROOT/'tests/test_safety_reliability.py',ROOT/'tests/test_reliability.py',ROOT/'tests/test_avoidance_failures.py')}
(stage/'after.json').write_text(json.dumps(r,default=str,indent=2)+'\n')
print(r['modelHash'],r['errors'],r['safetyReview'],r['fmeaReview'])
