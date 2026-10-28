"""Known feasibility problems check fixed-length elimination and failure reporting."""
from types import SimpleNamespace
import numpy as np
import pytest
from tools.boat_analysis.optimization.continuation import solve_stage


class Toy:
    lo = np.zeros(2)
    span = np.ones(2)*2
    model = SimpleNamespace(c={'designNames':['length', 'width']})
    constraint_names = ['width capacity']
    def __init__(self, capacity=1):
        self.capacity = capacity
    def evaluate(self, z):
        return {'eq':np.array([z[1]-z[0]]), 'ineq':np.array([self.capacity-z[1]])}
    def residual(self, z):
        r=self.evaluate(z)
        return np.r_[r['eq'], np.minimum(r['ineq'],0)]
    def residual_jacobian(self, z):
        return np.array([[-1.,1.],[0.,-1. if z[1]>self.capacity else 0.]])
    def jacobians(self, z):
        return np.array([[-1.,1.]]), np.array([[0.,-1.]])
    def feasible(self, z):
        r=self.evaluate(z)
        return abs(r['eq'][0])<1e-4 and r['ineq'][0]>-1e-4


def test_length_is_fixed_while_other_variable_finds_equilibrium():
    r=solve_stage(Toy(),np.array([.9,.9]),1.2,budget=20)
    assert r['feasible']
    assert r['design']['length']==1.2
    assert r['design']['width']==pytest.approx(1.2,abs=2e-4)
    assert 'feasible iterate' in r['history'][0]['message']


def test_incompatible_capacity_is_not_reported_as_feasible():
    r=solve_stage(Toy(.3),np.array([.9,.9]),1.2,budget=20)
    assert not r['feasible']
    assert r['design']['length']==1.2
    assert r['minimumMargin']<0


def test_length_outside_model_bounds_rejected():
    with pytest.raises(ValueError):
        solve_stage(Toy(),np.array([.9,.9]),3)


def test_archived_campaign_and_model_projection_agree():
    from tools.boat_analysis.evidence.continuation import model_source
    from tools.boat_analysis.evidence.records import ROOT, run_record, verify_run_sources
    directory=ROOT/'evidence/runs/2026-10-12-continuation'
    assert verify_run_sources(directory)>10
    record=run_record(directory,'sizing-continuation.json')
    assert record['targetReached'] and record['completed'] and not record['qualified']
    assert [a['lengthM'] for a in record['attempts']]==[2.,1.8,1.6,1.4,1.2]
    assert all(a['feasible'] and a['maxEquilibriumResidual']<1e-4 and a['minimumMargin']>-1e-4 for a in record['attempts'])
    from tools.boat_analysis.evidence.projection import read_projection
    assert read_projection('sizing-continuation') == model_source(directory)


def test_retained_target_is_rejected_by_current_geometry_policy():
    import sys
    if sys.platform!='linux':
        pytest.skip('Native C adapter uses Linux/GCC')
    from tools.boat_analysis.evidence.records import ROOT, run_record
    from tools.boat_analysis.optimization.search import Problem
    record=run_record(ROOT/'evidence/runs/2026-10-12-continuation','sizing-continuation.json')
    p=Problem();z=np.array(record['smallestFeasibleZ'])
    assert (p.lo+z*p.span)[0]==pytest.approx(1.2)
    r=p.evaluate(z)
    assert not p.feasible(z)
    assert r["structure"]["rudderAspectMargin"] < -0.9
    assert r["structure"]["rudderStockMargin"] < 0


def test_restored_baseline_retains_its_geometry_screen_evidence():
    import sys
    if sys.platform!='linux':
        pytest.skip('Native C adapter uses Linux/GCC')
    from tools.boat_analysis.evidence.records import ROOT, run_record, verify_run_sources
    from tools.boat_analysis.optimization.search import Problem
    directory=ROOT/'evidence/runs/2026-10-12-appendage-credibility'
    assert verify_run_sources(directory)>10
    record=run_record(directory,'sizing-continuation.json')
    assert record['targetReached'] and record['seedRestoration']['feasible']
    p=Problem(); z=np.array(record['smallestFeasibleZ'])
    assert (p.lo+z*p.span)[0]==pytest.approx(2.)
    r=p.evaluate(z)
    assert r["structure"]["rudderAspectMargin"] >= -1e-4
    assert r["structure"]["sweptSeparationMargin"] >= -1e-4


def test_finite_passage_projection_preserves_interrupted_status_and_lineage():
    from tools.boat_analysis.evidence.continuation import model_source, compatible_stages
    from tools.boat_analysis.evidence.records import ROOT, run_record, verify_run_sources
    directory=ROOT/'evidence/runs/2026-10-12-finite-passage'
    assert verify_run_sources(directory)>10
    record=run_record(directory,'sizing-continuation.json')
    assert not record['completed'] and not record['qualified']
    assert record['smallestFeasibleLengthM']==pytest.approx(1.4)
    stages=compatible_stages(directory)
    assert [s['lengthM'] for s in stages]==pytest.approx([2.,1.8,1.6,1.4])
    assert all(s['feasible'] for s in stages)
    from tools.boat_analysis.evidence.projection import read_projection
    assert read_projection('finite-passage-sizing') == model_source(directory,'BlueDog::Evidence::FinitePassageSizing')


def test_larger_archived_baseline_is_ineligible_under_current_challenge():
    import sys
    if sys.platform!='linux':
        pytest.skip('Native C adapter uses Linux/GCC')
    from tools.boat_analysis.evidence.records import ROOT, run_record
    from tools.boat_analysis.optimization.search import Problem
    record=run_record(ROOT/'evidence/runs/2026-10-12-finite-passage','sizing-continuation.json')
    p=Problem();z=np.array(record['smallestFeasibleZ'])
    assert not p.feasible(z)
    result=p.evaluate(z)
    assert result['envelope']['sweptLengthM'] > p.overall_length_limit_m
    assert result['structure']['overallLengthMargin'] < 0
    # Updated course distance may also change energy feasibility; this test
    # isolates the swept-length rejection rather than inheriting an old verdict.
    assert np.isfinite(result['concept']['voyageEnergyMargin'])
    assert result['concept']['installationVolumeMargin']>0
