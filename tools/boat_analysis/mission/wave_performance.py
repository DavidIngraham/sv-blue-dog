"""Bounded cached wave-aware averaged-tack envelope for the mission engine."""
from itertools import product
import numpy as np
from scipy.spatial import ConvexHull


def bracket(axis,value):
    axis=np.asarray(axis,float)
    exact=np.flatnonzero(np.isclose(axis,value,rtol=0,atol=1e-10))
    if len(exact):return [(float(axis[exact[0]]),1.)]
    if value<axis[0] or value>axis[-1]:raise ValueError('outside cached axis')
    i=np.searchsorted(axis,value)-1;f=(value-axis[i])/(axis[i+1]-axis[i])
    return [(float(axis[i]),1-f),(float(axis[i+1]),f)]


class WavePerformance:
    def __init__(self,record):
        self.record=record;self.nodes={tuple(r[k] for k in ('wind','height','period','direction')):r for r in record['nodes']}
        self.axes=[sorted({key[i] for key in self.nodes}) for i in range(4)]
        self.planes=None;self.power=0.;self.reason='not initialized'

    def set_condition(self,wind,height,period,direction):
        self.planes=None;direction%=360
        try:
            axes=list(self.axes);axes[3]=axes[3]+[360.]
            choices=[bracket(axis,value) for axis,value in zip(axes,(wind,height,period,direction))]
            points=np.zeros((5,2));power=0.
            for combination in product(*choices):
                key=tuple(v for v,w in combination);key=key[:3]+(key[3]%360,)
                weight=np.prod([w for v,w in combination]);node=self.nodes[key]
                if not node['supported']:raise ValueError('unsupported cached sailing state')
                points+=weight*np.asarray(node['velocities']);power+=weight*node['powerW']
            self.planes=ConvexHull(points).equations;self.power=float(power);self.reason='covered'
        except (ValueError,KeyError) as error:self.reason=str(error)
        return self.planes is not None

    def covered(self,wind):return self.planes is not None

    def speeds(self,wind,angles):
        angles=np.asarray(angles);radians=np.deg2rad(angles)
        if self.planes is None:return np.zeros_like(angles,dtype=float)
        directions=np.stack([np.cos(radians),np.sin(radians)],axis=-1)
        projection=directions@self.planes[:,:2].T
        limit=np.full_like(projection,np.inf,dtype=float)
        np.divide(-self.planes[:,2],projection,out=limit,where=projection>1e-12)
        return np.maximum(0,np.min(limit,axis=-1))
