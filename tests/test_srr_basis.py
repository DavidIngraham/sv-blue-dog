"""Independent arithmetic checks on the SRR engineering allocations."""
import json
import math
import pytest
from tools.boat_analysis.model.runtime import native,native_value


def values(name):
    report=json.loads(native('-analysis',name,'-json'))
    assert report['status']=='holds'
    return {r['name']:native_value(r['value']) for r in report['checks'][0]['values']}


def test_encounter_ranges_cover_latency_and_closure():
    result=values('BlueDogEncounterReview::Acquisition')['requiredRangesM']
    assert result==pytest.approx([(v+3)*38+d+10 for v,d in zip([3.5,1.5,15,4,4,2],[50,20,30,20,50,20])])
    assert max(result)==724 and max(result)<750


def test_recovery_risk_sensitivity_is_not_a_measured_probability():
    result=values('BlueDogRecoveryRisk::Sensitivity')
    expected=[(1-math.exp(-rate*48))*(1-math.exp(-.1*hours)) for rate,hours in zip(result['lossRatesPerHour'],result['recoveryHours'])]
    assert result['bounds']==pytest.approx(expected)
    assert result['bounds'][0]<result['bounds'][-1]
