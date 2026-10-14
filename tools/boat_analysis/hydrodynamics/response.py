"""Bounded interpolation of radiation/diffraction coefficients and RAO solve."""
from sysml_python import execution_session
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from tools.boat_analysis.generated import impedance_term


class ResponseTable:
    def __init__(self,record):
        self.record=record;self.meta=record['metadata'];self.policy=record['policy']
        axes=[np.array(record['policy'][key],float) for key in ('periods','speeds','directions')]
        axes[2]=np.r_[axes[2],360.]
        values=np.full(tuple(len(a) for a in axes)+(24,),np.nan)
        for row in record['rows']:
            indices=tuple(np.flatnonzero(np.isclose(axis,row[key]))[0] for axis,key in zip(axes,('period','speed','direction')))
            values[indices]=np.r_[np.asarray(row['addedMass']).ravel(),np.asarray(row['damping']).ravel(),row['forceReal'],row['forceImag']]
        values[:,:,-1]=values[:,:,0]
        if not np.isfinite(values).all():raise ValueError('Invalid BEM coefficients')
        self.interpolate=RegularGridInterpolator(axes,values,bounds_error=True)
        self.mesh_errors=None
        self.mass=np.array(self.meta['massMatrix']);self.stiffness=np.array(self.meta['stiffness'])
        self.impedance=impedance_term

    @execution_session()
    def solve(self,period,speed,direction,damping=None):
        x=self.interpolate([[period,speed,np.rad2deg(direction)%360]])[0]
        A=x[:9].reshape(3,3);B=x[9:18].reshape(3,3);F=x[18:21]+1j*x[21:24]
        omega=2*np.pi/period;k=omega**2/9.80665;encounter=omega-k*speed*np.cos(direction)
        zeta=self.policy['settings'][4] if damping is None else damping
        extra=np.diag(2*zeta*np.sqrt(np.diag(self.stiffness)*np.diag(self.mass)))
        Z=np.empty((3,3),complex)
        for i in range(3):
            for j in range(3):
                impedance=self.impedance(x=[encounter,self.mass[i,j],A[i,j],self.stiffness[i,j],B[i,j],extra[i,j]])
                Z[i,j]=impedance.realPart+1j*impedance.imaginaryPart
        result=np.linalg.solve(Z,F)
        if not np.isfinite(result).all() or np.linalg.cond(Z)>1e9:raise ValueError('Singular wave response')
        return result,encounter,k

    def samples(self,amplitude,period,speed,direction,count):
        response,encounter,k=self.solve(period,speed,direction)
        for index in range(count):
            phase=-2*np.pi*index/count
            value=amplitude*response*np.exp(1j*phase)
            rate=-1j*encounter*value
            # Capytaine order H,R,P -> point-motion order H,P,R.
            pose=np.r_[value.real[[0,2,1]],rate.real[[0,2,1]]]
            yield pose,phase,k,encounter

    def compare_mesh(self,coarse):
        from itertools import product
        self.mesh_errors={}
        for row in self.record['rows']:
            key=(row['period'],row['speed'],row['direction'])
            args=(*key[:2],np.deg2rad(key[2]))
            low=coarse.solve(*args)[0];high=self.solve(*args)[0]
            self.mesh_errors[key]=float(np.linalg.norm(low-high)/max(np.linalg.norm(high),1e-8))
        return self.mesh_errors

    def mesh_error(self,period,speed,direction):
        if self.mesh_errors is None:return 0.
        from itertools import product
        axes=[np.asarray(self.policy[k],float) for k in ('periods','speeds','directions')]
        axes[2]=np.r_[axes[2],360.]
        choices=[]
        for axis,value in zip(axes,(period,speed,np.rad2deg(direction)%360)):
            exact=np.flatnonzero(np.isclose(axis,value,rtol=0,atol=1e-10))
            if len(exact):choices.append([(axis[exact[0]],1.)]);continue
            if not axis[0]<=value<=axis[-1]:raise ValueError('Outside response mesh grid')
            i=np.searchsorted(axis,value)-1
            choices.append([(axis[i],1.),(axis[i+1],1.)])
        keys=[tuple(v for v,w in c) for c in product(*choices)]
        return max(self.mesh_errors[(p,v,d%360)] for p,v,d in keys)
