"""Current-run provenance, domain restrictions and honest numerical dispositions."""
import json
import numpy as np
import pytest

from tools.boat_analysis.evidence.records import CURRENT, AERODYNAMIC_REFERENCE, digest, run_record, verify_run_sources
from tools.boat_analysis.model.runtime import ROOT, native, native_value


def test_current_sources_and_projection_are_reproducible():
    from tools.boat_analysis.evidence.model import model_source
    assert verify_run_sources(CURRENT) > 10
    assert (ROOT / 'models/evidence/current-sizing.sysml').read_text(encoding='utf-8') == model_source(CURRENT, 'BlueDogCurrentSizing')


def test_full_search_keeps_design_free_and_controls_in_declared_domain():
    result = run_record(CURRENT, 'coupled-sizing-search.json')
    assert len(result['designBounds']) == len(result['design']) == 29
    for name, (lo, hi) in result['designBounds'].items():
        assert lo < hi and lo - 1e-9 <= result['design'][name] <= hi + 1e-9
    assert result['budgetPerPhase'] >= 40
    assert len(result['seedNormalizedDesignAndStates']) == 77
    assert len(result['feasibilityInitialNormalizedDesignAndStates']) == 77
    assert all(0 <= v <= 1 for v in result['seedNormalizedDesignAndStates'])
    if result['resumed']:
        assert result['resumeCheckpointSha256'] == digest(CURRENT / 'optimizer-start.json')
        assert result['seedNormalizedDesignAndStates'] == run_record(CURRENT, 'optimizer-start.json')['bestZ']
    assert not result['qualified']
    assert result['routeProfile'] == 'challenge' and not result['requiresEastProgress']
    assert 'finite storage/reserve' in result['energyConstraintScope']
    contract = json.loads((ROOT / '.tools/coupled-operation-contract.json').read_text())
    for state in result['stateRows']:
        # Stored states are signed by tack; incidence limits are in tack coordinates.
        tack = 1 if state[1] > 0 else -1
        assert contract['stateLower'][2] - 1e-8 <= state[2] * tack <= contract['stateUpper'][2] + 1e-8
        assert abs(state[5]) <= contract['stateUpper'][5] + 1e-8
    assert result['coarseFeasible'] == (result['maxEquilibriumResidual'] < 1e-4 and result['minimumMargin'] > -1e-4)


def test_current_replay_has_all_scenarios_and_native_reviews_match_evidence():
    replay = run_record(CURRENT, 'coupled-sizing-replay.json')
    assert len(replay['scenarios']) == 6
    assert {r['scenario'] for r in replay['scenarios']} == {'nominal', 'construction', 'aerodynamic', 'hydrodynamic', 'energy', 'combined'}
    for case in replay['scenarios']:
        assert len(case['cases']) == 8 and len(case['recovery']) == 4
        assert not case['qualified']
        expected = (case['numericallyBalanced'] and case['minimumOperatingMargin'] >= -1e-4
                    and min(case['structure'].values()) >= -1e-4
                    and min(case['westerlyRoute'][:3]) >= -1e-4)
        report = json.loads(native('-analysis', f"BlueDogCurrentSizing::{case['scenario']}Review", '-json'))
        values = {v['name']: native_value(v['value']) for v in report['checks'][0]['values']}
        assert values['operatingScreensPass'] == expected
        assert values['evidenceAccepted'] is False


def test_convergence_flags_recompute_from_recorded_coefficients():
    record = run_record(AERODYNAMIC_REFERENCE, 'wing-convergence.json')
    assert len(record['cases']) == 15
    assert sum(len(c['values']['Alpha']) for c in record['cases']) == 60
    assert record['validated'] is False
    for comparison in record['comparisons']:
        selected = [r for r in record['cases'] if r['reverseChord'] == comparison['reverseChord'] and r['beta_deg'] == comparison['beta_deg']]
        i, j = (1, 2) if comparison['comparison'] == 'wake' else (3, 4)
        difference = [np.max(np.abs(np.array(selected[i]['values'][key]) - selected[j]['values'][key])) for key in ('CLtot', 'CDi', 'CMytot')]
        assert list(comparison['maxAbsoluteDifference'].values()) == pytest.approx(difference)
        assert comparison['passesScreen'] == bool(np.all(np.array(difference) <= record['settings']['absoluteTolerance']))


def test_current_recovery_covers_ingress_media_and_missing_pitch_samples():
    recovery = run_record(CURRENT, 'coupled-recovery.json')
    diagnostic = run_record(CURRENT, 'coupled-pitch-diagnostic.json')
    assert len(recovery['cases']) == 24 and not recovery['qualified']
    assert {c['density_kg_m3'] for c in recovery['cases']} == {1000, 1025}
    assert {c['wing_state'] for c in recovery['cases']} == {'sealed', 'free_flooding_homogenized', 'full_water_retention'}
    expected = set()
    for case in recovery['cases']:
        assert len(case['points']) == 49
        for point in case['points']:
            if 'failure' in point:
                expected.add((case['density_kg_m3'], case['mast_trim_deg'], point['heel_deg'], case['wing_state']))
            else:
                assert abs(point['mass_residual_kg']) < 1e-5
                assert abs(point['pitch_torque_Nm']) < 1e-4
    actual = {(c['density_kg_m3'], c['mast_trim_deg'], c['heel_deg'], c.get('wing_state', 'sealed')) for c in diagnostic['cases']}
    assert actual == expected and not diagnostic['qualified']
