"""Relax only hull length, then check fixed longer hulls using native physics."""
import argparse
import hashlib
import json
from io import BytesIO

import numpy as np
import scipy
from scipy.optimize import minimize

try:
    from .native_design_kernel import Kernel, ROOT
    from .prepare_design_search import native_value
    from .publish_design_search import result_model
    from .render_requirements import MODELS, native
    from .solve_design import Problem
except ImportError:
    from native_design_kernel import Kernel, ROOT
    from prepare_design_search import native_value
    from publish_design_search import result_model
    from render_requirements import MODELS, native
    from solve_design import Problem

STUDY_MODEL = ROOT / 'models/hull-length-study.sysml'
RESULT_MODEL = ROOT / 'models/hull-length-results.sysml'
CONTRACT = ROOT / '.tools/hull-length-contract.json'
REPORT = ROOT / 'docs/analysis/hull-length.json'


def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def check_sources(hashes):
    for name, expected in hashes.items():
        if digest(ROOT/name) != expected:
            raise ValueError('Stale hull-length study: ' + name)


def prepare():
    baseline = json.loads((ROOT/'.tools/design-search-contract.json').read_text(encoding='utf-8'))
    check_sources(baseline['sourceHashes'])
    response = json.loads(native('-analysis', 'BlueDogHullLengthStudy::LengthInputs', '-json', models=MODELS+(STUDY_MODEL,)))
    if response['status'] != 'holds' or response.get('diagnostics'):
        raise ValueError('Invalid native hull-length contract')
    contract = baseline | {v['name']:native_value(v['value']) for v in response['checks'][0]['values']}
    # Only the search domain changes; retain the same compiled physics parameters.
    if contract['parameterValues'] != baseline['parameterValues']:
        raise ValueError('Length study unexpectedly changes physics parameters')
    contract['sourceHashes'] = baseline['sourceHashes'] | {'models/hull-length-study.sysml':digest(STUDY_MODEL)}
    contract['generatedCHash'] = baseline['generatedCHash']
    CONTRACT.write_bytes((json.dumps(contract, indent=2)+'\n').encode())


def problem_for(kernel, indices, fixed_length=None):
    problem = Problem(kernel, indices)
    problem.upper[0] = kernel.contract['massImpliedLengthCeiling']
    if fixed_length is not None:
        problem.lower[0] = problem.upper[0] = fixed_length
    # At a fixed length the first normalized coordinate is inert. All physics
    # evaluations and the stored physical design have exactly the chosen length.
    problem.span = problem.upper-problem.lower
    return problem


def solve(problem, seed, budget, minimize_length):
    result = problem.run(seed, budget)
    result['lengthOptimizationMessage'] = None
    if minimize_length and result['numericalFeasible']:
        c = problem.c
        physical = np.r_[[result['design'][k] for k in c['designNames']], np.array(result['states']).ravel()]
        z = (physical-problem.lower)/problem.span
        answer = minimize(lambda x:x[0], z, method='SLSQP', bounds=[(0,1)]*len(z),
            constraints=[{'type':'eq','fun':problem.equality},{'type':'ineq','fun':problem.inequality}],
            options={'maxiter':budget,'ftol':1e-9})
        result['lengthOptimizationMessage'] = str(answer.message)
        if problem.feasible(answer.x) and answer.x[0] <= z[0]:
            x = problem.lower+answer.x*problem.span
            rows = problem.evaluate(answer.x)
            result.update(design=dict(zip(c['designNames'],map(float,x[:problem.nd]))),
                states=x[problem.nd:].reshape(-1,6).tolist(),
                results=[dict(zip(c['outputNames'],map(float,row))) for row in rows],
                maxEquilibriumResidual=float(np.abs(rows[:,:problem.ne]).max()),
                minimumMargin=float(rows[:,problem.ne:problem.ne+problem.ng].min()),
                residualNorm=float(np.linalg.norm(problem.residual(answer.x))))
    return result


def rank(result):
    return (not result['numericalFeasible'], not result['operatingFeasible'],
        result['design']['lwl_m'] if result['numericalFeasible'] else
        -min(v['groundVMG'] for v in result['results']) if result['operatingFeasible'] else result['residualNorm'])


def read_report():
    report = json.loads(REPORT.read_text(encoding='utf-8'))
    check_sources(report['contract']['sourceHashes'] | report['driverHashes'])
    if digest(ROOT/'docs/analysis/design-search.json') != report['baselineReportHash']:
        raise ValueError('Baseline comparison changed; rerun the hull-length study')
    return report


def subjects(report):
    return result_model(report).replace('BlueDogDesignResults', 'BlueDogHullLengthResults').replace(
        '; }', '; in attribute :>> designUpper = BlueDogHullLengthStudy::limits.relaxedUpper; }').replace(
        'scripts/publish_design_search.py', 'scripts/study_hull_length.py --publish')


def plot(audit, report):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    checks = {name:{v['name']:v['value'] for v in check['values']} for name,check in zip(report['studies'],json.loads(audit)['checks'],strict=True)}
    points = [(float(v['waterlineLength']),float(v['worstGroundVMG'])) for name,v in checks.items()
        if name.startswith('fixed_') and v['operatingFeasible']=='true']
    fig,ax = plt.subplots(figsize=(9,4.5))
    if points:
        ax.plot(*zip(*points), 'o-', color='#176a9b', label='Fixed length; other dimensions and trim reoptimized')
    best=checks['nominal_5ms']
    if best['operatingFeasible']=='true':
        ax.scatter([float(best['waterlineLength'])],[float(best['worstGroundVMG'])],s=110,marker='*',color='#b75a36',zorder=4,label='Free-length nominal search')
    ax.axhline(report['contract']['min_ground_m_s'],linestyle='--',color='#25776d',label='Required upstream VMG')
    ax.axhline(0,color='#777777',linewidth=.8)
    ax.axvline(report['contract']['upper'][0],linestyle=':',color='#999999',label='Former length cap')
    ax.set(xlabel='Waterline length (m)',ylabel='Worst upstream VMG (m/s)',title='Hull-length sensitivity: nominal 5 m/s wind, 1.5 m/s adverse current')
    ax.grid(alpha=.2); ax.legend(fontsize=8,loc='lower left')
    fig.text(.5,.015,'Local numerical results under the current mass, resistance and wing assumptions; negative VMG means downstream drift.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.04,1,1)); stream=BytesIO()
    fig.savefig(stream,format='png',dpi=150,metadata={'Software':'SV Blue Dog native SysML analysis'});plt.close(fig)
    return stream.getvalue()


def publication_outputs():
    report = read_report()
    if RESULT_MODEL.read_text(encoding='utf-8') != subjects(report):
        raise ValueError('Run python -m scripts.study_hull_length --publish')
    arguments=[]
    for name in report['studies']:
        arguments.extend(('-analysis',f'BlueDogHullLengthResults::{name}Audit'))
    models=MODELS+(STUDY_MODEL,RESULT_MODEL)
    audit=native(*arguments,'-json',models=models)
    if json.loads(audit).get('diagnostics'):
        raise ValueError('Native length audit has diagnostics')
    return {ROOT/'docs/analysis/hull-length-audit.json':audit,
        ROOT/'docs/hull-length-results.md':native('-render-document','BlueDogHullLengthDocuments::LengthReport',models=models),
        ROOT/'docs/figures/hull-length.png':plot(audit,report)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--prepare',action='store_true')
    mode.add_argument('--publish',action='store_true')
    parser.add_argument('--starts',type=int,default=5)
    parser.add_argument('--sweep-starts',type=int,default=3)
    parser.add_argument('--budget',type=int,default=350)
    args=parser.parse_args()
    if args.prepare: prepare(); return
    if args.publish: RESULT_MODEL.write_bytes(subjects(read_report()).encode()); return
    if min(args.starts,args.sweep_starts,args.budget)<1:parser.error('Positive search budgets required')
    kernel=Kernel()
    contract=json.loads(CONTRACT.read_text(encoding='utf-8'))
    check_sources(contract['sourceHashes'])
    if contract['parameterValues'] != kernel.contract['parameterValues'] or contract['generatedCHash'] != kernel.contract['generatedCHash']:
        raise ValueError('Length contract differs from compiled native kernel')
    kernel.contract=contract
    groups=[('full_envelope',list(range(len(contract['winds']))),None,args.starts),('nominal_5ms',[2,3],None,args.starts)]
    groups += [('fixed_'+str(length).replace('.','_'),[2,3],length,args.sweep_starts) for length in contract['sweepLengths']]
    studies={}
    for name,indices,length,starts in groups:
        runs=[]
        for i in range(starts):
            result=solve(problem_for(kernel,indices,length),17+23*i,args.budget,length is None)
            runs.append(result)
            print(name,result['seed'],'length=',round(result['design']['lwl_m'],3),'VMG=',round(min(v['groundVMG'] for v in result['results']),4),'operating=',result['operatingFeasible'],flush=True)
        studies[name]={'fixedLength':length,'best':min(runs,key=rank),'runs':runs}
    report={'schema':1,'scipy':scipy.__version__,'numpy':np.__version__,'budgetPerStart':args.budget,'contract':contract,
        'baselineReportHash':digest(ROOT/'docs/analysis/design-search.json'),
        'driverHashes':{name:digest(ROOT/name) for name in ('scripts/study_hull_length.py','scripts/solve_design.py','scripts/native_design_kernel.py')},
        'supportedDesign':False,'studies':studies}
    REPORT.write_bytes((json.dumps(report,indent=2,allow_nan=False)+'\n').encode())


if __name__=='__main__':main()
