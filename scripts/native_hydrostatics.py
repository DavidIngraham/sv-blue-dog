"""Compile and invoke the authoritative SysML immersed-volume kernel."""
import ctypes as ct
import json,subprocess,threading
import numpy as np
from .native_design_kernel import ROOT,Sequence
from .study_open_sizing import digest
SOURCE=ROOT/'models/hydrostatics.sysml'
CONTRACT=ROOT/'.tools/hydrostatics-contract.json'
_RUNTIME_LOCK=threading.Lock()

def prepare():
    from .render_requirements import MODELS,native
    models=MODELS+(SOURCE,)
    audit=native('-analysis','BlueDogHydrostatics::analyticExample','-json',models=models)
    (ROOT/'docs/analysis/hydrostatics-audit.json').write_text(audit,encoding='utf-8')
    generated=ROOT/'.tools/hydrostatics.c'
    native('-compile','BlueDogHydrostatics::WetMoment','-source','-o',str(generated),models=models)
    balance=ROOT/'.tools/hydrostatics-balance.c'
    native('-compile','BlueDogHydrostatics::Balance','-source','-o',str(balance),models=models)
    CONTRACT.write_text(json.dumps({'sourceHash':digest(SOURCE),'generatedHash':digest(generated),'balanceHash':digest(balance)},indent=2)+'\n')
    actuator=native('-analysis','BlueDogWingActuator::accountingExample','-json',models=MODELS+(ROOT/'models/structure.sysml',ROOT/'models/wing-actuator.sysml'))
    (ROOT/'docs/analysis/wing-actuator-audit.json').write_text(actuator,encoding='utf-8')

class HydroKernel:
    def __init__(self):
        c=json.loads(CONTRACT.read_text());source=ROOT/'.tools/hydrostatics.c'
        if digest(SOURCE)!=c['sourceHash'] or digest(source)!=c['generatedHash']:raise ValueError('Stale hydrostatics kernel')
        batch=ROOT/'scripts/hydrostatics_batch.c'
        library=ROOT/f".tools/hydrostatics-{c['generatedHash'][:12]}-{digest(batch)[:12]}.so"
        if not library.exists():subprocess.run(['gcc','-O2','-shared','-fPIC',str(batch),'-I',str(ROOT/'.tools'),'-lm','-o',str(library)],check=True)
        self.lib=ct.CDLL(str(library));self.lock=_RUNTIME_LOCK
        self.lib.hydro_mesh.argtypes=[ct.POINTER(ct.c_double),ct.c_int64,ct.c_double,ct.POINTER(ct.c_double)]
        self.lib.hydro_mesh.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p
        source=ROOT/'.tools/hydrostatics-balance.c'
        if digest(source)!=c['balanceHash']:raise ValueError('Stale balance kernel')
        library=ROOT/f".tools/hydrostatics-balance-{c['balanceHash'][:16]}.so"
        if not library.exists():subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.balance_lib=ct.CDLL(str(library));self.balance_lib.sysml_run.argtypes=[Sequence,Sequence,ct.c_double,ct.c_double,ct.POINTER(Sequence)]
        self.balance_lib.sysml_run.restype=ct.c_int;self.balance_lib.sysml_error.restype=ct.c_char_p

    def balance(self,moments,cg,mass,density):
        arrays=[np.ascontiguousarray(a,dtype=np.float64) for a in [moments,cg]]
        if [a.shape for a in arrays]!=[(4,),(3,)] or any(not np.isfinite(a).all() for a in arrays) or not np.isfinite([mass,density]).all() or min(mass,density)<=0:raise ValueError('Invalid balance inputs')
        args=[Sequence(2,a.size,a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with self.lock:
            out=Sequence()
            if self.balance_lib.sysml_run(*args,mass,density,ct.byref(out)):raise ValueError(self.balance_lib.sysml_error().decode())
            if out.shape!=2 or out.length!=3:raise ValueError('Balance ABI mismatch')
            result=np.ctypeslib.as_array(out.data,shape=(3,)).copy()
        return result

    def moments(self,tetrahedra,waterline):
        points=np.ascontiguousarray(tetrahedra,dtype=np.float64)
        if points.ndim!=3 or points.shape[1:]!=(4,3) or len(points)==0 or not np.isfinite(points).all() or not np.isfinite(waterline):raise ValueError('Finite nonempty tetrahedra (n,4,3) and waterline required')
        with self.lock:
            result=np.zeros(4,dtype=np.float64)
            status=self.lib.hydro_mesh(points.ctypes.data_as(ct.POINTER(ct.c_double)),len(points),waterline,result.ctypes.data_as(ct.POINTER(ct.c_double)))
            if status==2:raise ValueError('Hydrostatics ABI mismatch')
            if status:raise ValueError(self.lib.sysml_error().decode())
        if not np.isfinite(result).all():raise ValueError('Nonfinite hydrostatics result')
        return result

if __name__=='__main__':prepare()
