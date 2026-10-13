"""Trade selection must preserve alternatives and reject incomplete evidence."""
from tools.boat_analysis.optimization.frontier import nondominated


def test_frontier_preserves_mass_speed_trade_and_rejects_dominated():
    rows=[dict(id='light',feasible=True,mass=10.,hours=30.),
          dict(id='fast',feasible=True,mass=15.,hours=20.),
          dict(id='dominated',feasible=True,mass=16.,hours=31.),
          dict(id='failed',feasible=False,mass=1.,hours=1.),
          dict(id='missing',feasible=True,mass=1.),
          dict(id='invalid',feasible=True,mass=float('nan'),hours=1.)]
    assert {r['id'] for r in nondominated(rows,('mass','hours'))}=={'light','fast'}


def test_equal_metrics_do_not_silently_discard_different_concepts():
    rows=[dict(id=n,feasible=True,mass=10.,hours=20.) for n in ('a','b')]
    assert len(nondominated(rows,('mass','hours')))==2
