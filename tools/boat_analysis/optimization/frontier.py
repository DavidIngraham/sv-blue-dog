"""Generate alternatives under overall-length caps, without a preference score.

This is a local, quasi-steady concept search. Whole-mission paired scenarios
must supply the later comparison metrics; no completion probability is inferred.
"""
import argparse
import json
import math
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
    for cap in caps:
        problem = problem_factory(overall_length_limit_m=cap)
        starting_points = seeds or [problem.initial()]
        for seed_index, seed in enumerate(starting_points):
            for objective in ('massKg', 'conditionalPassageHours'):
                def metrics(z):
                    r = problem.evaluate(z)
                    return {'massKg':r['mass']['totalMass'],
                            'conditionalPassageHours':float(r['westerlyRoute'][5])}
                constraints = [
                    {'type':'eq', 'fun':lambda z: problem.evaluate(z)['eq'],
                     'jac':lambda z: problem.jacobians(z)[0]},
                    {'type':'ineq', 'fun':lambda z: problem.evaluate(z)['ineq'],
                     'jac':lambda z: problem.jacobians(z)[1]}]
                result = minimize(lambda z: metrics(z)[objective], np.clip(seed,0,1),
                                  method='SLSQP', bounds=[(0,1)]*len(seed),
                                  constraints=constraints,
                                  options={'maxiter':budget,'ftol':1e-7})
                evaluated = problem.evaluate(result.x)
                rows.append(dict(capM=cap, seed=seed_index, objective=objective,
                    feasible=problem.feasible(result.x), solverConverged=bool(result.success),
                    message=str(result.message), iterations=int(result.nit),
                    z=result.x.tolist(),
                    design=dict(zip(problem.model.c['designNames'], evaluated['design'].tolist())),
                    overallLengthM=evaluated['envelope']['sweptLengthM'],
                    maxEquilibriumResidual=float(np.max(np.abs(evaluated['eq']))),
                    minimumMargin=float(np.min(evaluated['ineq'])), **metrics(result.x)))
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
    report=solve(args.caps,seeds,args.budget)
    paths=['tools/boat_analysis/optimization/frontier.py','tools/boat_analysis/optimization/search.py']
    report['sourceHashes']=source_hashes(paths)
    report['capsM']=args.caps
    report['solverBudget']=args.budget
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(f"{len(report['frontier'])} nondominated feasible alternatives from {len(report['candidates'])} solves; not vessel qualification")


if __name__=='__main__':main()
