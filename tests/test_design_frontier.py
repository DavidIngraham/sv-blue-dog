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


def test_feasible_iterates_survive_infeasible_termination_and_seed_next_objective(monkeypatch):
    import numpy as np
    from types import SimpleNamespace
    from tools.boat_analysis.optimization import frontier

    class Problem:
        lo = np.zeros(1)
        resolution = 1
        model = SimpleNamespace(c={'designNames':['length_m']})
        def __init__(self, **kwargs): pass
        def initial(self): return np.array([.5])
        def feasible(self,z): return z[0] <= .7
        def jacobians(self,z): return np.zeros((1,1)), -np.ones((1,1))
        def evaluate(self,z):
            return dict(mass={'totalMass':10+z[0]},westerlyRoute=[0,0,0,0,0,20-z[0]],
                        envelope={'sweptLengthM':z[0]},eq=np.zeros(1),ineq=np.array([.7-z[0]]),design=z)
    starts=[]
    def limited_solve(fun,start,**kwargs):
        starts.append(start.copy())
        kwargs['callback'](np.array([.3 if len(starts)==1 else .6]))
        return SimpleNamespace(x=np.array([.9]),success=False,message='Iteration limit',nit=2)
    monkeypatch.setattr(frontier,'minimize',limited_solve)
    report=frontier.solve([1.2],[],budget=2,problem_factory=Problem)
    assert [r['z'][0] for r in report['candidates']] == [.3,.6]
    assert all(r['feasible'] and not r['solverConverged'] for r in report['candidates'])
    assert starts[1][0] == .3
    assert len(report['frontier']) == 2
    assert not report['qualified']
