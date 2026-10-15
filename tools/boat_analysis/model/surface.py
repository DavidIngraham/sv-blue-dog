"""Native surface physics with Python quadrature and bounded polar sampling.

Opt-in provider: historical uniform-flow replay remains reproducible. The local
finite-wing coefficient approximation does not resolve spanwise circulation.
"""
from sysml_python import execution_session

import numpy as np

from tools.boat_analysis.generated import operation, wind_sample, strip_load, sailing_core, Design, Parameters, OperatingState, HydroState
from .runtime import analysis_values


def policy_inputs():
    return analysis_values('BlueDogSurfaceEnvironment::Inputs')


class SurfaceOperation:
    """Drop-in operating provider, also usable by the existing sizing optimizer."""
    def __init__(self, contract, polar, policy, shear=True, strips=None):
        self.contract=contract;self.polar=polar
        self.policy=list(policy);self.shear=shear
        self.strips=int(strips or policy[3])
        if self.strips<1 or not 0<policy[1]<policy[2]<policy[0]:
            raise ValueError('Invalid wind height, roughness or quadrature')
        self.wind=wind_sample
        self.strip=strip_load
        self.core=sailing_core

    def pack(self, design, parameters, state, aero, mass, hydro):
        values=operation.prepare_inputs(design=design, parameters=parameters, state=state,
                                        aero=aero, mass=mass, hydro=hydro, environment=self.contract['environment'])
        return tuple(values[name] for name in ('design','parameters','state','aero','mass','hydro'))

    def __call__(self, **inputs):
        return self.evaluate(**inputs)

    @execution_session()
    def evaluate(self,design,parameters,state,aero,mass,hydro,*,motion=None,motion_origin=(0,0,0)):
        design,parameters,state,aero,mass,hydro=self.pack(design,parameters,state,aero,mass,hydro)
        d,p,s=Design.from_array(design),Parameters.from_array(parameters),OperatingState.from_array(state)
        hydro=HydroState.from_array(hydro)
        q=self.contract['environment'];height=np.sqrt(d.sail_m2*d.sail_AR);chord=d.sail_m2/height
        theta,beta,heel=np.deg2rad([s.windFrom_deg,s.leeway_deg,s.heel_deg])
        ax=s.windSpeed_m_s*np.cos(theta)+s.speed_m_s*np.cos(beta)
        ay=s.windSpeed_m_s*np.sin(theta)-s.speed_m_s*np.sin(beta)
        reference_angle=np.arctan2(ay,ax)
        strip_inputs=[];poses=[];speeds=[];lift=[];ratios=[];alphas=[];margins=[];height_margins=[]
        reverse=s.windFrom_deg<0
        bounds=self.polar.axes[2]
        lower,upper=(-bounds[-1],-bounds[0]) if reverse else (bounds[0],bounds[-1])
        for fraction in (np.arange(self.strips)+.5)/self.strips:
            z=(d.deck_height_m+fraction*height)*np.cos(heel)-hydro.waterline_m
            velocity=np.zeros(3);matrix=np.eye(3)
            if motion is not None:
                from ..environment.motion import point_motion
                # Rotation origin is midships at mean water. Existing steady
                # heel is retained in the strip point before oscillatory motion.
                point=[d.mast_x_fraction*d.length_m,-(d.deck_height_m+fraction*height)*np.sin(heel),z]
                position,velocity,matrix=point_motion(point,motion,motion_origin)
                z=position[2]
            sample=self.wind(x=[s.windSpeed_m_s,self.policy[0],self.policy[1],z,theta,s.speed_m_s,beta,float(self.shear),self.policy[2]]).as_array()
            if motion is not None:
                # Wind-from vector: point velocity adds to apparent wind.
                # Stored wind y is starboard-positive; point positions,
                # velocities and returned forces use port-positive Cartesian y.
                local=matrix.T@(np.array([sample[1],-sample[2],0.])+velocity)
                sample[1:3]=[local[0],-local[1]];sample[3]=np.linalg.norm(local[:2])
            difference=(np.arctan2(sample[2],sample[1])-reference_angle+np.pi)%(2*np.pi)-np.pi
            alpha=s.incidence_deg+np.rad2deg(difference)
            # Numerical extension only: a negative incidence margin rejects the
            # state; clipped coefficients never establish supported performance.
            margin=min(alpha-lower,upper-alpha)/max(upper-lower,1.)
            coeff=self.polar.evaluate(d.sail_AR,d.camber_scale,np.clip(alpha,lower,upper),reverse_flow=reverse)
            cl=coeff[0]*p.wingLiftScale;cd=(coeff[1]+p.profileCd)*p.wingDragScale
            normal=cl*np.cos(np.deg2rad(alpha))+cd*np.sin(np.deg2rad(alpha))
            mast=coeff[2]*q[23]+((1-d.mast_fraction if reverse else d.mast_fraction)-.5)*normal
            strip_inputs.append([p.airDensity,d.sail_m2/self.strips,sample[1],sample[2],heel,z,cl,cd,chord,mast])
            poses.append((matrix,position,z) if motion is not None else None)
            speeds.append(sample[3]);lift.append(abs(cl));ratios.append(sample[0]);alphas.append(alpha)
            margins.append(margin);height_margins.append(sample[4])
        loads=self.strip.batch(shared={},cases={'x':strip_inputs}).values
        if motion is not None:
            for load,(matrix,position,z) in zip(loads,poses):
                world=matrix@np.r_[load[:2],0.]
                load[:2]=world[:2];load[2]=world[1]*z-position[1]*world[2]
        force=np.sum(loads,axis=0)
        extension=[1,*force,min(speeds),max(lift),0,min(*margins,*height_margins)]
        result=self.core(d=d,p=p,q=q,s=s,aero=aero,massData=mass,hydro=hydro,surface=extension).to_mapping()
        result.update(windRatioMin=min(ratios),windRatioMax=max(ratios),
                      localAlphaMin=min(alphas),localAlphaMax=max(alphas),
                      surfaceIncidenceMargin=min(margins),surfaceHeightMargin=min(height_margins),
                      airRollMoment=force[2],signedMastMoment=force[3])
        return result
