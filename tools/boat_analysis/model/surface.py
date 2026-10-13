"""Native surface physics with Python quadrature and bounded polar sampling.

Opt-in provider: historical uniform-flow replay remains reproducible. The local
finite-wing coefficient approximation does not resolve spanwise circulation.
"""
import ctypes as ct
import hashlib
import json
import re
import subprocess
import threading

import numpy as np

from .abi import Sequence
from .runtime import ROOT, model_files, native, native_value


class Number(ct.Structure):
    _fields_=[('real',ct.c_bool),('integer',ct.c_int64),('value',ct.c_double)]


class NumberSequence(ct.Structure):
    _fields_=[('shape',ct.c_int8),('length',ct.c_int64),('data',ct.POINTER(Number))]


class NativeCalculation:
    def __init__(self, name, arguments):
        fingerprint=hashlib.sha256(name.encode())
        for path in model_files():
            fingerprint.update(path.read_bytes().replace(b'\r\n',b'\n'))
        stem=ROOT/'.tools'/('surface-'+name.split('::')[-1]+'-'+fingerprint.hexdigest()[:16])
        source=stem.with_suffix('.c');library=stem.with_suffix('.so')
        if not library.exists():
            native('-compile',name,'-source','-o',str(source))
            subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.lib=ct.CDLL(str(library));self.lock=threading.Lock()
        signature=re.search(r'int sysml_run\((.*?)\) \{',source.read_text())[1]
        result_type=signature.split(',')[-1].strip()
        self.result_type={'sysml_seq_real *result':Sequence,'sysml_seq_num *result':NumberSequence,
                          'sysml_real *result':ct.c_double}.get(result_type)
        if self.result_type is None or signature.count('sysml_seq_real v_')!=arguments:
            raise ValueError('Unsupported native surface ABI: '+signature)
        self.lib.sysml_run.argtypes=[Sequence]*arguments+[ct.POINTER(self.result_type)]
        self.lib.sysml_run.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p

    def __call__(self,*vectors):
        arrays=[np.ascontiguousarray(v,dtype=float) for v in vectors]
        if any(a.ndim!=1 or not np.isfinite(a).all() for a in arrays):
            raise ValueError('Finite one-dimensional native inputs required')
        args=[Sequence(2,a.size,a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with self.lock:
            out=self.result_type()
            if self.lib.sysml_run(*args,ct.byref(out)):raise ValueError(self.lib.sysml_error().decode())
            if self.result_type is ct.c_double:values=np.array([out.value])
            elif self.result_type is NumberSequence:
                values=np.array([out.data[i].value if out.data[i].real else out.data[i].integer for i in range(out.length)])
            else:values=np.ctypeslib.as_array(out.data,shape=(out.length,)).copy()
        if not np.isfinite(values).all():raise ValueError('Nonfinite surface calculation')
        return values


def policy_inputs():
    report=json.loads(native('-analysis','BlueDogSurfaceEnvironment::Inputs','-json'))
    return {v['name']:native_value(v['value']) for v in report['checks'][0]['values']}


class SurfaceOperation:
    """Drop-in operating provider, also usable by the existing sizing optimizer."""
    def __init__(self, original, polar, policy, shear=True, strips=None):
        self.original=original;self.contract=original.contract;self.polar=polar
        self.policy=list(policy);self.shear=shear
        self.strips=int(strips or policy[3])
        if self.strips<1 or not 0<policy[1]<policy[2]<policy[0]:
            raise ValueError('Invalid wind height, roughness or quadrature')
        self.wind=NativeCalculation('MarineSurface::WindSample',1)
        self.strip=NativeCalculation('MarineSurface::StripLoad',1)
        self.core=NativeCalculation('MarineSailing::Core',8)

    def evaluate(self,design,parameters,state,aero,mass,hydro):
        d,p,s=np.asarray(design),np.asarray(parameters),np.asarray(state)
        q=self.contract['environment'];height=np.sqrt(d[4]*d[5]);chord=d[4]/height
        theta,beta,heel=np.deg2rad(s[[4,6,8]])
        ax=s[0]*np.cos(theta)+s[3]*np.cos(beta)
        ay=s[0]*np.sin(theta)-s[3]*np.sin(beta)
        reference_angle=np.arctan2(ay,ax)
        loads=[];speeds=[];lift=[];ratios=[];alphas=[];margins=[];height_margins=[]
        reverse=s[4]<0
        bounds=self.polar.axes[2]
        lower,upper=(-bounds[-1],-bounds[0]) if reverse else (bounds[0],bounds[-1])
        for fraction in (np.arange(self.strips)+.5)/self.strips:
            z=(d[3]+fraction*height)*np.cos(heel)-hydro[0]
            sample=self.wind([s[0],self.policy[0],self.policy[1],z,theta,s[3],beta,float(self.shear),self.policy[2]])
            difference=(np.arctan2(sample[2],sample[1])-reference_angle+np.pi)%(2*np.pi)-np.pi
            alpha=s[5]+np.rad2deg(difference)
            # Numerical extension only: a negative incidence margin rejects the
            # state; clipped coefficients never establish supported performance.
            margin=min(alpha-lower,upper-alpha)/max(upper-lower,1.)
            coeff=self.polar.evaluate(d[5],d[6],np.clip(alpha,lower,upper),reverse_flow=reverse)
            cl=coeff[0]*p[16];cd=(coeff[1]+p[14])*p[17]
            normal=cl*np.cos(np.deg2rad(alpha))+cd*np.sin(np.deg2rad(alpha))
            mast=coeff[2]*q[23]+((1-d[8] if reverse else d[8])-.5)*normal
            loads.append(self.strip([p[32],d[4]/self.strips,sample[1],sample[2],heel,z,cl,cd,chord,mast]))
            speeds.append(sample[3]);lift.append(abs(cl));ratios.append(sample[0]);alphas.append(alpha)
            margins.append(margin);height_margins.append(sample[4])
        force=np.sum(loads,axis=0)
        extension=[1,*force,min(speeds),max(lift),0,min(*margins,*height_margins)]
        values=self.core(d,p,q,s,aero,mass,hydro,extension)
        if len(values)!=len(self.contract['outputNames']):raise ValueError('Surface operation ABI mismatch')
        result=dict(zip(self.contract['outputNames'],values))
        result.update(windRatioMin=min(ratios),windRatioMax=max(ratios),
                      localAlphaMin=min(alphas),localAlphaMax=max(alphas),
                      surfaceIncidenceMargin=min(margins),surfaceHeightMargin=min(height_margins),
                      airRollMoment=force[2],signedMastMoment=force[3])
        return result
