"""Compile and call the coupled native force/energy calculation."""
import ctypes as ct
import json,re,subprocess,threading
import numpy as np
from .native_design_kernel import ROOT,Sequence
from .study_open_sizing import digest,validate
_LOCK=threading.Lock()
CONTRACT=ROOT/'.tools/coupled-operation-contract.json'

def prepare():
    from .render_requirements import MODELS,native
    from .prepare_design_search import native_value
    models=MODELS+(ROOT/'models/structure.sysml',ROOT/'models/wing-actuator.sysml',ROOT/'models/coupled-operation.sysml')
    audit=json.loads(native('-analysis','BlueDogDesignSearch::SearchInputs','-json',models=models))
    if audit['status']!='holds':raise ValueError('Environment input export failed')
    inputs={v['name']:native_value(v['value']) for v in audit['checks'][0]['values']}
    source=ROOT/'.tools/coupled-operation.c'
    native('-compile','BlueDogCoupledOperation::Evaluate','-source','-o',str(source),models=models)
    text=(ROOT/'models/coupled-operation.sysml').read_text()
    names=[n.strip() for n in re.search(r'return result.*?;\s*\((.*?)\)',text,re.S)[1].split(',')]
    c={'sourceHashes':{p.relative_to(ROOT).as_posix():digest(p) for p in models},'generatedHash':digest(source),'outputNames':names,'environment':inputs['parameterValues']}
    structural=json.loads(native('-analysis','BlueDogCoupledOperation::Inputs','-json',models=models))
    c.update({v['name']:native_value(v['value']) for v in structural['checks'][0]['values']})
    c['structure']=c['structureValues']
    route_source=ROOT/'.tools/coupled-route.c'
    native('-compile','BlueDogCoupledOperation::Route','-source','-o',str(route_source),models=models)
    c['routeHash']=digest(route_source)
    structural_source=ROOT/'.tools/coupled-structure.c'
    native('-compile','BlueDogCoupledOperation::DesignMargins','-source','-o',str(structural_source),models=models)
    c['structureHash']=digest(structural_source)
    for generated in [source,structural_source,route_source]:
        signature=re.search(r'int sysml_run\((.*?)\) \{',generated.read_text(),re.S)
        if not signature or not signature[1].endswith('sysml_seq_real *result'):
            raise ValueError('Expected homogeneous Real C output ABI: '+generated.name)
    c['structureNames']=[n.strip() for n in re.search(r'calc def DesignMargins.*?return result.*?;\s*\((.*?)\)',text,re.S)[1].split(',')]
    CONTRACT.write_text(json.dumps(c,indent=2)+'\n')
    reference=json.loads((ROOT/'docs/analysis/coupled-mass-reference.json').read_text())
    inputs=[list(reference['design'].values()),list(reference['parameters'].values()),c['environment'],[5,1,1,2,0,0,0,0,0],[.6,.02,-.07],list(reference['mass'].values()),[0,0,1]]
    literal=lambda values:'('+','.join(format(v,'.17g') for v in values)+')'
    replay=ROOT/'.tools/coupled-operation-replay.sysml'
    replay.write_text('package CoupledOperationReplay { private import ScalarValues::*; analysis example { out attribute result : Real [*] ordered nonunique = BlueDogCoupledOperation::Evaluate('+','.join(literal(a) for a in inputs)+'); } }')
    audit=json.loads(native('-analysis','CoupledOperationReplay::example','-json',models=models+(replay,)))
    if audit['status']!='holds':raise ValueError('Operating arithmetic replay failed')
    values=native_value(audit['checks'][0]['values'][0]['value'])
    record={'sourceHashes':c['sourceHashes'],'inputs':inputs,'outputs':dict(zip(names,values)),'scope':'Synthetic arithmetic replay, not an equilibrium or mission case.'}
    (ROOT/'docs/analysis/coupled-operation-audit.json').write_text(json.dumps(record,indent=2)+'\n')

class OperationKernel:
    def __init__(self):
        self.contract=json.loads(CONTRACT.read_text());c=self.contract;validate(c['sourceHashes'])
        source=ROOT/'.tools/coupled-operation.c'
        if digest(source)!=c['generatedHash']:raise ValueError('Stale operating kernel')
        library=ROOT/f".tools/coupled-operation-{c['generatedHash'][:16]}.so"
        if not library.exists():subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.lib=ct.CDLL(str(library));self.lib.sysml_run.argtypes=[Sequence]*7+[ct.POINTER(Sequence)]
        self.lib.sysml_run.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p
    def evaluate(self,design,parameters,state,aero,mass,hydro):
        p=np.asarray(parameters)
        if len(p)!=38 or not 0<p[1]<=1 or not 0<p[2]<=1 or min(p[6:8])<0 or sum(p[6:8])>1+1e-12 or not 0<=p[9]<=1:raise ValueError('Invalid drive efficiencies or duty')
        arrays=[np.ascontiguousarray(a,dtype=float) for a in [design,p,self.contract['environment'],state,aero,mass,hydro]]
        if [a.shape for a in arrays]!=[(28,),(38,),(len(self.contract['environment']),),(9,),(3,),(21,),(3,)] or any(not np.isfinite(a).all() for a in arrays):raise ValueError('Invalid operation inputs')
        if arrays[3][3]<=0 or arrays[6][2]<=0:raise ValueError('Positive speed and wetted area required')
        args=[Sequence(2,a.size,a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with _LOCK:
            out=Sequence()
            if self.lib.sysml_run(*args,ct.byref(out)):raise ValueError(self.lib.sysml_error().decode())
            if out.shape!=2 or out.length!=len(self.contract['outputNames']):raise ValueError('Operation ABI mismatch')
            result=np.ctypeslib.as_array(out.data,shape=(out.length,)).copy()
        if not np.isfinite(result).all():raise ValueError('Nonfinite operation result')
        return dict(zip(self.contract['outputNames'],result))

class StructureKernel:
    def __init__(self):
        self.contract=json.loads(CONTRACT.read_text());c=self.contract;validate(c['sourceHashes'])
        source=ROOT/'.tools/coupled-structure.c'
        if digest(source)!=c['structureHash']:raise ValueError('Stale structural kernel')
        library=ROOT/f".tools/coupled-structure-{c['structureHash'][:16]}.so"
        if not library.exists():subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.lib=ct.CDLL(str(library));self.lib.sysml_run.argtypes=[Sequence]*6+[ct.c_double,ct.POINTER(Sequence)]
        self.lib.sysml_run.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p
    def evaluate(self,design,parameters,mass,geometry,loads,waterline):
        arrays=[np.ascontiguousarray(a,dtype=float) for a in [design,parameters,mass,geometry,self.contract['structure'],loads]]
        if [a.shape for a in arrays]!=[(28,),(38,),(21,),(51,),(10,),(3,)] or any(not np.isfinite(a).all() for a in arrays) or not np.isfinite(waterline):raise ValueError('Invalid structural inputs')
        args=[Sequence(2,a.size,a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with _LOCK:
            out=Sequence()
            if self.lib.sysml_run(*args,waterline,ct.byref(out)):raise ValueError(self.lib.sysml_error().decode())
            if out.shape!=2 or out.length!=len(self.contract['structureNames']):raise ValueError('Structure ABI mismatch')
            result=np.ctypeslib.as_array(out.data,shape=(out.length,)).copy()
        if not np.isfinite(result).all():raise ValueError('Nonfinite structural output')
        return dict(zip(self.contract['structureNames'],result))

class RouteKernel:
    def __init__(self):
        self.contract=json.loads(CONTRACT.read_text());c=self.contract;validate(c['sourceHashes'])
        source=ROOT/'.tools/coupled-route.c'
        if digest(source)!=c['routeHash']:raise ValueError('Stale route kernel')
        library=ROOT/f".tools/coupled-route-{c['routeHash'][:16]}.so"
        if not library.exists():subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.lib=ct.CDLL(str(library));self.lib.sysml_run.argtypes=[Sequence]*3+[ct.POINTER(Sequence)]
        self.lib.sysml_run.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p
    def evaluate(self,water,states,policy=None):
        arrays=[np.ascontiguousarray(a,dtype=float) for a in [water,states,self.contract['routeParameters'] if policy is None else policy]]
        if [a.shape for a in arrays]!=[(8,),(48,),(6,)] or any(not np.isfinite(a).all() for a in arrays):raise ValueError('Invalid route inputs')
        args=[Sequence(2,a.size,a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with _LOCK:
            out=Sequence()
            if self.lib.sysml_run(*args,ct.byref(out)):raise ValueError(self.lib.sysml_error().decode())
            if out.shape!=2 or out.length!=6:raise ValueError('Route ABI mismatch')
            result=np.ctypeslib.as_array(out.data,shape=(out.length,)).copy()
        if not np.isfinite(result).all():raise ValueError('Nonfinite route output')
        return result

if __name__=='__main__':prepare()
