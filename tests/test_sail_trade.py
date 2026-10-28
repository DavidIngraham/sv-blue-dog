"""The sail trade separates missing evidence, failed requirements and preference."""
import json
import re
from pathlib import Path
import pytest
from tools.boat_analysis.model.runtime import ROOT, model_files, native
MODEL = ROOT / "models/blue-dog.sysml"
MODELS_TRADE = tuple(p for p in model_files() if p != MODEL) + (MODEL,)


def values(check):return {v['name']:v['value'] for v in check['values']}


def test_published_assessments_do_not_reject_unknown_candidates():
    args = [arg for case in ('tailAssessment','camberAssessment','softAssessment','buoyancyIllustration') for arg in ('-analysis', 'BlueDog::Analyses::SailTrade::'+case)]
    r=json.loads(native(*args, '-json'))
    assert r['status'] == 'holds'
    for case in r['checks'][:3]:
        v=values(case)
        assert v['knownFailure']=='false'
        assert v['qualified']=='false'
        assert v['evidenceComplete']=='false'
    for case in r['checks'][:3]:
        assert 'Equal development contender' in values(case)['developmentDecision']
    moments=values(r['checks'][3])
    assert float(moments['positiveMomentNm'])==pytest.approx(98.0665)
    assert float(moments['negativeMomentNm'])==pytest.approx(-98.0665)


@pytest.mark.parametrize('gates,qualified,failed,decision',[
    (['passed']*7,'true','false','Eligible for selection'),
    (['failed']+['unknown']*6,'false','true','Resolve verified failure'),
    (['passed']*6+['unknown'],'true','false','Eligible for selection'),
    (['passed']*6+['failed'],'true','false','Eligible for selection'),
    (['unknown']+['passed']*6,'false','false','Equal development contender'),
])
def test_soft_sail_can_qualify_or_fail_from_actual_gates(tmp_path,gates,qualified,failed,decision):
    source=MODEL.read_text(encoding='utf-8')
    replacement='attribute gates : Evidence [7] ordered nonunique default = ('+', '.join('Evidence::'+g for g in gates)+');'
    source,n=re.subn(r'attribute gates : Evidence \[7\] ordered nonunique default =.*?;',replacement,source,count=1,flags=re.S)
    assert n==1
    fixture=tmp_path/'sail-trade.sysml';fixture.write_text(source,encoding='utf-8')
    result=json.loads(native('-analysis','BlueDog::Analyses::SailTrade::softAssessment','-json',models=MODELS_TRADE[:-1]+(fixture,)))
    assert result['status']=='holds' and not result.get('diagnostics')
    v=values(result['checks'][0]);assert v['qualified']==qualified;assert v['knownFailure']==failed
    assert decision in v['developmentDecision']
    if qualified=='true':assert 'no hardware decision' in v['developmentDecision']
    if gates[6]=='failed':assert 'Provisional study concern' in v['reliabilityStudyDisposition']
