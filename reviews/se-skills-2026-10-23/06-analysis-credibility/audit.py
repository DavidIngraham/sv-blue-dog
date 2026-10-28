from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.credibility_audit import native_credibility_audit
import hashlib,json
stage=ROOT/'reviews/se-skills-2026-10-23/06-analysis-credibility'
r=native_credibility_audit()
names=['tools/boat_analysis/evidence/records.py','tools/boat_analysis/model/runtime.py','tools/boat_analysis/model/install.py','tools/boat_analysis/model/uncertainty.py','tools/boat_analysis/aerodynamics/polar.py','tools/boat_analysis/geometry/vessel.py','tools/boat_analysis/geometry/hydro.py','tools/boat_analysis/aerodynamics/vsp/polar_grid.py','tools/boat_analysis/aerodynamics/vsp/reference_vsp.py','tools/boat_analysis/mission/motion_campaign.py','tools/boat_analysis/mission/surface_campaign.py','tools/boat_analysis/mission/wave_campaign.py','tools/boat_analysis/optimization/search.py','tools/boat_analysis/optimization/frontier.py','tools/boat_analysis/aerodynamics/vsp/extract_sections.py','tests/test_analysis_credibility.py','tests/test_upstream_client.py','pyproject.toml','uv.lock']
r['driverHashes']={name:hashlib.sha256((ROOT/name).read_text().encode()).hexdigest() for name in names}
(stage/'after.json').write_text(json.dumps(r,default=str,indent=2)+'\n')
print(r['summary'],r['errors'])
