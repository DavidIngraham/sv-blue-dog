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
STRUCTURE = ROOT/'models/structure.sysml'
ROUTE = ROOT/'models/sizing-route.sysml'
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
    r = json.loads(native('-analysis', 'BlueDogOpenSizing::Inputs', '-json', models=MODELS+(STRUCTURE,ROUTE,MODEL,)))
    if r['status'] != 'holds' or r.get('diagnostics'):
        raise ValueError('Invalid sizing inputs')
    c.update({v['name']:native_value(v['value']) for v in r['checks'][0]['values']})
    c['outputNames'][5] = 'wing_height_unconstrained'
    native('-compile', 'BlueDogOpenSizing::EvaluateCase', '-source', '-o', str(ROOT/'.tools/open-sizing.c'), models=MODELS+(STRUCTURE,ROUTE,MODEL,))
    c['sourceHashes']['models/open-sizing.sysml'] = digest(MODEL)
    c['sourceHashes']['models/structure.sysml'] = digest(STRUCTURE)
    c['sourceHashes']['models/sizing-route.sysml'] = digest(ROUTE)
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
        if [a.size for a in arrays] != [len(self.contract['designNames']), len(self.contract['parameterNames']), 9] or any(a.ndim != 1 or not np.isfinite(a).all() for a in arrays):
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
    lo,hi=np.asarray(lower),np.asarray(upper)
    # Relative to the endpoint/value, not the full bracket: a small servo is
    # not boundary-limited merely because its mass-implied ceiling is enormous.
    near_lower=x-lo <= np.maximum(1e-8,tolerance*np.maximum(np.abs(lo),np.abs(x)))
    near_upper=hi-x <= np.maximum(1e-8,tolerance*np.maximum(np.abs(hi),np.abs(x)))
    return [{'name':name,'index':i,'side':side,'value':float(x[i])}
        for i,name in enumerate(names) for side,hit in [('lower',near_lower[i]),('upper',near_upper[i])] if hit]


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
            def structural_start(seed):
                # A physically scaled starting point, not a fixed design. Uniform
                # draws across large capacity/geometry brackets overwhelm the first solve.
                base=np.array([1.8,.35,.5,3,.06,.6,.025,.3,3,-.05,220,.25,1,.15,.42,.6,.4,.8,.8,.06])
                if seed!=17: base *= np.exp(np.random.default_rng(seed).normal(0,.25,len(base)))
                states=np.array([[1.0,50 if c['windward'][i] else 130,6,3,-2,8] for i in indices])
                return np.clip((np.r_[base,states.ravel()]-p.lower)/p.span,1e-6,1-1e-6)
            p.initial=structural_start
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
        # Manufacture whole 200 g/m2 plies, then re-solve all geometry and trim.
        # The rounded recipe is one discrete candidate, not an integer global optimum.
        relaxed=best
        recipe=np.ceil(np.array([best['design'][n] for n in c['designNames'][15:19]])/.2-1e-8)*.2
        q=Problem(kernel,indices)
        q.lower[:q.nd]=history[-1]['lower'];q.upper[:q.nd]=history[-1]['upper']
        q.lower[15:19]=recipe;q.upper[15:19]=recipe;q.span=q.upper-q.lower
        x=np.r_[[best['design'][n] for n in c['designNames']],np.array(best['states']).ravel()]
        z=np.divide(x-q.lower,q.span,out=np.zeros_like(x),where=q.span!=0)
        q.initial=lambda seed:np.clip(z,0,1)
        rounded=q.run(17,budget)
        hits=boundary_hits(rounded,history[-1]['lower'],np.maximum(history[-1]['upper'],q.upper[:q.nd]),c['designNames'])
        print(name,'whole plies',recipe/.2,'operating',rounded['operatingFeasible'],
            'VMG',min(v['groundVMG'] for v in rounded['results']),flush=True)
        studies[name]={'best':rounded,'continuousBest':relaxed,'plyCounts':(recipe/.2).round().astype(int).tolist(),
            'rounds':history,'roundedBoundaryHits':hits,'boundaryLimited':any(c['expandable'+h['side'].title()][h['index']] for h in hits)}
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
    water_index=c['outputNames'].index('waterVMG')+1
    lines += ['    part route : BlueDogSizingRoute::Profile {',
        '        attribute :>> waterVMG = ('+', '.join(f'stress_cases_{i}.rows#({water_index})' for i in range(8))+');',
        '    }', '    analysis routeAudit : BlueDogSizingRoute::Assessment { subject :>> profile = route; }']
    source='\n'.join(lines+['}',''])
    path=ROOT/'.tools/open-sizing-replay.sysml';path.write_text(source,encoding='utf-8')
    audit=native(*arguments,'-json',models=MODELS+(STRUCTURE,ROUTE,MODEL,path))
    replay=json.loads(audit)
    if replay['status']!='holds' or replay.get('diagnostics'): raise ValueError('Sizing replay failed')
    actual=[native_value(next(v['value'] for v in case['values'] if v['name']=='rows')) for case in replay['checks']]
    np.testing.assert_allclose(actual,expected,rtol=1e-9,atol=1e-7)
    route_audit=native('-analysis','BlueDogOpenSizingResults::routeAudit','-json',models=MODELS+(STRUCTURE,ROUTE,MODEL,path))
    route_json=json.loads(route_audit)
    if route_json['status']!='holds' or route_json.get('diagnostics'): raise ValueError('Route audit failed')
    route_values={v['name']:v['value'] for v in route_json['checks'][0]['values']}

    text=['# Joint sizing results','', '<!-- Generated by scripts.study_open_sizing; edit the model and rerun. -->','',
        'Twenty sizing variables vary together, including laminate dry-glass mass and hull rib spacing. Objective: find a numerical progress fit, then minimize total mass. No minimum-length objective.',
        '', 'These stationary cases retain 1.5 m/s adverse current at every point. Passing is a numerical screen, not Q-101 mission qualification. FDM/glass mass, beam strength/stiffness, panel pressure, freeboard, reserve buoyancy and launch clearance are screened. Continuous layup sizing is rounded upward to whole 200 g/m2 plies, then geometry and trim are reoptimized. Physical evidence remains outstanding.', '',
        '| Screen | Balanced / hardware fit | Progress fit | Worst ground VMG (m/s) | Total mass (kg) | Numerical boundary limited |',
        '| --- | --- | --- | ---: | ---: | --- |']
    for name,study in report['studies'].items():
        b=study['best'];text.append(f'| {name} | {b["operatingFeasible"]} | {b["numericalFeasible"]} | {min(r["groundVMG"] for r in b["results"]):.3f} | {b["results"][0]["totalMass"]:.2f} | {study["boundaryLimited"]} |')
    text+=['','| Sizing variable | Nominal | Stress cases |','| --- | ---: | ---: |']
    for key in c['designNames']:
        text.append('| '+key+' | '+' | '.join(f'{s["best"]["design"][key]:.4g}' for s in report['studies'].values())+' |')
    text+=['','## Structural and hydrostatic outputs','', '| Quantity | Nominal | Stress cases |', '| --- | ---: | ---: |']
    for key in ('hullArealMass','wingStructuralMass','keelStructuralMass','rudderStructuralMass','keelStressMPa','keelTipDeflection','deckEdgeFreeboard','reserveDisplacementFraction','immersedDepth'):
        text.append('| '+key+' | '+' | '.join(f'{study["best"]["results"][0][key]:.4g}' for study in report['studies'].values())+' |')
    text+=['','[Construction assumptions and units](structure-sizing.md) / [Traced requirements](structure-requirements.md)']
    text+=['','## Declared route profile','',
        'Native time-weighted assessment of the stress-case design, with signed downstream/upstream current and negative-progress intervals retained. The weather fractions and hold strategy are illustrative, not accepted field evidence.',
        '', '| Downstream mean (m/s) | Upstream mean (m/s) | Progress met | Elapsed hours | Mission supported |',
        '| ---: | ---: | --- | --- | --- |',
        '| '+' | '.join(route_values[k] for k in ('downstreamMean','upstreamMean','progressMet','elapsedHours','missionSupported'))+' |',
        '', 'The optimizer still uses the stationary stress screen; this route assessment is a separate Q-101/Q-102 interpretation. It does not optimize a route or assert a safe holding strategy.',
        '', '## Layup selection', '',
        'Dry fabric is rounded upward to 200 g/m2 plies, then geometry and trim are re-solved. Ply counts (hull / wing / keel / rudder):','']
    for name,study in report['studies'].items(): text.append(f'- {name}: '+ ' / '.join(map(str,study['plyCounts'])))
    text+=['','## Search boundaries','', 'Expandable bounds are numerical brackets, not requirements. Bounds within 0.5% relative to the endpoint/value (absolute floor 1e-8) are flagged; brackets expand between rounds. Remaining hits are unresolved, not accepted design limits. Assembly mass and placement constraints remain enforced.']
    for name,s in report['studies'].items():
        text+=['',f'**{name}:** '+(', '.join(h['name']+' ('+h['side']+')' for h in s['roundedBoundaryHits']) or 'No sizing boundary hits.')]
    text+=['','[Method and assumptions](design-search.md#joint-sizing-without-premature-dimension-caps)  [Search record](analysis/open-sizing.json)  [Native replay](analysis/open-sizing-audit.json)','']
    return {ROOT/'docs/analysis/sizing-route-audit.json':route_audit, ROOT/'docs/structure-requirements.md':native('-render-document','BlueDogStructureDocuments::StructureReport','-diagram-form','mermaid',models=MODELS+(STRUCTURE,ROUTE,MODEL)),ROOT/'models/open-sizing-results.sysml':source,ROOT/'docs/analysis/open-sizing-audit.json':audit,ROOT/'docs/open-sizing-results.md':'\n'.join(text)}


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
