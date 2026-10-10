"""Joint sizing with expandable numerical brackets and native replay."""
import argparse
import ctypes as ct
import hashlib
import json
import subprocess
import threading

import numpy as np

from .native_design_kernel import Kernel, Sequence, ROOT
from .prepare_design_search import native_value
from .render_requirements import MODELS, native
from .solve_design import Problem

MODEL = ROOT/'models/open-sizing.sysml'
CONTRACT = ROOT/'.tools/open-sizing-contract.json'
REPORT = ROOT/'docs/analysis/open-sizing.json'
DRIVERS = ('scripts/study_open_sizing.py', 'scripts/solve_design.py', 'scripts/native_design_kernel.py')


def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def validate(hashes):
    for name, expected in hashes.items():
        if digest(ROOT/name) != expected:
            raise ValueError('Stale open sizing input: '+name)


def prepare():
    c = json.loads((ROOT/'.tools/design-search-contract.json').read_text(encoding='utf-8'))
    validate(c['sourceHashes'])
    r = json.loads(native('-analysis', 'BlueDogOpenSizing::Inputs', '-json', models=MODELS+(MODEL,)))
    if r['status'] != 'holds' or r.get('diagnostics'):
        raise ValueError('Invalid sizing inputs')
    c.update({v['name']:native_value(v['value']) for v in r['checks'][0]['values']})
    c['outputNames'][5] = 'wing_height_unconstrained'
    native('-compile', 'BlueDogOpenSizing::EvaluateCase', '-source', '-o', str(ROOT/'.tools/open-sizing.c'), models=MODELS+(MODEL,))
    c['sourceHashes']['models/open-sizing.sysml'] = digest(MODEL)
    c['generatedCHash'] = hashlib.sha256((ROOT/'.tools/open-sizing.c').read_bytes()).hexdigest()
    CONTRACT.write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')


class SizingKernel(Kernel):
    def __init__(self):
        self.contract = json.loads(CONTRACT.read_text(encoding='utf-8'))
        validate(self.contract['sourceHashes'])
        source, library = ROOT/'.tools/open-sizing.c', ROOT/'.tools/open-sizing.so'
        if hashlib.sha256(source.read_bytes()).hexdigest() != self.contract['generatedCHash']:
            raise ValueError('Stale compiled sizing source')
        subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.lib = ct.CDLL(str(library))
        self.lib.sysml_run.argtypes = [Sequence,Sequence,Sequence,ct.POINTER(Sequence)]
        self.lib.sysml_run.restype = ct.c_int
        self.lib.sysml_error.restype = ct.c_char_p
        self.parameters = np.asarray(self.contract['parameterValues'],dtype=float)
        self.lock = threading.Lock()


    def evaluate(self, design, scenario):
        arrays = [np.ascontiguousarray(a, dtype=np.float64) for a in (design, self.parameters, scenario)]
        if [a.size for a in arrays] != [15, len(self.contract['parameterNames']), 9] or any(a.ndim != 1 or not np.isfinite(a).all() for a in arrays):
            raise ValueError('Invalid sizing kernel inputs')
        args = [Sequence(2, a.size, a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with self.lock:
            output = Sequence()
            if self.lib.sysml_run(*args, ct.byref(output)):
                raise ValueError(self.lib.sysml_error().decode())
            if output.shape != 2 or output.length != len(self.contract['outputNames']):
                raise ValueError('Unexpected native sizing output representation')
            rows = np.ctypeslib.as_array(output.data, shape=(output.length,)).copy()
        if not np.isfinite(rows).all(): raise ValueError('Nonfinite sizing output')
        return rows


def boundary_hits(result, lower, upper, names, tolerance=0.005):
    x = np.array([result['design'][name] for name in names])
    z = (x-np.asarray(lower))/(np.asarray(upper)-lower)
    return [{'name':name,'index':i,'side':side,'value':float(x[i])}
        for i,name in enumerate(names) for side,hit in [('lower',z[i]<=tolerance),('upper',z[i]>=1-tolerance)] if hit]


def expanded_bounds(c, lower, upper, hits):
    lower,upper = np.array(lower,copy=True),np.array(upper,copy=True)
    for hit in hits:
        i=hit['index']; side=hit['side']
        if c['expandable'+side.title()][i]:
            if side=='lower': lower[i] *= 0.5
            else: upper[i] *= 2
    return lower,upper


def rank(r):
    return (not r['numericalFeasible'],not r['operatingFeasible'],
        r['results'][0]['totalMass'] if r['numericalFeasible'] else
        -min(v['groundVMG'] for v in r['results']) if r['operatingFeasible'] else r['residualNorm'])


def run(starts, budget, rounds):
    kernel=SizingKernel(); c=kernel.contract; studies={}
    for name,indices in [('nominal_5ms',[2,3]),('stress_cases',list(range(8)))]:
        lower=np.array(c['lower']); upper=np.array(c['upper']); history=[]; warm=None
        for iteration in range(rounds):
            p=Problem(kernel,indices); p.lower[:p.nd]=lower; p.upper[:p.nd]=upper; p.span=p.upper-p.lower
            original_initial=p.initial
            # Transfer the nominal geometry as one stress-case start; keep the
            # other random starts so the larger problem can find other basins.
            if warm is None and name == 'stress_cases':
                nominal = studies['nominal_5ms']['best']
                x = np.r_[[nominal['design'][n] for n in c['designNames']],
                    np.array([nominal['states'][0 if c['windward'][i] else 1] for i in indices]).ravel()]
                initial_nominal = np.clip((x-p.lower)/p.span,1e-6,1-1e-6)
                p.initial = lambda seed: initial_nominal.copy() if seed == 17 else original_initial(seed)
            if warm is not None:
                x=np.r_[[warm['design'][n] for n in c['designNames']],np.array(warm['states']).ravel()]
                warm_z=np.clip((x-p.lower)/p.span,1e-6,1-1e-6)
                p.initial=lambda seed: warm_z.copy() if seed==17 else original_initial(seed)
            runs=[p.run(17+23*i,budget) for i in range(starts)]
            # Keep a feasible earlier candidate if a larger bracket makes convergence harder.
            if warm is not None: runs.append(warm)
            best=min(runs,key=rank)
            hits=boundary_hits(best,lower,upper,c['designNames'])
            history.append({'lower':lower.tolist(),'upper':upper.tolist(),'runs':runs,'best':best,'boundaryHits':hits})
            print(name,iteration,'feasible',best['numericalFeasible'],'VMG',min(v['groundVMG'] for v in best['results']),
                'mass',best['results'][0]['totalMass'],'boundaries',[(h['name'],h['side']) for h in hits],flush=True)
            next_lower,next_upper=expanded_bounds(c,lower,upper,hits)
            if np.array_equal(lower,next_lower) and np.array_equal(upper,next_upper): break
            lower,upper=next_lower,next_upper; warm=best
        studies[name]={'best':best,'rounds':history,'boundaryLimited':any(c['expandable'+h['side'].title()][h['index']] for h in hits)}
    report={'schema':1,'contract':c,'driverHashes':{n:digest(ROOT/n) for n in DRIVERS},
        'startsPerRound':starts,'budgetPerStart':budget,'maximumRounds':rounds,
        'scope':'Stationary progress screens, not route-integrated mission feasibility',
        'supportedDesign':False,'studies':studies}
    REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def read_report():
    report=json.loads(REPORT.read_text(encoding='utf-8'))
    validate(report['contract']['sourceHashes']|report['driverHashes'])
    return report


def publication_outputs():
    report=read_report(); c=report['contract']; lines=['package BlueDogOpenSizingResults {']; arguments=[]
    expected=[]
    seq=lambda values:'('+', '.join(format(float(x),'.17g') for x in values)+')'
    for name,study in report['studies'].items():
        b=study['best']
        for n,(idx,state,row) in enumerate(zip(b['scenarioIndices'],b['states'],b['results'],strict=True)):
            label=f'{name}_{n}'
            scenario=[c['winds'][idx],int(c['windward'][idx]),c['foulingDrag'][idx],*state]
            lines += [f'    part {label}Input : BlueDogOpenSizing::Candidate {{',
                f'        attribute :>> design = {seq([b["design"][key] for key in c["designNames"]])};',
                f'        attribute :>> scenario = {seq(scenario)};', '    }',
                f'    analysis {label} : BlueDogOpenSizing::Audit {{ subject :>> trial = {label}Input; }}']
            arguments.extend(('-analysis','BlueDogOpenSizingResults::'+label))
            expected.append([row[key] for key in c['outputNames']])
    source='\n'.join(lines+['}',''])
    path=ROOT/'.tools/open-sizing-replay.sysml';path.write_text(source,encoding='utf-8')
    audit=native(*arguments,'-json',models=MODELS+(MODEL,path))
    replay=json.loads(audit)
    if replay['status']!='holds' or replay.get('diagnostics'): raise ValueError('Sizing replay failed')
    actual=[native_value(next(v['value'] for v in case['values'] if v['name']=='rows')) for case in replay['checks']]
    np.testing.assert_allclose(actual,expected,rtol=1e-9,atol=1e-7)
    text=['# Joint sizing results','', '<!-- Generated by scripts.study_open_sizing; edit the model and rerun. -->','',
        'All fifteen sizing variables vary together. Objective: find a numerical progress fit, then minimize total mass. No minimum-length objective.',
        '', 'These stationary cases retain 1.5 m/s adverse current at every point. Passing is a numerical screen, not Q-101 mission qualification. Structural, freeboard and route-profile evidence remain outstanding.', '',
        '| Screen | Balanced / hardware fit | Progress fit | Worst ground VMG (m/s) | Total mass (kg) | Numerical boundary limited |',
        '| --- | --- | --- | ---: | ---: | --- |']
    for name,study in report['studies'].items():
        b=study['best'];text.append(f'| {name} | {b["operatingFeasible"]} | {b["numericalFeasible"]} | {min(r["groundVMG"] for r in b["results"]):.3f} | {b["results"][0]["totalMass"]:.2f} | {study["boundaryLimited"]} |')
    text+=['','| Sizing variable | Nominal | Stress cases |','| --- | ---: | ---: |']
    for key in c['designNames']:
        text.append('| '+key+' | '+' | '.join(f'{s["best"]["design"][key]:.4g}' for s in report['studies'].values())+' |')
    text+=['','## Search boundaries','', 'Expandable bounds are numerical brackets, not requirements. Bounds within 0.5% of their range are flagged; brackets expand between rounds. Remaining hits are unresolved, not accepted design limits. Assembly mass and placement constraints remain enforced.']
    for name,s in report['studies'].items():
        text+=['',f'**{name}:** '+(', '.join(h['name']+' ('+h['side']+')' for h in s['rounds'][-1]['boundaryHits']) or 'No sizing boundary hits.')]
    text+=['','[Method and assumptions](design-search.md#joint-sizing-without-premature-dimension-caps)  [Search record](analysis/open-sizing.json)  [Native replay](analysis/open-sizing-audit.json)','']
    return {ROOT/'models/open-sizing-results.sysml':source,ROOT/'docs/analysis/open-sizing-audit.json':audit,ROOT/'docs/open-sizing-results.md':'\n'.join(text)}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare',action='store_true');p.add_argument('--publish',action='store_true')
    p.add_argument('--starts',type=int,default=3);p.add_argument('--budget',type=int,default=350);p.add_argument('--rounds',type=int,default=3)
    a=p.parse_args()
    if min(a.starts,a.budget,a.rounds)<1: p.error('Positive budgets required')
    if a.prepare: prepare()
    elif a.publish:
        for path,content in publication_outputs().items():path.write_text(content,encoding='utf-8')
    else:run(a.starts,a.budget,a.rounds)


if __name__=='__main__':main()
