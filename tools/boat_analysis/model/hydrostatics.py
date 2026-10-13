"""Compile and invoke the authoritative SysML immersed-volume kernel."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import ctypes as ct
import json
import numpy as np
from tools.boat_analysis.model.runtime import ROOT
from .native_kernel import KernelSpec, NativeKernel, load_library
from tools.boat_analysis.evidence.records import digest
SOURCE=ROOT/'models/analyses/recovery.sysml'
CONTRACT=ROOT/'.tools/hydrostatics-contract.json'

def prepare():
    from tools.boat_analysis.model.runtime import MODELS,native
    models=MODELS+(SOURCE,)
    audit=native('-analysis','BlueDogHydrostatics::analyticExample','-json',models=models)
    output_path('hydrostatics-audit.json').write_text(audit,encoding='utf-8')
    generated=ROOT/'.tools/hydrostatics.c'
    native('-compile','BlueDogHydrostatics::WetMoment','-source','-o',str(generated),models=models)
    balance=ROOT/'.tools/hydrostatics-balance.c'
    native('-compile','BlueDogHydrostatics::Balance','-source','-o',str(balance),models=models)
    CONTRACT.write_text(json.dumps({'sourceHash':digest(SOURCE),'generatedHash':digest(generated),'balanceHash':digest(balance)},indent=2)+'\n')
    actuator=native('-analysis','BlueDogWingActuator::accountingExample','-json',models=MODELS+(ROOT/'models/vehicle/structure.sysml',ROOT/'models/analyses/actuation.sysml'))
    output_path('wing-actuator-audit.json').write_text(actuator,encoding='utf-8')

class HydroKernel:
    def __init__(self):
        c=json.loads(CONTRACT.read_text());source=ROOT/'.tools/hydrostatics.c'
        if digest(SOURCE)!=c['sourceHash'] or digest(source)!=c['generatedHash']:raise ValueError('Stale hydrostatics kernel')
        batch=ROOT/'tools/boat_analysis/model/hydrostatics_batch.c'
        # Copy the specialized shim alongside its included generated source.
        wrapper=source.parent/('mesh-'+digest(batch)[:16]+'.c')
        wrapper.write_bytes(batch.read_bytes())
        self.lib,self.lock=load_library(wrapper,dependencies=(source,))
        self.lib.hydro_mesh.argtypes=[ct.POINTER(ct.c_double),ct.c_int64,ct.c_double,ct.POINTER(ct.c_double)]
        self.lib.hydro_mesh.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p
        source=ROOT/'.tools/hydrostatics-balance.c'
        if digest(source)!=c['balanceHash']:raise ValueError('Stale balance kernel')
        self.balance_runtime=NativeKernel(KernelSpec(source,('moments','cg','mass','density'),3))

    def balance(self,moments,cg,mass,density):
        arrays=[np.ascontiguousarray(a,dtype=np.float64) for a in [moments,cg]]
        if [a.shape for a in arrays]!=[(4,),(3,)] or any(not np.isfinite(a).all() for a in arrays) or not np.isfinite([mass,density]).all() or min(mass,density)<=0:raise ValueError('Invalid balance inputs')
        return self.balance_runtime.evaluate(*arrays,mass,density)

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
