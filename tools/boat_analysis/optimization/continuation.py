"""Trace fixed-length feasibility without changing physical acceptance criteria."""
import json
import time
from types import SimpleNamespace
import numpy as np
from scipy.optimize import least_squares, minimize

from .search import Problem
from ..evidence.records import CURRENT, run_record, output_path, source_hashes, validate
from ..model.runtime import ROOT


def solve_stage(problem, seed, length, budget=60, extensions=2):
    """Remove length from the unknowns; extend only while violations improve."""
    fixed = (length - problem.lo[0]) / problem.span[0]
    if not 0 <= fixed <= 1:
        raise ValueError('Requested length outside the model search bounds')
    def expand(y):
        return np.r_[fixed, y]
    def residual(y):
        return problem.residual(expand(y))
    def jacobian(y):
        return problem.residual_jacobian(expand(y))[:, 1:]
    best = np.clip(np.asarray(seed)[1:], 0, 1)
    history = []
    class FeasibleIterate(Exception):
        def __init__(self, x):
            self.x = np.array(x, copy=True)
    for chunk in range(extensions + 1):
        before = float(np.linalg.norm(residual(best)))
        if problem.feasible(expand(best)):
            break
        anchor = best.copy()
        constraints = [
            {'type':'eq', 'fun':lambda y:problem.evaluate(expand(y))['eq'],
             'jac':lambda y:problem.jacobians(expand(y))[0][:, 1:]},
            {'type':'ineq', 'fun':lambda y:problem.evaluate(expand(y))['ineq'],
             'jac':lambda y:problem.jacobians(expand(y))[1][:, 1:]}]
        iterations = 0
        best_iterate = anchor.copy()
        best_merit = before
        def accept_iterate(y):
            nonlocal iterations, best_iterate, best_merit
            iterations += 1
            merit = float(np.linalg.norm(residual(y)))
            if merit < best_merit:
                best_iterate, best_merit = np.array(y, copy=True), merit
            if problem.feasible(expand(y)):
                raise FeasibleIterate(y)
        try:
            correction = minimize(lambda y:.5*np.sum((y-anchor)**2), anchor,
                                  jac=lambda y:y-anchor, method='SLSQP', callback=accept_iterate,
                                  bounds=[(0,1)]*len(anchor), constraints=constraints,
                                  options={'maxiter':budget, 'ftol':1e-8})
        except FeasibleIterate as found:
            correction = SimpleNamespace(x=found.x, nit=iterations,
                                         message='Stopped at a freshly checked feasible iterate')
        corrected = float(np.linalg.norm(residual(correction.x)))
        history.append(dict(chunk=chunk, method='SLSQP', before=before, after=corrected,
                            iterations=correction.nit, message=str(correction.message)))
        if corrected < before or problem.feasible(expand(correction.x)):
            best = correction.x
        if problem.feasible(expand(best)):
            break
        if best_merit < float(np.linalg.norm(residual(best))):
            best = best_iterate
        def stop(intermediate_result):
            if problem.feasible(expand(intermediate_result.x)):
                raise StopIteration
        result = least_squares(residual, best, jac=jacobian, bounds=(0, 1),
                               max_nfev=budget, callback=stop,
                               ftol=1e-8, xtol=1e-8, gtol=1e-8)
        after = float(np.linalg.norm(residual(result.x)))
        history.append(dict(chunk=chunk, method='least_squares', before=before, after=after,
                            evaluations=result.nfev, message=str(result.message)))
        if after < float(np.linalg.norm(residual(best))):
            best = result.x
        if problem.feasible(expand(best)) or after >= before * .95:
            break
    z = expand(best)
    r = problem.evaluate(z)
    details = {}
    if 'mass' in r:
        from ..geometry.vessel import operating_envelope
        design=dict(zip(problem.model.c['designNames'], (problem.lo+z*problem.span)[:29]))
        details=dict(mass=r['mass'],concept=r['concept'],westerlyRoute=r['westerlyRoute'].tolist(),
                     operating=r['rows'],stateRows=r['states'].tolist(),
                     envelope=operating_envelope(design,problem.model.parameters[33]))
    return dict(**details,lengthM=length, feasible=problem.feasible(z),
                merit=float(np.linalg.norm(problem.residual(z))),
                maxEquilibriumResidual=float(np.max(np.abs(r['eq']))),
                minimumMargin=float(np.min(r['ineq'])),
                worstConstraints=sorted(zip(problem.constraint_names, map(float, r['ineq'])), key=lambda x:x[1])[:12],
                normalizedDesignAndStates=z.tolist(), history=history,
                design=dict(zip(problem.model.c['designNames'], (problem.lo+z*problem.span)[:29])))


def run(target=1.2, step=.2, minimum_step=.025, budget=60, extensions=2, seed_run="2026-10-12-appendage-credibility"):
    if not 0 < minimum_step <= step or budget < 1 or extensions < 0:
        raise ValueError('Invalid continuation settings')
    p = Problem()
    p.checkpoint_path = ROOT / '.tools/continuation-progress.json'
    seed_directory = ROOT/'evidence/runs'/seed_run
    saved = run_record(seed_directory, 'sizing-continuation.json')
    accepted = np.array(saved['smallestFeasibleZ'])
    hashes = source_hashes(list(saved['sourceHashes']) + list(p.context['sourceHashes']) + [
        'tools/boat_analysis/optimization/continuation.py',
        'tools/boat_analysis/optimization/search.py',
        str((seed_directory/'sizing-continuation.json').relative_to(ROOT)),
        'tools/boat_analysis/geometry/vessel.py'])
    seed_restoration = None
    if not p.feasible(accepted):
        seed_length = float((p.lo + accepted*p.span)[0])
        seed_restoration = solve_stage(p, accepted, seed_length, budget, extensions)
        validate(hashes)
        seed_restoration.update(sourceHashes=hashes, qualified=False)
        output_path('sizing-seed-restoration.json').write_text(json.dumps(seed_restoration, indent=2)+'\n')
        if not seed_restoration['feasible']:
            raise ValueError('Seed restoration failed under current constraints; inspect sizing-seed-restoration.json before reducing length')
        accepted = np.array(seed_restoration['normalizedDesignAndStates'])
    length = float((p.lo + accepted*p.span)[0])
    if not p.lo[0] <= target < length:
        raise ValueError('Target must be below the seed and within model bounds')
    report = dict(sourceHashes=hashes, seedRun=seed_run, targetM=target,
                  settings=dict(stepM=step, minimumStepM=minimum_step, budget=budget, extensions=extensions),
                  attempts=[], seedRestoration=seed_restoration, qualified=False, completed=False,
                  scope='Fixed-length coarse feasibility continuation; no physical requirements relaxed. Not a minimum-size proof or refined verification.')
    started = time.time()
    best_infeasible = None
    def save():
        validate(hashes)
        report.update(smallestFeasibleLengthM=length, smallestFeasibleZ=accepted.tolist(),
                      bestInfeasible=best_infeasible, elapsedSeconds=time.time()-started)
        output_path('sizing-continuation.json').write_text(json.dumps(report, indent=2)+'\n')
    save()
    while length > target + 1e-8:
        proposed = max(target, round(length-step, 9))
        # Reach round-number milestones from a non-round starting length.
        if not report['attempts']:
            proposed = max(target, round(np.floor((length-1e-8)/step)*step, 9))
        print(f'CONTINUATION {length:.3f} -> {proposed:.3f} m', flush=True)
        attempt = solve_stage(p, accepted, proposed, budget, extensions)
        report['attempts'].append(attempt)
        if not attempt['feasible']:
            # A second physically distinct seed retains greater hull volume and
            # lowers wing/ballast loading. Only an initial guess, never a bound.
            alternative = accepted.copy()
            physical = p.lo + alternative*p.span
            physical[1] *= 1.08
            physical[4] *= .9
            physical[15] *= .9
            alternative = np.clip((physical-p.lo)/p.span, 0, 1)
            second = solve_stage(p, alternative, proposed, budget, extensions)
            second['seedVariant'] = 'wider hull, reduced wing and ballast'
            report['attempts'].append(second)
            if second['feasible'] or second['merit'] < attempt['merit']:
                attempt = second
        if attempt['feasible']:
            accepted = np.array(attempt['normalizedDesignAndStates'])
            length = proposed
            print(f'ACCEPTED {length:.3f} m', flush=True)
            save()  # Preserve numerical evidence before generating presentation artifacts.
            from ..geometry.export import export_candidate
            export_candidate(p.model, attempt['design'], ROOT/'build/analysis/concepts'/f'candidate-{length:.3f}.glb', provenance={'sourceHashes':hashes,'stageLengthM':length,'qualified':False})
        else:
            if best_infeasible is None or attempt['merit'] < best_infeasible['merit']:
                best_infeasible = attempt
            step /= 2
            print(f'UNRESOLVED {proposed:.3f} m; next step {step:.3f} m', flush=True)
        save()
        if step < minimum_step:
            break
    report.update(completed=True, targetReached=length <= target+1e-8)
    save()
    print(f'FINISHED smallest coarse-feasible length {length:.3f} m', flush=True)
