"""Independent checks of route signs, modular lifting, CG and saved verdicts."""
import sys
import numpy as np
import pytest
from scripts.study_mission_sizing import read_report, ROOT


def test_saved_results_follow_constraints_and_keep_waterline_fixed():
    r=read_report()
    for study in r['studies'].values():
        b=study['rounded'];assert b['design']['lwl_m']==2
        hardware=b['maxEquilibriumResidual']<=.001 and b['minimumHardwareMargin']>=-.0001
        assert b['operatingFeasible']==hardware
        assert b['numericalFeasible']==(hardware and b['route'][3]>=-1e-4)
        assert b['targetMarginMet']==(hardware and b['route'][3]>=.1-1e-6)
        for name in r['contract']['designNames'][15:19]:
            assert b['design'][name]/.2==pytest.approx(round(b['design'][name]/.2))
        for row in b['results']:
            assert row['transportBodyMass']+row['wingStructuralMass']+row['batteryMass']+row['keelAssembly']==pytest.approx(row['totalMass'])
            if hardware:
                assert max(row[n] for n in ['transportBodyMass','wingStructuralMass','batteryMass','keelAssembly'])<=15.001
                assert row['cgBelowBottom']>=.02-1e-5
        assert all(p['speed'] is None for p in study['polar'] if not p['valid'])
    assert r['missionSupported'] is False


@pytest.fixture(scope='module')
def kernel():
    if sys.platform!='linux':pytest.skip('Compiled native C requires Linux/GCC')
    from scripts.study_mission_sizing import MissionKernel
    return MissionKernel(1)


def test_route_keeps_negative_intervals_and_current_sign(kernel):
    q=np.array(kernel.contract['routeParameters'])
    v=np.array([.2,.8,1.8,1.2])
    expected_up=q[1]*(q[0]*v[0]-q[3])+q[2]*(q[0]*v[2]-q[4])
    expected_down=q[1]*(q[0]*v[1]+q[3])+q[2]*(q[0]*v[3]+q[4])
    result=kernel.route(v)
    assert result[0]==pytest.approx(expected_up)
    assert result[1]==pytest.approx(expected_down)
    assert kernel.route([0,0,0,0])[3]<0
    with pytest.raises(ValueError):kernel.route([1,2,3])


def test_cg_matches_independent_component_moments_and_rejects_zero_ballast(kernel):
    b=read_report()['studies']['printed_ribs']['rounded'];c=kernel.contract
    d=np.array([b['design'][n] for n in c['designNames']]);s=np.r_[5,1,1,b['states'][0]]
    row=dict(zip(c['outputNames'],kernel.evaluate(d,s)))
    L,B,A,AR,Ak,sk,Ar,sr,ballast=d[:9];draft=row['draft'];F=d[13]
    shell=row['hullArealMass']*(L*B*(F-draft)+(L+B)*(F*F-draft*draft))
    moment=(row['wingStructuralMass']*(F+np.sqrt(A*AR)/2)+d[11]*2*F
            -row['batteryMass']*draft/2-row['keelStructuralMass']*(draft+sk/2)
            -row['rudderStructuralMass']*(draft+sr/2)-ballast*(draft+sk)+shell)
    assert row['centerOfGravity']==pytest.approx(moment/row['totalMass'],abs=1e-9)
    d[8]=0
    no_ballast=dict(zip(c['outputNames'],kernel.evaluate(d,s)))
    assert no_ballast['low_mass_center']<0


def test_compiled_rows_match_saved_native_replay(kernel):
    r=read_report();c=r['contract']
    for study in r['studies'].values():
        kernel.parameters[97]=study['architecture'];b=study['rounded'];d=[b['design'][n] for n in c['designNames']]
        for env,state,row in zip([[5,1,1],[5,0,1],[8,1,1],[8,0,1]],b['states'],b['results']):
            np.testing.assert_allclose(kernel.evaluate(d,env+state),[row[n] for n in c['outputNames']],rtol=1e-8,atol=1e-6)
    kernel.parameters[97]=1


def test_native_readiness_stays_false_without_recovery_evidence():
    import json
    from scripts.study_mission_sizing import native, MODELS_NEW
    if sys.platform == 'linux':pytest.skip('Pinned interpreter runs on Windows')
    r=json.loads(native('-analysis','BlueDogMissionSizing::currentReadiness','-json',models=MODELS_NEW))
    assert r['status']=='holds' and not r.get('diagnostics')
    values={v['name']:v['value'] for v in r['checks'][0]['values']}
    assert str(values['supported']).lower()=='false'
