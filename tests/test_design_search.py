"""Check the saved search against independent native interpretation and provenance."""
from copy import deepcopy
import json
import numpy as np
import pytest

from scripts.prepare_design_search import native_value
from scripts.publish_design_search import ROOT, read_search, result_model


@pytest.mark.parametrize('scope', ['full_envelope', 'nominal_5ms'])
def test_native_replay_matches_compiled_search(run_model, scope):
    search = read_search()
    best = search['studies'][scope]['best']
    code, report = run_model('', '-analysis', f'BlueDogDesignResults::{scope}Audit')
    assert code == 0 and not report['diagnostics']
    v = {entry['name']:entry['value'] for entry in report['checks'][0]['values']}
    expected = [[row[name] for name in search['contract']['outputNames']] for row in best['results']]
    np.testing.assert_allclose(np.asarray(native_value(v['rows'])).reshape(np.shape(expected)), expected, rtol=1e-10, atol=1e-8)
    assert v['boundsValid'] == 'true'
    assert v['fullEnvelopeCovered'] == ('true' if scope == 'full_envelope' else 'false')
    assert v['numericalFeasible'] == str(best['numericalFeasible']).lower()
    assert v['supportedDesign'] == v['evidenceReady'] == v['passagePossible'] == 'false'
    assert v['conservativeRoundTripHours'] == 'null'
    assert float(v['maxEquilibriumResidual']) < search['contract']['equilibrium_tolerance']
    assert float(v['worstGroundVMG']) == pytest.approx(min(r['groundVMG'] for r in best['results']))


def test_mutated_trim_is_not_a_balanced_solution(run_model):
    report = deepcopy(read_search())
    report['studies'] = {'nominal_5ms':report['studies']['nominal_5ms']}
    report['studies']['nominal_5ms']['best']['states'][0][0] += .3
    source = result_model(report).replace('BlueDogDesignResults', 'SearchMutation')
    code, output = run_model(source, '-analysis', 'SearchMutation::nominal_5msAudit')
    assert code == 0
    v = {entry['name']:entry['value'] for entry in output['checks'][0]['values']}
    assert float(v['maxEquilibriumResidual']) > report['contract']['equilibrium_tolerance']
    assert v['numericalFeasible'] == 'false'


def test_out_of_bounds_design_is_rejected(run_model):
    report = deepcopy(read_search())
    report['studies'] = {'nominal_5ms':report['studies']['nominal_5ms']}
    report['studies']['nominal_5ms']['best']['design']['lwl_m'] = 4
    source = result_model(report).replace('BlueDogDesignResults', 'SearchMutation')
    code, output = run_model(source, '-analysis', 'SearchMutation::nominal_5msAudit')
    assert code != 0
    assert output['checks'][0]['status'] != 'holds'


def test_results_and_saved_subjects_have_current_provenance():
    report = read_search()
    assert (ROOT/'models/design-search-results.sysml').read_text() == result_model(report)
    for study in report['studies'].values():
        assert len(study['runs']) == 3
        assert all(r['operatingFeasible'] for r in study['runs'])
        assert not any(r['numericalFeasible'] for r in study['runs'])
        assert all(r['optimizationMessage'] is None for r in study['runs'])
