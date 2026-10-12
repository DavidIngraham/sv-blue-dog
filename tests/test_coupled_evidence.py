"""Reproducible evidence checks; numerical passes cannot become qualification."""
import json
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import baseline_record


def test_coupled_search_preserves_balance_and_explicit_nonqualification():
    r=baseline_record('coupled-sizing-search.json')
    assert r['coarseFeasible'] and not r['qualified']
    assert r['maxEquilibriumResidual']<1e-4
    assert r['minimumMargin']>=-1e-4
    assert min(r['route'][:3])>=-1e-4 and min(r['westerlyRoute'][:3])>=-1e-4
    assert len(r['design'])==29 and len(r['stateRows'])==8
    # The report must expose its numerical boundary, not claim a solved minimum.
    assert 'global optimum' in r['scope']


def test_all_declared_sensitivities_are_recorded():
    r=baseline_record('coupled-sizing-replay.json')
    assert not r['qualified']
    assert {c['scenario'] for c in r['scenarios']}=={'nominal','construction','aerodynamic','hydrodynamic','energy','combined'}
    for c in r['scenarios']:
        assert not c['qualified'] and len(c['cases'])==8 and len(c['recovery'])==4
        for row in c['cases']:
            assert isinstance(row['energyConstraintsEnforced'],bool)
            if not row['energyConstraintsEnforced']:
                assert not row['energyConstrainedAttempt']['screenFeasible']
                assert 'minimumEnergyMargin' in row['energyConstrainedAttempt']
        for curve in c['recovery']:
            assert len(curve['points'])==49
            assert curve['failedEquilibria']==sum('failure' in point for point in curve['points'])
            for point in curve['points']:
                if 'failure' in point:continue
                assert abs(point['mass_residual_kg'])<1e-5
                assert abs(point['pitch_torque_Nm'])<1e-4
        if c['sampledStaticScreensPass']:
            assert c['numericallyBalanced']
            assert c['minimumOperatingMargin']>=-1e-4
            assert min(c['structure'].values())>=-1e-4
            assert min(c['route'][:3])>=-1e-4
            assert min(c['westerlyRoute'][:3])>=-1e-4
            assert all(curve['failedEquilibria']==0 and curve['minimumInteriorRestoring_Nm']>0 for curve in c['recovery'])


def test_water_ingress_sensitivity_covers_both_media_and_locked_rig_positions():
    r=baseline_record('coupled-recovery.json')
    assert not r['qualified'] and len(r['cases'])==24
    assert {c['density_kg_m3'] for c in r['cases']}=={1000,1025}
    assert {c['mast_trim_deg'] for c in r['cases']}=={0,90,180,270}
    for c in r['cases']:
        assert len(c['points'])==49
        assert c['retained_water_kg']>0 if c['wing_state']=='full_water_retention' else c['retained_water_kg']==0
        for p in c['points']:
            if 'failure' not in p:
                assert abs(p['mass_residual_kg'])<1e-5
                assert abs(p['pitch_torque_Nm'])<1e-4



def test_missing_pitch_samples_have_full_range_diagnostic():
    recovery=baseline_record('coupled-recovery.json')
    diagnostic=baseline_record('coupled-pitch-diagnostic.json')
    expected={(c['density_kg_m3'],c['mast_trim_deg'],p['heel_deg']) for c in recovery['cases'] for p in c['points'] if 'failure' in p}
    actual={(c['density_kg_m3'],c['mast_trim_deg'],c['heel_deg']) for c in diagnostic['cases']}
    assert expected==actual and not diagnostic['qualified']
    assert diagnostic['pitchRange_deg']==[-180,180]
    for c in diagnostic['cases']:
        for r in c['roots']:
            assert abs(r['mass_residual_kg'])<1e-5
            assert abs(r['pitch_torque_Nm'])<1e-4


def test_replay_enforces_energy_before_using_a_diagnostic(monkeypatch):
    from tools.boat_analysis.optimization import replay
    calls=[]
    def solve(*args,**kwargs):
        calls.append(kwargs['require_energy'])
        return {'screenFeasible':True,'equilibrated':True}
    monkeypatch.setattr(replay,'solve_state',solve)
    result=replay.operating_case(None,None,5,True,1,[1,2,3,4,5,6],35)
    assert calls==[True] and result['energyConstraintsEnforced']
    calls.clear()
    def failed(*args,**kwargs):
        calls.append(kwargs['require_energy'])
        return {'screenFeasible':not kwargs['require_energy'],'equilibrated':True,'state':[5,1,1,1,2,3,4,5,6],'message':'diagnostic','outputs':{'cycleMargin':-.8,'reserveMarginScaled':-.7,'peakMargin':-.2}}
    monkeypatch.setattr(replay,'solve_state',failed)
    result=replay.operating_case(None,None,5,True,1,[1,2,3,4,5,6],35)
    assert calls==[True,False] and not result['energyConstraintsEnforced']
    assert result['energyConstrainedAttempt']['minimumEnergyMargin']==-.2
