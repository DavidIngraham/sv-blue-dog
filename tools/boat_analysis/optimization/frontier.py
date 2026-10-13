"""Generate alternatives under overall-length caps, without a preference score.

This is a local, quasi-steady concept search. Whole-mission paired scenarios
must supply the later comparison metrics; no completion probability is inferred.
"""
import argparse
import json
import math
import platform
import subprocess
import scipy
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from .search import Problem
from ..evidence.records import source_hashes
from ..model.runtime import ROOT


def nondominated(rows, objectives):
    """Minimization frontier; do not compare incomplete or failed candidates."""
    eligible = [r for r in rows if r['feasible'] and all(
        name in r and math.isfinite(r[name]) for name in objectives)]
    return [r for r in eligible if not any(
        all(other[n] <= r[n] for n in objectives) and
        any(other[n] < r[n] for n in objectives)
        for other in eligible if other is not r)]


def solve(caps, seeds, budget=60, problem_factory=Problem):
    rows = []
    warm_seed = None
    for cap in sorted(set(caps), reverse=True):
        problem = problem_factory(overall_length_limit_m=cap)
        starting_points = seeds or [warm_seed if warm_seed is not None else problem.initial()]
        for seed_index, seed in enumerate(starting_points):
            for objective in ('massKg', 'conditionalPassageHours'):
                start = np.clip(seed if warm_seed is None else warm_seed, 0, 1) if not seeds else np.clip(seed, 0, 1)
                if start.shape != problem.lo.shape or not np.isfinite(start).all():
                    raise ValueError('Seed must contain one finite normalized value per design/state variable')
                best = None
                def metrics(z):
                    r = problem.evaluate(z)
                    return {'massKg':r['mass']['totalMass'],
                            'conditionalPassageHours':float(r['westerlyRoute'][5])}
                def retain(z):
                    nonlocal best
                    if problem.feasible(z):
                        value = metrics(z)[objective]
                        if best is None or value < best[0]:
                            best = (value, np.array(z, copy=True))
                def objective_value(z):
                    if 'invalidGeometry' in problem.evaluate(z):
                        return 1e12
                    return metrics(z)[objective]
                retain(start)
                constraints = [
                    {'type':'eq', 'fun':lambda z: problem.evaluate(z)['eq'],
                     'jac':lambda z: problem.jacobians(z)[0]},
                    {'type':'ineq', 'fun':lambda z: problem.evaluate(z)['ineq'],
                     'jac':lambda z: problem.jacobians(z)[1]}]
                result = minimize(objective_value, start,
                                  method='SLSQP', bounds=[(0,1)]*len(seed),
                                  constraints=constraints, callback=retain,
                                  options={'maxiter':budget,'ftol':1e-7})
                retain(result.x)
                chosen = best[1] if best is not None else result.x
                if best is not None:
                    warm_seed = chosen.copy()
                evaluated = problem.evaluate(chosen)
                if 'invalidGeometry' in evaluated:
                    rows.append(dict(capM=cap, seed=seed_index, objective=objective, feasible=False, solverConverged=bool(result.success), message=str(result.message), invalidGeometry=evaluated['invalidGeometry'], z=chosen.tolist()))
                    continue
                rows.append(dict(capM=cap, seed=seed_index, objective=objective,
                    feasible=problem.feasible(chosen), solverConverged=bool(result.success),
                    message=str(result.message), iterations=int(result.nit),
                    z=chosen.tolist(), initialZ=start.tolist(),
                    selection='best feasible accepted iterate' if best is not None else 'terminal infeasible iterate',
                    resolution=problem.resolution,
                    design=dict(zip(problem.model.c['designNames'], evaluated['design'].tolist())),
                    overallLengthM=evaluated['envelope']['sweptLengthM'],
                    maxEquilibriumResidual=float(np.max(np.abs(evaluated['eq']))),
                    minimumMargin=float(np.min(evaluated['ineq'])), **metrics(chosen)))
    frontier = nondominated(rows, ('overallLengthM','massKg','conditionalPassageHours'))
    return dict(candidates=rows, frontier=frontier, qualified=False,
        scope='Local monohull concept alternatives; conditional steady passage, no calibrated mission probability. Cost and construction effort require BOM/process estimates. Hull length and all other design parameters remain free under the swept overall-length cap.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--caps',type=float,nargs='+',default=[.8,1.,1.2])
    parser.add_argument('--budget',type=int,default=60)
    parser.add_argument('--seed',type=Path,help='Current-contract normalized vectors as a JSON list')
    parser.add_argument('--output',type=Path,default=ROOT/'build/analysis/design-frontier.json')
    args=parser.parse_args()
    if args.budget<1:parser.error('Positive solve budget required')
    seeds=[np.asarray(z,dtype=float) for z in json.loads(args.seed.read_text())] if args.seed else []
    paths=subprocess.check_output(['git','ls-files','tools/boat_analysis'],cwd=ROOT,text=True).splitlines()
    paths=[p for p in paths if p.endswith('.py')]+['uv.lock','build/analysis/wing-polar-grid.json','build/analysis/wing-geometry.json','build/analysis/coupled-fixed-design.json']
    hashes=source_hashes(paths)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    report=solve(args.caps,seeds,args.budget)
    report['sourceHashes']=hashes
    report['sourceRevision']=revision
    report['runtime']={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}
    report['suppliedSeeds']=[z.tolist() for z in seeds]
    report['capsM']=args.caps
    report['solverBudget']=args.budget
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(f"{len(report['frontier'])} nondominated feasible alternatives from {len(report['candidates'])} solves; not vessel qualification")


if __name__=='__main__':main()
