"""Candidate-specific averaged-tack performance and electrical configuration.

Convex combinations of the four solved velocity vectors per wind represent
averaged sailing schedules, not measured polars or resolved tacking trajectories.
Interpolation is limited to the solved wind interval; outside it only drift is
credited and coverage is reported. No extrapolated sailing speed is invented.
"""
from copy import deepcopy
import numpy as np
from scipy.spatial import ConvexHull


class Performance:
    def __init__(self, record):
        self.winds=np.array(record['winds'],dtype=float)
        self.valid=np.asarray(record.get('validWinds',[True]*len(self.winds)),dtype=bool)
        self.planes=[ConvexHull(np.array(v)).equations for v in record['velocities']]
        if len(self.winds)!=len(self.planes) or np.any(np.diff(self.winds)<=0):
            raise ValueError('Invalid candidate wind grid')
    def covered(self,wind):
        if not self.winds[0]<=wind<=self.winds[-1]:return False
        exact=np.flatnonzero(np.isclose(self.winds,wind,rtol=0,atol=1e-12))
        if len(exact):return bool(self.valid[exact[0]])
        i=np.searchsorted(self.winds,wind)-1
        return bool(self.valid[i] and self.valid[i+1])
    def speeds(self,wind,angles):
        angles=np.asarray(angles);radians=np.deg2rad(angles)
        directions=np.stack([np.cos(radians),np.sin(radians)],axis=-1)
        if not self.covered(wind):return np.zeros_like(angles,dtype=float)
        samples=[]
        for planes in self.planes:
            projection=directions@planes[:,:2].T
            limit=np.full_like(projection,np.inf,dtype=float)
            np.divide(-planes[:,2],projection,out=limit,where=projection>1e-12)
            samples.append(np.maximum(0,np.min(limit,axis=-1)))
        i=min(np.searchsorted(self.winds,wind,side='right')-1,len(self.winds)-2)
        fraction=(wind-self.winds[i])/(self.winds[i+1]-self.winds[i])
        return samples[i]*(1-fraction)+samples[i+1]*fraction


def configure(inputs,problem,result):
    from ..geometry.vessel import operating_envelope
    out=deepcopy(inputs);d=dict(zip(problem.model.c['designNames'],result['design']))
    q=problem.model.operation.contract['environment'];parameters=problem.model.parameters
    rows=result['rows'];states=result['states'];winds=problem.context['windSpeeds']
    velocities=[]
    for i in range(len(winds)):
        points=[[0.,0.]]
        for state in states[i*4:(i+1)*4]:
            angle=np.deg2rad(state[1]+state[3])
            points.append([float(state[0]*np.cos(angle)),float(state[0]*np.sin(angle))])
        velocities.append(points)
    out['performance']={'winds':winds,'velocities':velocities,'scope':__doc__.strip()}
    envelope=operating_envelope(d,parameters[33])
    capacity=d['battery_Wh']*q[15]
    out['energy']=[capacity,capacity*q[16],q[22],max(r['averagePower'] for r in rows),inputs['energy'][4],
                   d['panel_m2']*q[10]*q[11]*q[12]*parameters[11],q[13],q[14]]
    out['storage']={'selfDischargeW':q[19],'maxChargeW':q[17]*d['battery_Wh']}
    out['dimensions']=[envelope['sweptLengthM'],envelope['sweptBeamM'],max(r['v'] for r in rows)]
    out['candidate']={'design':d,'mass':result['mass'],'envelope':envelope,'energyScreen':result['concept'],
                      'qualification':False,'powerPolicy':'Maximum operating bus load throughout; maneuver energy remains an explicit extra scenario allowance.'}
    return out
