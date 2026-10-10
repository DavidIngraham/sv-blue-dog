"""Reproducible evidence checks; numerical passes cannot become qualification."""
import json
from scripts.native_design_kernel import ROOT
from scripts.study_open_sizing import validate


def test_coupled_search_preserves_balance_and_explicit_nonqualification():
    r=json.loads((ROOT/'docs/analysis/coupled-sizing-search.json').read_text());validate(r['sourceHashes'])
    assert r['coarseFeasible'] and not r['qualified']
    assert r['maxEquilibriumResidual']<1e-4
    assert r['minimumMargin']>=-1e-4
    assert len(r['design'])==28 and len(r['stateRows'])==8
    # The report must expose its numerical boundary, not claim a solved minimum.
    assert 'global optimum' in r['scope']


def test_all_declared_sensitivities_are_recorded():
    r=json.loads((ROOT/'docs/analysis/coupled-sizing-replay.json').read_text());validate(r['sourceHashes'])
    assert not r['qualified']
    assert {c['scenario'] for c in r['scenarios']}=={'nominal','construction','aerodynamic','energy','combined'}
    for c in r['scenarios']:
        assert not c['qualified'] and len(c['cases'])==8 and len(c['recovery'])==4
        for curve in c['recovery']:
            assert len(curve['points'])==49
            for point in curve['points']:
                assert abs(point['mass_residual_kg'])<1e-5
                assert abs(point['pitch_torque_Nm'])<1e-4
        if c['sampledStaticScreensPass']:
            assert c['numericallyBalanced']
            assert c['minimumOperatingMargin']>=-1e-4
            assert min(c['structure'].values())>=-1e-4
            assert min(c['route'][:3])>=-1e-4
            assert all(curve['minimumInteriorRestoring_Nm']>0 for curve in c['recovery'])


def test_water_ingress_sensitivity_covers_both_media_and_locked_rig_positions():
    r=json.loads((ROOT/'docs/analysis/coupled-recovery.json').read_text());validate(r['sourceHashes'])
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


def test_coupled_publications_are_generated_and_current():
    from scripts.publish_coupled_inputs import publication as inputs
    from scripts.publish_coupled_results import publication as results
    assert (ROOT/'docs/coupled-inputs.md').read_text(encoding='utf-8')==inputs()
    assert (ROOT/'docs/coupled-results.md').read_text(encoding='utf-8')==results()
