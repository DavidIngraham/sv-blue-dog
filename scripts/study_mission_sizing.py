"""Two-metre architecture comparison, native polar physics and route optimization."""
import argparse
import ctypes as ct
import json
import subprocess
import threading
import numpy as np
from scipy.optimize import least_squares, minimize
from .native_design_kernel import ROOT, Sequence
from .study_open_sizing import SizingKernel, digest, validate, CONTRACT, STRUCTURE, ROUTE, MODEL, boundary_hits, expanded_bounds
from .render_requirements import MODELS, native
from .prepare_design_search import native_value
from .solve_design import Problem

SOURCE = ROOT/'models/mission-sizing.sysml'
MODELS_NEW = MODELS+(STRUCTURE,ROUTE,MODEL,SOURCE)
RECORD = ROOT/'docs/analysis/mission-sizing.json'
CONTRACT_NEW = ROOT/'.tools/mission-sizing-contract.json'
DRIVERS = ('scripts/study_mission_sizing.py','scripts/solve_design.py')


def prepare():
    c=json.loads(CONTRACT.read_text(encoding='utf-8'));validate(c['sourceHashes'])
    settings=json.loads(native('-analysis','BlueDogMissionSizing::Inputs','-json',models=MODELS_NEW))
    inputs={v['name']:native_value(v['value']) for v in settings['checks'][0]['values']}
    c.update(inputs)
    c['parameterNames']+=['ribbedArchitecture','assemblyLimit','attachmentMass','ribWall','ribPitch','cgBelowBottom']
    c['parameterValues']+=[1]+inputs['extraParameters']
    c['outputNames'][4]='route_progress_external'
    c['outputNames'].insert(46,'low_mass_center')
    c['outputNames']+=['transportBodyMass','batteryMass','centerOfGravity','cgBelowBottom']
    c['marginCount']+=1
    c['sourceHashes']['models/mission-sizing.sysml']=digest(SOURCE)
    for target,name in [('EvaluateCase','mission-sizing'),('Route','mission-route')]:
        native('-compile','BlueDogMissionSizing::'+target,'-source','-o',str(ROOT/f'.tools/{name}.c'),models=MODELS_NEW)
    c['generatedHashes']={name:digest(ROOT/f'.tools/{name}.c') for name in ['mission-sizing','mission-route']}
    CONTRACT_NEW.write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')


class MissionKernel(SizingKernel):
    def __init__(self,architecture):
        self.contract=json.loads(CONTRACT_NEW.read_text(encoding='utf-8'));validate(self.contract['sourceHashes'])
        for name,expected in self.contract['generatedHashes'].items():
            source=ROOT/f'.tools/{name}.c';lib=ROOT/f'.tools/{name}.so'
            if digest(source)!=expected:raise ValueError('Stale native C')
            subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(lib)],check=True)
            dll=ct.CDLL(str(lib));dll.sysml_error.restype=ct.c_char_p;dll.sysml_run.restype=ct.c_int
            if name=='mission-sizing':
                self.lib=dll;dll.sysml_run.argtypes=[Sequence,Sequence,Sequence,ct.POINTER(Sequence)]
            else:
                self.route_lib=dll;dll.sysml_run.argtypes=[Sequence,Sequence,ct.POINTER(Sequence)]
        self.parameters=np.array(self.contract['parameterValues'],dtype=float)
        self.parameters[97]=architecture
        self.lock=threading.Lock()

    def route(self,water):
        a=np.ascontiguousarray(water,dtype=np.float64)
        if a.shape!=(4,) or not np.isfinite(a).all():raise ValueError('Four finite VMGs required')
        with self.lock:
            out=Sequence();arg=Sequence(2,4,a.ctypes.data_as(ct.POINTER(ct.c_double)))
            q=np.ascontiguousarray(self.contract['routeParameters'],dtype=np.float64)
            par=Sequence(2,len(q),q.ctypes.data_as(ct.POINTER(ct.c_double)))
            if self.route_lib.sysml_run(arg,par,ct.byref(out)):raise ValueError(self.route_lib.sysml_error().decode())
            if out.shape!=2 or out.length!=4:raise ValueError('Route ABI mismatch')
            return np.ctypeslib.as_array(out.data,shape=(4,)).copy()


class MissionProblem(Problem):
    def __init__(self,kernel):
        super().__init__(kernel,[0,1,2,3])
        self.environment=np.array([[w,up,1] for w in self.c['routeWinds'] for up in [1,0]],dtype=float)
        self.lower[0]=self.upper[0]=self.c['waterline']
        self.span=self.upper-self.lower
        self.vi=self.c['outputNames'].index('waterVMG')

    def route(self,z):return self.kernel.route(self.evaluate(z)[:,self.vi])

    def hardware(self,z):return self.evaluate(z)[:,5:self.ne+self.ng].ravel()

    def seed(self,number):
        d=np.array([2,.58,1.0,4,.08,.65,.025,.25,5,-.05,230,.25,.6,.17,.45,.6,.4,1.6,1.0,.029])
        if number!=17:d[1:]*=np.exp(np.random.default_rng(number).normal(0,.2,len(d)-1))
        states=np.array([[1.5,50 if e[1] else 140,8,3,-2,10] for e in self.environment])
        x=np.r_[d,states.ravel()]
        return np.clip(np.divide(x-self.lower,self.span,out=np.zeros_like(x),where=self.span!=0),0,1)

    def solve(self,seed,budget,initial=None):
        z=self.seed(seed) if initial is None else initial
        fit=least_squares(lambda x:np.r_[self.equality(x),np.minimum(self.hardware(x),0)],z,bounds=(0,1),max_nfev=budget)
        constraints=[{'type':'eq','fun':self.equality},{'type':'ineq','fun':self.hardware}]
        frontier=minimize(lambda x:-self.route(x)[3],fit.x,method='SLSQP',bounds=[(0,1)]*len(z),constraints=constraints,options={'maxiter':budget,'ftol':1e-8})
        def valid(x):return np.abs(self.equality(x)).max()<=.001 and self.hardware(x).min()>=-.0001
        options=[x for x in [fit.x,frontier.x] if valid(x)]
        best=max(options,key=lambda x:self.route(x)[3]) if options else fit.x
        # Preserve a useful route margin before considering mass. No claim of
        # equal slack in unlike structural/energy/recovery constraints.
        target=self.c['targetMargin']
        mass_index=self.c['outputNames'].index('totalMass')
        refined=None
        if valid(best) and self.route(best)[3]>=target:
            refined=minimize(lambda x:self.evaluate(x)[0,mass_index],best,method='SLSQP',bounds=[(0,1)]*len(z),
                constraints=constraints+[{'type':'ineq','fun':lambda x:self.route(x)[3]-target}],options={'maxiter':budget,'ftol':1e-8})
            if valid(refined.x) and self.route(refined.x)[3]>=target-1e-6:best=refined.x
        x=self.lower+best*self.span
        rows=self.evaluate(best)
        return {'seed':seed,'operatingFeasible':bool(valid(best)),'route':self.route(best).tolist(),
            'numericalFeasible':bool(valid(best) and self.route(best)[3]>=-1e-4),
            'targetMarginMet':bool(valid(best) and self.route(best)[3]>=target-1e-6),
            'design':dict(zip(self.c['designNames'],map(float,x[:self.nd]))),'states':x[self.nd:].reshape(-1,6).tolist(),
            'results':[dict(zip(self.c['outputNames'],map(float,row))) for row in rows],
            'maxEquilibriumResidual':float(np.abs(rows[:,:4]).max()),'minimumHardwareMargin':float(self.hardware(best).min()),
            'frontierMessage':str(frontier.message),'massMessage':str(refined.message) if refined else None}


def ranking(r):
    return (not r['operatingFeasible'],not r['targetMarginMet'],
        r['results'][0]['totalMass'] if r['targetMarginMet'] else -r['route'][3])


def polar_grid(p,best,budget):
    """Fixed-design angle grid. Failed balance points are recorded, never interpolated as valid."""
    d=np.array([best['design'][n] for n in p.c['designNames']]);points=[]
    for wind in [3,5,8,12,15]:
        for angle in [35,45,60,80,100,120,140,160]:
            up=angle<90;lo=np.array(p.c['stateLowerUp' if up else 'stateLowerDown'],dtype=float);hi=np.array(p.c['stateUpperUp' if up else 'stateUpperDown'],dtype=float)
            lo[1]=hi[1]=angle;span=hi-lo
            state=np.array(best['states'][0 if up else 1]);y=np.clip(np.divide(state-lo,span,out=np.zeros(6),where=span!=0),0,1)
            def row(z):return p.kernel.evaluate(d,np.r_[wind,int(up),1,lo+z*span])
            phase=least_squares(lambda z:np.r_[row(z)[:4],np.minimum(row(z)[5:47],0)],y,bounds=(0,1),max_nfev=budget)
            sol=minimize(lambda z:-row(z)[p.c['outputNames'].index('boatSpeed')],phase.x,method='SLSQP',bounds=[(0,1)]*6,
                constraints=[{'type':'eq','fun':lambda z:row(z)[:4]},{'type':'ineq','fun':lambda z:row(z)[5:47]}],options={'maxiter':budget,'ftol':1e-8})
            candidates=[phase.x,sol.x];valid=[z for z in candidates if np.abs(row(z)[:4]).max()<=.001 and row(z)[5:47].min()>=-1e-4]
            chosen=max(valid,key=lambda z:row(z)[p.c['outputNames'].index('boatSpeed')]) if valid else phase.x
            r=row(chosen)
            points.append({'wind':wind,'angle':angle,'valid':bool(valid),'state':(lo+chosen*span).tolist(),
                'speed':float(r[p.c['outputNames'].index('boatSpeed')]) if valid else None,'maxEquilibriumResidual':float(np.abs(r[:4]).max()),'minimumHardwareMargin':float(r[5:47].min())})
    return points


def run(starts,budget):
    studies={}
    # One library instance: never overwrite a loaded shared object between recipes.
    k=MissionKernel(0)
    for architecture,name in [(0,'printed_infill'),(1,'printed_ribs')]:
        k.parameters[97]=architecture;p=MissionProblem(k)
        runs=[];brackets=[];warm=None
        for bracket in range(3):
            round_runs=[p.solve(17+23*i,budget,warm if i==0 else None) for i in range(starts)]
            runs+=round_runs
            best=min(runs,key=ranking)
            hits=boundary_hits(best,p.lower[:p.nd],p.upper[:p.nd],p.c['designNames'])
            hits=[h for h in hits if h['index']!=0]
            brackets.append({'lower':p.lower[:p.nd].tolist(),'upper':p.upper[:p.nd].tolist(),'hits':hits})
            lo,hi=expanded_bounds(p.c,p.lower[:p.nd],p.upper[:p.nd],hits)
            if np.array_equal(lo,p.lower[:p.nd]) and np.array_equal(hi,p.upper[:p.nd]):break
            if bracket==2:break
            p.lower[:p.nd]=lo;p.upper[:p.nd]=hi;p.span=p.upper-p.lower;p.last=None
            x=np.r_[[best['design'][n] for n in p.c['designNames']],np.array(best['states']).ravel()]
            warm=np.clip(np.divide(x-p.lower,p.span,out=np.zeros_like(x),where=p.span!=0),0,1)
        recipe=np.ceil(np.array([best['design'][n] for n in p.c['designNames'][15:19]])/.2-1e-8)*.2
        p.lower[15:19]=p.upper[15:19]=recipe;p.span=p.upper-p.lower;p.last=None
        x=np.r_[[best['design'][n] for n in p.c['designNames']],np.array(best['states']).ravel()]
        z=np.clip(np.divide(x-p.lower,p.span,out=np.zeros_like(x),where=p.span!=0),0,1)
        rounded=p.solve(17,budget,z)
        print(name,rounded['operatingFeasible'],rounded['route'],'mass',rounded['results'][0]['totalMass'],flush=True)
        hits=boundary_hits(rounded,brackets[-1]['lower'],brackets[-1]['upper'],p.c['designNames'])
        boundary_limited=any(h['index']!=0 and p.c['expandable'+h['side'].title()][h['index']] for h in hits)
        studies[name]={'boundaryLimited':boundary_limited,'architecture':architecture,'runs':runs,'brackets':brackets,'rounded':rounded,'polar':polar_grid(p,rounded,120)}
    report={'sourceHashes':k.contract['sourceHashes'],'driverHashes':{n:digest(ROOT/n) for n in DRIVERS},
        'contract':k.contract,'starts':starts,'budget':budget,'studies':studies,'missionSupported':False}
    RECORD.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def read_report():
    r=json.loads(RECORD.read_text(encoding='utf-8'));validate(r['sourceHashes']|r['driverHashes']);return r


def publish():
    r=read_report();c=r['contract'];lines=['# Two-metre mission sizing','',
        '<!-- Generated by scripts.study_mission_sizing; edit the models and rerun. -->','',
        'Fixed 2 m **waterline**, not overall length. One geometry per construction option is shared across four clean-water operating points. Winds are water-relative; the illustrative easterly profile uses equal time fractions at 5 and 8 m/s with opposing upstream currents of 0.5 and 1.0 m/s. Downstream current assists. Negative intervals remain in the signed mean. No free waiting or station keeping is assumed.', '',
        'The solver first maximizes the minimum route progress/duration margin, then minimizes mass only if it can retain 10% route margin. Each leg must average 0.5 m/s, and the 100 km + 100 km route must take at most 72 hours. A separate 5% maneuver allowance remains. These are synthetic planning cases, not an approved weather window.', '',
        '| Construction | Hardware screen | Route screen | 10% route margin | Upstream mean m/s | Downstream mean m/s | Hours | Mass kg |',
        '|---|---|---|---|---:|---:|---:|---:|']
    seq=lambda v:'('+', '.join(format(float(x),'.17g') for x in v)+')'
    source=['package BlueDogMissionSizingResults {'];expected=[];args=[]
    for name,study in r['studies'].items():
        b=study['rounded'];route=b['route']
        lines.append(f"| {name} | {b['operatingFeasible']} | {b['numericalFeasible']} | {b['targetMarginMet']} | {route[0]:.3f} | {route[1]:.3f} | {route[2]:.1f} | {b['results'][0]['totalMass']:.2f} |")
        params=list(c['parameterValues']);params[97]=study['architecture']
        for i,(env,state,row) in enumerate(zip([[5,1,1],[5,0,1],[8,1,1],[8,0,1]],b['states'],b['results'])):
            label=name+str(i)
            source += [f'analysis {label} {{ out attribute rows : ScalarValues::Real [*] ordered nonunique = BlueDogMissionSizing::EvaluateCase({seq(b["design"].values())}, {seq(params)}, {seq(env+state)}); }}']
            args+=['-analysis','BlueDogMissionSizingResults::'+label];expected.append([row[n] for n in c['outputNames']])
        source += [f'analysis {name}Route {{ out attribute rows : ScalarValues::Real [*] ordered nonunique = BlueDogMissionSizing::Route({seq([row["waterVMG"] for row in b["results"]])}, {seq(c["routeParameters"])}); }}']
        args+=['-analysis','BlueDogMissionSizingResults::'+name+'Route'];expected.append(route)
    source+=['}'];path=ROOT/'models/mission-sizing-results.sysml';path.write_text('\n'.join(source)+'\n',encoding='utf-8')
    audit=json.loads(native(*args,'-json',models=MODELS_NEW+(path,)))
    if audit['status']!='holds' or audit.get('diagnostics'):raise ValueError('Native replay failed')
    for case,want in zip(audit['checks'],expected,strict=True):
        got=native_value(next(v['value'] for v in case['values'] if v['name']=='rows'));np.testing.assert_allclose(got,want,rtol=1e-8,atol=1e-6)
    (ROOT/'docs/analysis/mission-sizing-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    lines += ['', '**Mission supported: false.** The mass-center screen is not full-angle stability or capsize proof. Construction/buckling, polar validation, environmental evidence, minimum-load stability and physical N-051/N-052 recovery remain open.', '', '| Parameter | Printed infill | Printed ribs |','|---|---:|---:|']
    for n in c['designNames']:lines.append('| '+n+' | '+' | '.join(f"{s['rounded']['design'][n]:.4g}" for s in r['studies'].values())+' |')
    lines += ['', '| Mass/stability output | Printed infill | Printed ribs |','|---|---:|---:|']
    for n in ['transportBodyMass','wingStructuralMass','batteryMass','keelAssembly','centerOfGravity','cgBelowBottom']:
        lines.append('| '+n+' | '+' | '.join(f"{s['rounded']['results'][0][n]:.4g}" for s in r['studies'].values())+' |')
    lines+=['','## Fixed-design polar coverage','','The saved JSON contains every attempted point, including failures. A failed solve is not a zero-speed prediction or proof that the heading is impossible. These clean-water curves do not establish wave or weed performance.','', '| Construction | Valid / attempted polar points |','|---|---:|']
    for name,s in r['studies'].items():lines.append(f"| {name} | {sum(v['valid'] for v in s['polar'])} / {len(s['polar'])} |")
    lines+=['','[Method, assumptions and evidence gates](mission-sizing.md). [Complete numerical record](analysis/mission-sizing.json).','']
    (ROOT/'docs/mission-sizing-results.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--publish',action='store_true');parser.add_argument('--starts',type=int,default=3);parser.add_argument('--budget',type=int,default=500)
    a=parser.parse_args()
    if a.starts<1 or a.budget<1:parser.error('Positive search budgets required')
    if a.prepare:prepare()
    elif a.publish:publish()
    else:run(a.starts,a.budget)
