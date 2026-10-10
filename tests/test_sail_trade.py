"""The sail trade separates missing evidence, failed requirements and preference."""
import json
import re
from pathlib import Path
import pytest
from scripts.study_sail_trade import MODEL, MODELS_TRADE, ROOT, native, publication_outputs


def values(check):return {v['name']:v['value'] for v in check['values']}


def test_published_assessments_do_not_reject_unknown_candidates():
    r=json.loads((ROOT/'docs/analysis/sail-trade.json').read_text(encoding='utf-8'))
    for case in r['checks'][:3]:
        v=values(case)
        assert v['knownFailure']=='false'
        assert v['qualified']=='false'
        assert v['evidenceComplete']=='false'
    assert 'Lead development' in values(r['checks'][0])['developmentDecision']
    assert 'Deprioritize' in values(r['checks'][2])['developmentDecision']
    moments=values(r['checks'][3])
    assert float(moments['positiveMomentNm'])==pytest.approx(98.0665)
    assert float(moments['negativeMomentNm'])==pytest.approx(-98.0665)


@pytest.mark.parametrize('gates,qualified,failed,decision',[
    (['passed']*7,'true','false','Eligible for selection'),
    (['failed']+['unknown']*6,'false','true','Resolve verified failure'),
])
def test_soft_sail_can_qualify_or_fail_from_actual_gates(tmp_path,gates,qualified,failed,decision):
    source=MODEL.read_text(encoding='utf-8')
    replacement='attribute gates : Evidence [7] ordered nonunique default = ('+', '.join('Evidence::'+g for g in gates)+');'
    source,n=re.subn(r'attribute gates : Evidence \[7\] ordered nonunique default =.*?;',replacement,source,count=1,flags=re.S)
    assert n==1
    fixture=tmp_path/'sail-trade.sysml';fixture.write_text(source,encoding='utf-8')
    result=json.loads(native('-analysis','BlueDogSailTrade::softAssessment','-json',models=MODELS_TRADE[:-1]+(fixture,)))
    assert result['status']=='holds' and not result.get('diagnostics')
    v=values(result['checks'][0]);assert v['qualified']==qualified;assert v['knownFailure']==failed
    assert decision in v['developmentDecision']


def test_native_generated_artifacts_are_current():
    for path,content in publication_outputs().items():
        saved=path.read_text(encoding='utf-8').replace('<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->\n','')
        assert saved==content
