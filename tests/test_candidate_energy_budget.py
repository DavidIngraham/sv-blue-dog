"""Published candidate accounting must reconcile with immutable replay evidence."""
import pytest
from tools.boat_analysis.evidence.records import run_record
from tools.boat_analysis.model.runtime import ROOT, analysis_values


def test_candidate_budget_reconciles_with_archived_replay():
    record = run_record(ROOT / 'evidence/runs/2026-10-13-srr-readiness', 'srr-readiness.json')
    replay = record['refinedReplay']
    result = analysis_values('BlueDogCandidateEnergy::Reconciliation')
    assert result['averageBusW'] == pytest.approx(max(c['outputs']['averagePower'] for c in replay['cases']))
    assert result['peakBusW'] == pytest.approx(max(c['outputs']['peakPower'] for c in replay['cases']))
    for key in ['requiredWh', 'departureWh']:
        assert result[key] == pytest.approx(replay['concept'][key], abs=1e-8)
    assert result['exposureHours'] == pytest.approx(replay['concept']['passageHours'])
    assert result['headroomWh'] == pytest.approx(replay['concept']['departureWh']-replay['concept']['requiredWh'])
    assert result['hardwareBudgetComplete'] is False


def test_candidate_budget_projection_is_reproducible():
    from tools.publishing.srr import render
    path = ROOT / 'models/evidence/srr-current.sysml'
    before = path.read_bytes()
    render('2026-10-13-srr-readiness')
    assert path.read_bytes() == before


def test_candidate_budget_is_the_primary_published_budget(rendered_site):
    text = (rendered_site / 'imports/docs/energy.md').read_text()
    assert text.index('Retained candidate: sailing power') < text.index('Illustrative load-accounting example')
    assert 'Base electronics (unresolved component split)' in text
    assert 'Total required at departure' in text
    assert 'Unresolved equipment allocations' in text
    assert 'hardwareBudgetComplete' not in text
    assert 'sysml-report' not in text
