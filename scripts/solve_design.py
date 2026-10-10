"""Search shared vessel designs; all engineering equations execute from SysML."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import least_squares, minimize

try:
    from .native_design_kernel import Kernel, ROOT
except ImportError:
    from native_design_kernel import Kernel, ROOT


class Problem:
    def __init__(self, kernel, indices):
        self.kernel, self.indices = kernel, list(indices)
        self.c = kernel.contract
        self.nd = len(self.c["designNames"])
        self.ne = self.c["equationCount"]
        self.ng = self.c["marginCount"]
        self.environment = np.array([[self.c["winds"][i], self.c["windward"][i], self.c["foulingDrag"][i]] for i in indices])
        self.lower = np.r_[self.c["lower"], np.concatenate([self.c["stateLowerUp" if row[1] else "stateLowerDown"] for row in self.environment])]
        self.upper = np.r_[self.c["upper"], np.concatenate([self.c["stateUpperUp" if row[1] else "stateUpperDown"] for row in self.environment])]
        self.span = self.upper - self.lower
        self.last = None

    def evaluate(self, z):
        if self.last is not None and np.array_equal(self.last[0], z):
            return self.last[1]
        x = self.lower + np.asarray(z) * self.span
        rows = np.array([self.kernel.evaluate(x[:self.nd], np.r_[env, state]) for env, state in zip(self.environment, x[self.nd:].reshape(-1, 6))])
        self.last = (np.array(z, copy=True), rows)
        return rows

    def equality(self, z):
        return self.evaluate(z)[:, :self.ne].ravel()

    def inequality(self, z):
        return self.evaluate(z)[:, self.ne:self.ne+self.ng].ravel()

    def residual(self, z):
        return np.r_[self.equality(z), np.minimum(self.evaluate(z)[:, self.ne+1:self.ne+self.ng].ravel(), 0)]

    def feasible(self, z):
        return bool(np.max(np.abs(self.equality(z))) <= self.c["equilibrium_tolerance"] and np.min(self.inequality(z)) >= -self.c["margin_tolerance"])

    def initial(self, seed):
        rng = np.random.default_rng(seed)
        z = rng.uniform(0.25, 0.75, self.lower.size)
        states = []
        for wind, up, foul in self.environment:
            states.append([2.5, 50 if up else 130, 7, 3, -2, 8])
        z[self.nd:] = (np.array(states).ravel() - self.lower[self.nd:]) / self.span[self.nd:]
        return np.clip(z, 0.001, 0.999)

    def run(self, seed, budget):
        initial = self.initial(seed)
        phase = least_squares(self.residual, initial, bounds=(0, 1), max_nfev=budget, ftol=1e-9, xtol=1e-9, gtol=1e-9)
        best = phase.x
        # Keep physical equilibrium and hardware constraints hard; maximize the
        # worst progress rather than publishing an unbalanced penalty compromise.
        start_margin = float(self.evaluate(best)[:, self.ne].min())
        frontier = minimize(lambda w: -w[-1], np.r_[best, start_margin - 0.01],
            method="SLSQP", bounds=[(0,1)] * best.size + [(-10, 10)],
            constraints=[
                {"type":"eq", "fun":lambda w:self.equality(w[:-1])},
                {"type":"ineq", "fun":lambda w:self.evaluate(w[:-1])[:,self.ne+1:self.ne+self.ng].ravel()},
                {"type":"ineq", "fun":lambda w:self.evaluate(w[:-1])[:,self.ne] - w[-1]},
            ], options={"maxiter":budget,"ftol":1e-8})
        candidate = frontier.x[:-1]
        if np.max(np.abs(self.equality(candidate))) <= self.c["equilibrium_tolerance"] and np.min(self.evaluate(candidate)[:,self.ne+1:self.ne+self.ng]) >= -self.c["margin_tolerance"]:
            best = candidate
        refined = None
        if self.feasible(best):
            mass_index = self.c["outputNames"].index("totalMass")
            refined = minimize(lambda z: self.evaluate(z)[0, mass_index], best, method="SLSQP", bounds=[(0,1)] * best.size,
                constraints=[{"type":"eq", "fun":self.equality}, {"type":"ineq", "fun":self.inequality}],
                options={"maxiter":budget, "ftol":1e-8})
            if self.feasible(refined.x):
                best = refined.x
        # Resolve each operating point to its best progress at the selected
        # fixed design; nonlimiting states in a max-min solve are otherwise arbitrary.
        for row in range(len(self.indices)):
            sl = slice(self.nd + 6 * row, self.nd + 6 * (row + 1))
            def with_state(y):
                trial = best.copy()
                trial[sl] = y
                return trial
            update = minimize(lambda y:-self.evaluate(with_state(y))[row,self.c["outputNames"].index("groundVMG")], best[sl],
                method="SLSQP", bounds=[(0,1)]*6,
                constraints=[
                    {"type":"eq", "fun":lambda y:self.evaluate(with_state(y))[row,:self.ne]},
                    {"type":"ineq", "fun":lambda y:self.evaluate(with_state(y))[row,self.ne+1:self.ne+self.ng]},
                ], options={"maxiter":budget,"ftol":1e-9})
            candidate = with_state(update.x)
            value = self.evaluate(candidate)[row]
            old = self.evaluate(best)[row]
            if np.abs(value[:self.ne]).max() <= self.c["equilibrium_tolerance"] and value[self.ne+1:self.ne+self.ng].min() >= -self.c["margin_tolerance"] and value[self.ne] >= old[self.ne]:
                best = candidate
        x = self.lower + best * self.span
        rows = self.evaluate(best)
        return {"seed":seed, "feasibilityStatus":int(phase.status), "feasibilityMessage":str(phase.message),
            "functionEvaluations":int(phase.nfev), "frontierMessage":str(frontier.message),
            "operatingFeasible":bool(np.abs(rows[:,:self.ne]).max() <= self.c["equilibrium_tolerance"] and rows[:,self.ne+1:self.ne+self.ng].min() >= -self.c["margin_tolerance"]), "optimizationMessage":str(refined.message) if refined is not None else None,
            "numericalFeasible":self.feasible(best), "maxEquilibriumResidual":float(np.abs(rows[:,:self.ne]).max()),
            "minimumMargin":float(rows[:,self.ne:self.ne+self.ng].min()), "residualNorm":float(np.linalg.norm(self.residual(best))),
            "design":dict(zip(self.c["designNames"], map(float,x[:self.nd]))),
            "states":x[self.nd:].reshape(-1,6).tolist(), "scenarioIndices":self.indices,
            "results":[dict(zip(self.c["outputNames"], map(float,row))) for row in rows]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starts", type=int, default=3)
    parser.add_argument("--budget", type=int, default=160)
    parser.add_argument("--scope", choices=["all","nominal","both"], default="both")
    parser.add_argument("--output", default="docs/analysis/design-search.json")
    args=parser.parse_args()
    if args.starts < 1 or args.budget < 1: parser.error("Positive search budget required")
    kernel=Kernel()
    groups={"full_envelope":range(len(kernel.contract["winds"])), "nominal_5ms":[2,3]}
    if args.scope=="all": groups.pop("nominal_5ms")
    if args.scope=="nominal": groups.pop("full_envelope")
    studies={}
    for name,indices in groups.items():
        problem=Problem(kernel,indices)
        runs=[]
        for i in range(args.starts):
            result=problem.run(17+i*23,args.budget)
            runs.append(result)
            print(name, result["seed"], "feasible=",result["numericalFeasible"], "eq=",round(result["maxEquilibriumResidual"],5), "min-margin=",round(result["minimumMargin"],5), flush=True)
        best=min(runs,key=lambda r:(not r["numericalFeasible"], not r["operatingFeasible"], r["results"][0]["totalMass"] if r["numericalFeasible"] else -min(v["groundVMG"] for v in r["results"]) if r["operatingFeasible"] else r["residualNorm"]))
        studies[name]={"best":best,"runs":runs}
    report={"schema":1,"scipy":scipy.__version__,"numpy":np.__version__,"budgetPerStart":args.budget,
        "contract":kernel.contract,"driverHashes":{name:hashlib.sha256((ROOT/name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for name in ("scripts/solve_design.py","scripts/native_design_kernel.py")},
        "supportedDesign":False,"studies":studies}
    (ROOT/args.output).write_bytes((json.dumps(report,indent=2,allow_nan=False)+"\n").encode())


if __name__=="__main__": main()
