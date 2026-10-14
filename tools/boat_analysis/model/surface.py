"""Native surface physics with Python quadrature and bounded polar sampling.

Opt-in provider: historical uniform-flow replay remains reproducible. The local
finite-wing coefficient approximation does not resolve spanwise circulation.
"""
import hashlib
import json

import numpy as np

from tools.boat_analysis.generated import operation
from sysml_python.backends.native import KernelSpec, NativeKernel
from .runtime import ROOT, model_files, native, native_value


class NativeCalculation:
    def __init__(self, name, arguments, output_size=None):
        fingerprint=hashlib.sha256(name.encode())
        for path in model_files():
            fingerprint.update(path.read_bytes().replace(b'\r\n',b'\n'))
        source=ROOT/'.tools'/('surface-'+name.split('::')[-1]+'-'+fingerprint.hexdigest()[:16]+'.c')
        if not source.exists():
            native('-compile',name,'-source','-o',str(source))
        self.runtime=NativeKernel(KernelSpec(source,tuple(f'input{i}' for i in range(arguments)),output_size))

    def __call__(self,*vectors):
        return self.runtime.evaluate(*vectors)

    def evaluate_batch(self, *, shared, cases, **options):
        return self.runtime.evaluate_batch(shared=shared,cases=cases,**options)


def policy_inputs():
    report=json.loads(native('-analysis','BlueDogSurfaceEnvironment::Inputs','-json'))
    return {v['name']:native_value(v['value']) for v in report['checks'][0]['values']}


class SurfaceOperation:
    """Drop-in operating provider, also usable by the existing sizing optimizer."""
    def __init__(self, contract, polar, policy, shear=True, strips=None):
        self.contract=contract;self.polar=polar
        self.policy=list(policy);self.shear=shear
        self.strips=int(strips or policy[3])
        if self.strips<1 or not 0<policy[1]<policy[2]<policy[0]:
            raise ValueError('Invalid wind height, roughness or quadrature')
        self.wind=NativeCalculation('MarineSurface::WindSample',1)
        self.strip=NativeCalculation('MarineSurface::StripLoad',1,output_size=4)
        self.core=NativeCalculation('MarineSailing::Core',8)

    def pack(self, design, parameters, state, aero, mass, hydro):
        values=operation.prepare_inputs(design=design, parameters=parameters, state=state,
                                        aero=aero, mass=mass, hydro=hydro, environment=self.contract['environment'])
        return tuple(values[name] for name in ('design','parameters','state','aero','mass','hydro'))

    def __call__(self, **inputs):
        return self.evaluate(**inputs)

    def evaluate(self,design,parameters,state,aero,mass,hydro,*,motion=None,motion_origin=(0,0,0)):
        design,parameters,state,aero,mass,hydro=self.pack(design,parameters,state,aero,mass,hydro)
        d,p,s=np.asarray(design),np.asarray(parameters),np.asarray(state)
        q=self.contract['environment'];height=np.sqrt(d[4]*d[5]);chord=d[4]/height
        theta,beta,heel=np.deg2rad(s[[4,6,8]])
        ax=s[0]*np.cos(theta)+s[3]*np.cos(beta)
        ay=s[0]*np.sin(theta)-s[3]*np.sin(beta)
        reference_angle=np.arctan2(ay,ax)
        strip_inputs=[];poses=[];speeds=[];lift=[];ratios=[];alphas=[];margins=[];height_margins=[]
        reverse=s[4]<0
        bounds=self.polar.axes[2]
        lower,upper=(-bounds[-1],-bounds[0]) if reverse else (bounds[0],bounds[-1])
        for fraction in (np.arange(self.strips)+.5)/self.strips:
            z=(d[3]+fraction*height)*np.cos(heel)-hydro[0]
            velocity=np.zeros(3);matrix=np.eye(3)
            if motion is not None:
                from ..environment.motion import point_motion
                # Rotation origin is midships at mean water. Existing steady
                # heel is retained in the strip point before oscillatory motion.
                point=[d[9]*d[0],-(d[3]+fraction*height)*np.sin(heel),z]
                position,velocity,matrix=point_motion(point,motion,motion_origin)
                z=position[2]
            sample=self.wind([s[0],self.policy[0],self.policy[1],z,theta,s[3],beta,float(self.shear),self.policy[2]])
            if motion is not None:
                # Wind-from vector: point velocity adds to apparent wind.
                # Stored wind y is starboard-positive; point positions,
                # velocities and returned forces use port-positive Cartesian y.
                local=matrix.T@(np.array([sample[1],-sample[2],0.])+velocity)
                sample[1:3]=[local[0],-local[1]];sample[3]=np.linalg.norm(local[:2])
            difference=(np.arctan2(sample[2],sample[1])-reference_angle+np.pi)%(2*np.pi)-np.pi
            alpha=s[5]+np.rad2deg(difference)
            # Numerical extension only: a negative incidence margin rejects the
            # state; clipped coefficients never establish supported performance.
            margin=min(alpha-lower,upper-alpha)/max(upper-lower,1.)
            coeff=self.polar.evaluate(d[5],d[6],np.clip(alpha,lower,upper),reverse_flow=reverse)
            cl=coeff[0]*p[16];cd=(coeff[1]+p[14])*p[17]
            normal=cl*np.cos(np.deg2rad(alpha))+cd*np.sin(np.deg2rad(alpha))
            mast=coeff[2]*q[23]+((1-d[8] if reverse else d[8])-.5)*normal
            strip_inputs.append([p[32],d[4]/self.strips,sample[1],sample[2],heel,z,cl,cd,chord,mast])
            poses.append((matrix,position,z) if motion is not None else None)
            speeds.append(sample[3]);lift.append(abs(cl));ratios.append(sample[0]);alphas.append(alpha)
            margins.append(margin);height_margins.append(sample[4])
        loads=self.strip.evaluate_batch(shared={},cases={'input0':strip_inputs}).values
        if motion is not None:
            for load,(matrix,position,z) in zip(loads,poses):
                world=matrix@np.r_[load[:2],0.]
                load[:2]=world[:2];load[2]=world[1]*z-position[1]*world[2]
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
